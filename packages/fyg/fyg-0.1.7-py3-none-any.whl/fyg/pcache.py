import getpass
from base64 import b64encode, b64decode
from .util import read, write

class PCache(object):
	def __init__(self, cfg):
		self.fname = cfg
		self._cache = read(cfg, isjson=True, default={}, b64=True)

	def _save(self):
		write(self._cache, self.fname, isjson=True, b64=True)

	def __call__(self, key, password=True, overwrite=False):
		dk = b64encode(key.encode()).decode()
		if overwrite or dk not in self._cache:
			p = (password and getpass.getpass or input)(key)
			if input("store %s? [Y/n]: "%(password and "password" or "value")).lower().startswith("n"):
				return p
			self._cache[dk] = b64encode(p.encode()).decode()
			self._save()
		return b64decode(self._cache[dk]).decode()