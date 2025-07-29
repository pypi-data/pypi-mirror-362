#!/usr/bin/env python

import functools
import json
import logging
import sys
import webbrowser
from collections.abc import Callable, Generator
from contextlib import contextmanager
from pathlib import Path

from click import (
    Choice,
    IntRange,
    argument,
    confirm,
    echo,
    group,
    option,
    password_option,
    style,
    version_option,
)
from msal import SerializableTokenCache
from msal.exceptions import MsalError
from requests.exceptions import RequestException

from edmgr import auth
from edmgr.client import Client
from edmgr.config import get_log_level_from_verbose, settings
from edmgr.download import _fasp_download, write_download
from edmgr.exceptions import (
    EdmAPIError,
    EdmAuthError,
    EdmTokenExpiredError,
    EdmTokenNotFoundError,
)
from edmgr.formatters import (
    format_artifacts,
    format_entitlement,
    format_entitlements,
    format_releases,
)
from edmgr.utils import print_local_time

logger = logging.getLogger(__name__)


ASCII_ART = """
███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██╔████╔██║
██╔══╝  ██║  ██║██║╚██╔╝██║
███████╗██████╔╝██║ ╚═╝ ██║
╚══════╝╚═════╝ ╚═╝     ╚═╝
"""

CONTEXT_SETTINGS = {"token_normalize_func": lambda x: x.lower()}


def echo_error(msg: str) -> None:
    echo(style(text=msg, fg="red", bold=True), err=True)


def echo_info(msg: str) -> None:
    echo(style(text=msg, fg="green", bold=True))


def exception_handler(exc: Exception):
    if isinstance(exc, EdmTokenNotFoundError) or isinstance(exc, EdmTokenExpiredError):
        msg = (
            f"{exc}\nPlease login using `edmgr login` "
            "or set EDM_ACCESS_TOKEN environment variable to a valid token."
        )
        return echo_error(msg)
    if isinstance(exc, EdmAuthError) or isinstance(exc, MsalError):
        return echo_error(f"Authentication error: {exc}")
    if isinstance(exc, RequestException) or isinstance(exc, EdmAPIError):
        return echo_error(f"API Error: {exc}")
    logger.debug(f"Unexpected {type(exc)}: {exc}")
    return echo_error(f"Error: {exc}")


def cli_output(formatter, data, **kwargs) -> None:
    output_format = kwargs.pop("format")
    if output_format in ("json", "jsonpp"):
        indent = None
        sort_keys = False
        if output_format == "jsonpp":
            indent = 4
            sort_keys = True
        output = json.dumps(data, indent=indent, sort_keys=sort_keys)
    else:
        output = formatter(data, **kwargs)
    echo(output)


def pagination_params(offset: int | None, limit: int) -> dict:
    if offset is not None:
        return {"offset": offset, "limit": limit}
    return {}


def decode_token():
    token = get_current_token()
    payload = auth.decode_jwt_token(token, check_signature=False, check_claims=False)
    payload["token"] = token
    return payload


@contextmanager
def cached_client() -> Generator[Client, None, None]:
    """
    Load access token from disk cache if found and return a context manager
    wrapping a Client instanciated with either a JWT token or a MSAL TokenCache.

    JWT string cache takes precedence if found, otherwise cached MSAL TokenCache
    is used if found.

    If no cache file is found, return a a context manager wrapping a Client
    instance initialised with no arguments, the Client will use the token found
    in settings.

    :return: Context manager wrapping a Client instance initialised with an
             access token (if found)
    """
    token = auth.get_jwt_cache()
    msal_cache = auth.get_msal_cache()
    try:
        if token:
            logger.debug("Cached JWT token found")
            client = Client(token=token)
        else:
            if msal_cache:
                logger.debug("Cached MSAL cache found")
                client = Client(msal_cache=msal_cache)
            else:
                client = Client()
        yield client
    finally:
        if msal_cache and msal_cache.has_state_changed:
            auth.save_msal_cache(msal_cache)


def get_current_token() -> str:
    """
    Load access token from disk cache if found and return it.

    JWT string cache takes precedence if found, otherwise cached MSAL access token
    is returned if found.

    If no cache file is found, return the token found in settings.

    :return: JWT string
    """
    token = auth.get_jwt_cache()
    if token:
        return token
    msal_cache = auth.get_msal_cache()
    if msal_cache:
        token = auth.token_from_msal_cache(msal_cache)
        if token:
            return token
    token = Client().token
    if token:
        return token
    raise EdmTokenNotFoundError("Access token not found.")


def logout_and_clear_cache():
    cache = auth.get_msal_cache()
    if cache is not None:
        auth.msal_logout(cache)
    auth.delete_cache()


def common_options(command_func):
    @option(
        "-f",
        "--format",
        type=Choice(["table", "json", "jsonpp"], case_sensitive=False),
        default="table",
        show_default=True,
        help="Output format -> tabular, json or json prettify",
    )
    @functools.wraps(command_func)
    def common_options_wrapper(*args, **kwargs):
        return command_func(*args, **kwargs)

    return common_options_wrapper


