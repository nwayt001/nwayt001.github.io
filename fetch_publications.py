#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and update the index.md file.
This script uses the scholarly library to scrape publication data.
"""

import time
import re
from datetime import datetime
from scholarly import scholarly

# Configuration
SCHOLAR_ID = "leelUAgAAAAJ"  # Your Google Scholar ID
OUTPUT_FILE = "index.md"
LATEX_OUTPUT_FILE = "publications.tex"  # LaTeX output for CV
PUBLICATIONS_MARKER_START = "## Publications"
RATE_LIMIT_DELAY = 5  # Seconds between requests to avoid being blocked
YOUR_NAME_VARIANTS = ["Nicholas Waytowich", "N Waytowich", "NR Waytowich",
                      "Nicholas R Waytowich", "Waytowich, N", "Waytowich, NR"]

def fetch_publications(scholar_id):
    """Fetch all publications for a given Google Scholar author ID."""
    print(f"Fetching publications for Scholar ID: {scholar_id}")

    try:
        # Search for the author
        search_query = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(search_query)

        print(f"Found author: {author.get('name', 'Unknown')}")
        print(f"Total publications found: {len(author.get('publications', []))}")

        publications = []

        # Get detailed info for each publication
        for i, pub in enumerate(author.get('publications', []), 1):
            try:
                # Fill publication details
                pub_filled = scholarly.fill(pub)

                # Extract relevant fields
                title = pub_filled.get('bib', {}).get('title', 'Untitled')
                authors = pub_filled.get('bib', {}).get('author', 'Unknown authors')
                venue = pub_filled.get('bib', {}).get('venue', '')
                year = pub_filled.get('bib', {}).get('pub_year', '')

                # Ensure year is a string for consistent sorting
                if year:
                    year = str(year)

                # Get PDF link if available
                pdf_url = pub_filled.get('eprint_url', '')

                # Get citation link
                pub_url = pub_filled.get('pub_url', '')

                # Create publication entry
                pub_entry = {
                    'title': title,
                    'authors': authors,
                    'venue': venue,
                    'year': year,
                    'pdf_url': pdf_url,
                    'pub_url': pub_url
                }

                publications.append(pub_entry)

                print(f"  [{i}/{len(author['publications'])}] {title[:60]}...")

                # Rate limiting to avoid being blocked
                time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                print(f"  Error fetching publication {i}: {e}")
                continue

        return publications

    except Exception as e:
        print(f"Error fetching author data: {e}")
        return []

def bold_name_in_authors(authors_str):
    """Bold your name in the author list for LaTeX."""
    for name_variant in YOUR_NAME_VARIANTS:
        # Replace the name with bolded version
        authors_str = authors_str.replace(name_variant, f"\\textbf{{{name_variant}}}")
    return authors_str

def escape_latex_chars(text):
    """Escape special LaTeX characters."""
    # Characters that need escaping in LaTeX
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

def format_publication_latex(pub):
    """Format a single publication as LaTeX for CV."""
    year = pub.get('year', '')
    authors = pub.get('authors', '')
    title = pub.get('title', '')
    venue = pub.get('venue', '')

    # Escape LaTeX special characters
    title = escape_latex_chars(title)
    venue = escape_latex_chars(venue)

    # Bold your name in the author list (before escaping, as we add LaTeX commands)
    authors = bold_name_in_authors(authors)
    authors = escape_latex_chars(authors)

    # Build the LaTeX string
    latex = f"\\cvitem{{{year}}}{{{authors}. \\textit{{{title}}}"

    if venue:
        latex += f". In: \\textit{{{venue}}}"

    if year:
        latex += f". {year}"

    latex += "}\n\\vspace{2mm}\n"

    return latex

def format_publication_markdown(pub):
    """Format a single publication as markdown."""
    # Build the markdown string
    md = f"**{pub['title']}**<br/>\n"
    md += f"{pub['authors']}<br/>\n"

    if pub['venue'] and pub['year']:
        md += f"{pub['venue']}, {pub['year']}<br/>\n"
    elif pub['venue']:
        md += f"{pub['venue']}<br/>\n"
    elif pub['year']:
        md += f"{pub['year']}<br/>\n"

    # Add links if available
    links = []
    if pub['pdf_url']:
        links.append(f"[PDF]({pub['pdf_url']})")
    if pub['pub_url'] and pub['pub_url'] != pub['pdf_url']:
        links.append(f"[Link]({pub['pub_url']})")

    if links:
        md += " | ".join(links) + "\n"

    return md

def update_index_file(publications):
    """Update the index.md file with fetched publications."""
    print(f"\nUpdating {OUTPUT_FILE}...")

    try:
        # Read current content
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the publications section
        pub_marker_index = content.find(PUBLICATIONS_MARKER_START)

        if pub_marker_index == -1:
            print("Error: Publications section not found in index.md")
            return False

        # Keep everything before the publications section
        before_pubs = content[:pub_marker_index]

        # Create new publications section
        new_pubs_section = PUBLICATIONS_MARKER_START + "\n\n"
        new_pubs_section += f'<span class="auto-updated">Auto-updated from Google Scholar</span>\n'
        new_pubs_section += f'<p class="last-updated">Last updated: {datetime.now().strftime("%B %d, %Y")}</p>\n\n'

        # Group publications by year
        pubs_by_year = {}
        for pub in publications:
            year = pub.get('year', 'Unknown')
            if not year:
                year = 'Unknown'
            if year not in pubs_by_year:
                pubs_by_year[year] = []
            pubs_by_year[year].append(pub)

        # Sort years in descending order (Unknown goes last)
        def sort_year_key(year):
            if year == 'Unknown' or year == '':
                return '0000'  # Put Unknown at the end
            return str(year)

        sorted_years = sorted(pubs_by_year.keys(), key=sort_year_key, reverse=True)

        # Add publications grouped by year
        for year in sorted_years:
            if year != 'Unknown':
                new_pubs_section += f"### {year}\n\n"

            for pub in pubs_by_year[year]:
                new_pubs_section += format_publication_markdown(pub) + "\n"

        # Combine everything
        new_content = before_pubs + new_pubs_section

        # Write back to file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Successfully updated {OUTPUT_FILE} with {len(publications)} publications")
        return True

    except Exception as e:
        print(f"Error updating index file: {e}")
        return False

def create_latex_file(publications):
    """Create a LaTeX file with publications formatted for CV."""
    print(f"\nCreating {LATEX_OUTPUT_FILE}...")

    try:
        # Group publications by year
        pubs_by_year = {}
        for pub in publications:
            year = pub.get('year', 'Unknown')
            if not year:
                year = 'Unknown'
            if year not in pubs_by_year:
                pubs_by_year[year] = []
            pubs_by_year[year].append(pub)

        # Sort years in descending order (Unknown goes last)
        def sort_year_key(year):
            if year == 'Unknown' or year == '':
                return '0000'  # Put Unknown at the end
            return str(year)

        sorted_years = sorted(pubs_by_year.keys(), key=sort_year_key, reverse=True)

        # Build LaTeX content
        latex_content = "% Publications formatted for CV\n"
        latex_content += f"% Auto-generated from Google Scholar on {datetime.now().strftime('%B %d, %Y')}\n"
        latex_content += "% Copy and paste into your CV .tex file\n\n"

        # Add publications grouped by year
        for year in sorted_years:
            if year != 'Unknown':
                latex_content += f"% === {year} ===\n"

            for pub in pubs_by_year[year]:
                latex_content += format_publication_latex(pub)
                latex_content += "\n"

        # Write to file
        with open(LATEX_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        print(f"Successfully created {LATEX_OUTPUT_FILE} with {len(publications)} publications")
        return True

    except Exception as e:
        print(f"Error creating LaTeX file: {e}")
        return False

def main():
    """Main function to orchestrate the update process."""
    print("=" * 60)
    print("Google Scholar Publications Updater")
    print("=" * 60)

    # Fetch publications
    publications = fetch_publications(SCHOLAR_ID)

    if not publications:
        print("\nNo publications found or error occurred.")
        return 1

    # Update the index file (markdown)
    success_md = update_index_file(publications)

    # Create LaTeX file for CV
    success_tex = create_latex_file(publications)

    if success_md and success_tex:
        print("\n✓ Publications updated successfully!")
        print(f"✓ Markdown: {OUTPUT_FILE}")
        print(f"✓ LaTeX: {LATEX_OUTPUT_FILE}")
        return 0
    else:
        print("\n✗ Some updates failed.")
        if not success_md:
            print(f"  ✗ Failed: {OUTPUT_FILE}")
        if not success_tex:
            print(f"  ✗ Failed: {LATEX_OUTPUT_FILE}")
        return 1

if __name__ == "__main__":
    exit(main())
