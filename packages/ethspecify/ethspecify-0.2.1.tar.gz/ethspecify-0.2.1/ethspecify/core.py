import difflib
import functools
import hashlib
import io
import os
import re
import requests
import textwrap
import tokenize


def strip_comments(code):
    # Split the original code into lines so we can decide which to keep or skip
    code_lines = code.splitlines(True)  # Keep line endings in each element

    # Dictionary: line_index -> list of (column, token_string)
    non_comment_tokens = {}

    # Tokenize the entire code
    tokens = tokenize.generate_tokens(io.StringIO(code).readline)
    for ttype, tstring, (srow, scol), _, _ in tokens:
        # Skip comments and pure newlines
        if ttype == tokenize.COMMENT:
            continue
        if ttype in (tokenize.NEWLINE, tokenize.NL):
            continue
        # Store all other tokens, adjusting line index to be zero-based
        non_comment_tokens.setdefault(srow - 1, []).append((scol, tstring))

    final_lines = []
    # Reconstruct or skip lines
    for i, original_line in enumerate(code_lines):
        # If the line has no non-comment tokens
        if i not in non_comment_tokens:
            # Check whether the original line is truly blank (just whitespace)
            if original_line.strip():
                # The line wasn't empty => it was a comment-only line, so skip it
                continue
            else:
                # A truly empty/blank line => keep it
                final_lines.append("")
        else:
            # Reconstruct this line from the stored tokens (preserving indentation/spaces)
            tokens_for_line = sorted(non_comment_tokens[i], key=lambda x: x[0])
            line_str = ""
            last_col = 0
            for col, token_str in tokens_for_line:
                # Insert spaces if there's a gap
                if col > last_col:
                    line_str += " " * (col - last_col)
                line_str += token_str
                last_col = col + len(token_str)
            # Strip trailing whitespace at the end of the line
            final_lines.append(line_str.rstrip())

    return "\n".join(final_lines)


def grep(root_directory, search_pattern, excludes=[]):
    matched_files = []
    regex = re.compile(search_pattern)
    exclude_patterns = [re.compile(pattern) for pattern in excludes]
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if any(pattern.search(file_path) for pattern in exclude_patterns):
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    if any(regex.search(line) for line in file):
                        matched_files.append(file_path)
            except (UnicodeDecodeError, IOError):
                continue
    return matched_files


def diff(a_name, a_content, b_name, b_content):
    diff = difflib.unified_diff(
        a_content.splitlines(), b_content.splitlines(),
        fromfile=a_name, tofile=b_name, lineterm=""
    )
    return "\n".join(diff)


@functools.lru_cache()
def get_links(version="nightly"):
    url = f"https://raw.githubusercontent.com/jtraglia/ethspecify/main/pyspec/{version}/links.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@functools.lru_cache()
def get_pyspec(version="nightly"):
    url = f"https://raw.githubusercontent.com/jtraglia/ethspecify/main/pyspec/{version}/pyspec.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_previous_forks(fork, version="nightly"):
    pyspec = get_pyspec(version)
    config_vars = pyspec["mainnet"][fork]["config_vars"]
    previous_forks = ["phase0"]
    for key in config_vars.keys():
        if key.endswith("_FORK_VERSION"):
            if key != f"{fork.upper()}_FORK_VERSION":
                if key != "GENESIS_FORK_VERSION":
                    f = key.split("_")[0].lower()
                    previous_forks.append(f)
    return list(reversed(previous_forks))


def get_spec(attributes, preset, fork, version="nightly"):
    pyspec = get_pyspec(version)
    spec = None
    if "function" in attributes or "fn" in attributes:
        if "function" in attributes and "fn" in attributes:
            raise Exception(f"cannot contain 'function' and 'fn'")
        if "function" in attributes:
            function_name = attributes["function"]
        else:
            function_name = attributes["fn"]

        spec = pyspec[preset][fork]["functions"][function_name]
        spec_lines = spec.split("\n")
        start, end = None, None

        try:
            vars = attributes["lines"].split("-")
            if len(vars) == 1:
                start = min(len(spec_lines), max(1, int(vars[0])))
                end = start
            elif len(vars) == 2:
                start = min(len(spec_lines), max(1, int(vars[0])))
                end = max(1, min(len(spec_lines), int(vars[1])))
            else:
                raise Exception(f"Invalid lines range for {function_name}: {attributes['lines']}")
        except KeyError:
            pass

        if start or end:
            start = start or 1
            if start > end:
                raise Exception(f"Invalid lines range for {function_name}: ({start}, {end})")
            # Subtract one because line numbers are one-indexed
            spec = "\n".join(spec_lines[start-1:end])
            spec = textwrap.dedent(spec)

    elif "constant_var" in attributes:
        if spec is not None:
            raise Exception(f"Tag can only specify one spec item")
        info = pyspec[preset][fork]["constant_vars"][attributes["constant_var"]]
        spec = (
            attributes["constant_var"]
            + (": " + info[0] if info[0] is not None else "")
            + " = "
            + info[1]
        )
    elif "preset_var" in attributes:
        if spec is not None:
            raise Exception(f"Tag can only specify one spec item")
        info = pyspec[preset][fork]["preset_vars"][attributes["preset_var"]]
        spec = (
            attributes["preset_var"]
            + (": " + info[0] if info[0] is not None else "")
            + " = "
            + info[1]
        )
    elif "config_var" in attributes:
        if spec is not None:
            raise Exception(f"Tag can only specify one spec item")
        info = pyspec[preset][fork]["config_vars"][attributes["config_var"]]
        spec = (
            attributes["config_var"]
            + (": " + info[0] if info[0] is not None else "")
            + " = "
            + info[1]
        )
    elif "custom_type" in attributes:
        if spec is not None:
            raise Exception(f"Tag can only specify one spec item")
        spec = (
            attributes["custom_type"]
            + " = "
            + pyspec[preset][fork]["custom_types"][attributes["custom_type"]]
        )
    elif "ssz_object" in attributes:
        if spec is not None:
            raise Exception(f"Tag can only specify one spec item")
        spec = pyspec[preset][fork]["ssz_objects"][attributes["ssz_object"]]
    elif "dataclass" in attributes:
        if spec is not None:
            raise Exception(f"Tag can only specify one spec item")
        spec = pyspec[preset][fork]["dataclasses"][attributes["dataclass"]].replace("@dataclass\n", "")
    else:
        raise Exception("invalid spec tag")
    return spec

