"""Flask web application for red-plex GUI."""
import logging
import os

from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_socketio import SocketIO, emit

from red_plex.infrastructure.cli.cli import update_collections_from_collages
from red_plex.infrastructure.config.config import (
    load_config,
    save_config
)
from red_plex.infrastructure.config.models import Configuration
from red_plex.infrastructure.db.local_database import LocalDatabase
from red_plex.infrastructure.logger.logger import configure_logger
from red_plex.infrastructure.plex.plex_manager import PlexManager
from red_plex.infrastructure.rest.gazelle.gazelle_api import GazelleAPI
from red_plex.infrastructure.service.collection_processor import CollectionProcessingService
from red_plex.use_case.create_collection.album_fetch_mode import AlbumFetchMode

# pylint: disable=W0703,W0718,R0914,R0915
class WebSocketHandler(logging.Handler):
    """Custom logging handler that sends log messages via WebSocket."""

    def __init__(self, socketio_instance, app_instance):
        super().__init__()
        self.socketio = socketio_instance
        self.app = app_instance

    def emit(self, record):
        """Emit a log record via WebSocket."""
        try:
            msg = self.format(record)
            with self.app.app_context():
                self.socketio.emit('status_update', {'message': msg})
        except Exception:
            # Avoid recursion if there's an error in the handler
            pass


