import logging
import os
from copy import deepcopy
from pathlib import Path

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}


def get_log_level(log_level: str) -> int:
    try:
        return LOG_LEVELS[log_level.lower()]
    except KeyError as e:
        msg = (
            "Invalid log level."
            f" Please use one of the following: {', '.join(LOG_LEVELS.keys())}"
        )
        raise ValueError(msg) from e


def get_log_level_from_verbose(verbosity: int) -> int:
    levels = list(LOG_LEVELS)
    try:
        level = levels[verbosity + 1]
    except IndexError as e:
        raise ValueError("Invalid verbosity level. Please choose 1, 2 or 3.") from e
    return get_log_level(level)


try:
    WORK_DIR = Path.home()
except (KeyError, RuntimeError):
    WORK_DIR = Path(".")

TOKEN_HOST_URL = "https://account.arm.com"

PROD = {
    "access_token": os.getenv("EDM_ACCESS_TOKEN"),
    "authority": "/".join(
        [TOKEN_HOST_URL, "armb2c.onmicrosoft.com", "B2C_1A_ROPC_Auth.ropc"]
    ),
    "jwks_uri": "/".join(
        [
            TOKEN_HOST_URL,
            "armb2c.onmicrosoft.com",
            "b2c_1a_hv.sign-in.1.1.0/discovery/v2.0/keys",
        ]
    ),
    "client_id": "bcca11a6-8f8f-42d9-aa4d-0f46815d9c75",
    "account_scopes": ["openid bcca11a6-8f8f-42d9-aa4d-0f46815d9c75 offline_access"],
    "edm_root": str(Path(os.getenv("EDM_ROOT", f"{WORK_DIR}/.edm")).expanduser()),
    "downloads": str(
        Path(os.getenv("EDM_DOWNLOADS", f"{WORK_DIR}/Artifacts")).expanduser()
    ),
    "base_url": "https://api.arm.com",
    "aspera_url": "https://arm-dropzones.ibmaspera.com",
    "entitlement_endpoint": "e-product-entitlement-customer/v1/entitlements",
    "log_level": get_log_level(os.getenv("EDM_LOG_LEVEL", "error")),
    "no_progress_bar": False,
}


QA = {
    **PROD,
    "base_url": "https://qas.api.arm.com",
    "authority": "/".join(
        [TOKEN_HOST_URL, "armb2ctest.onmicrosoft.com", "B2C_1A_ROPC_Auth.ropc"]
    ),
    "jwks_uri": "/".join(
        [
            TOKEN_HOST_URL,
            "armb2ctest.onmicrosoft.com",
            "discovery/v2.0/keys?p=b2c_1a_ropc_auth.ropc",
        ]
    ),
    "client_id": "243bffb8-b622-471b-9474-05e26dd1e51a",
    "account_scopes": ["openid 243bffb8-b622-471b-9474-05e26dd1e51a offline_access"],
}


SANDBOX = {
    **QA,
    "base_url": "https://sandbox.api.arm.com",
}


ENVS = (
    "QA",
    "PROD",
    "SANDBOX",
)


class Settings:
    def __init__(self):
        self._env: dict = None
        self.set_env(os.getenv("EDM_ENV", "PROD"))

    def __getitem__(self, key):
        return self._env[key]

    def __setitem__(self, key, val):
        self._env[key] = val

    def __str__(self) -> str:
        return str(self._env)

    def get(self, key, default=None):
        return self._env.get(key, default)

    def set_env(self, env: str):
        env = env.upper()
        if env not in ENVS:
            msg = (
                "Invalid environment name."
                f" Please use one of the following: {', '.join(ENVS)}"
            )
            raise ValueError(msg)
        self._env = deepcopy(globals()[env])
        return self


settings = Settings()
