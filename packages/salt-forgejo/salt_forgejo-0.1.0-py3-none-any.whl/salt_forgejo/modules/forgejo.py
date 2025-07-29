import re
from urllib.parse import urljoin, urlparse

import requests
from salt.exceptions import SaltConfigurationError

__context__ = {}
__salt__ = {}


def _join(base, path):
    scheme = __salt__["config.get"](f"forgejo:{base}:scheme", default="https")
    return urljoin(f"{scheme}://{base}", path)


def _session(base):
    if base not in __context__:
        s = requests.Session()
        token = __salt__["config.get"](f"forgejo:{base}:token", default=SaltConfigurationError)
        if token is SaltConfigurationError:
            raise SaltConfigurationError(f"Missing token for forgejo:{base}")
        s.headers["Authorization"] = f"token {token}"
        s.headers["User-Agent"] = "salt fogejo module"
        __context__[base] = s
    return __context__[base]


# git@git.tsun.dev:kfdm/salt-hinagiku.git
REPO_GIT_RE = re.compile(r"\S+@(?P<host>\S+):(?P<owner>\S+)/(?P<repo>.+)\.\S+")


def parse(repo):
    url = urlparse(repo)
    if url.netloc:
        parts = url.path.split("/")
        return url.netloc, parts[1], parts[2]
    return REPO_GIT_RE.match(url.path).groups()


# https://codeberg.org/api/swagger#/repository/repoGet
def repo(base, owner, repo):
    result = _session(base).get(
        url=_join(base, f"/api/v1/repos/{owner}/{repo}"),
    )
    result.raise_for_status()
    return result.json()


# https://codeberg.org/api/swagger#/organization/orgListRepos
def org_repos(base, owner):
    result = _session(base).get(
        url=_join(base, f"/api/v1/orgs/{owner}/repos"),
    )
    result.raise_for_status()
    return result.json()


# https://codeberg.org/api/swagger#/repository/repoEdit
def repo_patch(base, owner, repo, changes):
    result = _session(base).patch(
        url=_join(base, f"/api/v1/repos/{owner}/{repo}"),
        json=changes,
    )
    result.raise_for_status()
    return result.json()


# https://codeberg.org/api/swagger#/repository/repoListKeys
def repo_keys_list(base, owner, repo):
    result = _session(base).get(
        url=_join(base, f"/api/v1/repos/{owner}/{repo}/keys"),
    )
    result.raise_for_status()
    return result.json()


# https://codeberg.org/api/swagger#/repository/repoCreateKey
def repo_key_post(base, owner, repo, keyfile, read_only=True, title=None):
    keydata = __salt__["file.read"](keyfile)

    # If title is not set, then we'll try to get it from the key itself
    if title is None:
        _, _, title = keydata.split(" ")

    result = _session(base).post(
        url=_join(base, f"/api/v1/repos/{owner}/{repo}/keys"),
        json={
            "key": keydata,
            "title": title,
            "read_only": read_only,
        },
    )
    result.raise_for_status()
    return result.json()


def orgParse(org):
    url = urlparse(org)
    match url.path.split("/"):
        case _, org:
            return url.netloc, org
        case _, "org", org:
            return url.netloc, org
    raise Exception(f"Unable to parse org: {org}")


# https://codeberg.org/api/swagger#/organization/orgGet
def orgGet(base, org):
    result = _session(base).get(
        url=_join(base, f"/api/v1/orgs/{org}"),
    )
    result.raise_for_status()
    return result.json()


# https://codeberg.org/api/swagger#/organization/orgEdit
def orgEdit(base, org, changes):
    result = _session(base).patch(
        url=_join(base, f"/api/v1/orgs/{org}"),
        json=changes,
    )
    result.raise_for_status()
    return result.json()
