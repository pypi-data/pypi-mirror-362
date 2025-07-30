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

import os
import tempfile

import pytest

from bdtemplater.bdtemplatize import main


class TestIdempotent:
    """Test suite for the --idempotent flag."""

    def test_idempotent_requires_output_file(self):
        """Test that --idempotent requires --output flag."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write("Hello @name@")
            template_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as vars_file:
                vars_file.write('name = "World"')
                vars_file.flush()

                # Test that --idempotent without --output exits with code 4
                with pytest.raises(SystemExit) as excinfo:
                    main([template_file.name, vars_file.name, "--idempotent"])

                assert excinfo.value.code == 4

                # Clean up
                os.unlink(template_file.name)
                os.unlink(vars_file.name)

    def test_idempotent_creates_new_file(self):
        """Test that --idempotent creates a new file when output doesn't exist."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write("Hello @name@")
            template_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as vars_file:
                vars_file.write('name = "World"')
                vars_file.flush()

                with tempfile.NamedTemporaryFile(delete=False) as output_file:
                    output_path = output_file.name

                # Remove the output file so it doesn't exist
                os.unlink(output_path)

                # Test that --idempotent creates the file normally
                try:
                    main(
                        [
                            template_file.name,
                            vars_file.name,
                            "--idempotent",
                            "--output",
                            output_path,
                            "--strip-quotes",
                        ]
                    )

                    # Verify file was created with correct content
                    assert os.path.exists(output_path)
                    with open(output_path) as f:
                        content = f.read()
                    assert content == "Hello World"

                finally:
                    # Clean up
                    os.unlink(template_file.name)
                    os.unlink(vars_file.name)
                    if os.path.exists(output_path):
                        os.unlink(output_path)

    def test_idempotent_matches_existing_file(self):
        """Test that --idempotent succeeds when output file matches template."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write("Hello @name@")
            template_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as vars_file:
                vars_file.write('name = "World"')
                vars_file.flush()

                with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
                    # Pre-populate output file with expected content
                    output_file.write("Hello World")
                    output_file.flush()
                    output_path = output_file.name

                # Test that --idempotent succeeds when content matches
                try:
                    main(
                        [
                            template_file.name,
                            vars_file.name,
                            "--idempotent",
                            "--output",
                            output_path,
                            "--strip-quotes",
                        ]
                    )

                    # Verify file still exists and content is unchanged
                    assert os.path.exists(output_path)
                    with open(output_path) as f:
                        content = f.read()
                    assert content == "Hello World"

                finally:
                    # Clean up
                    os.unlink(template_file.name)
                    os.unlink(vars_file.name)
                    os.unlink(output_path)

    def test_idempotent_differs_from_existing_file(self):
        """Test that --idempotent exits with code 5 when output file differs."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write("Hello @name@")
            template_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as vars_file:
                vars_file.write('name = "World"')
                vars_file.flush()

                with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
                    # Pre-populate output file with different content
                    output_file.write("Hello Universe")
                    output_file.flush()
                    output_path = output_file.name

                # Test that --idempotent exits with code 5 when content differs
                try:
                    with pytest.raises(SystemExit) as excinfo:
                        main(
                            [
                                template_file.name,
                                vars_file.name,
                                "--idempotent",
                                "--output",
                                output_path,
                                "--strip-quotes",
                            ]
                        )

                    assert excinfo.value.code == 5

                    # Verify file still exists and content is unchanged
                    assert os.path.exists(output_path)
                    with open(output_path) as f:
                        content = f.read()
                    assert content == "Hello Universe"

                finally:
                    # Clean up
                    os.unlink(template_file.name)
                    os.unlink(vars_file.name)
                    os.unlink(output_path)

    def test_idempotent_implies_force(self):
        """Test that --idempotent implies --force flag."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".bdt", delete=False
        ) as template_file:
            template_file.write("Hello @name@")
            template_file.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".tfvars", delete=False
            ) as vars_file:
                vars_file.write('name = "World"')
                vars_file.flush()

                with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
                    # Pre-populate output file with different content
                    output_file.write("Hello Universe")
                    output_file.flush()
                    output_path = output_file.name

                # Test that --idempotent doesn't fail due to existing file
                # but fails due to content mismatch (exit code 5)
                try:
                    with pytest.raises(SystemExit) as excinfo:
                        main(
                            [
                                template_file.name,
                                vars_file.name,
                                "--idempotent",
                                "--output",
                                output_path,
                                "--strip-quotes",
                            ]
                        )

                    # Should exit with code 5 (content mismatch), not code 3
                    assert excinfo.value.code == 5

                finally:
                    # Clean up
                    os.unlink(template_file.name)
                    os.unlink(vars_file.name)
                    os.unlink(output_path)


# Contains AI-generated edits.