def get_db():
    """Get database connection for current thread."""
    if 'db' not in g:
        g.db = LocalDatabase()
    return g.db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

    configure_logger()

    logger = logging.getLogger('red_plex')

    ws_handler = WebSocketHandler(socketio, app)

    if logger.handlers:
        ws_handler.setFormatter(logger.handlers[0].formatter)
    ws_handler.setLevel(logger.level)

    logger.addHandler(ws_handler)

    logger.propagate = False

    @app.teardown_appcontext
    def close_db(error):
        """Close database connection."""
        db = g.pop('db', None)
        if db is not None:
            db.close()

        if error is not None:
            logger.error("Error during request teardown: %s", error)

    def map_fetch_mode(fetch_mode_str) -> AlbumFetchMode:
        """Map the fetch mode string to an AlbumFetchMode enum."""
        if fetch_mode_str == 'query':
            return AlbumFetchMode.QUERY
        return AlbumFetchMode.TORRENT_NAME

    @app.route('/')
    def index():
        """Home page."""
        return render_template('index.html')

    @app.route('/config')
    def config_view():
        """View configuration."""
        try:
            config_data = load_config()
            return render_template('config.html', config=config_data.to_dict())
        except Exception as e:
            flash(f'Error loading configuration: {str(e)}', 'error')
            return render_template('config.html', config={})

    @app.route('/config/edit', methods=['GET', 'POST'])
    def config_edit():
        """Edit configuration."""
        if request.method == 'POST':
            try:
                config_data = request.form.to_dict()

                # Convert nested structure for site configs
                sites_config = {}
                for key, value in config_data.items():
                    if key.startswith('RED_') or key.startswith('OPS_'):
                        site, field = key.split('_', 1)
                        if site not in sites_config:
                            sites_config[site] = {}
                        if field == 'RATE_LIMIT_CALLS':
                            sites_config[site].setdefault('RATE_LIMIT', {})['calls'] = int(value)
                        elif field == 'RATE_LIMIT_SECONDS':
                            sites_config[site].setdefault('RATE_LIMIT', {})['seconds'] = int(value)
                        else:
                            sites_config[site][field] = value

                # Build final config
                final_config = {
                    'LOG_LEVEL': config_data.get('LOG_LEVEL', 'INFO'),
                    'PLEX_URL': config_data.get('PLEX_URL', ''),
                    'PLEX_TOKEN': config_data.get('PLEX_TOKEN', ''),
                    'SECTION_NAME': config_data.get('SECTION_NAME', 'Music'),
                }
                final_config.update(sites_config)

                # Save configuration
                config = Configuration.from_dict(final_config)
                save_config(config)

                flash('Configuration saved successfully!', 'success')
                return redirect(url_for('config_view'))
            except Exception as e:
                flash(f'Error saving configuration: {str(e)}', 'error')

        try:
            config_data = load_config()
            return render_template('config_edit.html', config=config_data.to_dict())
        except Exception as e:
            flash(f'Error loading configuration: {str(e)}', 'error')
            return render_template('config_edit.html', config={})

    @app.route('/collages')
    def collages():
        """View collages."""
        try:
            db = get_db()
            collages = db.get_all_collage_collections()
            return render_template('collages.html', collages=collages)
        except Exception as e:
            flash(f'Error loading collages: {str(e)}', 'error')
            return render_template('collages.html', collages=[])

    @app.route('/collages/convert', methods=['GET', 'POST'])
    def collages_convert():
        """Convert collages."""
        if request.method == 'POST':
            try:
                collage_ids = request.form.get('collage_ids', '').split()
                site = request.form.get('site')
                fetch_mode = request.form.get('fetch_mode', 'torrent_name')

                if not collage_ids:
                    flash('Please provide at least one collage ID.', 'error')
                    return render_template('collages_convert.html')

                if not site:
                    flash('Please select a site.', 'error')
                    return render_template('collages_convert.html')

                # Start processing in background
                def process_collages():
                    logger = logging.getLogger('red_plex')
                    thread_db = None
                    try:
                        thread_db = LocalDatabase()
                        album_fetch_mode = map_fetch_mode(fetch_mode)

                        with app.app_context():
                            socketio.emit('status_update',
                                          {'message': 'Starting collage conversion process...'})

                        logger.info("WebSocket logging is configured and ready.")
                        logger.info("Connecting to Plex server...")

                        try:
                            plex_manager = PlexManager(db=thread_db)
                        except Exception as e:
                            logger.error('Failed to initialize PlexManager: %s', e)
                            with app.app_context():
                                socketio.emit('status_update', {
                                    'message': f'Failed to connect to Plex server: {str(e)}',
                                    'error': True
                                })
                            return

                        logger.info("Successfully connected to Plex server.")

                        gazelle_api = GazelleAPI(site)
                        processor = CollectionProcessingService(thread_db,
                                                                plex_manager,
                                                                gazelle_api)

                        def web_echo(message):
                            logger.info(message)

                        def web_confirm(message):
                            logger.info('Auto-confirming: %s', message)
                            return True

                        processor.process_collages(
                            collage_ids=collage_ids,
                            album_fetch_mode=album_fetch_mode,
                            echo_func=web_echo,
                            confirm_func=web_confirm
                        )

                        with app.app_context():
                            socketio.emit('status_update', {
                                'message': 'Collage processing completed successfully!',
                                'finished': True
                            })

                    except Exception as e:
                        logger.critical('An unhandled error occurred: %s', e, exc_info=True)
                        with app.app_context():
                            socketio.emit('status_update', {
                                'message': f'Error: {str(e)}',
                                'error': True
                            })
                    finally:
                        if thread_db:
                            thread_db.close()

                socketio.start_background_task(target=process_collages)

                flash('Processing started! Check the status below.', 'info')
                return render_template('collages_convert.html',
                                       processing=True)

            except Exception as e:
                flash(f'Error starting collage conversion: {str(e)}', 'error')

        return render_template('collages_convert.html')

    @app.route('/bookmarks')
    def bookmarks():
        """View bookmarks."""
        try:
            db = get_db()
            bookmarks = db.get_all_bookmark_collections()
            return render_template('bookmarks.html', bookmarks=bookmarks)
        except Exception as e:
            flash(f'Error loading bookmarks: {str(e)}', 'error')
            return render_template('bookmarks.html', bookmarks=[])

    @app.route('/bookmarks/convert', methods=['GET', 'POST'])
    def bookmarks_convert():
        """Convert bookmarks."""
        if request.method == 'POST':
            try:
                site = request.form.get('site')
                fetch_mode = request.form.get('fetch_mode', 'torrent_name')

                if not site:
                    flash('Please select a site.', 'error')
                    return render_template('bookmarks_convert.html')

                # Start processing in background
                def process_bookmarks():
                    logger = logging.getLogger('red_plex')
                    thread_db = None
                    try:
                        thread_db = LocalDatabase()
                        album_fetch_mode = map_fetch_mode(fetch_mode)

                        with app.app_context():
                            socketio.emit('status_update',
                                          {'message': 'Starting bookmark conversion process...'})

                        gazelle_api = GazelleAPI(site)
                        plex_manager = PlexManager(db=thread_db)
                        processor = CollectionProcessingService(thread_db,
                                                                plex_manager,
                                                                gazelle_api)

                        def web_echo(message):
                            logger.info(message)

                        def web_confirm(message):
                            logger.info('Auto-confirming: %s', message)
                            return True

                        processor.process_bookmarks(
                            album_fetch_mode=album_fetch_mode,
                            echo_func=web_echo,
                            confirm_func=web_confirm
                        )

                        with app.app_context():
                            socketio.emit('status_update', {
                                'message': 'Bookmark processing completed successfully!',
                                'finished': True
                            })
                    except Exception as e:
                        logger.critical(
                            'An unhandled error occurred during bookmark processing: %s',
                            e,
                            exc_info=True)
                        with app.app_context():
                            socketio.emit('status_update', {
                                'message': f'Error: {str(e)}',
                                'error': True
                            })
                    finally:
                        if thread_db:
                            thread_db.close()

                socketio.start_background_task(target=process_bookmarks)

                flash('Processing started! Check the status below.', 'info')
                return render_template('bookmarks_convert.html',
                                       processing=True)

            except Exception as e:
                flash(f'Error starting bookmark conversion: {str(e)}', 'error')

        return render_template('bookmarks_convert.html')

    @app.route('/database')
    def database():
        """View database status."""
        try:
            db = get_db()
            db_path = db.db_path
            db_exists = os.path.exists(db_path)

            # Get some basic stats
            stats = {}
            if db_exists:
                try:
                    stats['albums'] = len(db.get_all_albums())
                    stats['collages'] = len(db.get_all_collage_collections())
                    stats['bookmarks'] = len(db.get_all_bookmark_collections())
                except Exception as e:
                    logger.warning('Error getting database stats: %s', e)
                    stats = {'albums': 0, 'collages': 0, 'bookmarks': 0}
            else:
                stats = {'albums': 0, 'collages': 0, 'bookmarks': 0}

            return render_template('database.html',
                                   db_path=db_path,
                                   db_exists=db_exists,
                                   stats=stats)
        except Exception as e:
            flash(f'Error loading database status: {str(e)}', 'error')
            return render_template('database.html',
                                   db_path="Unknown",
                                   db_exists=False,
                                   stats={})

    @app.route('/database/albums/update', methods=['POST'])
    def database_albums_update():
        """Update albums from Plex and update collections from collages."""
        try:
            def update_albums():
                logger = logging.getLogger('red_plex')
                thread_db = None
                try:
                    thread_db = LocalDatabase()

                    with app.app_context():
                        socketio.emit('status_update',
                                      {'message': 'Starting albums update from Plex...'})

                    plex_manager = PlexManager(db=thread_db)

                    plex_manager.populate_album_table()

                    with app.app_context():
                        socketio.emit('status_update',
                                      {'message': 'Albums update completed. '
                                                  'Starting collections update...'})

                    all_collages = thread_db.get_all_collage_collections()
                    if all_collages:
                        logger.info('Updating %s collage collections...', len(all_collages))

                        update_collections_from_collages(
                            local_database=thread_db,
                            collage_list=all_collages,
                            plex_manager=plex_manager,
                            fetch_bookmarks=False,
                            fetch_mode=AlbumFetchMode.TORRENT_NAME
                        )
                        logger.info('Collections update from collages completed!')
                    else:
                        logger.info('No stored collages found to update.')

                    with app.app_context():
                        socketio.emit('status_update', {
                            'message': 'Albums and collections update completed successfully!',
                            'finished': True
                        })
                except Exception as e:
                    logger.critical('An unhandled error occurred during album update: %s',
                                    e,
                                    exc_info=True)
                    with app.app_context():
                        socketio.emit('status_update', {
                            'message': f'Error updating albums: {str(e)}',
                            'error': True
                        })
                finally:
                    if thread_db:
                        thread_db.close()

            socketio.start_background_task(target=update_albums)

            flash('Albums and collections update started!', 'info')
        except Exception as e:
            flash(f'Error starting albums update: {str(e)}', 'error')

        return redirect(url_for('database'))

    @app.route('/database/<table>/reset', methods=['POST'])
    def database_reset(table):
        """Reset database table."""
        try:
            db = get_db()
            if table == 'albums':
                db.reset_albums()
                flash('Albums table reset successfully!', 'success')
            elif table == 'collages':
                db.reset_collage_collections()
                flash('Collages table reset successfully!', 'success')
            elif table == 'bookmarks':
                db.reset_bookmark_collections()
                flash('Bookmarks table reset successfully!', 'success')
            else:
                flash(f'Unknown table: {table}', 'error')
        except Exception as e:
            flash(f'Error resetting {table} table: {str(e)}', 'error')

        return redirect(url_for('database'))

    @socketio.on('connect')
    def handle_connect():
        """Handle WebSocket connection."""
        emit('status_update', {'message': 'Connected to red-plex server'})

    return app, socketio
