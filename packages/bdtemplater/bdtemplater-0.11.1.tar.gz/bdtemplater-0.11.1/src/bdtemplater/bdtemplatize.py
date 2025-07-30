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

import sys
from typing import Callable, Dict, List, Optional

from bdtemplaterpostprocessor.default_post_process import default_post_process

# Import version for --version flag
try:
    from . import __version__
except ImportError:  # pragma: no cover
    # Fallback if import fails (e.g., when run directly)
    try:  # pragma: no cover
        import sys  # pragma: no cover
        from pathlib import Path  # pragma: no cover

        # Try to import from parent directory
        parent_dir = Path(__file__).parent  # pragma: no cover
        sys.path.insert(0, str(parent_dir))  # pragma: no cover
        import __init__  # type: ignore  # pragma: no cover

        __version__ = __init__.__version__  # type: ignore  # pragma: no cover
        sys.path.pop(0)  # pragma: no cover
    except ImportError:  # pragma: no cover
        __version__ = "unknown"  # pragma: no cover


def get_possibly_commented_value(value: str, strip_quotes: bool = False) -> str:
    """
    Get the possible commented value from a string.

    :param value: The string to check for a commented value.
    :return: The uncommented value if it exists, otherwise None.
    """
    value = value.strip()
    if not value:
        value = ""
    ### Strip comments
    # Remove comments that are not inside quotes
    # Use a simple state machine to track quote states
    in_quote = False
    quote_char = None
    result = []
    i = 0

    while i < len(value):
        char = value[i]

        # Handle escape sequences - skip the next character
        if char == "\\" and i + 1 < len(value):
            result.append(char)
            result.append(value[i + 1])
            i += 2
            continue

        # Check for quote start/end (only if not escaped)
        if char in ['"', "'"]:
            if not in_quote:
                # Starting a quote
                in_quote = True
                quote_char = char
            elif char == quote_char:
                # Ending the quote
                in_quote = False
                quote_char = None

        # If we hit a comment outside of quotes, stop processing
        if char == "#" and not in_quote:
            break

        result.append(char)
        i += 1

    value = "".join(result).strip()

    if strip_quotes:
        # Only strip outermost quotes, not quotes that are part of the content
        if len(value) >= 2:
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
    return value


def read_from_file(the_file: str) -> str:
    """
    Read the content from a file.

    :param the_file: Path to the template file.
    :return: Content of the template file as a string.
    """
    try:
        with open(the_file) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {the_file}")
    except OSError as e:
        raise OSError(f"Error reading {the_file}: {e}")


def process_dictionary(
    properties: str,
    strip_quotes: bool,
    only_keys: Optional[List[str]],
    env_dict: Optional[Dict[str, str]],
    not_keys: Optional[List[str]],
) -> Dict[str, str]:
    """
    Process the input strings into a workable properties dictionary
    """
    # Parse tfvars file
    tfdict = {}

    # Inject environment variables if provided
    if env_dict:
        tfdict.update(env_dict)
    for line in properties.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            try:
                key, value = line.split("=", 1)
                tfdict[key.strip()] = get_possibly_commented_value(value, strip_quotes)
            except ValueError:
                print(f"Warning: Skipping malformed line: {line}", file=sys.stderr)
                continue

    # If tfdict is empty after parsing, log a warning to stderr
    if not tfdict:
        print("Warning: Properties content is invalid or empty.", file=sys.stderr)

    # Remove specified keys if not_keys is provided
    if not_keys:
        for key in not_keys:
            tfdict.pop(key, None)  # Use pop with default None to avoid KeyError

    if only_keys:
        # Filter tfdict to only include keys in only_keys
        tfdict = {key: tfdict[key] for key in only_keys if key in tfdict}
    return tfdict