def paginate_options(command_func):
    @option(
        "-o",
        "--offset",
        type=IntRange(1, max_open=True),
        help="Page number to paginate output",
    )
    @option(
        "-l",
        "--limit",
        type=IntRange(1, max_open=True),
        default=10,
        help=(
            "Number of records per page to be displayed. "
            "By default it shows 10 records per page. "
            "This option is ignored if no offset was given."
        ),
    )
    @functools.wraps(command_func)
    def paginate_options_wrapper(*args, **kwargs):
        return command_func(*args, **kwargs)

    return paginate_options_wrapper


def main():
    try:
        cli()
    except Exception as e:
        exception_handler(e)
        sys.exit(1)


@group()
@option(
    "-k",
    "--environment",
    type=Choice(["prod", "sandbox", "qa"], case_sensitive=False),
    default="prod",
    show_default=True,
    help="Configuration environment",
)
@option("-v", "--verbose", count=True)
@version_option(package_name="edmgr", message="%(package)s, version %(version)s")
def cli(environment, verbose):
    settings.set_env(environment.upper())

    if verbose:
        verbosity = min(verbose, 3)
        settings["log_level"] = get_log_level_from_verbose(verbosity)

    logging.basicConfig(
        level=settings["log_level"],
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s - : %(message)s",
        datefmt="%m-%d %H:%M:%S",
    )


@cli.command(context_settings=CONTEXT_SETTINGS, help="Print configuration")
def show_config():
    echo(json.dumps(settings._env, indent=4, sort_keys=True))


@cli.group(help="Login using credentials/token")
def login():
    pass


@login.command(
    context_settings=CONTEXT_SETTINGS, help="Login using username and password"
)
@option(
    "-u",
    "--username",
    type=str,
    prompt=True,
    required=True,
    help="Username (email) used for logging on to Arm",
)
@password_option(
    required=True, confirmation_prompt=False, help="Password used for logging on to Arm"
)
def credentials(username: str, password: str):
    logout_and_clear_cache()
    echo(style(text="Logging in, please wait...", fg="yellow", bold=False))
    msal_cache = SerializableTokenCache()
    auth.msal_login(username=username, password=password, cache=msal_cache)
    auth.save_msal_cache(msal_cache)

    echo(ASCII_ART)
    echo_info("Logged in successfully")


@cli.command(context_settings=CONTEXT_SETTINGS, help="Logout by deleting cached token")
def logout():
    logout_and_clear_cache()
    echo_info("Successfully logged out and cached token removed")


@login.command(context_settings=CONTEXT_SETTINGS, help="Login using JWT string")
@argument("token")
def token(token: str):
    logout_and_clear_cache()
    auth.decode_jwt_token(token)
    auth.save_jwt_cache(token)

    echo_info(f"Token saved in {settings['edm_root']}")


@login.command(
    context_settings=CONTEXT_SETTINGS,
    help="Print Access Token as JWT string with some extra information.",
)
def show_token():
    payload = decode_token()
    msg = (
        "Client token:"
        f"\n - Token Owner: {payload.get('given_name')} {payload.get('family_name')}"
        f"\n - Email: {payload.get('emails')}"
        f"\n - Expires: {print_local_time(payload.get('exp'))}"
        f"\n - Access Token: {payload.get('token')}"
    )
    echo_info(msg)


@cli.command(
    context_settings=CONTEXT_SETTINGS, help="Print a list of available entitlements."
)
@option("-e", "--entitlement-id", type=str, help="Entitlement ID to retrieve one")
@option("-p", "--product-code", type=str, help="Filter by product code")
@paginate_options
@common_options
def entitlements(
    entitlement_id: str | None = None, product_code: str | None = None, **kwargs
):
    with cached_client() as client:
        params = {}
        params.update(pagination_params(kwargs.pop("offset"), kwargs.pop("limit")))
        entitlements: list | None = None
        if product_code:
            entitlements = client.find_entitlements(
                search_query={"product.id": product_code}, params=params, **kwargs
            )
            if entitlement_id:
                entitlements = list(
                    filter(lambda x: x["id"] == entitlement_id, entitlements)
                )
        else:
            entitlements = client.get_entitlements(
                entitlement_id=entitlement_id, params=params, **kwargs
            )
    if entitlements:
        return cli_output(format_entitlements, entitlements, **kwargs)
    if entitlement_id or product_code:
        return echo_error("Couldn't find Entitlements with the given filters")
    echo_error("Couldn't find any Entitlements")


@cli.command(context_settings=CONTEXT_SETTINGS, help="Print single entitlement details")
@option("-p", "--product-code", type=str, help="Filter by product code")
@common_options
@paginate_options
@argument("entitlement_id")
def entitlement(entitlement_id: str, product_code: str | None = None, **kwargs):
    with cached_client() as client:
        entitlements: list | None = client.get_entitlements(
            entitlement_id=entitlement_id
        )
    if entitlements:
        return cli_output(
            format_entitlement, entitlements[0], product_code=product_code, **kwargs
        )
    echo_error(f"Couldn't find Entitlement {entitlement_id}")


