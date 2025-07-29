__opts__ = {}
__salt__ = {}


def patch(name, **kwargs):
    ret = {"name": name, "result": False, "changes": {}}

    base, owner, repo = __salt__["forgejo.parse"](name)
    original = __salt__["forgejo.repo"](base, owner, repo)

    if __opts__["test"]:
        for key in kwargs:
            if original[key] != kwargs[key]:
                ret["changes"][key] = kwargs[key]
        ret["result"] = None
        ret["comment"] = f"Will update {name}"
    else:
        updated = __salt__["forgejo.repo_patch"](base, owner, repo, changes=kwargs)
        for key in kwargs:
            if original[key] != updated[key]:
                ret["changes"][key] = updated[key]
        ret["result"] = True
        ret["comment"] = f"Updated {name}"
    return ret


def repo_key(name, source, **kwargs):
    ret = {"name": name, "result": False, "changes": {}}
    keyfile = __salt__["cp.cache_file"](source)
    hash = __salt__["keygen.get_key_hash"](keyfile)

    base, owner, repo = __salt__["forgejo.parse"](name)
    for key in __salt__["forgejo.repo_keys_list"](base, owner, repo):
        if key["fingerprint"] == hash:
            ret["comment"] = f"Found existing key: {hash}"
            ret["result"] = True
            return ret

    if __opts__["test"]:
        ret["comment"] = f"Would install key: {source}"
        ret["result"] = None
        return ret

    ret["changes"] = __salt__["forgejo.repo_key_post"](base, owner, repo, keyfile, **kwargs)
    ret["comment"] = "Key Updated"
    ret["result"] = True
    return ret


def org(name, **kwargs):
    ret = {"name": name, "result": False, "changes": {}}
    base, org = __salt__["forgejo.orgParse"](name)

    original = __salt__["forgejo.orgGet"](base, org)

    if __opts__["test"]:
        for key in kwargs:
            if original[key] != kwargs[key]:
                ret["changes"][key] = kwargs[key]
        ret["result"] = None
        ret["comment"] = f"Will update {name}"
    else:
        updated = __salt__["forgejo.orgEdit"](base, org, changes=kwargs)
        for key in kwargs:
            if original[key] != updated[key]:
                ret["changes"][key] = updated[key]
        ret["result"] = True
        ret["comment"] = f"Updated {name}"
    return ret