def get_latest_fork(version="nightly"):
    """A helper function to get the latest non-eip fork."""
    pyspec = get_pyspec(version)
    forks = sorted(
        pyspec["mainnet"].keys(),
        key=lambda x: (x != "phase0", x.startswith("eip"), x)
    )
    for fork in reversed(forks):
        if not fork.startswith("eip"):
            return fork

def parse_common_attributes(attributes):
    try:
        preset = attributes["preset"]
    except KeyError:
        preset = "mainnet"

    try:
        version = attributes["version"]
    except KeyError:
        version = "nightly"

    try:
        fork = attributes["fork"]
    except KeyError:
        fork = get_latest_fork(version)

    try:
        style = attributes["style"]
    except KeyError:
        style = "hash"

    return preset, fork, style, version

def get_spec_item(attributes):
    preset, fork, style, version = parse_common_attributes(attributes)
    spec = get_spec(attributes, preset, fork, version)

    if style == "full" or style == "hash":
        return spec
    elif style == "diff":
        previous_forks = get_previous_forks(fork, version)

        previous_fork = None
        previous_spec = None
        for i, _ in enumerate(previous_forks):
            previous_fork = previous_forks[i]
            previous_spec = get_spec(attributes, preset, previous_fork, version)
            if previous_spec != "phase0":
                try:
                    previous_previous_fork = previous_forks[i+1]
                    previous_previous_spec = get_spec(attributes, preset, previous_previous_fork, version)
                    if previous_previous_spec == previous_spec:
                        continue
                except KeyError:
                    pass
                except IndexError:
                    pass
            if previous_spec != spec:
                break
            if previous_spec == "phase0":
                raise Exception("there is no previous spec for this")
        return diff(previous_fork, strip_comments(previous_spec), fork, strip_comments(spec))
    if style == "link":
        if "function" in attributes or "fn" in attributes:
            if "function" in attributes and "fn" in attributes:
                raise Exception(f"cannot contain 'function' and 'fn'")
            if "function" in attributes:
                function_name = attributes["function"]
            else:
                function_name = attributes["fn"]
            for key, value in get_links(version).items():
                if fork in key and key.endswith(function_name):
                    return value
            return "Could not find link"
        else:
            return "Not available for this type of spec"
    else:
        raise Exception("invalid style type")


def extract_attributes(tag):
    attr_pattern = re.compile(r'(\w+)="(.*?)"')
    return dict(attr_pattern.findall(tag))


def replace_spec_tags(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Define regex to match self-closing tags and long (paired) tags separately
    pattern = re.compile(
        r'(?P<self><spec\b[^>]*\/>)|(?P<long><spec\b[^>]*>[\s\S]*?</spec>)',
        re.DOTALL
    )

    def rebuild_opening_tag(attributes, hash_value):
        # Rebuild a fresh opening tag from attributes, overriding any existing hash.
        new_opening = "<spec"
        for key, val in attributes.items():
            if key != "hash":
                new_opening += f' {key}="{val}"'
        new_opening += f' hash="{hash_value}">'
        return new_opening

    def rebuild_self_closing_tag(attributes, hash_value):
        # Build a self-closing tag from attributes, forcing a single space before the slash.
        new_tag = "<spec"
        for key, val in attributes.items():
            if key != "hash":
                new_tag += f' {key}="{val}"'
        new_tag += f' hash="{hash_value}" />'
        return new_tag

    def replacer(match):
        # Always use the tag text from whichever group matched:
        if match.group("self") is not None:
            original_tag_text = match.group("self")
        else:
            original_tag_text = match.group("long")
        # Determine the original opening tag (ignore inner content)
        if match.group("self") is not None:
            original_tag_text = match.group("self")
        else:
            long_tag_text = match.group("long")
            opening_tag_match = re.search(r'<spec\b[^>]*>', long_tag_text)
            original_tag_text = opening_tag_match.group(0) if opening_tag_match else long_tag_text

        attributes = extract_attributes(original_tag_text)
        print(f"spec tag: {attributes}")
        preset, fork, style, version = parse_common_attributes(attributes)
        spec = get_spec(attributes, preset, fork, version)
        hash_value = hashlib.sha256(spec.encode('utf-8')).hexdigest()[:8]

        if style == "hash":
            # Rebuild a fresh self-closing tag.
            updated_tag = rebuild_self_closing_tag(attributes, hash_value)
            return updated_tag
        else:
            # For full/diff styles, rebuild as a long (paired) tag.
            new_opening = rebuild_opening_tag(attributes, hash_value)
            spec_content = get_spec_item(attributes)
            prefix = content[:match.start()].splitlines()[-1]
            prefixed_spec = "\n".join(
                f"{prefix}{line}" if line.rstrip() else prefix.rstrip()
                for line in spec_content.rstrip().split("\n")
            )
            updated_tag = f"{new_opening}\n{prefixed_spec}\n{prefix}</spec>"
            return updated_tag


    # Replace all matches in the content
    updated_content = pattern.sub(replacer, content)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
