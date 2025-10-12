# Nicholas Waytowich - Professional Bio Site

A modern, professional bio and portfolio website for Dr. Nicholas Waytowich, Machine Learning Research Scientist at the US Army Research Laboratory.

## Features

### 🎨 Modern Design
- Custom CSS with modern typography (Inter font family)
- Professional color scheme with blue accents
- Responsive design for mobile and desktop
- Smooth animations and transitions
- Card-based layouts for publications and projects

### 📚 Auto-Updating Publications
- Automated publication synchronization from Google Scholar
- Monthly updates via GitHub Actions
- No manual updates needed for new publications
- Last updated timestamp displayed
- **LaTeX export** - Generates `publications.tex` file formatted for CV use

### 🚀 Portfolio Section
- Dedicated projects page showcasing research work
- Project cards with tags and links
- Research areas overview
- Collaborations and competition highlights

### 🧭 Enhanced Navigation
- Smooth scrolling between sections
- Active section highlighting
- Easy access to CV and Google Scholar profile

## How It Works

### Auto-Publication Updates

The site uses a Python script (`fetch_publications.py`) that:
1. Connects to Google Scholar using the `scholarly` library
2. Fetches all publications for the specified author ID
3. Formats them in markdown with proper styling
4. Updates the `index.md` file automatically
5. **Generates `publications.tex`** - LaTeX formatted publications for your CV
   - Uses `\cvitem{}{}` format
   - Automatically bolds your name in author lists
   - Escapes special LaTeX characters
   - Groups by year

This is automated via GitHub Actions (`.github/workflows/update-publications.yml`) that:
- Runs on the 1st of every month at 3 AM UTC
- Can be triggered manually from the GitHub Actions tab
- Only commits changes if new publications are found
- Uses rate limiting to avoid Google Scholar blocks

### File Structure

```
.
├── index.md                    # Main bio page with about and publications
├── projects.md                 # Portfolio/projects page
├── _layouts/
│   └── default.html           # Custom Jekyll layout with navigation
├── assets/
│   ├── css/
│   │   └── custom.css         # Modern styling
│   └── js/
│       └── navigation.js      # Smooth scrolling and nav highlighting
├── .github/
│   └── workflows/
│       └── update-publications.yml  # Auto-update workflow
├── fetch_publications.py      # Google Scholar scraper
└── requirements.txt           # Python dependencies
```

## Local Development

### Prerequisites
- Python 3.11+
- Jekyll (for local testing)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nwayt001/nwayt001.github.io.git
cd nwayt001.github.io
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Test the publication updater (optional):
```bash
python fetch_publications.py
```

4. Run Jekyll locally (optional):
```bash
bundle exec jekyll serve
```

## Manual Publication Update

To manually update publications:

```bash
# Run the updater
python fetch_publications.py

# This generates:
# - index.md (updated with new publications)
# - publications.tex (LaTeX format for your CV)

# Commit the markdown changes (LaTeX file is in .gitignore)
git add index.md
git commit -m "Update publications"
git push
```

### Using the LaTeX File for Your CV

After running the script, you'll find `publications.tex` in your directory. To use it:

1. Open `publications.tex` in any text editor
2. Copy the formatted publications
3. Paste into your Overleaf CV `.tex` file
4. The format matches your existing style:
   - `\cvitem{year}{authors. \textit{title}. In: \textit{venue}. year}`
   - Your name is automatically bolded: `\textbf{Waytowich, N}`
   - Special characters are escaped for LaTeX
   - Publications grouped by year with comments

Or trigger the GitHub Action:
1. Go to the Actions tab in GitHub
2. Select "Update Publications from Google Scholar"
3. Click "Run workflow"

## Configuration

### Update Frequency
To change how often publications are updated, edit `.github/workflows/update-publications.yml`:
```yaml
schedule:
  - cron: '0 3 1 * *'  # Currently: 1st of month at 3 AM UTC
```

### Google Scholar ID
To change the Google Scholar profile, edit `fetch_publications.py`:
```python
SCHOLAR_ID = "leelUAgAAAAJ"  # Your Scholar ID
```

### Styling
Customize colors and design in `assets/css/custom.css`:
```css
:root {
  --primary-color: #2563eb;
  --primary-dark: #1e40af;
  /* ... more variables */
}
```

## Technologies Used

- **Jekyll** - Static site generator (GitHub Pages)
- **Python** - Publication fetching automation
- **scholarly** - Google Scholar scraping library
- **GitHub Actions** - CI/CD automation
- **Custom CSS** - Modern, responsive styling
- **JavaScript** - Navigation and scroll effects

## Credits

Designed and developed with assistance from Claude Code.

## License

Personal website - All rights reserved.
