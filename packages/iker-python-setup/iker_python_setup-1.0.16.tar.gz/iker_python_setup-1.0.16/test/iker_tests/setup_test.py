import os
import re
import unittest
import unittest.mock

import iker.setup
from iker_tests import resources_directory


class Test(unittest.TestCase):

    def test_read_version_tuple(self):
        major, minor, patch = iker.setup.read_version_tuple(os.path.join(resources_directory, "unittest/setup"),
                                                            version_file="VERSION",
                                                            patch_env_var="DUMMY_BUILD")
        self.assertEqual(major, 1)
        self.assertEqual(minor, 2)
        self.assertEqual(patch, 3)

    def test_read_version_tuple__none_cwd(self):
        with unittest.mock.patch("os.getcwd", return_value=os.path.join(resources_directory, "unittest/setup")):
            major, minor, patch = iker.setup.read_version_tuple(None,
                                                                version_file="VERSION",
                                                                patch_env_var="DUMMY_BUILD")
        self.assertEqual(major, 1)
        self.assertEqual(minor, 2)
        self.assertEqual(patch, 3)

    def test_read_version_tuple__excessive_patch(self):
        major, minor, patch = iker.setup.read_version_tuple(os.path.join(resources_directory, "unittest/setup"),
                                                            version_file="VERSION_EXCESSIVE_PATCH",
                                                            patch_env_var="DUMMY_BUILD")
        self.assertEqual(major, 1)
        self.assertEqual(minor, 2)
        self.assertEqual(patch, 3)

    def test_read_version_tuple__no_patch(self):
        major, minor, patch = iker.setup.read_version_tuple(os.path.join(resources_directory, "unittest/setup"),
                                                            version_file="VERSION_NO_PATCH",
                                                            patch_env_var="DUMMY_BUILD")
        self.assertEqual(major, 1)
        self.assertEqual(minor, 2)
        self.assertEqual(patch, 0)

    def test_read_version_tuple__env_patch(self):
        with unittest.mock.patch.dict(os.environ, {"DUMMY_BUILD": "12345"}):
            major, minor, patch = iker.setup.read_version_tuple(os.path.join(resources_directory, "unittest/setup"),
                                                                version_file="VERSION_NO_PATCH",
                                                                patch_env_var="DUMMY_BUILD")
        self.assertEqual(major, 1)
        self.assertEqual(minor, 2)
        self.assertEqual(patch, 12345)

    def test_read_version_tuple__patch_out_of_range(self):
        with unittest.mock.patch.dict(os.environ, {"DUMMY_BUILD": "123456789"}):
            major, minor, patch = iker.setup.read_version_tuple(os.path.join(resources_directory, "unittest/setup"),
                                                                version_file="VERSION_NO_PATCH",
                                                                patch_env_var="DUMMY_BUILD")
        self.assertEqual(major, 1)
        self.assertEqual(minor, 2)
        self.assertEqual(patch, 999999)

    def test_version_string_local(self):
        version_string = iker.setup.version_string_local(os.path.join(resources_directory, "unittest/setup"),
                                                         version_file="VERSION",
                                                         patch_env_var="DUMMY_BUILD")
        self.assertEqual(version_string, "1.2.3")

    def test_version_string_local__excessive_patch(self):
        version_string = iker.setup.version_string_local(os.path.join(resources_directory, "unittest/setup"),
                                                         version_file="VERSION_EXCESSIVE_PATCH",
                                                         patch_env_var="DUMMY_BUILD")
        self.assertEqual(version_string, "1.2.3")

    def test_version_string_local__no_patch(self):
        version_string = iker.setup.version_string_local(os.path.join(resources_directory, "unittest/setup"),
                                                         version_file="VERSION_NO_PATCH",
                                                         patch_env_var="DUMMY_BUILD")
        self.assertEqual(version_string, "1.2.0")

    def test_version_string_local__env_patch(self):
        with unittest.mock.patch.dict(os.environ, {"DUMMY_BUILD": "12345"}):
            version_string = iker.setup.version_string_local(os.path.join(resources_directory, "unittest/setup"),
                                                             version_file="VERSION_NO_PATCH",
                                                             patch_env_var="DUMMY_BUILD")
        self.assertEqual(version_string, "1.2.12345")

    def test_version_string_local__patch_out_of_range(self):
        with unittest.mock.patch.dict(os.environ, {"DUMMY_BUILD": "123456789"}):
            version_string = iker.setup.version_string_local(os.path.join(resources_directory, "unittest/setup"),
                                                             version_file="VERSION_NO_PATCH",
                                                             patch_env_var="DUMMY_BUILD")
        self.assertEqual(version_string, "1.2.999999")

    def test_version_string_scm(self):
        version_string = iker.setup.version_string_scm(os.path.join(resources_directory, "unittest/setup"),
                                                       version_file="VERSION",
                                                       patch_env_var="DUMMY_BUILD",
                                                       scm_branch_name="dummy_branch",
                                                       scm_branch_env_var="DUMMY_BRANCH")
        self.assertTrue(version_string.startswith("1.2.0"))
        self.assertTrue(re.match(r"^\d+\.\d+\.\d+(\+g[0-9a-f]{7}(\.dirty)?)?$", version_string))

    def test_version_string_scm__none_cwd(self):
        with unittest.mock.patch("os.getcwd", return_value=os.path.join(resources_directory, "unittest/setup")):
            version_string = iker.setup.version_string_scm(None,
                                                           version_file="VERSION",
                                                           patch_env_var="DUMMY_BUILD",
                                                           scm_branch_name="dummy_branch",
                                                           scm_branch_env_var="DUMMY_BRANCH")
        self.assertTrue(version_string.startswith("1.2.0"))
        self.assertTrue(re.match(r"^\d+\.\d+\.\d+(\+g[0-9a-f]{7}(\.dirty)?)?$", version_string))

    def test_version_string_scm__env_branch(self):
        with unittest.mock.patch.dict(os.environ, {"DUMMY_BRANCH": "dummy_branch"}):
            version_string = iker.setup.version_string_scm(os.path.join(resources_directory, "unittest/setup"),
                                                           version_file="VERSION",
                                                           patch_env_var="DUMMY_BUILD",
                                                           scm_branch_name="dummy_branch",
                                                           scm_branch_env_var="DUMMY_BRANCH")
        self.assertEqual(version_string, "1.2.3")

    def test_version_string_scm__scm_root_not_found(self):
        with (
            unittest.mock.patch("os.listdir", return_value=[]),
            self.assertRaises(ValueError),
        ):
            iker.setup.version_string_scm(os.path.join(resources_directory, "unittest/setup"),
                                          version_file="VERSION",
                                          patch_env_var="DUMMY_BUILD",
                                          scm_branch_name="dummy_branch",
                                          scm_branch_env_var="DUMMY_BRANCH")

    def test_version_string(self):
        version_string = iker.setup.version_string(os.path.join(resources_directory, "unittest/setup"),
                                                   version_file="VERSION",
                                                   patch_env_var="DUMMY_BUILD",
                                                   scm_branch_name="dummy_branch",
                                                   scm_branch_env_var="DUMMY_BRANCH")
        self.assertTrue(version_string.startswith("1.2.0"))
        self.assertTrue(re.match(r"^\d+\.\d+\.\d+(\+g[0-9a-f]{7}(\.dirty)?)?$", version_string))

    def test_version_string__env_branch(self):
        with unittest.mock.patch.dict(os.environ, {"DUMMY_BRANCH": "dummy_branch"}):
            version_string = iker.setup.version_string(os.path.join(resources_directory, "unittest/setup"),
                                                       version_file="VERSION",
                                                       patch_env_var="DUMMY_BUILD",
                                                       scm_branch_name="dummy_branch",
                                                       scm_branch_env_var="DUMMY_BRANCH")
        self.assertEqual(version_string, "1.2.3")

    def test_version_string__with_exception_handled(self):
        with unittest.mock.patch("iker.setup.version_string_scm", side_effect=Exception()):
            version_string = iker.setup.version_string(os.path.join(resources_directory, "unittest/setup"),
                                                       version_file="VERSION",
                                                       patch_env_var="DUMMY_BUILD",
                                                       scm_branch_name="dummy_branch",
                                                       scm_branch_env_var="DUMMY_BRANCH")
        self.assertEqual(version_string, "1.2.3")

    def test_version_string__with_exception_raised(self):
        with (
            unittest.mock.patch("iker.setup.version_string_scm", side_effect=Exception()),
            self.assertRaises(Exception),
        ):
            iker.setup.version_string(os.path.join(resources_directory, "unittest/setup"),
                                      version_file="VERSION",
                                      patch_env_var="DUMMY_BUILD",
                                      scm_branch_name="dummy_branch",
                                      scm_branch_env_var="DUMMY_BRANCH",
                                      strict=True)

    def test_version_string__default_fallback(self):
        with (
            unittest.mock.patch("iker.setup.version_string_scm", side_effect=Exception()),
            unittest.mock.patch("iker.setup.version_string_local", side_effect=Exception()),
        ):
            version_string = iker.setup.version_string(os.path.join(resources_directory, "unittest/setup"),
                                                       version_file="VERSION",
                                                       patch_env_var="DUMMY_BUILD",
                                                       scm_branch_name="dummy_branch",
                                                       scm_branch_env_var="DUMMY_BRANCH")
        self.assertEqual(version_string, "0.0.0")