def generate_template_from_files(
    template_file: str,
    properties_files: List[str],
    strip_quotes: bool = False,
    only_keys: Optional[List[str]] = None,
    post_process: Callable[[str], str] = default_post_process,
    env_dict: Optional[Dict[str, str]] = None,
    not_keys: Optional[List[str]] = None,
) -> str:
    """
    Generate a template by replacing placeholders in the template file with
    values from the properties files.

    :param template_file: Path to the template file containing placeholders.
    :param properties_files: Path to a file or list of paths to files containing
        property values.
    :param only_keys: Optional list of keys to look for in the properties files.
    :param post_process: Optional function to process the final output.
    :param env_dict: Optional dictionary of environment variables to inject.
    :param not_keys: Optional list of keys to remove from the properties dictionary.
    :return: Processed output string with placeholders replaced.

    :raises FileNotFoundError: If the template or properties files do not exist.
    :raises OSError: If there is an error reading the files."""

    template = read_from_file(template_file)

    # Handle both single file and list of files
    if isinstance(properties_files, str):
        properties_files = [properties_files]

    # Read and merge content from all properties files
    merged_properties = ""
    for properties_file in properties_files:
        file_content = read_from_file(properties_file)
        merged_properties += file_content + "\n"

    return generate_template(
        template,
        merged_properties,
        strip_quotes,
        only_keys,
        post_process,
        env_dict,
        not_keys,
    )


def generate_template(
    template: str,
    properties: str,
    strip_quotes: bool,
    only_keys: Optional[List[str]] = None,
    post_process: Callable[[str], str] = default_post_process,
    env_dict: Optional[Dict[str, str]] = None,
    not_keys: Optional[List[str]] = None,
) -> str:
    tfdict = process_dictionary(properties, strip_quotes, only_keys, env_dict, not_keys)
    # Use all keys from tfdict if no only_keys is provided
    if only_keys is None:
        only_keys = list(tfdict.keys())
    else:
        missing_only_keys = [key for key in only_keys if key not in tfdict]
        if missing_only_keys:
            raise KeyError(
                f"Keys in only_keys missing from tfvars: {', '.join(missing_only_keys)}"
            )

    # Initialize output with the template content
    output = template

    # Replace placeholders with values from tfvars
    for key_name in only_keys:
        placeholder = f"@{key_name}@"
        if key_name in tfdict:
            output = output.replace(placeholder, tfdict[key_name])

    return post_process(output)


