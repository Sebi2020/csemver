import re,copy
from collections import namedtuple,OrderedDict

from .utils import deprecated,constrain

__author__ = "Sebastian Tilders"
__version__ = "0.2.0"
_vsearch = re.compile(r"""
	^
	(0|[1-9][0-9]*){1}\.(0|[1-9][0-9]*){1}.(0|[1-9][0-9]*){1} # Version
	(\-(0|([1-9][0-9]*|
	[a-zA-Z-][a-zA-Z0-9-]*)
	(\.(0|[1-9][0-9]*|
	[a-zA-Z-][a-zA-Z0-9-]*)
	)*))? # Prerelease
	(\+(0|([1-9][0-9]*|
	[a-zA-Z-][a-zA-Z0-9-]*)
	(\.(0|[1-9][0-9]*|
	[a-zA-Z-][a-zA-Z0-9-]*)
	)*))? # Build
	$
	""",re.VERBOSE)

_valid_ident = re.compile(r"""
					   ^
					   (0|([1-9][0-9]*|
						[a-zA-Z-][a-zA-Z0-9-]*)
						(\.(0|[1-9][0-9]*|
						[a-zA-Z-][a-zA-Z0-9-]*)
						)*)
					   $
					   """, re.VERBOSE)
_num = re.compile(r"^[1-9][0-9]*$")

if not hasattr(__builtins__, 'cmp'):
    def cmp(a, b):
        return (a > b) - (a < b)


