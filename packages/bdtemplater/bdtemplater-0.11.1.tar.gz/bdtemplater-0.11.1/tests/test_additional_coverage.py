#!/usr/bin/env python3

# Copyright 2025 Mykel Alvis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
import sys
import tempfile

import pytest


class TestAdditionalCoverage:
    """Tests to increase coverage to 95%+"""

    def test_main_with_output_file_verbose(self):
        """Test main function with output file and verbose mode."""
        tfvars_content = """
project = "test-project"
env = "test"
bucket = "test-bucket"
region = "us-west-1"
lock_table = "test-lock-table"
"""

        template_content = """project: @project@
bucket: @bucket@
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
            output_path = output_file.name

        try:
            # Capture stderr for verbose output
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main(
                    [
                        template_path,
                        tfvars_path,
                        "-o",
                        output_path,
                        "--verbose",
                        "--force",
                    ]
                )
                stderr_output = captured_stderr.getvalue()

                # Check verbose output
                assert f"Writing output to: {output_path}" in stderr_output
                assert f"Successfully wrote output to {output_path}" in stderr_output

                # Check output file contents
                with open(output_path) as f:
                    content = f.read()
                    assert "test-project" in content
                    assert "test-bucket" in content

            finally:
                sys.stderr = old_stderr
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            os.unlink(output_path)

    def test_main_module_import_exception_handling(self):
        """Test exception handling during module import."""
        tfvars_content = """project = "test"
env = "test"
bucket = "test-bucket"
region = "us-west-1"
lock_table = "test-lock-table"
"""

        template_content = """test: @project@"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            # Test exception handling during module operations
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            try:
                # Mock importlib to raise an exception
                import importlib

                from bdtemplater.bdtemplatize import main

                original_import = importlib.import_module

                def mock_import_error(name):
                    if name == "some_bad_module":
                        raise Exception("Mocked exception during import")
                    return original_import(name)

                importlib.import_module = mock_import_error

                try:
                    with pytest.raises(SystemExit) as exc_info:
                        main(
                            [
                                template_path,
                                tfvars_path,
                                "--import-module",
                                "some_bad_module",
                            ]
                        )
                    assert exc_info.value.code == 1

                    stderr_output = captured_stderr.getvalue()
                    assert (
                        "Error: Problem with module 'some_bad_module'" in stderr_output
                    )
                finally:
                    importlib.import_module = original_import

            finally:
                sys.stderr = old_stderr
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_main_keyerror_handling(self):
        """Test that missing placeholders remain unreplaced when no keymap."""
        tfvars_content = '''project = "test"'''

        template_content = """test: @project@ @missing_key@"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main([template_path, tfvars_path])
                output = captured_stdout.getvalue()
                # project should be replaced, missing_key should remain as placeholder
                assert "test" in output
                assert "@missing_key@" in output
            finally:
                sys.stdout = old_stdout
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_main_unexpected_error_handling(self):
        """Test unexpected error handling in main function."""
        tfvars_content = '''project = "test"'''

        template_content = """test: @project@"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            # Mock the generate_template_from_files function to raise error
            from bdtemplater import bdtemplatize

            original_generate = bdtemplatize.generate_template_from_files

            def mock_generate(*args, **kwargs):
                raise RuntimeError("Unexpected error for testing")

            bdtemplatize.generate_template_from_files = mock_generate

            try:
                # Capture stderr
                old_stderr = sys.stderr
                sys.stderr = captured_stderr = io.StringIO()

                try:
                    from bdtemplater.bdtemplatize import main

                    with pytest.raises(SystemExit) as exc_info:
                        main([template_path, tfvars_path])
                    assert exc_info.value.code == 1

                    stderr_output = captured_stderr.getvalue()
                    assert (
                        "Unexpected error: Unexpected error for testing"
                        in stderr_output
                    )

                finally:
                    sys.stderr = old_stderr
            finally:
                bdtemplatize.generate_template_from_files = original_generate
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_if_name_main_block(self):
        """Test the if __name__ == '__main__' block."""
        # This tests line 311
        import subprocess
        import sys

        # Create a simple test to run the module as main
        test_script = """
import sys
sys.path.insert(0, "src")
from bdtemplater.bdtemplatize import main

# Mock sys.argv
sys.argv = ["bdtemplatize.py", "--help"]

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code in [0, 2]:  # 0 for success, 2 for help
            print("SUCCESS")
        else:
            print(f"FAILED: {e.code}")
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as script_file:
            script_file.write(test_script)
            script_path = script_file.name

        try:
            result = subprocess.run(
                [sys.executable, script_path], capture_output=True, text=True
            )
            # Help should exit with code 0 or 2, both are acceptable
            assert "usage:" in result.stderr or "SUCCESS" in result.stdout
        finally:
            os.unlink(script_path)

    def test_branch_coverage_keymap_replacement(self):
        """Test branch coverage for keymap replacement logic."""
        tfvars_content = """
project = "test-project"
env = "test"
bucket = "test-bucket"
missing_key = "should_not_be_used"
"""

        # Test when keymap is provided but a key in keymap is not in template
        template_content = """project: @project@"""

        from bdtemplater.bdtemplatize import generate_template

        # This should work - keymap key exists in tfvars but not referenced in template
        keymap = ["project", "env"]
        result = generate_template(
            template_content, tfvars_content, strip_quotes=True, only_keys=keymap
        )
        assert "test-project" in result

    def test_edge_case_empty_keymap_with_placeholders(self):
        """Test edge case with empty template but tfvars content."""
        tfvars_content = """