def main(argv: Optional[List[str]] = None) -> None:
    """Main command-line interface for bdtemplater."""
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(
        description=(
            "Generate templates by replacing placeholders with values from "
            "properties files"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                         # Use defaults:
                                                   # DEFAULT.bdt and
                                                   # terraform.tfvars
  %(prog)s template.bdt myvars.tfvars              # Specify both files
  %(prog)s -t template.bdt -r vars.tfvars          # Use short options
  %(prog)s --template tpl.bdt --properties-file t.txt # Long options
  %(prog)s -r vars1.tfvars -r vars2.tfvars         # Multiple properties files
  %(prog)s --properties-file file1.tfvars --properties-file file2.tfvars
                                                   # Multiple properties files
  %(prog)s -k project,env,bucket                   # Use custom only-keys
  %(prog)s --only-keys project,env,bucket             # Use custom only-keys long option
  %(prog)s --not-keys secret,password              # Remove keys from properties
  %(prog)s -s                                      # Strip quotes from values
  %(prog)s --strip-quotes                          # Strip quotes from values
  %(prog)s --no-strip-quotes                       # Don't strip quotes (default)
  %(prog)s -o output.tf                            # Write output to file
  %(prog)s --output output.tf                      # Write output to file
  %(prog)s -f -o output.tf                         # Force overwrite
                                                   # existing output file
  %(prog)s --force --output output.tf              # Force overwrite
                                                   # existing output file
  %(prog)s --idempotent -o output.tf               # Check if output matches template
  %(prog)s -e                                      # Inject environment variables
  %(prog)s --env                                   # Inject environment variables
  %(prog)s --env-prefix                            # Inject env vars with 'env.' prefix
  %(prog)s --env-key-strip MYAPP_                  # Strip MYAPP_ prefix from env keys
  %(prog)s --env-key-strip AWS_ --env-key-strip K8S_ # Strip multiple prefixes
  %(prog)s --env-key-strip-hcdefaults              # Strip HashiCorp tool prefixes
  %(prog)s --post-process post.processor.func      # Run a post-processing function
  %(prog)s --import-module mymodule                # Import external module
                                                   # for post-processing
  %(prog)s --dump                                  # Show template and substitution dict
  %(prog)s -v                                      # Show version information
  %(prog)s --version                               # Show version information
  %(prog)s --verbose                               # Show more verbose output

        """,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version information and exit",
    )

    parser.add_argument(
        "template_file",
        nargs="?",
        default="DEFAULT.bdt",
        help="Template file containing placeholders (default: DEFAULT.bdt)",
    )

    parser.add_argument(
        "properties_file",
        nargs="?",
        default="terraform.tfvars",
        help="File containing property values (default: terraform.tfvars)",
    )

    parser.add_argument(
        "-t",
        "--template",
        dest="template_file_alt",
        help="Template file (alternative to positional argument)",
    )

    parser.add_argument(
        "-r",
        "--properties-file",
        dest="properties_files_alt",
        action="append",
        help="Properties file (can be used multiple times, overrides "
        "positional argument)",
    )

    parser.add_argument(
        "-k",
        "--only-keys",
        dest="only_keys",
        help="Comma-separated list of keys to look for in properties file",
    )

    parser.add_argument(
        "-n",
        "--not-keys",
        dest="not_keys",
        help="Comma-separated list of keys to remove from properties dictionary",
    )

    parser.add_argument(
        "--import-module",
        dest="import_module",
        help="Import external module for custom post-processing functions",
    )

    parser.add_argument(
        "--post-process",
        dest="post_process_func",
        default="default_post_process",
        help="Post-processing function name (default: default_post_process)",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="Output file path (default: print to stdout)",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force overwrite of output file if it exists",
    )

    parser.add_argument(
        "--idempotent",
        action="store_true",
        help="Check if generated template matches existing output file. "
        "Implies --force. Exit with code 4 if no output file specified, "
        "exit with code 5 if output file exists but differs from generated template.",
    )

    parser.add_argument(
        "--dump",
        action="store_true",
        help="Write template and substitution dictionary to stderr and exit",
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    parser.add_argument(
        "-s",
        "--strip-quotes",
        action="store_true",
        default=False,
        help="Strip outer quotes from property values (default: False)",
    )

    parser.add_argument(
        "--no-strip-quotes",
        action="store_false",
        dest="strip_quotes",
        help="Don't strip outer quotes from property values",
    )

    parser.add_argument(
        "-e",
        "--env",
        action="store_true",
        help="Inject system environment variables into the properties map",
    )

    parser.add_argument(
        "--env-prefix",
        action="store_true",
        help="Prefix environment variable keys with 'env.' (implies --env flag)",
    )

    parser.add_argument(
        "--env-key-strip",
        action="append",
        dest="env_key_strip",
        help=(
            "Strip prefix from environment variable keys "
            "(can be used multiple times, implies --env flag)"
        ),
    )

    parser.add_argument(
        "--env-key-strip-hcdefaults",
        action="store_true",
        dest="env_key_strip_hcdefaults",
        help=(
            "Strip common HashiCorp tool prefixes: TF_VAR_, PKR_VAR_, WP_VAR_, "
            "VAULT_, NOMAD_ (implies --env flag)"
        ),
    )

    args = parser.parse_args(argv)

    # Make --env-key-strip, --env-key-strip-hcdefaults, and --env-prefix imply --env
    if args.env_key_strip and not args.env:
        args.env = True
    if args.env_key_strip_hcdefaults and not args.env:
        args.env = True
    if args.env_prefix and not args.env:
        args.env = True

    # Validate that --idempotent requires --output
    if args.idempotent and not args.output_file:
        print(
            "Error: --idempotent flag requires --output flag to be set",
            file=sys.stderr,
        )
        sys.exit(4)

    # If --idempotent is set, imply --force
    if args.idempotent:
        args.force = True

    # Use alternative arguments if provided
    template_file = args.template_file_alt or args.template_file

    # Handle properties files - use list if --properties-file provided,
    # otherwise use positional
    if args.properties_files_alt:
        properties_files = args.properties_files_alt
    else:
        # Check if any environment flags are specified (they imply --env)
        env_flags_present = any(
            [
                args.env,
                args.env_prefix,
                args.env_key_strip,
                args.env_key_strip_hcdefaults,
            ]
        )

        # If env flags are present and using default properties file, make it optional
        if env_flags_present and args.properties_file == "terraform.tfvars":
            properties_files = []
        else:
            properties_files = [args.properties_file]

    if args.verbose:
        print(f"Template file: {template_file}", file=sys.stderr)
        if len(properties_files) == 0:
            print(
                "No properties files (using environment variables only)",
                file=sys.stderr,
            )
        elif len(properties_files) == 1:
            print(f"Properties file: {properties_files[0]}", file=sys.stderr)
        else:
            print(f"Properties files: {properties_files}", file=sys.stderr)
        if args.env:
            print("Environment variable injection enabled", file=sys.stderr)
            if args.env_key_strip_hcdefaults:
                print(
                    "HashiCorp default prefixes will be stripped: "
                    "TF_VAR_, PKR_VAR_, WP_VAR_, VAULT_, NOMAD_",
                    file=sys.stderr,
                )
            if args.env_key_strip:
                print(
                    f"Environment variable key prefixes to strip: {args.env_key_strip}",
                    file=sys.stderr,
                )
            if args.env_prefix:
                print(
                    "Environment variable keys will be prefixed with 'env.'",
                    file=sys.stderr,
                )

    # Check if files exist
    if not os.path.exists(template_file):
        print(f"Error: Template file '{template_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Check each properties file exists (only if files are provided)
    for properties_file in properties_files:
        if not os.path.exists(properties_file):
            print(
                f"Error: Properties file '{properties_file}' not found",
                file=sys.stderr,
            )
            sys.exit(1)

    # Parse keymap if provided
    only_keys = None
    if args.only_keys:
        only_keys = [key.strip() for key in args.only_keys.split(",") if key.strip()]
        if args.verbose:
            print(f"Using only keys: {only_keys}", file=sys.stderr)

    # Parse not_keys if provided
    not_keys = None
    if args.not_keys:
        not_keys = [key.strip() for key in args.not_keys.split(",") if key.strip()]
        if args.verbose:
            print(f"Keys to remove: {not_keys}", file=sys.stderr)

    # Handle post-processing function
    post_process_func = default_post_process

    if args.import_module:
        try:
            if args.verbose:
                print(f"Importing module: {args.import_module}", file=sys.stderr)

            # Add current directory to Python path for module imports
            original_path = sys.path.copy()
            if "." not in sys.path:
                sys.path.insert(0, ".")

            # Import the external module
            import importlib

            # Clear module from cache if it exists to ensure fresh import
            if args.import_module in sys.modules:
                del sys.modules[args.import_module]

            module = importlib.import_module(args.import_module)

            # Get the post-processing function from the module
            if hasattr(module, args.post_process_func):
                post_process_func = getattr(module, args.post_process_func)
                if args.verbose:
                    print(
                        f"Using post-processing function: {args.post_process_func} "
                        f"from {args.import_module}",
                        file=sys.stderr,
                    )
            else:
                print(
                    f"Warning: Function '{args.post_process_func}' not found in "
                    f"module '{args.import_module}', using default",
                    file=sys.stderr,
                )
                # Ensure the default post-processing function is used if the
                # specified function is invalid
                post_process_func = default_post_process

            # Restore original Python path
            sys.path = original_path

        except ImportError as e:
            print(
                f"Error: Could not import module '{args.import_module}': {e}",
                file=sys.stderr,
            )
            sys.exit(1)
        except Exception as e:
            print(
                f"Error: Problem with module '{args.import_module}': {e}",
                file=sys.stderr,
            )
            sys.exit(1)

    # Prepare environment variables if requested
    env_dict = None
    if args.env:
        # Start with the original environment
        env_dict = dict(os.environ)

        # Build list of prefixes to strip
        strip_prefixes = []

        # Add HashiCorp defaults if requested
        if args.env_key_strip_hcdefaults:
            hc_defaults = ["TF_VAR_", "PKR_VAR_", "WP_VAR_", "VAULT_", "NOMAD_"]
            strip_prefixes.extend(hc_defaults)

        # Add user-specified prefixes
        if args.env_key_strip:
            strip_prefixes.extend(args.env_key_strip)

        # Apply key stripping if any prefixes are specified (before prefixing)
        if strip_prefixes:
            stripped_env_dict = {}
            for key, value in env_dict.items():
                stripped_key = key
                # Apply each strip prefix in order
                for prefix in strip_prefixes:
                    if stripped_key.startswith(prefix):
                        stripped_key = stripped_key[len(prefix) :]
                        break  # Only strip the first matching prefix
                stripped_env_dict[stripped_key] = value
            env_dict = stripped_env_dict

        # Apply prefix if requested (after stripping)
        if args.env_prefix:
            # Prefix all environment variable keys with "env."
            env_dict = {f"env.{key}": value for key, value in env_dict.items()}

        if args.verbose:
            prefix_msg = " with 'env.' prefix" if args.env_prefix else ""

            # Calculate total number of prefixes stripped
            total_stripped = 0
            if args.env_key_strip_hcdefaults:
                total_stripped += 5  # TF_VAR_, PKR_VAR_, WP_VAR_, VAULT_, NOMAD_
            if args.env_key_strip:
                total_stripped += len(args.env_key_strip)

            strip_msg = (
                f" (after stripping {total_stripped} prefixes)"
                if total_stripped > 0
                else ""
            )
            print(
                f"Injected {len(env_dict)} environment variables"
                f"{prefix_msg}{strip_msg}",
                file=sys.stderr,
            )

    # Handle --dump flag
    if args.dump:
        # Read template file
        template_content = read_from_file(template_file)

        # Read and merge properties files
        merged_properties = ""
        for properties_file in properties_files:
            file_content = read_from_file(properties_file)
            merged_properties += file_content + "\n"

        # Process dictionary to get substitution dictionary
        tfdict = process_dictionary(
            merged_properties, args.strip_quotes, only_keys, env_dict, not_keys
        )

        # Build the dump output string
        dump_output = []
        dump_output.append(template_content)
        dump_output.append("\n---\n")

        # Add substitution dictionary as key=value pairs
        for key, value in sorted(tfdict.items()):
            dump_output.append(f"{key}={value}\n")

        # Write the collected string to stderr and exit
        print("".join(dump_output), file=sys.stderr, end="")
        sys.exit(0)

    try:
        # Generate the template
        if args.verbose:
            print("Generating template...", file=sys.stderr)

        result = generate_template_from_files(
            template_file,
            properties_files,
            strip_quotes=args.strip_quotes,
            only_keys=only_keys,
            post_process=post_process_func,
            env_dict=env_dict,
            not_keys=not_keys,
        )

        # Output the result
        if args.output_file:
            # Handle idempotency check
            if args.idempotent:
                if os.path.exists(args.output_file):
                    # Read existing file content
                    try:
                        with open(args.output_file) as f:
                            existing_content = f.read()

                        # Compare existing content with generated template
                        if existing_content != result:
                            print(
                                f"Error: Generated template differs from existing "
                                f"output file '{args.output_file}'",
                                file=sys.stderr,
                            )
                            sys.exit(5)

                        if args.verbose:
                            print(
                                f"Template matches existing output file "
                                f"'{args.output_file}' - no changes needed",
                                file=sys.stderr,
                            )
                        # File matches, no need to write
                        return
                    except OSError as e:
                        print(
                            f"Error: Could not read existing output file "
                            f"'{args.output_file}': {e}",
                            file=sys.stderr,
                        )
                        sys.exit(1)

                # File doesn't exist, will write it normally below
                if args.verbose:
                    print(
                        f"Output file '{args.output_file}' does not exist - "
                        f"creating it",
                        file=sys.stderr,
                    )
            else:
                # Check if output file exists and force is not specified
                if os.path.exists(args.output_file) and not args.force:
                    print(
                        f"Error: Output file '{args.output_file}' already exists. "
                        f"Use --force to overwrite.",
                        file=sys.stderr,
                    )
                    sys.exit(3)

            if args.verbose:
                print(f"Writing output to: {args.output_file}", file=sys.stderr)
            with open(args.output_file, "w") as f:
                f.write(result)
            if args.verbose:
                print(
                    f"Successfully wrote output to {args.output_file}", file=sys.stderr
                )
        else:
            print(result)

        if args.verbose:
            print("Template generation completed successfully", file=sys.stderr)

    except (OSError, FileNotFoundError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Contains AI-generated edits.
