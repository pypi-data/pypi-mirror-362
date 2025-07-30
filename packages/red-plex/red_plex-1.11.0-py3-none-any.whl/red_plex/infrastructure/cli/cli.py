"""Collection creator CLI."""
import os
import subprocess
import sys
from typing import List

import click
import yaml

from red_plex.domain.models import Collection
from red_plex.infrastructure.config.config import (
    CONFIG_FILE_PATH,
    load_config,
    save_config,
    ensure_config_exists
)
from red_plex.infrastructure.config.models import Configuration
from red_plex.infrastructure.db.local_database import LocalDatabase
from red_plex.infrastructure.logger.logger import logger, configure_logger
from red_plex.infrastructure.plex.plex_manager import PlexManager
from red_plex.infrastructure.rest.gazelle.gazelle_api import GazelleAPI
from red_plex.infrastructure.service.collection_processor import CollectionProcessingService
from red_plex.use_case.create_collection.album_fetch_mode import AlbumFetchMode
from red_plex.use_case.create_collection.query.query_sync_collection import (
    QuerySyncCollectionUseCase)
from red_plex.use_case.create_collection.torrent_name.torrent_name_sync_collection import (
    TorrentNameCollectionCreatorUseCase)


@click.group()
@click.pass_context
def cli(ctx):
    """A CLI tool for creating Plex collections from RED and OPS collages."""
    if 'db' not in ctx.obj:
        ctx.obj['db'] = LocalDatabase()


# config
@cli.group()
def config():
    """View or edit configuration settings."""


# config show
@config.command('show')
def show_config():
    """Display the current configuration."""
    config_data = load_config()
    path_with_config = (
            f"Configuration path: {CONFIG_FILE_PATH}\n\n" +
            yaml.dump(config_data.to_dict(), default_flow_style=False)
    )
    click.echo(path_with_config)


# config edit
@config.command('edit')
def edit_config():
    """Open the configuration file in the default editor."""
    # Ensure the configuration file exists
    ensure_config_exists()

    # Default to 'nano' if EDITOR is not set
    editor = os.environ.get('EDITOR', 'notepad' if os.name == 'nt' else 'nano')
    click.echo(f"Opening config file at {CONFIG_FILE_PATH}...")
    try:
        subprocess.call([editor, CONFIG_FILE_PATH])
    except FileNotFoundError:
        message = f"Editor '{editor}' not found. \
            Please set the EDITOR environment variable to a valid editor."
        logger.error(message)
        click.echo(message)
    except Exception as exc:  # pylint: disable=W0718
        logger.exception('Failed to open editor: %s', exc)
        click.echo(f"An error occurred while opening the editor: {exc}")


# config reset
@config.command('reset')
def reset_config():
    """Reset the configuration to default values."""
    if click.confirm('Are you sure you want to reset the configuration to default values?'):
        save_config(Configuration.default())
        click.echo(f"Configuration reset to default values at {CONFIG_FILE_PATH}")


# collages
@cli.group('collages')
def collages():
    """Possible operations with site collages."""


# collages update
@collages.command('update')
@click.pass_context
@click.option(
    '--fetch-mode', '-fm',
    type=click.Choice(['torrent_name', 'query']),
    default='torrent_name',
    show_default=True,
    help=(
            '(Optional) Album lookup strategy:\n'
            '\n- torrent_name: uses torrent dir name to search in Plex, '
            'if you don\'t use Beets/Lidarr \n'
            '\n- query: uses queries to Plex instead of searching by path name '
            '(if you use Beets/Lidarr)\n'
    )
)
def update_collages(ctx, fetch_mode: str):
    """Synchronize all stored collections with their source collages."""
    fetch_mode = map_fetch_mode(fetch_mode)
    try:
        local_database = ctx.obj.get('db', None)
        local_database: LocalDatabase
        all_collages = local_database.get_all_collage_collections()

        if not all_collages:
            click.echo("No collages found in the db.")
            return

        # Initialize PlexManager once, populate its db once
        plex_manager = PlexManager(local_database)
        if not plex_manager:
            return
        plex_manager.populate_album_table()

        update_collections_from_collages(
            local_database=local_database,
            collage_list=all_collages,
            plex_manager=plex_manager,
            fetch_bookmarks=False,
            fetch_mode=fetch_mode)
    except Exception as exc:  # pylint: disable=W0718
        logger.exception('Failed to update stored collections: %s', exc)
        click.echo(f"An error occurred while updating stored collections: {exc}")


