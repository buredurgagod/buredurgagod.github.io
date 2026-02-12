import os
import re

def update_html_paths(directory):
    # Mapping of old paths to new paths
    # We moved css, js, images, fonts, vendors to src/assets/
    # So "css/" -> "src/assets/css/"
    # "js/" -> "src/assets/js/"
    # "images/" -> "src/assets/images/"
    # "fonts/" -> "src/assets/fonts/"
    # "vendors/" -> "src/assets/vendors/"
    
    replacements = {
        'href="css/': 'href="src/assets/css/',
        'src="js/': 'src="src/assets/js/',
        'src="images/': 'src="src/assets/images/',
        'href="images/': 'href="src/assets/images/',
        'src="vendors/': 'src="src/assets/vendors/',
        'href="vendors/': 'href="src/assets/vendors/',
        # Handle cases with ./ prefix
        'href="./css/': 'href="./src/assets/css/',
        'src="./js/': 'src="./src/assets/js/',
        'src="./images/': 'src="./src/assets/images/',
        'href="./images/': 'href="./src/assets/images/',
        'src="./vendors/': 'src="./src/assets/vendors/',
        'href="./vendors/': 'href="./src/assets/vendors/',
        # Also handle fonts if referenced in HTML (unlikely but possible)
        # Fonts are usually referenced in CSS, which is fine since they are relative to CSS file
        # But if referenced in HTML:
        'href="fonts/': 'href="src/assets/fonts/',
    }

    # CSS files might need updates if they reference images/fonts relative to themselves.
    # If css/style.css references ../images/bg.jpg, and we moved:
    # old: css/style.css, images/bg.jpg -> relative is ../images/bg.jpg
    # new: src/assets/css/style.css, src/assets/images/bg.jpg -> relative is ../images/bg.jpg
    # So relative paths in CSS should remain valid!
    
    # However, if we moved CSS but NOT images, it would break. But we moved ALL assets.
    # So CSS/JS internal references should be fine if they use relative paths.
    
    for root, dirs, files in os.walk(directory):
        # Skip node_modules and .git and dist and src
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.git' in dirs:
            dirs.remove('.git')
        if 'dist' in dirs:
            dirs.remove('dist')
        if 'src' in dirs:
            dirs.remove('src') # Don't process files inside src if we are only targeting root HTMLs?
            # Wait, the prompt says "Move assets to src/assets, Keep HTML in root".
            # So we only need to update HTML files in the root.
            
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                updated_content = content
                for old, new in replacements.items():
                    updated_content = updated_content.replace(old, new)
                
                # Also need to handle url('...') in inline styles if any
                # e.g. style="background-image: url('./images/...')"
                # This is harder with simple replace.
                # Let's try simple replace for url('./images/ -> url('./src/assets/images/
                
                updated_content = updated_content.replace("url('./images/", "url('./src/assets/images/")
                updated_content = updated_content.replace('url("./images/', 'url("./src/assets/images/')
                updated_content = updated_content.replace("url('images/", "url('src/assets/images/")
                updated_content = updated_content.replace('url("images/', 'url("src/assets/images/')

                if content != updated_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    print(f"Updated {file}")

if __name__ == "__main__":
    update_html_paths(os.getcwd())
