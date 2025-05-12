# LMathNotes - Hugo-based Mathematical Research Notes Repository

lmathnotes is a specialized Hugo-based web application designed for organizing, displaying, and navigating mathematical research notes with a focus on LaTeX content. It provides a comprehensive system for managing academic notes with advanced features for confidentiality, history tracking, and content exploration.

## Features

### Content Organization
- Chronological organization of notes in dated directories
- Specialized handling for LaTeX/TeX files with custom viewer
- Support for both standard research notes and handwritten notebook collections
- Full-text search across all note content, titles, and descriptions

### Navigation & Display
- **Homepage View**: Chronological listing of all notes with expandable descriptions
- **Monthly Notes View**: Notes organized by month with consistent display
- **Handwritten Notebooks View**: Special display for handwritten notebook collections
- **History View**: Chain visualization connecting related notes via prev.txt references
- **TeX Viewer**: Specialized viewer for LaTeX files with syntax highlighting

### Specialized Features

#### TeX File Handling
- Custom TeX viewer with syntax highlighting via Prism.js
- Line numbers for easy reference
- Soft wrap toggle for improved readability
- Automatic preamble separation with collapsible display
- One-click download option
- File metadata display (size, path)

#### Search Capabilities
- Real-time searching across all content
- Case-smart search (uppercase for exact matches, lowercase for case-insensitive)
- Visual feedback with dynamic filtering of results
- Keyboard shortcut support (Escape to clear/focus)
- "No results" messaging with clear user feedback

#### History Tracking
- Visualization of note evolution through connected history chains
- Bidirectional navigation between related notes
- Recursive history display with circular reference detection
- Client-side JavaScript for dynamic history exploration

#### Confidential Content Protection
- Confidential notes marked via `conf.txt` files
- Content protection with CSS blur effect
- Universal keyboard shortcut (Cmd+B / Ctrl+B) to toggle blur state
- Consistent protection across all views (main, monthly, handwritten, history)
- Selection prevention for blurred content

### Technical Details
- Built on Hugo static site generator
- Custom templates for specialized content types
- Local storage for preserving UI state (open/closed sections)
- Responsive design for all screen sizes
- Custom CSS for distinct styling of different content types

## File Types & Conventions

The system uses several special files to manage content and relationships:

| File | Purpose |
|------|---------|
| `description.txt` | Defines note title (first line) and description (remaining text) |
| `prev.txt` | Lists note IDs that precede the current note in history |
| `conf.txt` | Marks a note as confidential (triggering blur effect) |
| `*.tex` | LaTeX source files (rendered in custom viewer) |
| `*.pdf` | Compiled PDF documents (available for direct viewing/download) |

Note ID refers to the directory name of a note (e.g., `2025-05-11-blur-test-1`). These IDs are used in `prev.txt` files to establish relationships between notes and in URL parameters for the history view.

## Directory Structure

```
- content/
  - YYYY-MM/
    - YYYY-MM-DD-Note-Title/
      - YYYY-MM-DD-Note-Title.tex  (Main TeX file)
      - YYYY-MM-DD-Note-Title.pdf  (Compiled PDF)
      - description.txt            (Title and description)
      - prev.txt                   (Historical connections)
      - conf.txt                   (Optional, for confidential notes)
      - additional files...        (Images, bibliographies, etc.)
  - Handwritten_Notebooks/
    - YYYY-MM-NN_Notebook_description/
      - description.txt
      - PDF files...
- layouts/
  - Custom templates for different views
- static/
  - css/
  - js/
  - icons/
```

## URL Structure

| URL Pattern | Purpose |
|-------------|---------|
| `/` | Homepage with chronological listing of all notes |
| `/YYYY-MM/` | Monthly note listing |
| `/Handwritten_Notebooks/` | Handwritten notebooks listing |
| `/history?note=YYYY-MM-DD-Note-Title` | History view for specific note |
| `/tex-viewer?path=content/path/to/file.tex` | TeX file viewer |

## Setup Instructions

1. Install Hugo (extended version recommended)
2. Clone this repository
3. Run `hugo server` to start the development server
4. Access the site at `http://localhost:1313/`

For production deployment:
1. Run `hugo` to build the static site
2. Deploy the `public` directory to your web server

## Configuration

Configuration is managed through `hugo.toml`:

- Custom media types for TeX files
- Server headers for correct content type handling
- Module mounts for serving content directory as static files
- Theme configuration for Paperesque base theme

## Usage Guidelines

### Adding New Notes
1. Create a new directory with the naming pattern `YYYY-MM-DD-Note-Title`
2. Add your main TeX file with matching name
3. Create a `description.txt` with title and description
4. (Optional) Add `prev.txt` to link to previous related notes
5. (Optional) Add `conf.txt` if the note contains confidential information

### Navigation
- Use the main page for chronological browsing
- Use search for finding specific content
- Use history view to track research evolution

### Working with Confidential Content
- Add an empty `conf.txt` file to any note directory to mark as confidential
- Use Cmd+B (Mac) or Ctrl+B (Windows/Linux) to toggle blur effect
- Content remains protected until explicitly revealed by the user

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
Copyright (c) 2025 Leonid Petrov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

*lmathnotes - Organize your mathematical research journey*
