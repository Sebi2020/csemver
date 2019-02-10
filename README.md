# csemver
csemver is the object orientied optimized Version of semver. It is much more consistent because you only need one object for all operations.

## Features
### Increase Versions
To increase the different versions **csemver** provides three methods
- incMajor
- incMinor
- incPatch

```python
from csemver import csemver as Version
a = Version();
print(a)
a.incMajor();
print(a)
a.incMinor();
print(a)
a.incPatch();
print(a)
```

```console
foo@bar:~$ python test.py
0.1.0
1.0.0
1.1.0
1.1.1
```

### Overwrite Version
To overwrite the current Version just set a new **Semver-String** for `csemver.number`
```python
from csemver import csemver as Version
a = Version();
print(a)
a.number ="1.0.0-pre+build.1";
print(a)
```
```bash
foo@bar:~$ python test.py
0.1.0
1.0.0-pre+build.1
```
### Reset Version
Delete the `number` property to reset the Version to `0.1.0`
```python
from csemver import csemver as Version
a = Version("1.0.0");
print(a)
del a.number
print(a)
```

```bash
foo@bar:~$ python test.py
1.0.0
0.1.0
```

### Compare different versions:
You can compare **csemver** instances with `>, >=, ==, !=, <=, <`
```python
from csemver import csemver as Version

a = Version("1.1.1")
b = Version("1.1.1")
repr(a)
repr(b)
print(a<b)

b.incPatch()
print(b)
print(a<b)
```

```bash
foo@bar:~$ python test.py
Version<1.1.1> instance at 0x00000159D2061BA8
Version<1.1.1> instance at 0x00000159D2061DD8
False
1.1.2
True
```