__salt__ = {}


def get_key_hash(path):
    output = __salt__["cmd.run"](f"ssh-keygen -lf {path}")
    return output.split(" ")[1]
