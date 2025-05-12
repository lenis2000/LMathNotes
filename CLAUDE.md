# Notes Repository Structure

## How Hugo Displays Content

This Hugo site is configured to display a collection of notes with special handling for TeX files and confidential content:

### Content Organization
- Content is organized in dated directories (like `2025-05-08-Macdonald-measures-type-D-quivers/`)
- Each directory typically contains:
  - TeX files (main and supporting)
  - PDFs (compiled documents)
  - description.txt (provides title and metadata)
  - Additional supporting files (images, bibliography)

### Template Structure
There are several main templates that handle displaying notes:
1. `layouts/index.html` - The main homepage template (overrides theme's index)
2. `layouts/Handwritten_Notebooks/list.html` - Template for displaying handwritten notebooks
3. `layouts/_default/monthly-notes.html` - Template for displaying notes by month
4. `layouts/_default/tex-viewer.html` - Template for the TeX file viewer
5. `layouts/_default/tex.html` - Template for displaying TeX file listings
6. `layouts/page/history.html` - Template for displaying note history chains
7. `layouts/partials/history-recursive.html` - Partial for recursively displaying note histories

### Main Page Display
- The index.html template lists content chronologically by date
- For each item, it shows:
  - Title and description extracted from description.txt
  - Links to PDF (blue) and TEX (green) files
  - Additional files as smaller links
  - Expandable description via details/summary elements
- Details elements maintain their open/closed state using localStorage
- Confidential notes can be blurred and toggled with Command+B/Ctrl+B

### Search Functionality
- Implemented in `layouts/partials/search-panel.html`
- Features:
  - Real-time searching as you type
  - Case-smart search (uppercase letters match exactly, lowercase matches both cases)
  - Searches across titles, descriptions, filenames, and TEX content
  - Keyboard shortcuts (Escape to clear/focus search)
  - Shows/hides date sections based on matching results
  - "No results" message when nothing matches

### TeX Viewer
- Custom tex-viewer.html template for displaying TeX files
- Accessed via URL: `/tex-viewer?path=content/path/to/file.tex`
- Features:
  - Syntax highlighting for LaTeX using Prism.js
  - Line numbers
  - Soft wrap toggle (on by default)
  - Preamble separation and collapsible display
  - Download button
  - File size display and path information
  - Mobile-responsive design

### Configuration
- Hugo is configured to serve .tex files as plain text
- Content directory is mounted as static files via module mounts
- Custom CSS provides distinct styling for PDF and TEX links
- Raw HTML rendering is enabled for proper content display

### File Handling
- PDF files are linked directly for download/viewing
- TeX files are displayed through the custom viewer
- Description.txt files provide metadata (first line = title, rest = description)
- Additional files are displayed with appropriate styling based on type
- prev.txt files define connections between notes for the history view
- conf.txt files mark notes as confidential with blur effect

### History View
- Implemented in `layouts/page/history.html` and `layouts/partials/history-recursive.html`
- Accessed via URL: `/history?note=2025-05-08-Note-Name`
- Shows the history chain of notes based on prev.txt connections
- Features:
  - Client-side JavaScript processes URL query parameters
  - Pre-renders all possible history chains at build time
  - Recursive display of note history
  - Circular reference detection
  - Displays titles, descriptions, and links from each note
  - Mobile-responsive design with nested styling
  - Error handling for missing or invalid notes
  - Supports blur functionality for confidential notes with Command+B/Ctrl+B toggle

### Confidential Content Handling
- Notes with a `conf.txt` file are treated as confidential
- Confidential notes display with a blur effect on descriptions and links
- Universal keyboard shortcut (Command+B on Mac, Ctrl+B on Windows/Linux) toggles blur
- Works consistently across all views (main page, monthly notes, handwritten notebooks, history)
- CSS blur filter implementation preserves layout while obscuring content
- Content marked as confidential also prevents selection when blurred