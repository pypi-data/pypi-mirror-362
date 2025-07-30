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

"""
Simple unit tests for generate_template function using only standard library.
Run with: uv run python -m tests.simple_test_bdtemplatize
"""

import os
import sys
import traceback

# Add the src directory to the path so we can import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from bdtemplater.bdtemplatize import default_post_process, generate_template


def test_successful_template_generation():
    """Test successful template generation with valid tfvars content."""
    print("Testing successful template generation...")

    tfvars_content = """project = "my-project"
env = "production"
bucket = "my-terraform-bucket"
region = "us-west-2"
lock_table = "my-lock-table"
databricks_version = "1.30.0"
"""

    test_template = "bucket: @bucket@, region: @region@, project: @project@"
    result = generate_template(test_template, tfvars_content, strip_quotes=True)
    assert isinstance(result, str), "Result should be a string"
    assert "my-terraform-bucket" in result, "Bucket name should be in result"
    assert "us-west-2" in result, "Region should be in result"
    assert "my-project" in result, "Project should be in result"
    print("✓ Successful template generation test passed")


def test_file_not_found():
    """Test behavior when content has invalid format."""
    print("Testing invalid content error...")

    # Now logs warning to stderr instead of raising exception
    result = generate_template(
        "test template",
        "invalid content without proper key=value pairs",
        strip_quotes=True,
    )
    # Should return template unchanged (no replacements)
    assert result == "test template", (
        "Should return template unchanged when no valid replacements"
    )
    print("✓ Invalid content test passed")


def test_missing_required_keys():
    """Test behavior when required keys are missing."""
    print("Testing missing required keys...")

    tfvars_content = """project = "my-project"
env = "production"
# Missing bucket, region, lock_table
"""

    # Now logs warning to stderr instead of raising exception
    result = generate_template("test template", tfvars_content, strip_quotes=True)
    # Should return template unchanged (no replacements for missing keys)
    assert result == "test template", (
        "Should return template unchanged when keys are missing"
    )
    print("✓ Missing required keys test passed")


def test_default_post_process():
    """Test the default post-processing function."""
    print("Testing default post-process function...")

    test_input = "This is a test string"
    result = default_post_process(test_input)
    assert result == test_input, "Default post-process should return input unchanged"
    print("✓ Default post-process test passed")


def test_custom_post_process():
    """Test custom post-processing function."""
    print("Testing custom post-process function...")

    tfvars_content = """project = "my-project"
env = "production"
bucket = "my-terraform-bucket"
region = "us-west-2"
lock_table = "my-lock-table"
"""

    def uppercase_post_process(input_text):
        return input_text.upper()

    test_template = "bucket: @bucket@, project: @project@"
    result = generate_template(
        test_template,
        tfvars_content,
        strip_quotes=True,
        post_process=uppercase_post_process,
    )
    assert result.isupper(), "Result should be uppercase due to post-processing"
    assert "MY-TERRAFORM-BUCKET" in result, "Bucket name should be uppercase"
    print("✓ Custom post-process test passed")


def test_quoted_values():
    """Test that quoted values are properly handled."""
    print("Testing quoted values handling...")

    tfvars_content = """project = "my-project"
env = "production"
bucket = "my-terraform-bucket"
region = "us-west-2"
lock_table = "my-lock-table"
"""

    test_template = "project: @project@, bucket: @bucket@"
    result = generate_template(test_template, tfvars_content, strip_quotes=True)
    # Values should have quotes stripped
    assert '"my-project"' not in result, "Quotes should be stripped from values"
    assert "my-project" in result, "Unquoted value should be present"
    print("✓ Quoted values test passed")


def test_default_databricks_version():
    """Test databricks version placeholder behavior."""
    print("Testing databricks version placeholder...")

    tfvars_content = """project = "my-project"
env = "production"
bucket = "my-terraform-bucket"
region = "us-west-2"
lock_table = "my-lock-table"
"""

    test_template = "version: @DATABRICKS_VERSION@"
    result = generate_template(test_template, tfvars_content, strip_quotes=True)
    # Since DATABRICKS_VERSION is not in tfvars, it should remain as placeholder
    assert "@DATABRICKS_VERSION@" in result, (
        "Should leave placeholder unchanged when not in tfvars"
    )
    print("✓ Databricks version placeholder test passed")


def test_malformed_lines_ignored():
    """Test that malformed lines are properly ignored."""
    print("Testing malformed lines handling...")

    tfvars_content = """project = "my-project"
env = "production"
bucket = "my-terraform-bucket"
region = "us-west-2"
lock_table = "my-lock-table"
malformed_line_without_equals
# comment line
"""

    # Should not raise an exception despite malformed line
    test_template = "bucket: @bucket@"
    result = generate_template(test_template, tfvars_content, strip_quotes=True)
    assert isinstance(result, str), "Should return string despite malformed lines"
    print("✓ Malformed lines test passed")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_successful_template_generation,
        test_file_not_found,
        test_missing_required_keys,
        test_default_post_process,
        test_custom_post_process,
        test_quoted_values,
        test_default_databricks_version,
        test_malformed_lines_ignored,
    ]

    passed = 0
    failed = 0

    print("Running simple unit tests for generate_template function...")
    print("=" * 60)

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            traceback.print_exc()
            failed += 1

    print("=" * 60)
    print(f"Tests completed: {passed} passed, {failed} failed")

    if failed > 0:
        sys.exit(1)
    else:
        print("All tests passed! 🎉")


if __name__ == "__main__":
    run_all_tests()
