"""Main CLI module."""

import shutil
from pathlib import Path

import click

from teachbooks.external_content.process_toc import (
    chmod_git_files,
    process_external_toc_entries,
)


@click.group()
@click.version_option()
def main():
    """TeachBooks command line tools."""
    pass


@main.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.argument("path-source", type=click.Path(exists=True, file_okay=True))
@click.option("--release", is_flag=True, help="Build book with release strategy")
@click.option(
    "--publish", is_flag=True, help="--public is deprecated. Use --release instead."
)
@click.option("--process-only", is_flag=True, help="Only pre-process content")
@click.pass_context
def build(ctx, path_source: str, publish: bool, release: bool, process_only: bool):
    """Pre-process book contents and run Jupyter Book build command."""
    from jupyter_book.cli.main import build as jupyter_book_build

    from teachbooks.release import copy_ext, make_release

    if publish:
        click.secho(
            "Warning: --publish is deprecated, use --release instead",
            fg="yellow",
            err=True,
        )

    strategy = "release" if release or publish else "draft"
    echo_info(f"running build with strategy '{strategy}'")
    path_src_folder = Path(path_source).absolute()
    if release or publish:
        path_conf, path_toc = make_release(path_src_folder)
        path_ext = path_src_folder / "_ext"
        if path_ext.exists():
            mg = "copying _ext/ directory to support APA in release [TEMPORARY FEATURE]"
            echo_info(click.style(mg, fg="yellow"))
            copy_ext(path_src_folder)
    else:
        path_conf = path_src_folder / "_config.yml"
        path_toc = path_src_folder / "_toc.yml"

    # Parse out external git entries from ToC
    path_toc = process_external_toc_entries(
        path_toc, path_toc.with_stem("_toc_with_local_paths"), book_root=path_src_folder
    )

    if not process_only:
        all_args = [str(path_src_folder)]
        if path_conf and path_conf.exists():
            all_args.extend(["--config", str(path_conf)])
        if path_toc and path_toc.exists():
            all_args.extend(["--toc", str(path_toc)])
        if ctx.args:
            all_args.extend(ctx.args)

        jupyter_book_build.main(args=all_args, standalone_mode=False)

        # Calculate and report build size
        build_dir = path_src_folder / "_build"
        total_size = sum(f.stat().st_size for f in build_dir.rglob("*") if f.is_file())
        size_mb = total_size / (1024 * 1024)
        echo_info(f"Build complete. Total size: {size_mb:.2f}MB")

        check_server()


@main.command()
@click.argument("path-source", type=click.Path(exists=True, file_okay=True))
@click.option("--external", is_flag=True, help="Empty _git/ directory.")
def clean(path_source, external: bool = False):
    """Stop teachbooks server and run Jupyter Book clean command."""
    from jupyter_book.cli.main import clean as jupyter_book_clean

    from teachbooks.serve import Server, ServerError

    workdir = Path(path_source) / ".teachbooks" / "server"

    # Check if a server is running and stop it if so
    try:
        server = Server.load(workdir)
        if server.is_running:
            echo_info("Stopping running server before cleaning...")
            server.stop()
            echo_info("Server stopped.")
    except ServerError:
        echo_info("No running server found.")

    # Clean external content
    gitdir = Path(path_source) / "_git"
    if external:
        if gitdir.exists():
            echo_info(f"Cleaning cloned git repositories in {gitdir}")
            shutil.rmtree(gitdir.absolute(), onerror=chmod_git_files)
        else:
            echo_info(f"No _git directory found at {gitdir}")
    else:
        if gitdir.exists():
            echo_info(
                "Skipping external content cleaning. Use --external"
                " to remove cloned git repositories."
            )

    # Now proceed with cleaning
    echo_info(f"Cleaning build artifacts in {path_source}...")
    jupyter_book_clean.main([str(path_source)])
    echo_info("Clean complete.")


