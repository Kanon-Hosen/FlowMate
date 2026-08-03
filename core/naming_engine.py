import os
import sys
import re
from datetime import datetime
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

def render_filename_template(
    template: str,
    counter: int,
    padding_digits: int,
    project_name: str,
    original_filename: str,
    extension: str
) -> str:
    """
    Evaluates dynamic filename template string with tokens.
    
    Tokens supported:
      {counter}   : Sequential padded number (e.g. 001)
      {project}   : Name of active project
      {date}      : Current date (YYYY-MM-DD)
      {time}      : Current time (HH-MM-SS)
      {original}  : Original filename base (without extension)
      {ext}       : File extension without leading dot (e.g. mp4)
    """
    if not template or not template.strip():
        template = "{counter}"

    now = datetime.now()
    formatted_counter = f"{counter:0{padding_digits}d}"
    orig_base = Path(original_filename).stem
    ext_clean = extension.lstrip(".")

    # Sanitize inputs
    clean_project = re.sub(r'[\\/*?:"<>|]', '_', project_name)
    clean_original = re.sub(r'[\\/*?:"<>|]', '_', orig_base)

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

    # Sanitize output filename to prevent invalid OS characters
    result = re.sub(r'[\\/*?:"<>|]', '_', result).strip()

    # Ensure proper extension
    ext_suffix = f".{ext_clean}" if ext_clean else ""
    if not result.lower().endswith(ext_suffix.lower()):
        result = f"{result}{ext_suffix}"

    return result