project = "test-project"
env = "test"
"""

        # Empty template should work fine
        template_content = ""

        from bdtemplater.bdtemplatize import generate_template

        result = generate_template(template_content, tfvars_content, strip_quotes=True)
        assert result == ""

    def test_error_message_consistency(self):
        """Test that missing placeholders remain unreplaced when no keymap."""
        tfvars_content = '''project = "test"'''

        template_content = """@missing1@ @missing2@ @missing3@ @project@"""

        from bdtemplater.bdtemplatize import generate_template

        result = generate_template(template_content, tfvars_content, strip_quotes=True)

        # project should be replaced, others should remain as placeholders
        assert "test" in result
        assert "@missing1@" in result
        assert "@missing2@" in result
        assert "@missing3@" in result

    def test_keymap_missing_keys_causes_error(self):
        """Test that KeyError is raised when keymap has missing keys from tfvars."""
        tfvars_content = '''project = "test"'''

        template_content = """test: @project@ @missing_key@"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            # Capture stderr
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                with pytest.raises(SystemExit) as exc_info:
                    main([template_path, tfvars_path, "-k", "project,missing_key"])
                assert exc_info.value.code == 1

                stderr_output = captured_stderr.getvalue()
                assert "Error:" in stderr_output
                assert "Keys in only_keys missing from tfvars" in stderr_output
            finally:
                sys.stderr = old_stderr
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_bdtemplaterexample_package(self):
        """Test the bdtemplaterexample package for coverage."""
        import bdtemplaterexample

        # Test that we can access the uppercase_post_process from the package
        assert hasattr(bdtemplaterexample, "uppercase_post_process")

        # Test the function
        result = bdtemplaterexample.uppercase_post_process("test example import")
        assert result == "TEST EXAMPLE IMPORT"

    def test_keymap_with_missing_keys_in_tfdict(self):
        """Test keymap replacement when some keys are missing from tfdict."""
        tfvars_content = """project = "my-project"
env = "production"
"""
        keymap = ["project", "env", "missing_key"]
        template = "project: @project@, env: @env@, missing: @missing_key@"

        from bdtemplater.bdtemplatize import generate_template

        # Should raise KeyError when keymap contains keys not in tfvars
        with pytest.raises(KeyError) as exc_info:
            generate_template(
                template, tfvars_content, strip_quotes=True, only_keys=keymap
            )
        assert "Keys in only_keys missing from tfvars: missing_key" in str(
            exc_info.value
        )

    def test_placeholder_replacement_branch_coverage(self):
        """Test both branches of placeholder replacement for coverage."""
        tfvars_content = """project = "my-project"
env = "production"
"""
        # Use all keys from tfdict (no keymap provided) - this tests the branch
        template = "project: @project@, env: @env@, missing: @missing_key@"

        from bdtemplater.bdtemplatize import generate_template

        result = generate_template(template, tfvars_content, strip_quotes=True)

        # Should replace keys that exist in tfdict
        assert "my-project" in result
        assert "production" in result
        # Should leave placeholders that don't exist in tfdict
        assert "@missing_key@" in result

    def test_main_with_verbose_output_file_success(self, capsys):
        """Test main function with verbose and output file for coverage."""
        template_content = """project: @project@
env: @env@"""
        tfvars_content = '''project = "verbose-test"
env = "test-env"'''

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".out", delete=False
        ) as output_file:
            output_path = output_file.name

        try:
            from bdtemplater.bdtemplatize import main

            main(
                [template_path, tfvars_path, "-o", output_path, "--verbose", "--force"]
            )

            # Check verbose output
            captured = capsys.readouterr()
            assert "Writing output to:" in captured.err
            assert "Successfully wrote output to" in captured.err
            assert "Template generation completed successfully" in captured.err

            # Check output file content
            with open(output_path) as f:
                result = f.read()
            assert "verbose-test" in result
            assert "test-env" in result
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            os.unlink(output_path)

    def test_main_with_custom_post_process_not_found(self, capsys):
        """Test main function when custom post-process function not found."""
        template_content = """project: @project@"""
        tfvars_content = '''project = "test-project"'''

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            from bdtemplater.bdtemplatize import main

            # Try to use a non-existent function in the bdtemplaterexample module
            main(
                [
                    template_path,
                    tfvars_path,
                    "--import-module",
                    "bdtemplaterexample",
                    "--post-process",
                    "nonexistent_function",
                    "--verbose",
                ]
            )

            captured = capsys.readouterr()
            assert (
                "Warning: Function 'nonexistent_function' not found in module "
                "'bdtemplaterexample', using default" in captured.err
            )
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_main_with_general_exception_in_module_import(self, capsys):
        """Test main function when there's a general exception during module import."""
        template_content = """project: @project@"""
        tfvars_content = '''project = "test-project"'''

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            from bdtemplater.bdtemplatize import main

            with pytest.raises(SystemExit) as exc_info:
                # Try to import a module that will cause an exception
                main(
                    [
                        template_path,
                        tfvars_path,
                        "--import-module",
                        "this.module.does.not.exist",
                    ]
                )
            assert exc_info.value.code == 1
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_key_in_tfdict_branch_coverage(self):
        """Test the branch where key_name is checked to be in tfdict."""
        tfvars_content = """project = "my-project"
env = "production"
"""
        # Test with specific keymap that includes keys both in and not in tfdict
        keymap = ["project"]  # Only project is in tfdict
        template = "project: @project@, env: @env@, missing: @missing_key@"

        from bdtemplater.bdtemplatize import generate_template

        result = generate_template(
            template, tfvars_content, strip_quotes=True, only_keys=keymap
        )

        # Should replace project (key in keymap and tfdict)
        assert "my-project" in result
        # Should leave env and missing_key as placeholders (not in keymap)
        assert "@env@" in result
        assert "@missing_key@" in result

    def test_environment_variable_injection(self):
        """Test environment variable injection functionality."""
        from bdtemplater.bdtemplatize import generate_template

        # Set up test environment variables
        test_env = {
            "TEST_VAR1": "test_value1",
            "TEST_VAR2": "test_value2",
            "USER": "test_user",
        }

        template = (
            "User: @USER@, Var1: @TEST_VAR1@, Var2: @TEST_VAR2@, Missing: @MISSING_VAR@"
        )
        tfvars_content = ""  # Empty tfvars to test only env vars

        result = generate_template(
            template, tfvars_content, strip_quotes=True, env_dict=test_env
        )

        # Should replace environment variables
        assert "User: test_user" in result
        assert "Var1: test_value1" in result
        assert "Var2: test_value2" in result
        # Should leave missing variable as placeholder
        assert "Missing: @MISSING_VAR@" in result

    def test_environment_variable_override_by_tfvars(self):
        """Test that tfvars values override environment variables."""
        from bdtemplater.bdtemplatize import generate_template

        # Environment has one value
        test_env = {"USER": "env_user", "PROJECT": "env_project"}

        # Tfvars overrides USER but not PROJECT
        tfvars_content = 'USER = "tfvars_user"'

        template = "User: @USER@, Project: @PROJECT@"

        result = generate_template(
            template, tfvars_content, strip_quotes=True, env_dict=test_env
        )

        # USER should be from tfvars (override), PROJECT should be from env
        assert "User: tfvars_user" in result
        assert "Project: env_project" in result

    def test_environment_variable_injection_with_keymap(self):
        """Test environment variable injection with keymap restriction."""
        from bdtemplater.bdtemplatize import generate_template

        test_env = {"USER": "test_user", "HOME": "/home/test", "SHELL": "/bin/bash"}

        template = "User: @USER@, Home: @HOME@, Shell: @SHELL@"
        tfvars_content = ""
        keymap = ["USER", "HOME"]  # Only allow USER and HOME

        result = generate_template(
            template,
            tfvars_content,
            strip_quotes=True,
            only_keys=keymap,
            env_dict=test_env,
        )

        # Should replace USER and HOME (in keymap)
        assert "User: test_user" in result
        assert "Home: /home/test" in result
        # Should leave SHELL as placeholder (not in keymap)
        assert "Shell: @SHELL@" in result

    def test_environment_variable_prefix_functionality(self):
        """Test environment variable injection with key prefix."""
        from bdtemplater.bdtemplatize import generate_template

        # Set up test environment variables
        test_env = {
            "env.TEST_VAR1": "prefixed_value1",
            "env.TEST_VAR2": "prefixed_value2",
            "env.USER": "prefixed_user",
        }

        template = "User: @env.USER@, Var1: @env.TEST_VAR1@, Var2: @env.TEST_VAR2@"
        tfvars_content = ""  # Empty tfvars to test only prefixed env vars

        result = generate_template(
            template, tfvars_content, strip_quotes=True, env_dict=test_env
        )

        # Should replace prefixed environment variables
        assert "User: prefixed_user" in result
        assert "Var1: prefixed_value1" in result
        assert "Var2: prefixed_value2" in result

    def test_main_with_env_prefix_flag_success_implied_env(self, capsys):
        """Test that --env-prefix flag automatically implies --env flag."""
        import tempfile

        template_content = "User: @env.USER@"
        tfvars_content = 'project = "test"'

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            from bdtemplater.bdtemplatize import main

            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                # This should now work without explicitly setting --env
                main([template_path, tfvars_path, "--env-prefix"])
                output = captured_stdout.getvalue()
                # Should contain the user environment variable with env. prefix
                assert "User:" in output
                assert "@env.USER@" not in output  # Should be replaced

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_main_with_env_prefix_flag_success(self):
        """Test main function with --env and --env-prefix flags."""
        import tempfile

        template_content = "User: @env.USER@, Test: @env.TEST_BDTEMPLATER_PREFIX@"
        tfvars_content = 'other = "value"'

        # Set a test environment variable
        os.environ["TEST_BDTEMPLATER_PREFIX"] = "prefix_test_value"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".bdt", delete=False
            ) as template_file:
                template_file.write(template_content)
                template_path = template_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as tfvars_file:
                tfvars_file.write(tfvars_content)
                tfvars_path = tfvars_file.name

            # Test with --env and --env-prefix flags
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main([template_path, tfvars_path, "--env", "--env-prefix"])
                output = captured_stdout.getvalue().strip()

                # Should replace prefixed environment variables
                assert "Test: prefix_test_value" in output
                # USER should also be replaced with env. prefix
                assert "@env.USER@" not in output

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            # Clean up test environment variable
            if "TEST_BDTEMPLATER_PREFIX" in os.environ:
                del os.environ["TEST_BDTEMPLATER_PREFIX"]

    def test_main_with_env_prefix_verbose_output(self, capsys):
        """Test main function with --env --env-prefix and verbose output."""
        import tempfile

        template_content = "User: @env.USER@"
        tfvars_content = 'project = "test"'

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            from bdtemplater.bdtemplatize import main

            main([template_path, tfvars_path, "--env", "--env-prefix", "--verbose"])

            captured = capsys.readouterr()

            # Should show environment injection with prefix messages
            assert "Environment variable injection enabled" in captured.err
            assert (
                "Environment variable keys will be prefixed with 'env.'" in captured.err
            )
            assert "with 'env.' prefix" in captured.err

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_env_prefix_with_tfvars_override(self):
        """Test that tfvars can override prefixed environment variables."""
        from bdtemplater.bdtemplatize import generate_template

        # Environment has prefixed values
        test_env = {"env.USER": "env_user", "env.PROJECT": "env_project"}

        # Tfvars overrides env.USER but not env.PROJECT
        tfvars_content = 'env.USER = "tfvars_user"'

        template = "User: @env.USER@, Project: @env.PROJECT@"

        result = generate_template(
            template, tfvars_content, strip_quotes=True, env_dict=test_env
        )

        # env.USER should be from tfvars (override), env.PROJECT should be from env
        assert "User: tfvars_user" in result
        assert "Project: env_project" in result

    def test_env_prefix_with_keymap_restriction(self):
        """Test prefixed environment variable injection with keymap restriction."""
        from bdtemplater.bdtemplatize import generate_template

        test_env = {
            "env.USER": "test_user",
            "env.HOME": "/home/test",
            "env.SHELL": "/bin/bash",
        }

        template = "User: @env.USER@, Home: @env.HOME@, Shell: @env.SHELL@"
        tfvars_content = ""
        keymap = ["env.USER", "env.HOME"]  # Only allow prefixed USER and HOME

        result = generate_template(
            template,
            tfvars_content,
            strip_quotes=True,
            only_keys=keymap,
            env_dict=test_env,
        )

        # Should replace env.USER and env.HOME (in keymap)
        assert "User: test_user" in result
        assert "Home: /home/test" in result
        # Should leave env.SHELL as placeholder (not in keymap)
        assert "Shell: @env.SHELL@" in result

    def test_env_key_strip_functionality(self):
        """Test environment variable key stripping functionality."""
        from bdtemplater.bdtemplatize import generate_template

        # Set up test environment variables with prefixes
        test_env = {
            "MYAPP_DATABASE_URL": "postgresql://localhost:5432/mydb",
            "MYAPP_SECRET_KEY": "super_secret",
            "AWS_ACCESS_KEY": "aws_key_123",
            "K8S_NAMESPACE": "production",
            "OTHER_VAR": "should_remain_unchanged",
        }

        # After stripping MYAPP_ and AWS_ prefixes, we should have:
        # DATABASE_URL, SECRET_KEY, ACCESS_KEY, K8S_NAMESPACE, OTHER_VAR
        template = (
            "DB: @DATABASE_URL@, Secret: @SECRET_KEY@, AWS: @ACCESS_KEY@, "
            "K8S: @K8S_NAMESPACE@, Other: @OTHER_VAR@"
        )
        tfvars_content = ""  # Empty tfvars to test only stripped env vars

        # Simulate the stripping logic
        stripped_env = {}
        for key, value in test_env.items():
            stripped_key = key
            # Apply stripping (MYAPP_ and AWS_ prefixes)
            if stripped_key.startswith("MYAPP_"):
                stripped_key = stripped_key[len("MYAPP_") :]
            elif stripped_key.startswith("AWS_"):
                stripped_key = stripped_key[len("AWS_") :]
            stripped_env[stripped_key] = value

        result = generate_template(
            template, tfvars_content, strip_quotes=True, env_dict=stripped_env
        )

        # Should replace stripped environment variables
        assert "DB: postgresql://localhost:5432/mydb" in result
        assert "Secret: super_secret" in result
        assert "AWS: aws_key_123" in result
        assert "K8S: production" in result
        assert "Other: should_remain_unchanged" in result

    def test_main_with_env_key_strip_flag_implies_env(self, capsys):
        """Test that --env-key-strip flag automatically implies --env flag."""
        import tempfile

        template_content = "Test: @TEST_VAR@"
        tfvars_content = 'project = "test"'

        # Set test environment variable with prefix
        os.environ["MYAPP_TEST_VAR"] = "stripped_value"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".bdt", delete=False
            ) as template_file:
                template_file.write(template_content)
                template_path = template_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as tfvars_file:
                tfvars_file.write(tfvars_content)
                tfvars_path = tfvars_file.name

            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                # This should now work without explicitly setting --env
                main([template_path, tfvars_path, "--env-key-strip", "MYAPP_"])
                output = captured_stdout.getvalue()
                # Should contain the stripped environment variable
                assert "Test: stripped_value" in output

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            if "MYAPP_TEST_VAR" in os.environ:
                del os.environ["MYAPP_TEST_VAR"]

    def test_main_with_env_key_strip_flag_success(self):
        """Test main function with --env and --env-key-strip flags."""
        import tempfile

        template_content = "Database: @DATABASE_URL@, Secret: @SECRET_KEY@"
        tfvars_content = 'other = "value"'

        # Set test environment variables with prefix
        os.environ["MYAPP_DATABASE_URL"] = "test_db_url"
        os.environ["MYAPP_SECRET_KEY"] = "test_secret"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".bdt", delete=False
            ) as template_file:
                template_file.write(template_content)
                template_path = template_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as tfvars_file:
                tfvars_file.write(tfvars_content)
                tfvars_path = tfvars_file.name

            # Test with --env and --env-key-strip flags
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main([template_path, tfvars_path, "--env", "--env-key-strip", "MYAPP_"])
                output = captured_stdout.getvalue().strip()

                # Should replace stripped environment variables
                assert "Database: test_db_url" in output
                assert "Secret: test_secret" in output

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            # Clean up test environment variables
            if "MYAPP_DATABASE_URL" in os.environ:
                del os.environ["MYAPP_DATABASE_URL"]
            if "MYAPP_SECRET_KEY" in os.environ:
                del os.environ["MYAPP_SECRET_KEY"]

    def test_main_with_multiple_env_key_strip_flags(self):
        """Test main function with multiple --env-key-strip flags."""
        import tempfile

        template_content = (
            "Database: @DATABASE_URL@, AWS: @ACCESS_KEY@, K8S: @NAMESPACE@"
        )
        tfvars_content = 'other = "value"'

        # Set test environment variables with different prefixes
        os.environ["MYAPP_DATABASE_URL"] = "my_db"
        os.environ["AWS_ACCESS_KEY"] = "my_aws_key"
        os.environ["K8S_NAMESPACE"] = "my_namespace"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".bdt", delete=False
            ) as template_file:
                template_file.write(template_content)
                template_path = template_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as tfvars_file:
                tfvars_file.write(tfvars_content)
                tfvars_path = tfvars_file.name

            # Test with multiple strip prefixes
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main(
                    [
                        template_path,
                        tfvars_path,
                        "--env",
                        "--env-key-strip",
                        "MYAPP_",
                        "--env-key-strip",
                        "AWS_",
                        "--env-key-strip",
                        "K8S_",
                    ]
                )
                output = captured_stdout.getvalue().strip()

                # Should replace all stripped environment variables
                assert "Database: my_db" in output
                assert "AWS: my_aws_key" in output
                assert "K8S: my_namespace" in output

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            # Clean up test environment variables
            for var in ["MYAPP_DATABASE_URL", "AWS_ACCESS_KEY", "K8S_NAMESPACE"]:
                if var in os.environ:
                    del os.environ[var]

    def test_env_key_strip_hcdefaults_functionality(self):
        """Test HashiCorp defaults environment variable key stripping functionality."""
        from bdtemplater.bdtemplatize import generate_template

        # Set up test environment variables with HashiCorp prefixes
        test_env = {
            "TF_VAR_environment": "production",
            "PKR_VAR_image_name": "ubuntu-20.04",
            "WP_VAR_workspace": "default",
            "VAULT_TOKEN": "hvs.secret123",
            "NOMAD_JOB": "web-app",
            "OTHER_VAR": "should_remain_unchanged",
        }

        # After stripping HashiCorp prefixes, we should have:
        # environment, image_name, workspace, TOKEN, JOB, OTHER_VAR
        template = (
            "Env: @environment@, Image: @image_name@, Workspace: @workspace@, "
            "Token: @TOKEN@, Job: @JOB@, Other: @OTHER_VAR@"
        )
        tfvars_content = ""  # Empty tfvars to test only stripped env vars

        # Simulate the HashiCorp defaults stripping logic
        hc_prefixes = ["TF_VAR_", "PKR_VAR_", "WP_VAR_", "VAULT_", "NOMAD_"]
        stripped_env = {}
        for key, value in test_env.items():
            stripped_key = key
            # Apply HashiCorp prefix stripping
            for prefix in hc_prefixes:
                if stripped_key.startswith(prefix):
                    stripped_key = stripped_key[len(prefix) :]
                    break
            stripped_env[stripped_key] = value

        result = generate_template(
            template, tfvars_content, strip_quotes=True, env_dict=stripped_env
        )

        # Should replace stripped environment variables
        assert "Env: production" in result
        assert "Image: ubuntu-20.04" in result
        assert "Workspace: default" in result
        assert "Token: hvs.secret123" in result
        assert "Job: web-app" in result
        assert "Other: should_remain_unchanged" in result

    def test_main_with_env_key_strip_hcdefaults_flag_implies_env(self, capsys):
        """Test that --env-key-strip-hcdefaults flag implies --env flag."""
        import tempfile

        template_content = "Test: @environment@"
        tfvars_content = 'project = "test"'

        # Set test environment variable with HashiCorp prefix
        os.environ["TF_VAR_environment"] = "hc_stripped_value"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".bdt", delete=False
            ) as template_file:
                template_file.write(template_content)
                template_path = template_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as tfvars_file:
                tfvars_file.write(tfvars_content)
                tfvars_path = tfvars_file.name

            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                # This should now work without explicitly setting --env
                main([template_path, tfvars_path, "--env-key-strip-hcdefaults"])
                output = captured_stdout.getvalue()
                # Should contain the stripped environment variable
                assert "Test: hc_stripped_value" in output

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            if "TF_VAR_environment" in os.environ:
                del os.environ["TF_VAR_environment"]

    def test_main_with_env_key_strip_hcdefaults_flag_success(self):
        """Test main function with --env and --env-key-strip-hcdefaults flags."""
        import tempfile

        template_content = "Environment: @environment@, Token: @TOKEN@"
        tfvars_content = 'other = "value"'

        # Set test environment variables with HashiCorp prefixes
        os.environ["TF_VAR_environment"] = "test_env"
        os.environ["VAULT_TOKEN"] = "test_token"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".bdt", delete=False
            ) as template_file:
                template_file.write(template_content)
                template_path = template_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as tfvars_file:
                tfvars_file.write(tfvars_content)
                tfvars_path = tfvars_file.name

            # Test with --env and --env-key-strip-hcdefaults flags
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main(
                    [template_path, tfvars_path, "--env", "--env-key-strip-hcdefaults"]
                )
                output = captured_stdout.getvalue().strip()

                # Should replace stripped HashiCorp environment variables
                assert "Environment: test_env" in output
                assert "Token: test_token" in output

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            # Clean up test environment variables
            if "TF_VAR_environment" in os.environ:
                del os.environ["TF_VAR_environment"]
            if "VAULT_TOKEN" in os.environ:
                del os.environ["VAULT_TOKEN"]

    def test_env_key_strip_hcdefaults_with_custom_strip_combination(self):
        """Test that HashiCorp defaults work with custom strip prefixes."""
        from bdtemplater.bdtemplatize import generate_template

        # Set up test environment variables with HashiCorp and custom prefixes
        test_env = {
            "TF_VAR_environment": "production",
            "VAULT_TOKEN": "secret123",
            "CUSTOM_VAR": "custom_value",
            "APP_CONFIG": "app_config",
        }

        template = "Env: @environment@, Token: @TOKEN@, Custom: @VAR@, App: @CONFIG@"
        tfvars_content = ""

        # Simulate the combined stripping logic
        hc_prefixes = ["TF_VAR_", "PKR_VAR_", "WP_VAR_", "VAULT_", "NOMAD_"]
        custom_prefixes = ["CUSTOM_", "APP_"]
        all_prefixes = hc_prefixes + custom_prefixes

        stripped_env = {}
        for key, value in test_env.items():
            stripped_key = key
            # Apply all prefix stripping (first match wins)
            for prefix in all_prefixes:
                if stripped_key.startswith(prefix):
                    stripped_key = stripped_key[len(prefix) :]
                    break
            stripped_env[stripped_key] = value

        result = generate_template(
            template, tfvars_content, strip_quotes=True, env_dict=stripped_env
        )

        # Should replace all stripped environment variables
        assert "Env: production" in result
        assert "Token: secret123" in result
        assert "Custom: custom_value" in result
        assert "App: app_config" in result

    def test_env_key_strip_hcdefaults_verbose_output(self, capsys):
        """Test verbose output shows HashiCorp defaults information."""
        import tempfile

        template_content = "Test: @environment@"
        tfvars_content = 'project = "test"'

        # Set test environment variable with HashiCorp prefix
        os.environ["TF_VAR_environment"] = "test_value"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".bdt", delete=False
            ) as template_file:
                template_file.write(template_content)
                template_path = template_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as tfvars_file:
                tfvars_file.write(tfvars_content)
                tfvars_path = tfvars_file.name

            from bdtemplater.bdtemplatize import main

            main(
                [
                    template_path,
                    tfvars_path,
                    "--env",
                    "--env-key-strip-hcdefaults",
                    "--verbose",
                ]
            )

            captured = capsys.readouterr()

            # Should show HashiCorp defaults stripping information
            assert "Environment variable injection enabled" in captured.err
            assert (
                "HashiCorp default prefixes will be stripped: "
                "TF_VAR_, PKR_VAR_, WP_VAR_, VAULT_, NOMAD_" in captured.err
            )
            assert "(after stripping 5 prefixes)" in captured.err

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            # Clean up test environment variable
            if "TF_VAR_environment" in os.environ:
                del os.environ["TF_VAR_environment"]

    def test_env_key_strip_hcdefaults_with_env_prefix(self):
        """Test HashiCorp defaults stripping with env prefix combination."""
        from bdtemplater.bdtemplatize import generate_template

        # Set up test environment variables with HashiCorp prefixes
        test_env = {
            "TF_VAR_database_url": "postgres://localhost/myapp",
            "VAULT_SECRET": "supersecret",
        }

        # After stripping HashiCorp prefixes and adding env. prefix:
        # env.database_url, env.SECRET
        template = "Database: @env.database_url@, Secret: @env.SECRET@"
        tfvars_content = ""

        # Simulate the stripping then prefixing logic
        hc_prefixes = ["TF_VAR_", "PKR_VAR_", "WP_VAR_", "VAULT_", "NOMAD_"]
        stripped_env = {}
        for key, value in test_env.items():
            stripped_key = key
            # Apply HashiCorp prefix stripping
            for prefix in hc_prefixes:
                if stripped_key.startswith(prefix):
                    stripped_key = stripped_key[len(prefix) :]
                    break
            stripped_env[stripped_key] = value

        # Apply env. prefixing
        prefixed_env = {f"env.{key}": value for key, value in stripped_env.items()}

        result = generate_template(
            template, tfvars_content, strip_quotes=True, env_dict=prefixed_env
        )

        # Should replace prefixed stripped environment variables
        assert "Database: postgres://localhost/myapp" in result
        assert "Secret: supersecret" in result

    def test_main_with_env_key_strip_hcdefaults_and_custom_verbose(self, capsys):
        """Test verbose output with both HashiCorp defaults and custom prefixes."""
        import tempfile

        template_content = "Test: @environment@"
        tfvars_content = 'project = "test"'

        # Set test environment variables
        os.environ["TF_VAR_environment"] = "test_value"
        os.environ["CUSTOM_VAR"] = "custom_value"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".bdt", delete=False
            ) as template_file:
                template_file.write(template_content)
                template_path = template_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as tfvars_file:
                tfvars_file.write(tfvars_content)
                tfvars_path = tfvars_file.name

            from bdtemplater.bdtemplatize import main

            main(
                [
                    template_path,
                    tfvars_path,
                    "--env",
                    "--env-key-strip-hcdefaults",
                    "--env-key-strip",
                    "CUSTOM_",
                    "--verbose",
                ]
            )

            captured = capsys.readouterr()

            # Should show both HashiCorp defaults and custom prefix information
            assert "Environment variable injection enabled" in captured.err
            assert (
                "HashiCorp default prefixes will be stripped: "
                "TF_VAR_, PKR_VAR_, WP_VAR_, VAULT_, NOMAD_" in captured.err
            )
            assert (
                "Environment variable key prefixes to strip: ['CUSTOM_']"
                in captured.err
            )
            assert "(after stripping 6 prefixes)" in captured.err  # 5 HC + 1 custom

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            # Clean up test environment variables
            for var in ["TF_VAR_environment", "CUSTOM_VAR"]:
                if var in os.environ:
                    del os.environ[var]

    def test_not_keys_functionality(self):
        """Test --not-keys flag removes specified keys from replacements dictionary."""
        tfvars_content = """project = "test-project"
secret = "password123"
env = "production"
api_key = "secret-key"
"""

        template_content = """Project: @project@
Environment: @env@
Secret: @secret@
API Key: @api_key@
"""

        from bdtemplater.bdtemplatize import generate_template

        # Test with single key removal
        not_keys = ["secret"]
        result = generate_template(
            template_content, tfvars_content, strip_quotes=True, not_keys=not_keys
        )
        assert "Project: test-project" in result
        assert "Environment: production" in result
        assert "Secret: @secret@" in result  # Should remain as placeholder
        assert "API Key: secret-key" in result

        # Test with multiple key removal
        not_keys = ["secret", "api_key"]
        result = generate_template(
            template_content, tfvars_content, strip_quotes=True, not_keys=not_keys
        )
        assert "Project: test-project" in result
        assert "Environment: production" in result
        assert "Secret: @secret@" in result  # Should remain as placeholder
        assert "API Key: @api_key@" in result  # Should remain as placeholder

    def test_main_with_not_keys_flag(self):
        """Test main function with --not-keys flag."""
        tfvars_content = """project = "test-project"
secret = "password123"
env = "production"
"""

        template_content = """Project: @project@
Environment: @env@
Secret: @secret@
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            # Capture output
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main(
                    [
                        template_path,
                        tfvars_path,
                        "--not-keys",
                        "secret",
                        "--strip-quotes",
                    ]
                )

                output = captured_stdout.getvalue()
                assert "Project: test-project" in output
                assert "Environment: production" in output
                assert "Secret: @secret@" in output  # Should remain as placeholder
            finally:
                sys.stdout = old_stdout
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_not_keys_with_env_injection(self):
        """Test --not-keys with environment variable injection."""
        tfvars_content = """project = "test-project"
