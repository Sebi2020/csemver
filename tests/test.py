import csemver as cs
from unittest import TestCase

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
		self.assertEqual(s.number['major'],1);
		self.assertEqual(s.number['minor'],2);
		self.assertEqual(s.number['patch'],3);
		self.assertEqual(s.number['prerelease'],"pre");
		self.assertEqual(s.number['build'],"build");

	def test_assign_version(self):
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