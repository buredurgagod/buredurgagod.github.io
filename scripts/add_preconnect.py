import os
import re

def add_preconnect_links(directory):
    # Map of URL to full preconnect tag
    preconnect_candidates = {
        "https://fonts.googleapis.com": '<link rel="preconnect" href="https://fonts.googleapis.com">',
        "https://fonts.gstatic.com": '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        "https://code.jquery.com": '<link rel="preconnect" href="https://code.jquery.com">',
        "https://use.fontawesome.com": '<link rel="preconnect" href="https://use.fontawesome.com">',
        "https://static.hotjar.com": '<link rel="preconnect" href="https://static.hotjar.com">'
    }
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check for <head>
                if "<head>" in content:
                    new_links = []
                    for url, tag in preconnect_candidates.items():
                        # 1. Check if the URL is used in the file
                        if url in content:
                            # 2. Check if preconnect already exists using regex
                            # Matches <link ... rel="preconnect" ... href="url" ...> or <link ... href="url" ... rel="preconnect" ...>
                            # We search for 'preconnect' logic.
                            # Simpler: just check if the URL is present with rel="preconnect"
                            
                            pattern = rf'<link\s+[^>]*href=["\']{re.escape(url)}["\'][^>]*rel=["\']preconnect["\']|<link\s+[^>]*rel=["\']preconnect["\'][^>]*href=["\']{re.escape(url)}["\']'
                            
                            if not re.search(pattern, content, re.IGNORECASE):
                                new_links.append(tag)
                    
                    if new_links:
                        # Insert before </head>
                        replacement = "\n\t" + "\n\t".join(new_links) + "\n</head>"
                        updated_content = content.replace("</head>", replacement)
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(updated_content)
                        print(f"Updated {file}")

if __name__ == "__main__":
    add_preconnect_links(os.getcwd())