@main.group(invoke_without_command=True)
# @click.argument("path-source", type=click.Path(exists=True, file_okay=True))
# @click.option("--test", is_flag=True, help="Build book with release strategy")
@click.option("-v", "--verbose", count=True)
@click.pass_context
def serve(ctx, verbose):
    """Start a web server to interact with the book locally.

    If serve dir path not provided, default is `./book/_build/html`.
    Checks to see if server is already running.
    """
    from teachbooks import BOOK_SERVE_DIR, SERVER_WORK_DIR
    from teachbooks.serve import Server

    if verbose > 0:
        echo_info("serve command invoked.")

    if ctx.invoked_subcommand is None:
        try:
            server = Server.load(Path(SERVER_WORK_DIR))
            if verbose > 0:
                echo_info(" server already exists")

            stdout_summary(server)
        except:  # noqa: E722 TODO: handle more gracefully.
            if verbose > 0:
                echo_info("no server found, creating a new one.")

            serve_dir = Path(BOOK_SERVE_DIR)

            if not serve_dir.exists():
                echo_info(
                    click.style("default directory not found: ", fg="yellow")
                    + f"{serve_dir}"
                )

                serve_dir = Path(".")
                print(
                    "            "
                    + click.style("serving current directory: ", fg="yellow")
                    + f"{serve_dir}"
                )
                print(
                    "            "
                    + click.style(
                        "specify a directory with: 'teachbooks serve path <path>'",
                        fg="yellow",
                    )
                )

            serve_path(serve_dir, verbose)


@serve.command()
@click.option("-v", "--verbose", count=True)
@click.argument("path-source", type=click.Path(exists=True, file_okay=True))
def path(path_source, verbose, no_build=False):
    """Specify relative path of directory to serve."""
    from teachbooks import BUILD_DIR, SERVER_WORK_DIR
    from teachbooks.serve import Server

    dir_with_build = Path(path_source).joinpath(BUILD_DIR)
    if dir_with_build.exists():
        serve_dir = dir_with_build
        echo_info("_build/html available and appended to path.")
    else:
        serve_dir = Path(path_source)

    echo_info(f"attempting to serve this directory: {serve_dir}")
    try:
        server = Server.load(Path(SERVER_WORK_DIR))
        if server.servedir == serve_dir:
            print("            " + "  ---> already serving this directory.")
            stdout_summary(server)
        else:
            print("            " + "  ---> already serving a different directory.")
            print("            " + "  ---> updating server directory...")
            server.stop()
            serve_path(serve_dir, verbose)
    except:  # noqa: E722 TODO: handle more gracefully.
        if verbose > 0:
            echo_info("no server found, creating a new one.")
        serve_path(serve_dir, verbose)


@serve.command()
def stop():
    """Stop the webserver."""
    from teachbooks import SERVER_WORK_DIR
    from teachbooks.serve import Server

    try:
        server = Server.load(Path(SERVER_WORK_DIR))
        server.stop()
        echo_info("server stopped.")
    except:  # noqa: E722 TODO: handle more gracefully.
        echo_info("no server found.")


def serve_path(servedir: str, verbose: int) -> None:
    """Start web server with specific path and verbosity."""
    from teachbooks import SERVER_WORK_DIR
    from teachbooks.serve import Server

    server = Server(
        servedir=Path(servedir), workdir=Path(SERVER_WORK_DIR), stdout=verbose
    )
    server.start(options=["--all"])
    stdout_summary(server)


def check_server():
    """Check if webserver is running and print status."""
    from teachbooks import SERVER_WORK_DIR
    from teachbooks.serve import Server

    try:
        server = Server.load(Path(SERVER_WORK_DIR))
        stdout_summary(server)
    except:  # noqa: E722 TODO: handle more gracefully
        echo_info("Use `teachbooks serve` to start a local server.")


def echo_info(message: str) -> None:
    """Wrapper for writing to stdout."""
    prefix = click.style("TeachBooks: ", fg="cyan", bold=True)
    click.echo(prefix + message)


def stdout_summary(server) -> None:
    """Print summary of server status."""
    echo_info(click.style(f"server running on: {server.url}", fg="green"))
    print(
        "            "
        + click.style(f"serving directory: {server.servedir}", fg="green")
    )
    print("            " + "To stop server, run: 'teachbooks serve stop'")
