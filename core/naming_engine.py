import os
import sys
import re
from datetime import datetime
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Pre-compiled fast regex pattern for OS filename sanitization
INVALID_CHARS_PATTERN = re.compile(r'[\\/*?:"<>|]')

def render_filename_template(
    template: str,
    counter: int,
    padding_digits: int,
    project_name: str,
    original_filename: str,
    extension: str
) -> str:
    """
    High-performance tokenized filename template evaluator.
    """
    if not template or not template.strip():
        template = "{counter}"

    now = datetime.now()
    formatted_counter = f"{counter:0{padding_digits}d}"
    orig_base = Path(original_filename).stem
    ext_clean = extension.lstrip(".")

    # Fast inline sanitization
    clean_project = INVALID_CHARS_PATTERN.sub('_', project_name)
    clean_original = INVALID_CHARS_PATTERN.sub('_', orig_base)

    replacements = {
        "{counter}": formatted_counter,
        "{project}": clean_project,
        "{date}": now.strftime("%Y-%m-%d"),
        "{time}": now.strftime("%H-%M-%S"),
        "{original}": clean_original,
        "{ext}": ext_clean,
    }

    result = template
    for token, val in replacements.items():
        result = result.replace(token, val)

    # Sanitize final output filename
    result = INVALID_CHARS_PATTERN.sub('_', result).strip()

    # Fast suffix check
    ext_suffix = f".{ext_clean}" if ext_clean else ""
    if not result.lower().endswith(ext_suffix.lower()):
        result = f"{result}{ext_suffix}"

    return result
