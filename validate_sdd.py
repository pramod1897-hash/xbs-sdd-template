#!/usr/bin/env python3
"""
SDD Template Validator

Validates that a Software Design Document (SDD) conforms to the required
structure defined in sdd-template.md.

Usage:
    python validate_sdd.py <path-to-sdd-file> [--template <path-to-template>]

Exit codes:
    0 - Validation passed
    1 - Validation failed (missing required sections or content issues)
    2 - Usage error (invalid arguments or file not found)
"""

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "1. Introduction",
    "1.1 Purpose",
    "1.2 Scope",
    "2. System Overview",
    "3. Architecture Design",
    "3.1 High-Level Architecture",
    "3.2 Architectural Patterns",
    "3.3 Technology Stack",
    "4. Component Design",
    "5. Interface Design",
    "6. Data Design",
    "7. Security Design",
    "8. Error Handling and Logging",
    "9. Performance and Scalability",
    "10. Deployment Design",
    "11. Testing Strategy",
    "12. Open Issues and Risks",
    "13. Revision History",
]

PLACEHOLDER_PATTERN = re.compile(r"^_.*_$", re.MULTILINE)
MIN_SECTION_LENGTH = 10


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Validate an SDD document against the required template structure."
    )
    parser.add_argument(
        "sdd_file",
        help="Path to the SDD document to validate",
    )
    parser.add_argument(
        "--template",
        default="sdd-template.md",
        help="Path to the SDD template file (default: sdd-template.md)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode: fail if placeholder text is detected in sections",
    )
    return parser.parse_args()


def read_file(path: str) -> str:
    file = Path(path)
    if not file.exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(2)
    if not file.is_file():
        print(f"ERROR: Path is not a file: {path}", file=sys.stderr)
        sys.exit(2)
    return file.read_text(encoding="utf-8")


def extract_headings(content: str) -> list[str]:
    """Extract all markdown headings from the document."""
    headings = []
    for line in content.splitlines():
        match = re.match(r"^#{1,6}\s+(.+)$", line.strip())
        if match:
            headings.append(match.group(1).strip())
    return headings


def extract_sections(content: str) -> dict[str, str]:
    """Extract sections from the document as a dict of heading -> body."""
    sections: dict[str, str] = {}
    current_heading = None
    current_body: list[str] = []

    for line in content.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_body).strip()
            current_heading = match.group(2).strip()
            current_body = []
        else:
            if current_heading is not None:
                current_body.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_body).strip()

    return sections


def check_required_sections(headings: list[str]) -> list[str]:
    """Return a list of required sections that are missing."""
    missing = []
    for required in REQUIRED_SECTIONS:
        if not any(required.lower() in h.lower() for h in headings):
            missing.append(required)
    return missing


def check_placeholder_sections(sections: dict[str, str]) -> list[str]:
    """Return sections that contain only placeholder text (italic lines)."""
    placeholder_sections = []
    for heading, body in sections.items():
        if not body:
            continue
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        non_placeholder_lines = [
            line for line in lines if not PLACEHOLDER_PATTERN.match(line)
        ]
        if lines and not non_placeholder_lines:
            placeholder_sections.append(heading)
    return placeholder_sections


def check_empty_sections(sections: dict[str, str]) -> list[str]:
    """Return sections that are completely empty (no content at all)."""
    empty_sections = []
    for heading, body in sections.items():
        if not body.strip():
            empty_sections.append(heading)
    return empty_sections


def validate(sdd_path: str, template_path: str, strict: bool) -> bool:
    """Run all validations. Returns True if validation passes."""
    print(f"Validating SDD document: {sdd_path}")
    print(f"Using template: {template_path}")
    print("-" * 60)

    sdd_content = read_file(sdd_path)
    headings = extract_headings(sdd_content)
    sections = extract_sections(sdd_content)

    errors: list[str] = []
    warnings: list[str] = []

    # Check required sections exist
    missing_sections = check_required_sections(headings)
    for section in missing_sections:
        errors.append(f"Missing required section: '{section}'")

    # Check for empty sections
    empty_sections = check_empty_sections(sections)
    for section in empty_sections:
        # Only warn about sections that are required
        if any(section.lower() in r.lower() for r in REQUIRED_SECTIONS):
            warnings.append(f"Empty section: '{section}'")

    # In strict mode, treat placeholder-only sections as errors
    if strict:
        placeholder_sections = check_placeholder_sections(sections)
        for section in placeholder_sections:
            if any(section.lower() in r.lower() for r in REQUIRED_SECTIONS):
                errors.append(
                    f"Section contains only placeholder text: '{section}'"
                )

    # Print results
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ⚠  {w}")
        print()

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  ✗  {e}")
        print()
        print(f"Validation FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return False

    print(f"Validation PASSED: 0 errors, {len(warnings)} warning(s).")
    return True


def main():
    args = parse_arguments()
    passed = validate(args.sdd_file, args.template, args.strict)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
