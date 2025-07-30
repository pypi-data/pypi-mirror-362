"""Test coverage for environment-only mode functionality."""

import os
import tempfile
import unittest
from unittest.mock import patch

from bdtemplater.bdtemplatize import main


class TestEnvironmentOptionalProperties(unittest.TestCase):
    """Test environment flags make properties file optional."""

    def test_env_flags_make_properties_optional(self):
        """Test that environment flags make properties file optional."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write("Hello @USER@")
            template_file.flush()

            try:
                # Test with --env flag and verbose output
                with patch("os.environ", {"USER": "World"}):
                    with patch("sys.stderr"):
                        main([template_file.name, "--env", "--verbose"])

                # Test with --env-prefix flag
                with patch("os.environ", {"USER": "World"}):
                    with patch("sys.stderr"):
                        main([template_file.name, "--env-prefix", "--verbose"])

                # Test with --env-key-strip flag
                with patch("os.environ", {"TEST_USER": "World"}):
                    with patch("sys.stderr"):
                        main(
                            [
                                template_file.name,
                                "--env-key-strip",
                                "TEST_",
                                "--verbose",
                            ]
                        )

                # Test with --env-key-strip-hcdefaults flag
                with patch("os.environ", {"TF_VAR_USER": "World"}):
                    with patch("sys.stderr"):
                        main(
                            [
                                template_file.name,
                                "--env-key-strip-hcdefaults",
                                "--verbose",
                            ]
                        )

            finally:
                os.unlink(template_file.name)

    def test_env_flags_present_check(self):
        """Test that env_flags_present check works correctly."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write("Hello @USER@")
            template_file.flush()

            try:
                # Test case where env flags are present and properties file is default
                with patch("os.environ", {"USER": "World"}):
                    with patch("sys.stderr"):
                        # This should trigger the env_flags_present = True and
                        # properties_file = "terraform.tfvars" case
                        main(
                            [
                                template_file.name,
                                "terraform.tfvars",
                                "--env",
                                "--verbose",
                            ]
                        )

            finally:
                os.unlink(template_file.name)


if __name__ == "__main__":
    unittest.main()

# Contains AI-generated edits.