# convert collection
@collages.command('convert')
@click.argument('collage_ids', nargs=-1)
@click.option('--site', '-s',
              type=click.Choice(['red', 'ops']),
              required=True,
              help='Specify the site: red (Redacted) or ops (Orpheus).')
@click.option(
    '--fetch-mode', '-fm',
    type=click.Choice(['torrent_name', 'query'], case_sensitive=False),  # Added case_sensitive
    default='torrent_name',
    show_default=True,
    help=(
            '(Optional) Album lookup strategy:\n'
            '\n- torrent_name: uses torrent dir name (original behavior).\n'
            '\n- query: uses Plex queries (Beets/Lidarr friendly).\n'
    )
)
@click.pass_context
def convert_collages(ctx, collage_ids, site, fetch_mode):
    """
    Create/Update Plex collections from given COLLAGE_IDS.
    """
    if not collage_ids:
        click.echo("Please provide at least one COLLAGE_ID.")
        ctx.exit(1)  # Exit with an error code

    album_fetch_mode_enum = map_fetch_mode(fetch_mode)

    # --- Dependency Setup ---
    local_database = ctx.obj.get('db')
    if not local_database:
        click.echo("Error: Database not initialized.", err=True)
        ctx.exit(1)

    plex_manager, gazelle_api = None, None
    try:
        plex_manager = PlexManager(db=local_database)
        gazelle_api = GazelleAPI(site)
    except Exception as e: # pylint: disable=W0718
        logger.error("Failed to initialize dependencies: %s", e, exc_info=True)
        click.echo(f"Error: Failed to initialize dependencies - {e}", err=True)
        ctx.exit(1)

    # --- Service Instantiation and Execution ---
    processor = CollectionProcessingService(local_database, plex_manager, gazelle_api)

    # Call the service, passing the necessary functions from click
    processor.process_collages(
        collage_ids=collage_ids,
        album_fetch_mode=album_fetch_mode_enum,
        echo_func=click.echo,
        confirm_func=click.confirm  # Pass the actual click.confirm
    )

    click.echo("Processing finished.")


# bookmarks
@cli.group()
def bookmarks():
    """Possible operations with your site bookmarks."""


# bookmarks update
@bookmarks.command('update')
@click.pass_context
@click.option(
    '--fetch-mode', '-fm',
    type=click.Choice(['torrent_name', 'query']),
    default='torrent_name',
    show_default=True,
    help=(
            '(Optional) Album lookup strategy:\n'
            '\n- torrent_name: uses torrent dir name to search in Plex, '
            'if you don\'t use Beets/Lidarr \n'
            '\n- query: uses queries to Plex instead of searching by path name '
            '(if you use Beets/Lidarr)\n'
    )
)
def update_bookmarks_collection(ctx, fetch_mode: str):
    """Synchronize all stored bookmarks with their source collages."""
    fetch_mode = map_fetch_mode(fetch_mode)
    try:
        local_database = ctx.obj.get('db', None)
        local_database: LocalDatabase
        all_bookmarks = local_database.get_all_bookmark_collections()

        if not all_bookmarks:
            click.echo("No bookmarks found in the db.")
            return

        plex_manager = PlexManager(local_database)
        if not plex_manager:
            return
        plex_manager.populate_album_table()

        update_collections_from_collages(
            local_database,
            all_bookmarks,
            plex_manager,
            fetch_bookmarks=True)

    except Exception as exc:  # pylint: disable=W0718
        logger.exception('Failed to update stored bookmarks: %s', exc)
        click.echo(f"An error occurred while updating stored bookmarks: {exc}")


# bookmarks convert
@bookmarks.command('convert')
@click.option('--site', '-s',
              type=click.Choice(['red', 'ops'], case_sensitive=False),
              required=True,
              help='Specify the site: red (Redacted) or ops (Orpheus).')
