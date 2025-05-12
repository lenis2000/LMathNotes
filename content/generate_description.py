#!/Users/leo/Desktop/notes/content/venv/bin/python

import os
import sys
import argparse
import openai
import re

# GPT-4.1 is already set up via environment variables (assumes OPENAI_API_KEY is set)
client = openai.OpenAI()

def get_ai_completion(prompt):
    """Get completion from GPT-4.1"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or "gpt-4-1106-preview"
            messages=[
                {"role": "system", "content": "You are an assistant specialized in mathematics and research papers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: Failed to get AI completion: {e}")
        sys.exit(1)

def extract_from_tex(tex_file):
    """Extract title, authors, and content from the TeX file"""
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Try to extract title
        title_match = re.search(r'\\title{([^}]*)}', content)
        title = title_match.group(1) if title_match else ""
        
        # Try to extract authors
        author_match = re.search(r'\\author{([^}]*)}', content)
        authors = author_match.group(1) if author_match else ""
        
        # Clean up LaTeX commands
        title = re.sub(r'\\[a-zA-Z]+{([^}]*)}', r'\1', title)
        authors = re.sub(r'\\[a-zA-Z]+{([^}]*)}', r'\1', authors)
        
        # Get the first 2000 characters for context
        preview = content[:2000]
        
        return {
            "title": title.strip(),
            "authors": authors.strip(),
            "preview": preview.strip()
        }
    except Exception as e:
        print(f"Error reading TeX file: {e}")
        return {"title": "", "authors": "", "preview": ""}

def create_description(tex_file, output_file, update_title=False, force=False):
    """Create or update the description.txt file"""
    # Extract info from TeX
    tex_info = extract_from_tex(tex_file)
    
    # Check if description file exists
    file_exists = os.path.exists(output_file)
    
    if not file_exists or force:
        # Create a new file with both title and description
        print(f"Generating new description file: {output_file}")
        
        prompt = f"""Based on this LaTeX document:
        
Title: {tex_info['title']}
Authors: {tex_info['authors']}
Content preview:
{tex_info['preview']}

Generate a title and description for this mathematical research note. 
The title should be concise and descriptive (include author names if available).
The description should be 2-3 sentences summarizing the key mathematical concepts and findings.

Format your response exactly like this, WITHOUT any brackets:
TITLE

DESCRIPTION
"""
        
        response = get_ai_completion(prompt)
        
        # Ensure proper formatting (blank line between title and description)
        lines = response.split('\n')
        if len(lines) > 0:
            # Remove any brackets from title and description
            title = lines[0].strip().replace('[', '').replace(']', '')
            description = '\n'.join(lines[1:]).strip().replace('[', '').replace(']', '')
            
            # Ensure there's a blank line between title and description
            content = f"{title}\n\n{description}"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Created description file with title and description")
        else:
            print("Error: AI response was not properly formatted")
            sys.exit(1)
            
    else:
        # Update existing file
        with open(output_file, 'r', encoding='utf-8') as f:
            current_content = f.read().strip().split('\n')
        
        if len(current_content) > 0:
            current_title = current_content[0]
            
            if update_title:
                # Update title but keep description
                print(f"Updating title in: {output_file}")
                
                prompt = f"""Based on this LaTeX document:
                
Title: {tex_info['title']}
Authors: {tex_info['authors']}
Content preview:
{tex_info['preview']}

Generate a new title for this mathematical research note.
The title should be concise and descriptive (include author names if available).

Current title: {current_title}

Return ONLY the new title."""
                
                new_title = get_ai_completion(prompt).replace('[', '').replace(']', '')
                
                # Get existing description (everything after the first line)
                if len(current_content) > 2:
                    existing_desc = '\n'.join(current_content[2:])
                else:
                    existing_desc = ""
                
                # Write updated content
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"{new_title}\n\n{existing_desc}")
                print("Updated title in description file")
                
            else:
                # Update description but keep title
                print(f"Updating description in: {output_file}")
                
                prompt = f"""Based on this LaTeX document:
                
Title: {tex_info['title']}
Authors: {tex_info['authors']}
Content preview:
{tex_info['preview']}

Generate a description for this mathematical research note.
The description should be 2-3 sentences summarizing the key mathematical concepts and findings.

Current title: {current_title}

Return ONLY the description."""
                
                new_desc = get_ai_completion(prompt).replace('[', '').replace(']', '')
                
                # Write updated content
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"{current_title}\n\n{new_desc}")
                print("Updated description in description file")

def main():
    parser = argparse.ArgumentParser(description='Generate description.txt from LaTeX files')
    parser.add_argument('directory', nargs='?', help='Directory to process (optional)')
    parser.add_argument('-d', '--directory', dest='dir_opt', help='Single directory to process (optional)')
    parser.add_argument('-t', '--title', action='store_true', help='Update title (first line)')
    parser.add_argument('-f', '--force', action='store_true', help='Force create/overwrite description')
    parser.add_argument('-a', '--all', action='store_true', help='Process all note directories')
    
    args = parser.parse_args()
    
    # Get content directory (parent directory of the script)
    content_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Process all directories if requested
    if args.all:
        # Get all subdirectories that match date pattern (YYYY-MM-DD-*)
        note_dirs = []
        for item in os.listdir(content_dir):
            full_path = os.path.join(content_dir, item)
            if os.path.isdir(full_path) and re.match(r'\d{4}-\d{2}-\d{2}-', item):
                note_dirs.append(full_path)
        
        if not note_dirs:
            print("No note directories found")
            sys.exit(1)
        
        print(f"Found {len(note_dirs)} note directories to process")
        
        # Process each directory
        for directory in note_dirs:
            try:
                process_directory(directory, args.title, args.force)
                print(f"Processed: {os.path.basename(directory)}")
                print("-" * 50)
            except Exception as e:
                print(f"Error processing {directory}: {e}")
    
    # Process a single directory
    elif args.directory or args.dir_opt:
        dir_path = args.directory or args.dir_opt
        
        # Check if it's a relative path
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(content_dir, dir_path)
            
        process_directory(dir_path, args.title, args.force)
    
    else:
        parser.print_help()
        sys.exit(1)
    
    print("All done!")

def process_directory(directory, update_title=False, force=False):
    """Process a single directory"""
    # Check if directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found")
        return
    
    print(f"Processing directory: {directory}")
    
    # Find TeX file in the directory
    tex_files = [f for f in os.listdir(directory) if f.endswith('.tex')]
    if not tex_files:
        print(f"Error: No TeX files found in '{directory}'")
        return
    
    tex_file = os.path.join(directory, tex_files[0])
    print(f"Found TeX file: {tex_file}")
    
    # Determine description file path
    desc_file = os.path.join(directory, "description.txt")
    
    # Create or update the description file
    create_description(tex_file, desc_file, update_title=update_title, force=force)

if __name__ == "__main__":
    main()