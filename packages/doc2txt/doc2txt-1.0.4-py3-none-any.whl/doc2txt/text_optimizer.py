"""Text optimization utilities for document text extraction."""


def is_table_row(line):
    """Check if a line appears to be a table row with | separators."""
    return '|' in line and line.count('|') >= 2


def optimize_text(text):
    """
    Optimize text formatting by merging lines without leading spaces to the previous line.

    This fixes the issue where doc files are rendered with visual line breaks.
    Special handling for table rows that contain | characters.

    Args:
        text (str): Raw text extracted from document

    Returns:
        str: Optimized text with merged lines
    """
    if not text:
        return text

    lines = text.split('\n')
    optimized_lines = []

    for i, line in enumerate(lines):
        if i == 0:
            # First line always gets added
            optimized_lines.append(line)
        else:
            # Check if current line starts with space, is empty, or is a table row
            if line.startswith(' ') or line.strip() == '' or is_table_row(line):
                # Line starts with space, is empty, or is a table row - keep as separate line
                optimized_lines.append(line)
            else:
                # Line doesn't start with space and is not a table row, merge with previous line
                if optimized_lines and optimized_lines[-1].strip() != '':
                    # Merge directly without adding space
                    optimized_lines[-1] += line
                else:
                    # Previous line was empty, start new line
                    optimized_lines.append(line)

    # Final step: remove leading spaces from each line (except table rows)
    final_lines = []
    for line in optimized_lines:
        if is_table_row(line):
            # Keep table rows as they are
            final_lines.append(line)
        else:
            # Remove leading spaces from non-table lines
            final_lines.append(line.lstrip(' '))

    return '\n'.join(final_lines)