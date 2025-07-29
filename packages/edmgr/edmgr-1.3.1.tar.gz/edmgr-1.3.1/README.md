# Entitlements and Download Manager

This package installs a CLI that allows users to see their entitlements,
released products for those entitlements and to download those products.


## Installation

### Basic Installation
```bash
$ python -m pip install edmgr
```
Python 3.10+ supported. Recommended Python 3.13.


### IBM Aspera FASP Downloads
In order to enable IBM Aspera FASP protocol for downloading artifacts, IBM
aspera-cli and its FASP protocol extension are required.

Please install it by following the instructions at
 - [IBM Aspera CLI Installation](https://github.com/IBM/aspera-cli#installation)
 - [IBM Aspera CLI FASP protocol](https://github.com/IBM/aspera-cli#fasp-protocol)

Please make sure that `ascli` executable is on your `$PATH` when running edmgr CLI.


## Usage - API Wrapper

```python
from edmgr import Client
import os

# Instanciate a Client using a JWT
client = Client(token=os.getenv('access_token'))

# NOTE: Client will look for EDM_ACCESS_TOKEN environment variable, if set it
# will use its value as a token thus a Client instance could be created
# without passing any argument.

client = Client()

# NOTE: Creating a Client instance with token keyword takes precedence over
# EDM_ACCESS_TOKEN environment variable.

# Instanciate a Client using username and password
client = Client(username=os.getenv('username'), password=os.getenv('password'))

# NOTE: When creating a Client instance with username and password, the
# client will obtain an access token and automatically refresh it once
# expired.

# NOTE: When EDM_ACCESS_TOKEN environment variable is set, its value will take
# precendence over username and password login method and won't be refreshed once expired.

# Get a list of entitlements
response: list = client.get_entitlements()

# Get a paginated list of entitlements
response: list = client.get_entitlements(params={'offset': 1, 'limit': 10})

# Get a list with a single entitlement
response: list = client.get_entitlements(entitlement_id="388295")

# Get a list of entitlements by performing a search query
# Note: not all the keys are searchable
response: list = client.find_entitlements({"product.id": "DS000"})

# Get a list of releases
response: list = client.get_releases(entitlement_id="388295")

# Get a list with a single release
response: list = client.get_releases(
  entitlement_id="388295", release_id="9456330a-54c6-48b9-a92d-990f9c302b42"
)

# Get a list of artifacts
response: list = client.get_artifacts(
  entitlement_id="388295", release_id="9456330a-54c6-48b9-a92d-990f9c302b42"
)

# Get a list with a single artifact
response: list = client.get_artifacts(
  entitlement_id="388295", release_id="9456330a-54c6-48b9-a92d-990f9c302b42",
  artifact_id="942b3b7d-d6fc-4fb6-ac6f-5afbf898514c"
)

# Get artifact's download url
response: dict = client.get_artifact_download_url(
  entitlement_id="388295", release_id="9456330a-54c6-48b9-a92d-990f9c302b42",
  artifact_id="942b3b7d-d6fc-4fb6-ac6f-5afbf898514c"
)

# Download all artifacts for a release (in the current directory)
artifacts: list = client.get_artifacts(
  entitlement_id="388295", release_id="9456330a-54c6-48b9-a92d-990f9c302b42",
)
for file_name, artifact_id in map(lambda x: (x['fileName'], x['id']), artifacts):
    with open(file_name, "wb") as file:
        client.download_artifact(
          file,
          entitlement_id="388295",
          release_id="9456330a-54c6-48b9-a92d-990f9c302b42",
          artifact_id=artifact_id
        )
```


## Usage - CLI

### Help

```
 $ edmgr --help
Usage: edmgr [OPTIONS] COMMAND [ARGS]...

Options:
  -k, --environment [prod|sandbox|qa]
                                  Configuration environment  [default: prod]
  --version                       Show the version and exit.
  -v, --verbose
  --help                          Show this message and exit.

Commands:
  artifacts           Print a list of artifacts for a particular release.
  download-artifacts  Download all artifacts for a particular release or...
  entitlement         Print single entitlement details
  entitlements        Print a list of available entitlements.
  login               Login using credentials/token
  logout              Logout by deleting cached token
  releases            Print a list of releases for a particular entitlement.
  show-config         Print configuration
```


### Login

There are three ways to authenticate on EDM.

1. Using a JWT token from the command line: Use `edmgr login token TOKEN`. The
   token will be persisted on disk and used until its expiration. Once the token
   has expired, a new one must be obtained by the user.
2. Using username and password (credentials): Use `edmgr login credentials`
   and press enter. You will be prompted for username and password, or use
   `edmgr login credentials --username USERNAME` and only the password will
   be prompted. An access token will be persisted on disk and refreshed
   automatically when expired.
3. Using a JWT token in an environment variable: Set `EDM_ACCESS_TOKEN="<JWT string>"`.
   The token will **not** be persisted on disk. Once the token has expired, a new
   one must be obtained by the user.

In case more than one authentication method is set, the above order also
determine the precedence of the method used by edmgr.

```
$ edmgr login --help
Usage: edmgr login [OPTIONS] COMMAND [ARGS]...

  Login using credentials/token

Options:
  --help  Show this message and exit.

Commands:
  credentials  Login using username and password
  show-token   Print Access Token as JWT string with some extra information.
  token        Login using JWT string
```


### Entitlements

```
$ edmgr entitlements --help
Usage: edmgr entitlements [OPTIONS]

  Print a list of available entitlements.

Options:
  -e, --entitlement-id TEXT       Entitlement ID to retrieve one
  -p, --product-code TEXT         Filter by product code
  -o, --offset INTEGER RANGE      Page number to paginate output  [x>=1]
  -l, --limit INTEGER RANGE       Number of records per page to be displayed.
                                  By default it shows 10 records per page.
                                  This option is ignored if no offset was
                                  given.  [x>=1]
  -f, --format [table|json|jsonpp]
                                  Output format -> tabular, json or json
                                  prettify  [default: table]
  --help                          Show this message and exit.
```

```
$ edmgr entitlement --help
Usage: edmgr entitlement [OPTIONS] ENTITLEMENT_ID

  Print single entitlement details

Options:
  -p, --product-code TEXT         Filter grouped entitlements by Product Code
  -o, --offset INTEGER RANGE      Page number to paginate output  [x>=1]
  -l, --limit INTEGER RANGE       Number of records per page to be displayed.
                                  By default it shows 10 records per page.
                                  This option is ignored if no offset was
                                  given.  [x>=1]
  -f, --format [table|json|jsonpp]
                                  Output format -> tabular, json or json
                                  prettify  [default: table]
  --help                          Show this message and exit.
```


### Releases

```
$ edmgr releases --help
Usage: edmgr releases [OPTIONS]

  Print a list of releases for a particular entitlement.

Options:
  -e, --entitlement-id TEXT       Entitlement ID  [required]
  -r, --release-id TEXT           Release ID to retrieve one
  -f, --format [table|json|jsonpp]
                                  Output format -> tabular, json or json
                                  prettify  [default: table]
  --help                          Show this message and exit.
```


### Artifacts

```
$ edmgr artifacts --help
Usage: edmgr artifacts [OPTIONS]

  Print a list of artifacts for a particular release.

Options:
  -e, --entitlement-id TEXT       Entitlement ID  [required]
  -r, --release-id TEXT           Release ID  [required]
  -a, --artifact-id TEXT          Artifact ID to retrieve one
  -f, --format [table|json|jsonpp]
                                  Output format -> tabular, json or json
                                  prettify  [default: table]
  --help                          Show this message and exit.
```


### Download Artifacts

```
$ edmgr download-artifacts --help
Usage: edmgr download-artifacts [OPTIONS]

  Download all artifacts for a particular release or only a specific one.

Options:
  -e, --entitlement-id TEXT  Entitlement ID  [required]
  -r, --release-id TEXT      Release ID  [required]
  -a, --artifact-id TEXT     Artifact ID
  -d, --download-dir TEXT    Directory in which artifacts are downloaded.
                             Default: $HOME/Artifacts
  -m, --mode [http|fasp]     The protocol used to download the files. Default:
                             http
  --help                     Show this message and exit.
```

### Shell Completions

Tab completions for Bash (version 4.4 and up), Zsh, and Fish can be enabled by
running the following command in your shell:

```bash
eval "$(_EDMGR_COMPLETE=<shell>_source edmgr)"
```
Where `<shell>` is either `bash`, `zsh` or `fish`


## Environment Variables

The following environment variables can be used to configure both API Wrapper and CLI.

- `EDM_ACCESS_TOKEN`: API authentication JWT, please refer to the above sections for more information
- `EDM_ROOT`: Directory in which EDM will store cached files. If not set, the default is `$HOME/.edm`
- `EDM_DOWNLOADS`: Directory in which EDM will save downloaded artifacts. If not set, the default is `$HOME/Artifacts`
- `EDM_LOG_LEVEL`: EDM log level. Options: critical, error, warning, info, debug. If not set, the default is `info`
- `EDM_ENV`: The name of the configuration environment used. Options: prod, sandbox, qa. If not set, the default is `prod`


## Known Bugs

- `ImportError: symbol not found in flat namespace (_ffi_prep_closure)`
is thrown by `edmgr.auth.decode_jwt_token()` with `check_signature` argument
`True` when running Python 3.7 on Apple M1. This is due to cffi 1.15.0 module's
lib `_cffi_backend.cpython-37m-darwin.so` trying to load `_ffi_prep_closure`
symbol. This bug affects CLI `edmgr login token` command
