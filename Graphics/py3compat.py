import sys

if sys.version_info.major == 2:
    def to_bin(x):
        return x
elif sys.version_info.major == 3:
    def to_bin(x):
        return bytes(x, "UTF-8")
else:
    assert False
