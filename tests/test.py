import csemver as cs
from unittest import TestCase
from unittest import SkipTest
import sys

class TestCsemver(TestCase):
	def test_valid_string(self):
		s = cs.csemver("1.0.0");
		self.assertTrue(isinstance(s, cs.csemver));

	def test_parse_empty(self):
		s = cs.parse();
		self.assertEqual(str(s), "0.1.0");

	def test_parse_with_value(self):
		s = cs.parse("1.0.0");
		self.assertEqual(str(s), "1.0.0");

	def test_inc_major(self):
		s = cs.parse("0.1.1");
		s.incMajor();
		self.assertEqual(str(s),"1.0.0")

	def test_inc_minor(self):
		s = cs.parse("0.1.1");
		s.incMinor();
		self.assertEqual(str(s),"0.2.0");

	def test_inc_patch(self):
		s = cs.parse("0.1.1");
		s.incPatch();
		self.assertEqual(str(s), "0.1.2");

	def test_number_descriptor(self):
		s = cs.parse("1.2.3-pre+build");
		self.assertEqual(s.number, "1.2.3-pre+build");

	def test_assign_version(self):
		if sys.version_info < (3, 0):
			raise SkipTest("must be Python 3.0 or greater")
		s = cs.parse("0.1.0");
		s.number = "1.0.0";
		self.assertEqual(str(s),"1.0.0");

	def test_addition(self):
		a = cs.parse("0.0.1");
		b = cs.parse("0.2.0");
		self.assertEqual(str(a+b),"0.2.0");
		
		a = cs.parse("0.1.1")
		b = cs.parse("0.2.1")
		self.assertEqual(str(a+b),"0.3.1");

		a = cs.parse("0.1.1")
		b = cs.parse("0.0.10")
		self.assertEqual(str(a+b),"0.1.11")

	def test_add_and_assign(self):
		a = cs.parse("0.1.1");
		oldId = id(a);
		b = cs.parse("0.0.4");
		a += b;
		self.assertEqual(oldId, id(a))
		self.assertEqual(str(a),"0.1.5");

	def test_comprehension_greater(self):
		a = cs.parse("2.0.0");
		b = cs.parse("1.0.0");
		self.assertTrue(a>b);
		a = cs.parse("2.0.0");
		b = cs.parse("2.0.0-pre");
		self.assertTrue(a>b);

		a = cs.parse("0.1.0-pre1");
		b = cs.parse("0.1.0-pre");
		self.assertTrue(a>b);

	def test_comprehension_smaller(self):
		a = cs.parse("1.0.0");
		b = cs.parse("2.0.0");
		self.assertTrue(a<b);
		a = cs.parse("1.0.0-pre");
		b = cs.parse("1.0.0");
		self.assertTrue(a<b);

		a = cs.parse("0.1.0-pre");
		b = cs.parse("0.1.0-pre1");
		self.assertTrue(a<b);

	def test_comprehension_equal(self):
		a = cs.parse("1.0.0");
		b = cs.parse("1.0.0");
		self.assertTrue(a == b);

		a = cs.parse("1.0.0-pre");
		b = cs.parse("1.0.0-pre");
		self.assertTrue(a == b);

		a = cs.parse("1.0.0-pre+build");
		b = cs.parse("1.0.0-pre+build");
		self.assertTrue(a == b);

		a = cs.parse("1.0.0-pre+build");
		b = cs.parse("1.0.0-pre+build1");
		self.assertTrue(a == b);

		a = cs.parse("1.0.0-pre1+build");
		b = cs.parse("1.0.0-pre+build");
		self.assertFalse(a == b);

	def test_comprehension_not_equal(self):
		a = cs.parse("1.0.0-pre+build");
		b = cs.parse("1.0.0-pre+build1");
		self.assertFalse(a != b);

	def test_index_ops(self):
		a = cs.parse(); # defaults to 0.1.0
		a['major'] = 2
		self.assertEqual(a.number,"2.1.0")
		a['minor'] = 2
		self.assertEqual(a.number,"2.2.0")
		a['patch'] = 1
		self.assertEqual(a.number,"2.2.1")
		a['prerelease'] = "dev"
		self.assertEqual(a.number,"2.2.1-dev")
		a['build'] = "build0"
		self.assertEqual(a.number,"2.2.1-dev+build0")
		#a['build'] = None
		#self.assertEqual(a.number,"2.2.1-dev")

	def test_special_fields(self):
		raise SkipTest("Deprecated")
		if sys.version_info < (3,0):
			raise SkipTest("must be Python 3.0 or greater");
		a = cs.parse();
		a.prerelease = "pre";
		self.assertEqual(a.number, "0.1.0-pre");

		a.build = "build2";
		self.assertEqual(a.number, "0.1.0-pre+build2");

		del a.prerelease
		self.assertEqual(a.number, "0.1.0+build2")

		del a.build
		self.assertEqual(a.number, "0.1.0")

	def test_special_field_setters(self):
		raise SkipTest("Deprecated")
		a = cs.parse();
		a.setPrerelease("pre");
		self.assertEqual(a.number, "0.1.0-pre");

		a.setBuild("build2");
		self.assertEqual(a.number, "0.1.0-pre+build2");

		a.delPrerelease();
		self.assertEqual(a.number, "0.1.0+build2")

		a.delBuild();
		self.assertEqual(a.number, "0.1.0")		