__salt__ = {}


# ssh-keygen -t rsa -b 4096 -N '' -f {{path}}/{{repo.key}}
def generate(path, bits=4096, type="rsa", passphrase=""):
    if __salt__["file.file_exists"](path):
        return {path: None}
    _ = __salt__["cmd.run"](f"ssh-keygen -t {type} -b {bits} -N '{passphrase}' -f {path}")
    return {path: True}