class csemver:
	""" Representation of an semantic software version """
	
	__slots__ = ['_version','str_to_fun'];
	def __init__(self, version = "0.1.0"):
		""" Initialises a new Version instance"""
		self._version = self._parse(version)
		self.str_to_fun = {
		'<': self.__lt__,
		'<=':self.__le__,
		'>': self.__gt__,
		'>=': self.__ge__,
		'==': self.__eq__,
		'!=': self.__ne__
		}
	
	def _build(self, val):
		if _valid_ident.match(val) is not None:
			self._version['build'] = val;
		else:
			raise ValueError("Not a valid build tag!")
		
	def _prerelease(self,val):
		newstr = sv.format_version(self._version['major'],self._version['minor'],self._version['patch'],val,self._version['build']);
		self._version = sv.parse(newstr);
	
	@deprecated
	def setNumber(self,val):
		self._version = self._parse(val)

	@deprecated
	def delNumber(self):
		self._version = self._parse("0.1.0")

	@property
	def number(self):
		"""
		Propery which contains directory for the current version.
		
		Delete this property to reset the version to 0.1.0 (Python Version >= 3)
		"""
		return str(self);

	@number.setter
	def number(self,value):
		""" Setter for the version number """
		self._version = self._parse(value)

	@number.deleter
	def number(self):
		""" Resets version number to 0.1.0 """
		self._version = self._parse("0.1.0")

	def incPatch(self, incBy=1):
		""" Increase patch version x.y.z -> x.y.(z+incBy) """
		self._version['patch'] += incBy
		return self

	def incMinor(self,incBy=1):
		""" Increase minor version x.y.z -> x.(y+incBy).0 """
		if(incBy>0):
			self._version['patch'] = 0
			self._version['minor'] += incBy
		return self

	def incMajor(self, incBy=1):
		""" Increase major version x.y.z -> (x+incBy).0.0 """
		if(incBy>0):
			self._version['patch'] = self._version['minor'] = 0
			self._version['major'] += incBy
		return self;

	def __getitem__(self, key):
		""" Returns either major, minor, patch, prerelease or build """
		if isinstance(key,int):
			return tuple(self._version.values())[key]

		return self._version[key];
	def __len__(self):
		l = 0
		for i in self._version.values():
			if i is not None:
				l+=1
		return l

	def __setitem__(self, key, val):
		if key not in ["major", "minor", "patch", "prerelease", "build"]:
			raise KeyError("Key does not exist");

		if key in ['major','minor','patch']:
			if not isinstance(val,(str,int)):
				raise TypeError("%s must be a number or a string!" % key)
			if isinstance(val,str) and _num.match(val) is None:
				raise ValueError("%s must be a number or a string!" % key)
			self._version[key] = int(val);
		else:
			if not isinstance(val, str):
				raise TypeError("%s must be a string" % key)
			if _valid_ident.match(val) is None:
				raise ValueError("%s must be a valid semver identifier!" % key)
			self._version[key] = str(val);

	def __delitem__(self,key):
		if key not in ["major", "minor", "patch", "prerelease", "build"]:
			raise KeyError("Key does not exist");
		self._version[key] = None

	def __str__(self):
		""" Returns a string representation of the semantic version """
		string = "%u.%u.%u" % tuple(self._version.values())[:3]
		if self._version['prerelease'] is not None:
			string += "-%s" % self._version['prerelease']
		if self._version['build'] is not None:
			string += "+%s" % self._version['build']
		return string;

	def _zip_vers(self, o):
		return zip(list(self._version.values())[:4], list(o._version.values())[:4])

	def __eq__(self, value):
	 	if not isinstance(value,csemver):
	 		raise TypeError("This type combination is not supported!");

	 	parts = self._zip_vers(value)
	 	for i,v in parts:
	 		if i != v:
	 			return False
 		return True
		

	def __gt__(self, value):
		if not isinstance(value,csemver):
			raise TypeError("This type combination is not supported!");
		parts = self._zip_vers(value)
		mmp = parts.__iter__()
		# Check major,minor,patch
		for n in range (0,3):
			i,v = next(mmp)
			if(i == v):continue
			if(i > v):
				return True
			else:
				return False
		
		# Check if one prerelease field is none
		i,v = next(mmp)
		if (i is None) and (v is not None):
			return True
		elif (i is not None) and (v is None):
			return False

		# Check prerelease identfiers
		pa = i.split(".")
		pb = v.split(".")
		if len(pa) > len(pb):
			return True
		pa_pb = zip(pa,pb)
		for i,v in pa_pb:
			if _num.match(i) is None and _num.match(v) is not None:
				return True
			if i > v:
				return True

		return False

	def __lt__(self, value):
		if not isinstance(value,csemver):
			raise TypeError("This type combination is not supported!");
		parts = self._zip_vers(value)
		mmp = parts.__iter__()
		# Check major,minor,patch
		for n in range (0,3):
			i,v = next(mmp)
			if(i == v):continue
			if(i < v):
				return True
			else:
				return False
		
		# Check if one prerelease field is none
		i,v = next(mmp)
		if (i is not None) and (v is None):
			return True
		elif (i is None) and (v is not None):
			return False

		# Check prerelease identfiers
		pa = i.split(".")
		pb = v.split(".")
		if len(pa) < len(pb):
			return True
		pa_pb = zip(pa,pb)
		for i,v in pa_pb:
			if _num.match(i) is not None and _num.match(v) is None:
				return True
			if i < v:
				return True

		return False

	def __le__(self, value):
	 	return not self.__gt__(value)

	def __ge__(self, value):
		return not self.__lt__(value)

	def __ne__(self, value):
		parts = self._zip_vers(value)
		for i,v in parts:
			if i != v:
	 			return True
		return False
		

	def __add__(self, value):
		"""
		Suppports addition of versions. The addition respects the semver rules
		"""
		if not isinstance(value,csemver):
			raise TypeError("This type combination is not supported!");
		newV = copy.deepcopy(self);
		newV.incMajor(value['major']);
		newV.incMinor(value['minor']);
		newV.incPatch(value['patch']);
		return newV;

	def __iadd__(self, value):
		"""
	 	Suppports addition + assignment of versions. The addition respects the semver rules
	 	"""
		if not isinstance(value,csemver):
			raise TypeError("This type combination is not supported!");
		self.incMajor(value['major']);
		self.incMinor(value['minor']);
		self.incPatch(value['patch']);
		return self;
	

	def __repr__(self):
		return "{:}<{:}> instance at 0x{:016X}".format(self.__class__.__name__,self.__str__(), id(self));

	@staticmethod
	def _parse(str):
		m = _vsearch.match(str)
		if m is None:
			raise ValueError("Invalid semver string: '%s'" % str);
		m = list(m.groups())
		ret = OrderedDict();
		ret['major'] = int(m[0])
		ret['minor'] = int(m[1])
		ret['patch'] = int(m[2])
		ret['prerelease'] = m[4]
		ret['build'] = m[9]
		return ret

def parse(version = "0.1.0"):
	""" Just an alias for csemver.csemver(version) """
	return csemver(version);

def parse_dir(v = "0.1.0"):
	if not isinstance(v, str):
		raise TypeError("You must supply a string")