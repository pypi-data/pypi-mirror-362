import os
from functools import lru_cache, partial
from logging import getLogger
from pathlib import Path

import jwt
from msal import ConfidentialClientApplication, SerializableTokenCache, TokenCache

from edmgr.config import settings
from edmgr.exceptions import EdmAuthError, EdmTokenExpiredError, EdmTokenNotFoundError

logger = getLogger(__name__)


@lru_cache(maxsize=2)
def _get_jwk_client(jwks_uri: str) -> jwt.PyJWKClient:
    logger.debug(f"Creating JWK Client for {jwks_uri}")
    return jwt.PyJWKClient(jwks_uri, cache_keys=True, max_cached_keys=2)


def decode_jwt_token(
    token: str, check_signature: bool = True, check_claims: bool = True
) -> dict:
    """
    Validates a JWT string by decoding its payload and checking if expired

    :param token: Encoded JWT in string format
    :raises EdmAuthError: if the token is invalid or expired
    :return: A tuple with:
        the encoded JWT in string format
        and a TokenMeta instance with the payload
    """
    options = {
        "verify_signature": check_signature,
        "verify_exp": check_claims,
        "verify_aud": False,
        "verify_iss": check_claims,
        "verify_iat": False,
        "verify_nbf": False,
        "require": ["exp", "iss"],
    }
    try:
        if check_signature:
            jwks_client = _get_jwk_client(settings["jwks_uri"])
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            logger.debug("Decoding JWT and verifying signature")
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                options=options,
            )
        else:
            logger.debug("Decoding JWT without signature verification")
            payload = jwt.decode(token, options=options)
    except jwt.ExpiredSignatureError as e:
        raise EdmTokenExpiredError("Token expired.") from e
    except jwt.InvalidTokenError as e:
        raise EdmAuthError(f"Invalid token: {e}") from e
    return payload


def get_msal_cache_path() -> Path:
    """Return pathlib.Path of the MSAL cache file"""
    return Path(settings["edm_root"]) / "msal_cache"


def get_jwt_cache_path() -> Path:
    """Return pathlib.Path of the JWT cache file"""
    return Path(settings["edm_root"]) / "token"


def _write_cache(data: str, cache_file: Path) -> int:
    cache_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    logger.debug(f"Writing cache file: {cache_file}")
    with open(
        cache_file, "w", opener=partial(os.open, mode=0o600), encoding="utf-8"
    ) as file_handler:
        bytes_written = file_handler.write(data)
    return bytes_written


def delete_cache() -> None:
    """Remove both MSAL and JWT cached files"""
    msal_cache: Path = get_msal_cache_path()
    cached_jwt: Path = get_jwt_cache_path()
    if msal_cache.is_file():
        logger.debug("Removing msal cache: %s", msal_cache)
        msal_cache.unlink()
    if cached_jwt.is_file():
        logger.debug("Removing cached token: %s", cached_jwt)
        cached_jwt.unlink()


def save_jwt_cache(token: str) -> int:
    jwt_cache_file: Path = get_jwt_cache_path()
    return _write_cache(token, jwt_cache_file)


def save_msal_cache(cache: SerializableTokenCache) -> int:
    msal_cache_file: Path = get_msal_cache_path()
    return _write_cache(cache.serialize(), msal_cache_file)


def msal_login(
    username: str | None = None,
    password: str | None = None,
    timeout: float | tuple | None = None,
    cache: TokenCache = None,
) -> str:
    """
    Get an access token in JWT string format from MSAL. The token is acquired
    using either a TokenCache instance or username and password.

    :param username: MSAuth Username
    :param password: MSAuth Password
    :param timeout: MSAuth API requests timeout
    :param cache: MSAL TokenCache instance
    :raises EdmAuthError: In the event of an error while acquiring the access token
    :return: Access token in JWT string format
    """
    if cache is None:
        cache = TokenCache()

    access_token: str | None = token_from_msal_cache(cache)
    if access_token is not None:
        try:
            decode_jwt_token(access_token)
            return access_token
        except EdmAuthError as err:
            logger.debug("MSAL token invalid/expired: %s", err)
            remove_token_from_msal_cache(cache, access_token)

    logger.debug("Acquiring new MSAL token")
    app = ConfidentialClientApplication(
        client_id=settings.get("client_id"),
        authority=settings.get("authority"),
        token_cache=cache,
        timeout=timeout,
    )
    accounts: list[dict] = cache.find(TokenCache.CredentialType.ACCOUNT, query={})
    msal_token: dict = {}

    if accounts:
        logger.debug("Account found in MSAL cache, attempting to retrieve token")
        msal_token = app.acquire_token_silent(
            settings.get("account_scopes"), account=accounts[0]
        )
    if not msal_token:
        if (username is None) or (password is None):
            raise EdmTokenNotFoundError("Access token not found on server.")

        logger.debug("Login token not found in MSAL cache, acquiring a new one")
        msal_token = app.acquire_token_by_username_password(
            username=username, password=password, scopes=settings.get("account_scopes")
        )
    if not msal_token:
        raise EdmAuthError("Unknown error while obtaining access token.")

    if "error" in msal_token:
        raise EdmAuthError(msal_token["error_description"])

    return msal_token["access_token"]


def msal_logout(cache: TokenCache) -> None:
    """
    Sings the current account off.

    :param cache: MSAL TokenCache instance used to login
    """
    accounts: list = cache.find(TokenCache.CredentialType.ACCOUNT, query={})
    if accounts:
        cache.remove_account(accounts[0])


def remove_token_from_msal_cache(cache: TokenCache, access_token: str) -> None:
    """
    Find and remove access token stored in MSAL cache.

    :param cache: MSAL TokenCache instance
    :param access_token: JWT string
    """
    expired_msal_tokens: list[dict] = cache.find(
        TokenCache.CredentialType.ACCESS_TOKEN, query={"secret": access_token}
    )
    if expired_msal_tokens:
        logger.debug("Removing expired token from cache: %s", access_token)
        cache.remove_at(expired_msal_tokens[0])


def token_from_msal_cache(cache: TokenCache) -> str | None:
    """
    Find and return access token stored in MSAL cache.

    :param cache: MSAL TokenCache instance

    :return: JWT string if found in cache, None otherwise
    """
    tokens: list = cache.find(TokenCache.CredentialType.ACCESS_TOKEN, query={})
    if tokens:
        access_token = tokens[0].get("secret")
        logger.debug("Token found in MSAL cache: %s", access_token)
    else:
        access_token = None
        logger.debug("Token not found in MSAL cache")
    return access_token


def get_msal_cache() -> SerializableTokenCache | None:
    """
    Load MSAL TokenCache from cached file.

    :return: SerializableTokenCache if file exists on disk, None otherwise
    """
    cache = None
    msal_cache: Path = get_msal_cache_path()
    if msal_cache.exists():
        cache = SerializableTokenCache()
        cache.deserialize(msal_cache.read_text(encoding="utf-8"))
    return cache


def get_jwt_cache() -> str | None:
    """
    Load JWT string from cached file.

    :return: JWT string if file exists on disk, None otherwise
    """
    token = None
    cached_jwt: Path = get_jwt_cache_path()
    if cached_jwt.exists():
        token = cached_jwt.read_text(encoding="utf-8")
    return token