@click.option(
    '--fetch-mode', '-fm',
    type=click.Choice(['torrent_name', 'query'], case_sensitive=False),
    default='torrent_name',
    show_default=True,
    help=(
            '(Optional) Album lookup strategy:\n'
            '\n- torrent_name: uses torrent dir name (original behavior).\n'
            '\n- query: uses Plex queries (Beets/Lidarr friendly).\n'
    )
)
@click.pass_context
def convert_collection_from_bookmarks(ctx, site: str, fetch_mode: str):
    """
    Create/Update a Plex collection based on your site bookmarks.
    """
    album_fetch_mode_enum = map_fetch_mode(fetch_mode)

    # --- Dependency Setup ---
    local_database = ctx.obj.get('db')
    if not local_database:
        click.echo("Error: Database not initialized.", err=True)
        ctx.exit(1)

    plex_manager, gazelle_api = None, None
    try:
        plex_manager = PlexManager(db=local_database)
        gazelle_api = GazelleAPI(site)  # Create GazelleAPI based on site
    except Exception as e: # pylint: disable=W0718
        logger.error("Failed to initialize dependencies: %s", e, exc_info=True)
        click.echo(f"Error: Failed to initialize dependencies - {e}", err=True)
        ctx.exit(1)

    # --- Service Instantiation and Execution ---
    processor = CollectionProcessingService(local_database, plex_manager, gazelle_api)

    try:
        # Call the specific bookmark processing method
        processor.process_bookmarks(
            album_fetch_mode=album_fetch_mode_enum,
            echo_func=click.echo,
            confirm_func=click.confirm
        )
    except Exception as exc:  # pylint: disable=W0718
        logger.exception(
            'Failed to create collection from bookmarks on site %s: %s',
            site.upper(), exc
        )
        click.echo(
            f'Failed to create collection from bookmarks on site {site.upper()}: {exc}',
            err=True
        )
        ctx.exit(1)

    click.echo("Bookmark processing finished.")


# db
@cli.group()
def db():
    """Manage database."""


# db location
@db.command('location')
@click.pass_context
def db_location(ctx):
    """Returns the location to the database."""
    local_database = ctx.obj.get('db', None)
    local_database: LocalDatabase
    db_path = local_database.db_path
    if os.path.exists(db_path):
        click.echo(f"Database exists at: {db_path}")
    else:
        click.echo("Database file does not exist.")


# db albums
@db.group('albums')
def db_albums():
    """Manage albums inside database."""


# db albums reset
@db_albums.command('reset')
@click.pass_context
def db_albums_reset(ctx):
    """Resets albums table from database."""
    if click.confirm('Are you sure you want to reset the db?'):
        try:
            local_database = ctx.obj.get('db', None)
            local_database: LocalDatabase
            local_database.reset_albums()
            click.echo("Albums table has been reset successfully.")
        except Exception as exc:  # pylint: disable=W0718
            click.echo(f"An error occurred while resetting the album table: {exc}")


@db_albums.command('update')
@click.pass_context
def db_albums_update(ctx):
    """Updates albums table from Plex."""
    try:
        local_database = ctx.obj.get('db', None)
        local_database: LocalDatabase
        plex_manager = PlexManager(db=local_database)
        plex_manager.populate_album_table()
        click.echo("Albums table has been updated successfully.")
    except Exception as exc:  # pylint: disable=W0703
        click.echo(f"An error occurred while updating the album table: {exc}")


# db collections
@db.group('collections')
def db_collections():
    """Manage albums inside database."""


# db collections reset
@db_collections.command('reset')
@click.pass_context
def db_collections_reset(ctx):
    """Resets collections table from database."""
    if click.confirm('Are you sure you want to reset the collection db?'):
        try:
            local_database = ctx.obj.get('db', None)
            local_database: LocalDatabase
            local_database.reset_collage_collections()
            click.echo("Collage collection db has been reset successfully.")
        except Exception as exc:  # pylint: disable=W0718
            logger.exception('Failed to reset collage collection db: %s', exc)
            click.echo(
                f"An error occurred while resetting the collage collection db: {exc}")


