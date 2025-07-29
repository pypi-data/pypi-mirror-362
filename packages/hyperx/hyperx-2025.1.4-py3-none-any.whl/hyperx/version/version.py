major = 2025
minor = 1
revision = 4
patch = 0

if patch != 0:
    __version__ = ".".join([str(major), str(minor), str(revision), str(patch)])
else:
    __version__ = ".".join([str(major), str(minor), str(revision)])
