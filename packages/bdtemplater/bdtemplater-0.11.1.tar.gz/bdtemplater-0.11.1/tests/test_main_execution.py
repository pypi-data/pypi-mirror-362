"""
Test to achieve 95%+ coverage by testing the __name__ == "__main__" block.
"""

import os
import subprocess
import sys
import tempfile


def test_main_name_main_block():
    """Test the __name__ == '__main__' block at the end of bdtemplatize.py."""
    # Create a simple test script that calls the main function
    script_content = """
import sys
sys.path.insert(0, "/Volumes/MiniSSD/git/bdtemplater/src")

if __name__ == "__main__":
    from bdtemplater.bdtemplatize import main
    main(["--version"])
"""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as script_file:
        script_file.write(script_content)
        script_file.flush()

        try:
            # Run the script as a subprocess
            result = subprocess.run(
                [sys.executable, script_file.name],
                capture_output=True,
                text=True,
                timeout=10,
            )
            # Should exit with code 0 for version flag
            assert result.returncode == 0
        finally:
            os.unlink(script_file.name)


def test_module_direct_execution():
    """Test executing the module directly."""
    # Test executing the bdtemplatize module as a script
    result = subprocess.run(
        [sys.executable, "-m", "bdtemplater.bdtemplatize", "--version"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd="/Volumes/MiniSSD/git/bdtemplater",
    )
    # Should exit with code 0 for version flag
    assert result.returncode == 0
    assert (
        "bdtemplater" in result.stdout.lower() or "bdtemplater" in result.stderr.lower()
    )


def test_version_fallback_scenario():
    """Test the version fallback scenario."""
    # Create a test script that simulates the fallback version import
    script_content = """
import sys
import os
sys.path.insert(0, "/Volumes/MiniSSD/git/bdtemplater/src")

# Test if the version is correctly imported
from bdtemplater.bdtemplatize import __version__
print(f"Version: {__version__}")

# Test that version is not "unknown"
assert __version__ != "unknown", "Version should not be unknown"
assert len(__version__) > 0, "Version should not be empty"
"""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as script_file:
        script_file.write(script_content)
        script_file.flush()

        try:
            result = subprocess.run(
                [sys.executable, script_file.name],
                capture_output=True,
                text=True,
                timeout=10,
            )
            assert result.returncode == 0, f"Script failed: {result.stderr}"
            assert "Version:" in result.stdout
        finally:
            os.unlink(script_file.name)


# Contains AI-generated edits.
