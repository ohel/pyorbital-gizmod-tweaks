import os

def readlinkabs(l):
    """
    Return an absolute path for the destination 
    of a symlink
    """
    if not (os.path.islink(l)):
        return None
    p = os.readlink(l)
    if os.path.isabs(p):
        return p
    return os.path.join(os.path.dirname(l), p)

