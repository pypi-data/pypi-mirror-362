"""
Test to trigger the general exception handler and other missing lines.
"""

import os
import tempfile
from unittest.mock import patch

import pytest

from bdtemplater.bdtemplatize import main


def test_general_exception_handler():
    """Test the general exception handler in main function."""

    # Create a test that should trigger the general exception handler
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".bdt", delete=False
    ) as template_file:
        template_file.write("Test: @test@")
        template_file.flush()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as props_file:
            props_file.write('test = "value"')
            props_file.flush()

            # Mock generate_template_from_files to raise an unexpected exception
            with patch(
                "bdtemplater.bdtemplatize.generate_template_from_files"
            ) as mock_generate:
                mock_generate.side_effect = RuntimeError("Unexpected error for testing")

                try:
                    with pytest.raises(SystemExit) as exc_info:
                        main([template_file.name, props_file.name])
                    assert exc_info.value.code == 1
                finally:
                    os.unlink(template_file.name)
                    os.unlink(props_file.name)


def test_os_error_handler():
    """Test the OSError handler in main function."""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".bdt", delete=False
    ) as template_file:
        template_file.write("Test: @test@")
        template_file.flush()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as props_file:
            props_file.write('test = "value"')
            props_file.flush()

            # Mock generate_template_from_files to raise an OSError
            with patch(
                "bdtemplater.bdtemplatize.generate_template_from_files"
            ) as mock_generate:
                mock_generate.side_effect = OSError("File system error")

                try:
                    with pytest.raises(SystemExit) as exc_info:
                        main([template_file.name, props_file.name])
                    assert exc_info.value.code == 1
                finally:
                    os.unlink(template_file.name)
                    os.unlink(props_file.name)


def test_key_error_handler():
    """Test the KeyError handler in main function."""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".bdt", delete=False
    ) as template_file:
        template_file.write("Test: @test@")
        template_file.flush()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as props_file:
            props_file.write('test = "value"')
            props_file.flush()

            # Mock generate_template_from_files to raise a KeyError
            with patch(
                "bdtemplater.bdtemplatize.generate_template_from_files"
            ) as mock_generate:
                mock_generate.side_effect = KeyError("Missing key")

                try:
                    with pytest.raises(SystemExit) as exc_info:
                        main([template_file.name, props_file.name])
                    assert exc_info.value.code == 1
                finally:
                    os.unlink(template_file.name)
                    os.unlink(props_file.name)


def test_file_not_found_error_handler():
    """Test the FileNotFoundError handler in main function."""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".bdt", delete=False
    ) as template_file:
        template_file.write("Test: @test@")
        template_file.flush()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as props_file:
            props_file.write('test = "value"')
            props_file.flush()

            # Mock generate_template_from_files to raise a FileNotFoundError
            with patch(
                "bdtemplater.bdtemplatize.generate_template_from_files"
            ) as mock_generate:
                mock_generate.side_effect = FileNotFoundError("File not found")

                try:
                    with pytest.raises(SystemExit) as exc_info:
                        main([template_file.name, props_file.name])
                    assert exc_info.value.code == 1
                finally:
                    os.unlink(template_file.name)
                    os.unlink(props_file.name)


def test_verbose_template_generation_completed():
    """Test verbose output for template generation completion."""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".bdt", delete=False
    ) as template_file:
        template_file.write("Test: @test@")
        template_file.flush()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tfvars", delete=False
        ) as props_file:
            props_file.write('test = "value"')
            props_file.flush()

            try:
                main([template_file.name, props_file.name, "--verbose"])
            finally:
                os.unlink(template_file.name)
                os.unlink(props_file.name)


# Contains AI-generated edits.