# db bookmarks
@db.group('bookmarks')
def db_bookmarks():
    """Manage bookmarks inside database."""


# db bookmarks reset
@db_bookmarks.command('reset')
@click.pass_context
def db_bookmarks_reset(ctx):
    """Resets bookmarks table from database."""
    if click.confirm('Are you sure you want to reset the collection bookmarks db?'):
        try:
            local_database = ctx.obj.get('db', None)
            local_database: LocalDatabase
            local_database.reset_bookmark_collections()
            click.echo("Collection bookmarks db has been reset successfully.")
        except Exception as exc:  # pylint: disable=W0718
            logger.exception('Failed to reset collection bookmarks db: %s', exc)
            click.echo(f"An error occurred while resetting the collection bookmarks db: {exc}")


def update_collections_from_collages(local_database: LocalDatabase,
                                     collage_list: List[Collection],
                                     plex_manager: PlexManager,
                                     fetch_bookmarks=False,
                                     fetch_mode: AlbumFetchMode = AlbumFetchMode.TORRENT_NAME):
    """
    Forces the update of each collage (force_update=True)
    """

    for collage in collage_list:
        logger.info('Updating collection for collage "%s"...', collage.name)
        gazelle_api = GazelleAPI(collage.site)

        if AlbumFetchMode.TORRENT_NAME == fetch_mode:
            collection_creator = TorrentNameCollectionCreatorUseCase(local_database,
                                                                     plex_manager,
                                                                     gazelle_api)
            result = collection_creator.execute(
                collage_id=collage.external_id,
                site=collage.site,
                fetch_bookmarks=fetch_bookmarks,
                force_update=True
            )
        else:
            collection_creator = QuerySyncCollectionUseCase(local_database,
                                                            plex_manager,
                                                            gazelle_api)
            result = collection_creator.execute(
                collage_id=collage.external_id,
                site=collage.site,
                fetch_bookmarks=fetch_bookmarks,
                force_update=True
            )

        if result.response_status is None:
            logger.info('No valid data found for collage "%s".', collage.name)
        else:
            logger.info('Collection for collage "%s" created/updated successfully with %s entries.',
                        collage.name, len(result.albums))


# gui
@cli.command()
@click.option('--host', '-h', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
@click.option('--port', '-p', default=8000, type=int, help='Port to bind to (default: 8000)')
@click.option('--debug', is_flag=True, help='Run in debug mode with auto-reloading.')
def gui(host, port, debug):
    """Launches the web interface using the Gunicorn production server."""

    # Build the bind address for Gunicorn
    bind_address = f"{host}:{port}"

    click.echo(f"🚀 Launching Gunicorn server at http://{bind_address}")

    # Create the list of arguments for the Gunicorn command
    command = [
        'gunicorn',
        '--worker-class', 'eventlet',
        '-w', '1',
        '--bind', bind_address,
    ]

    # If the --debug flag is passed, add Gunicorn's reload option
    if debug:
        click.echo("   -> Debug mode on (auto-reload enabled).")
        command.append('--reload')

    command.append('wsgi:app')

    try:
        # Execute the Gunicorn command
        subprocess.run(command, check=True)
    except FileNotFoundError:
        click.echo(
            "Error: 'gunicorn' command not found.",
            err=True
        )
        click.echo(
            "Please make sure you have installed it with: pip install gunicorn eventlet",
            err=True
        )
        sys.exit(1)


@cli.result_callback()
@click.pass_context
def finalize_cli(ctx, _result, *_args, **_kwargs):
    """Close the DB when all commands have finished."""
    local_database = ctx.obj.get('db', None)
    if local_database:
        local_database.close()


def map_fetch_mode(fetch_mode) -> AlbumFetchMode:
    """Map the fetch mode string to an AlbumFetchMode enum."""
    if fetch_mode == 'query':
        return AlbumFetchMode.QUERY
    return AlbumFetchMode.TORRENT_NAME


def main():
    """Actual entry point for the CLI when installed."""
    if 'gui' not in sys.argv:
        configure_logger()
    cli(obj={})  # pylint: disable=no-value-for-parameter


if __name__ == '__main__':
    main()
