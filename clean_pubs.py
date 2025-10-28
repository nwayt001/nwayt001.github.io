#!/usr/bin/env python3
"""
Clean up publications.tex to only show year for the first publication of each year.
This script modifies \cvitem entries so that only the first publication in each year
displays the year, making the CV more readable.
It also fixes escaped braces in \textbf commands.
"""

import re

def clean_publications(input_file='publications.tex', output_file='publications.tex'):
    """
    Read publications.tex and modify it so only the first publication
    of each year shows the year in \cvitem{year}{...}.
    Also fixes \textbf\{Name\} to \textbf{Name}.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # First, fix escaped braces in \textbf commands
        # Replace \textbf\{ with \textbf{
        content = content.replace(r'\textbf\{', r'\textbf{')
        # Replace \} that comes after \textbf{ (to close the textbf)
        content = re.sub(r'(\\textbf\{[^}]+)\\\}', r'\1}', content)

        # Split by lines
        lines = content.split('\n')

        cleaned_lines = []
        last_year = None

        for line in lines:
            # Check if this line contains a \cvitem
            cvitem_match = re.match(r'\\cvitem\{([^}]*)\}\{', line)

            if cvitem_match:
                year = cvitem_match.group(1)

                # If this year is the same as the last one, remove it
                if year == last_year and year != '':
                    # Replace \cvitem{year}{ with \cvitem{}{
                    line = line.replace(f'\\cvitem{{{year}}}{{', '\\cvitem{}{', 1)
                else:
                    # This is a new year, keep it
                    last_year = year

            cleaned_lines.append(line)

        # Write back to file
        cleaned_content = '\n'.join(cleaned_lines)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        print(f"✓ Successfully cleaned {input_file}")
        print(f"  • Years now only appear for the first publication of each year")
        print(f"  • Fixed escaped braces in \\textbf commands")
        return True

    except FileNotFoundError:
        print(f"✗ Error: {input_file} not found")
        print("  Run fetch_publications.py first to generate the file")
        return False
    except Exception as e:
        print(f"✗ Error cleaning publications: {e}")
        return False

if __name__ == "__main__":
    clean_publications()