@cli.command(
    context_settings=CONTEXT_SETTINGS,
    help="Print a list of releases for a particular entitlement.",
)
@option(
    "-e",
    "--entitlement-id",
    type=str,
    prompt=True,
    required=True,
    help="Entitlement ID",
)
@option("-r", "--release-id", type=str, help="Release ID to retrieve one")
@common_options
def releases(entitlement_id: str, release_id: str | None = None, **kwargs):
    with cached_client() as client:
        releases: list | None = client.get_releases(
            entitlement_id=entitlement_id, release_id=release_id, **kwargs
        )
    if releases:
        return cli_output(format_releases, releases, **kwargs)
    if release_id:
        return echo_error(
            "Couldn't find Release with the given Entitlement ID & Release ID"
        )
    echo_error("Couldn't find any Release with the given Entitlement ID")


@cli.command(
    context_settings=CONTEXT_SETTINGS,
    help="Print a list of artifacts for a particular release.",
)
@option(
    "-e",
    "--entitlement-id",
    type=str,
    prompt=True,
    required=True,
    help="Entitlement ID",
)
@option("-r", "--release-id", type=str, prompt=True, required=True, help="Release ID")
@option("-a", "--artifact-id", type=str, help="Artifact ID to retrieve one")
@common_options
def artifacts(
    entitlement_id: str, release_id: str, artifact_id: str | None = None, **kwargs
):
    with cached_client() as client:
        artifacts: list | None = client.get_artifacts(
            entitlement_id=entitlement_id,
            release_id=release_id,
            artifact_id=artifact_id,
        )
    if artifacts:
        return cli_output(format_artifacts, artifacts, **kwargs)
    msg_not_found_art = "Couldn't find artifacts with the given Entitlement"
    echo_error(
        f"{msg_not_found_art}{', Release & Artifact' if artifact_id else ' & Release'}"
    )


@cli.command(
    context_settings=CONTEXT_SETTINGS,
    help="Download all artifacts for a particular release or only a specific one.",
)
@option(
    "-e",
    "--entitlement-id",
    type=str,
    prompt=True,
    required=True,
    help="Entitlement ID",
)
@option("-r", "--release-id", type=str, prompt=True, required=True, help="Release ID")
@option("-a", "--artifact-id", type=str, help="Artifact ID")
@option(
    "-d",
    "--download-dir",
    type=str,
    help="Directory in which artifacts are downloaded. Default: $HOME/Artifacts",
)
@option(
    "-m",
    "--mode",
    type=Choice(["http", "fasp"], case_sensitive=False),
    default="http",
    help="The protocol used to download the files. Default: http",
)
def download_artifacts(
    entitlement_id: str,
    release_id: str,
    mode: str,
    artifact_id: str | None = None,
    download_dir: str | None = None,
):
    with cached_client() as client:
        artifacts: list | None = client.get_artifacts(
            entitlement_id=entitlement_id,
            release_id=release_id,
            artifact_id=artifact_id,
        )

    if not download_dir:
        download_dir = settings["downloads"]

    download_path = Path(download_dir).expanduser()
    download_path.mkdir(mode=0o700, parents=True, exist_ok=True)

    if not artifacts:
        return echo_error(
            f"No artifact found for Entitlement: {entitlement_id} Release: {release_id}"
        )
    get_download: Callable
    if mode == "http":
        get_download = client.get_artifact_download_http
    elif mode == "fasp":
        get_download = client._get_artifact_download_fasp

    for artifact in artifacts:
        is_controlled = "controlled" in artifact.get("repository", "ipw")
        file_name = artifact.get("fileName")
        art_id = artifact.get("id")
        if not file_name:
            echo_error(f"API Error: Invalid artifact fileName: {file_name}")

        # Controlled ip can only be downloaded via http
        if is_controlled:
            echo_info("Controlled IP found. Starting download via http...")
            country_code = decode_token().get("ip_country")
            download = client.get_artifact_download_http(
                entitlement_id=entitlement_id,
                release_id=release_id,
                artifact_id=art_id,
                country_code=country_code,
            )
        else:
            download = get_download(
                entitlement_id=entitlement_id, release_id=release_id, artifact_id=art_id
            )

        while download.error.get("name") == "eula-error":
            echo_error(download.error["description"])
            echo()
            if confirm(
                "Do you want to open the EULA link in your default Web browser?",
                default=True,
            ):
                eula_url = download.error["url"]
                echo("Opening default Web browser at link:")
                echo()
                echo(eula_url)
                webbrowser.open(eula_url)
                echo("Please sign the EULA then proceed or abort the download.")
            echo()
            confirm(
                "Do you want to proceed with the download?", default=True, abort=True
            )
            download = get_download(
                entitlement_id=entitlement_id, release_id=release_id, artifact_id=art_id
            )

        file_path = (Path(download_path) / file_name).resolve()
        echo(f"Downloading {file_path}")
        if mode == "http" or is_controlled:
            write_download(file_path, download)
        elif mode == "fasp":
            _fasp_download(file_path, download)
    echo_info("All done!")


if __name__ == "__main__":
    main()