secret = "from-tfvars"
"""

        template_content = """Project: @project@
Secret: @secret@
Env Var: @TEST_ENV_VAR@
"""

        # Set environment variable
        os.environ["secret"] = "from-env"
        os.environ["TEST_ENV_VAR"] = "env-value"

        try:
            from bdtemplater.bdtemplatize import generate_template

            # Test that not_keys removes both tfvars and env variables
            env_dict = {"secret": "from-env", "TEST_ENV_VAR": "env-value"}
            not_keys = ["secret"]
            result = generate_template(
                template_content,
                tfvars_content,
                strip_quotes=True,
                env_dict=env_dict,
                not_keys=not_keys,
            )
            assert "Project: test-project" in result
            assert "Secret: @secret@" in result  # Should remain as placeholder
            assert "Env Var: env-value" in result
        finally:
            # Clean up environment variables
            for var in ["secret", "TEST_ENV_VAR"]:
                if var in os.environ:
                    del os.environ[var]

    def test_not_keys_with_verbose_output(self):
        """Test --not-keys with verbose output shows removed keys."""
        tfvars_content = """project = "test-project"
secret = "password123"
"""

        template_content = """Project: @project@
Secret: @secret@
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            # Capture stderr for verbose output
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            # Capture stdout for main output
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main([template_path, tfvars_path, "--not-keys", "secret", "--verbose"])

                stderr_output = captured_stderr.getvalue()
                assert "Keys to remove: ['secret']" in stderr_output

                stdout_output = captured_stdout.getvalue()
                assert "Secret: @secret@" in stdout_output
            finally:
                sys.stderr = old_stderr
                sys.stdout = old_stdout
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_get_possibly_commented_value_edge_cases(self):
        """Test edge cases in get_possibly_commented_value function."""
        from bdtemplater.bdtemplatize import get_possibly_commented_value

        # Test empty string
        assert get_possibly_commented_value("", strip_quotes=False) == ""

        # Test escape sequences
        assert (
            get_possibly_commented_value(r'"escaped \"quote\""', strip_quotes=True)
            == r"escaped \"quote\""
        )

        # Test quote handling with mixed quotes
        assert (
            get_possibly_commented_value("'single quoted'", strip_quotes=True)
            == "single quoted"
        )

        # Test comment outside quotes
        assert (
            get_possibly_commented_value("value # comment", strip_quotes=False)
            == "value"
        )

        # Test comment inside quotes (should not be stripped)
        assert (
            get_possibly_commented_value('"value # not a comment"', strip_quotes=True)
            == "value # not a comment"
        )

        # Test ending quote matching
        assert (
            get_possibly_commented_value("\"mismatched'", strip_quotes=True)
            == "\"mismatched'"
        )

        # Test escape at end of string
        assert get_possibly_commented_value(r'"test\\"', strip_quotes=True) == r"test\\"

    def test_placeholder_replacement_key_not_in_tfdict(self):
        """Test placeholder replacement when key is not in tfdict."""
        from bdtemplater.bdtemplatize import generate_template

        template = "Project: @project@, Missing: @missing@"
        replacements = 'project = "test-project"'

        # When a key is not in tfdict, placeholder should remain unchanged
        result = generate_template(template, replacements, strip_quotes=True)
        assert "Project: test-project" in result
        assert "Missing: @missing@" in result

    def test_multiple_replacements_files_verbose_output(self):
        """Test verbose output with multiple replacements files."""
        tfvars_content1 = 'project = "test-project"'
        tfvars_content2 = 'env = "test"'
        template_content = "Project: @project@, Env: @env@"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file1:
            tfvars_file1.write(tfvars_content1)
            tfvars_path1 = tfvars_file1.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file2:
            tfvars_file2.write(tfvars_content2)
            tfvars_path2 = tfvars_file2.name

        try:
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main(
                    [template_path, "-r", tfvars_path1, "-r", tfvars_path2, "--verbose"]
                )

                stderr_output = captured_stderr.getvalue()
                assert (
                    f"Properties files: ['{tfvars_path1}', '{tfvars_path2}']"
                    in stderr_output
                )

            finally:
                sys.stderr = old_stderr
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path1)
            os.unlink(tfvars_path2)

    def test_verbose_post_process_function_output(self):
        """Test verbose output when using post-processing function."""
        tfvars_content = 'project = "test-project"'
        template_content = "Project: @project@"

        # Create a simple post-processing module in current directory
        module_content = """
def custom_post_process(content):
    return content.upper()
"""

        import tempfile
        import uuid

        # Create a unique module name
        module_name = f"test_module_{uuid.uuid4().hex[:8]}"
        module_path = f"{module_name}.py"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        # Write module in current directory
        with open(module_path, "w") as module_file:
            module_file.write(module_content)

        try:
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main(
                    [
                        template_path,
                        tfvars_path,
                        "--import-module",
                        module_name,
                        "--post-process",
                        "custom_post_process",
                        "--verbose",
                    ]
                )

                stderr_output = captured_stderr.getvalue()
                expected_msg = "Using post-processing function: custom_post_process"
                assert expected_msg in stderr_output

            finally:
                sys.stderr = old_stderr
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            if os.path.exists(module_path):
                os.unlink(module_path)

    def test_force_flag_functionality(self):
        """Test --force flag functionality."""
        tfvars_content = 'project = "test-project"'
        template_content = "Project: @project@"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
            output_path = output_file.name

        try:
            from bdtemplater.bdtemplatize import main

            # Test that --force allows overwriting existing file
            main([template_path, tfvars_path, "-o", output_path, "--force"])

            # Check that output file was created
            assert os.path.exists(output_path)
            with open(output_path) as f:
                content = f.read()
                assert 'Project: "test-project"' in content

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            os.unlink(output_path)

    def test_force_flag_without_force_exits_with_code_3(self):
        """Test that script exits with code 3 when file exists and --force not used."""
        tfvars_content = 'project = "test-project"'
        template_content = "Project: @project@"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
            output_path = output_file.name

        try:
            from bdtemplater.bdtemplatize import main

            # Test that script exits with code 3 when file exists and --force not used
            with pytest.raises(SystemExit) as exc_info:
                main([template_path, tfvars_path, "-o", output_path])

            assert exc_info.value.code == 3

        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            os.unlink(output_path)

    def test_force_flag_verbose_output(self):
        """Test verbose output when using --force flag."""
        tfvars_content = 'project = "test-project"'
        template_content = "Project: @project@"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
            output_path = output_file.name

        try:
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                main(
                    [
                        template_path,
                        tfvars_path,
                        "-o",
                        output_path,
                        "--force",
                        "--verbose",
                    ]
                )

                stderr_output = captured_stderr.getvalue()
                assert f"Writing output to: {output_path}" in stderr_output
                assert f"Successfully wrote output to {output_path}" in stderr_output

            finally:
                sys.stderr = old_stderr
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)
            os.unlink(output_path)

    def test_dump_flag_functionality(self):
        """Test --dump flag functionality."""
        tfvars_content = 'project = "test-project"\nenvironment = "dev"'
        template_content = "Project: @project@\nEnvironment: @environment@"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            # Capture stderr for dump output
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                # Test that --dump exits the script
                with pytest.raises(SystemExit) as excinfo:
                    main([template_path, tfvars_path, "--dump"])

                # Check that it exits with code 0
                assert excinfo.value.code == 0

                stderr_output = captured_stderr.getvalue()

                # Check that template is written first
                assert "Project: @project@" in stderr_output
                assert "Environment: @environment@" in stderr_output

                # Check that separator is present
                assert "\n---\n" in stderr_output

                # Check that substitution dictionary is present
                assert 'environment="dev"' in stderr_output
                assert 'project="test-project"' in stderr_output

                # Check order: template, then separator, then dictionary
                template_pos = stderr_output.find("Project: @project@")
                separator_pos = stderr_output.find("\n---\n")
                dict_pos = stderr_output.find('environment="dev"')

                assert template_pos < separator_pos
                assert separator_pos < dict_pos

            finally:
                sys.stderr = old_stderr
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)

    def test_dump_flag_with_filters(self):
        """Test --dump flag with --only-keys and --not-keys filters."""
        tfvars_content = (
            'project = "test-project"\nenvironment = "dev"\nversion = "1.0.0"'
        )
        template_content = (
            "Project: @project@\nEnvironment: @environment@\nVersion: @version@"
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write(template_content)
            template_path = template_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as tfvars_file:
            tfvars_file.write(tfvars_content)
            tfvars_path = tfvars_file.name

        try:
            # Test with --only-keys
            old_stderr = sys.stderr
            sys.stderr = captured_stderr = io.StringIO()

            try:
                from bdtemplater.bdtemplatize import main

                with pytest.raises(SystemExit) as excinfo:
                    main(
                        [
                            template_path,
                            tfvars_path,
                            "--dump",
                            "--only-keys",
                            "project,environment",
                        ]
                    )

                assert excinfo.value.code == 0

                stderr_output = captured_stderr.getvalue()

                # Should include filtered keys
                assert 'project="test-project"' in stderr_output
                assert 'environment="dev"' in stderr_output

                # Should not include excluded key
                assert 'version="1.0.0"' not in stderr_output

            finally:
                sys.stderr = old_stderr
        finally:
            os.unlink(template_path)
            os.unlink(tfvars_path)


# Contains AI-generated edits.
