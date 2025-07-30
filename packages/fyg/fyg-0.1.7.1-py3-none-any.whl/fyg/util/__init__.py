import os
from .io import read, write, writejson, ask, confirm, selnum
from .reporting import start_timer, end_timer, set_log, close_log, closedeeps, deeplog, log, set_error, error

def rm(pname):
    if os.path.islink(pname):
        log("removing symlink: %s"%(pname,), 2)
        os.remove(pname)
    elif os.path.isdir(pname):
        log("removing folder: %s"%(pname,), 2)
        os.rmdir(pname)
    elif os.path.exists(pname):
        log("removing file: %s"%(pname,), 2)
        os.remove(pname)
    else:
        log("can't remove file (doesn't exist): %s"%(pname,), 2)

def indir(data, path):
    for f in [os.path.join(path, p) for p in os.listdir(path)]:
        if os.path.isfile(f) and data == read(f, binary=True):
            return os.path.split(f)[-1]

def batch(dlist, f, *args, **kwargs):
    chunk = kwargs.pop("chunk", 1000)
    i = 0
    while i < len(dlist):
        f(dlist[i:i+chunk], *args, **kwargs)
        i += chunk

class Loggy(object):
    def subsig(self):
        pass

    def sig(self):
        ss = self.subsig()
        sig = self.__class__.__name__
        return ss and "%s(%s)"%(sig, ss) or sig

    def log(self, *msg):
        print(self.sig(), ":", *msg)

class Named(Loggy):
    def __init__(self, name):
        self.name = name

    def subsig(self):
        return self.name