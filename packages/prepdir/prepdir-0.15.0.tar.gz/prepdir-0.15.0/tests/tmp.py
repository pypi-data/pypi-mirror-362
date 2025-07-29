import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

GENERATED_HEADER_PATTERN = re.compile(
    r"^File listing generated (\d{4}-\d{2}-\d{2} [\d\:\.\s]+\d)?(?:\s+by\s+(.*))?$", re.MULTILINE
)

headers = [
    "File listing generated 2025-06-26 06:50:58.951077 by prepdir version 0.14.1 (pip install prepdir)",
    "File listing generated 2025-06-26 06:50:58.951077",
    "File listing generated 2025-06-26 06:50:58",
    "File listing generated 2025-06-26 06:50:58 by grok 3",
    "File listing generated 2025-06-26 01:02 by grok 3",
]

for header in headers:
    gen_header_match = GENERATED_HEADER_PATTERN.search(header)
    if gen_header_match:
        print(f"{header}: date={gen_header_match.group(1)}, c={gen_header_match.group(2)}")
    else:
        print(f"{header}: no match")
