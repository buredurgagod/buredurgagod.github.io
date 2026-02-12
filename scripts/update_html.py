import os
import re

def update_html_files(directory, images_dir):
    # Get list of available webp images
    webp_images = set()
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.endswith(".webp"):
                # Store relative path from images_dir
                rel_path = os.path.relpath(os.path.join(root, file), images_dir)
                webp_images.add(rel_path)

    print(f"Found {len(webp_images)} WebP images.")

    # Regex for img tags
    img_tag_pattern = re.compile(r'<img\s+([^>]*)src=["\']([^"\']+)["\']([^>]*)>', re.IGNORECASE)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                updated_content = content
                
                def replace_image(match):
                    attrs_before = match.group(1)
                    src = match.group(2)
                    attrs_after = match.group(3)

                    # Check if src is in images/
                    if "images/" in src:
                        # Extract part after images/
                        image_rel_path = src.split("images/", 1)[1]
                        # Check if webp exists
                        webp_rel_path = os.path.splitext(image_rel_path)[0] + ".webp"
                        
                        # We need to handle URL encoding if necessary, but simple check first
                        # Also handle if image is in subdirectory of images/
                        # The set webp_images contains paths relative to images_dir
                        
                        # Simple cleanup for matching
                        check_path = webp_rel_path.replace("%20", " ")

                        if check_path in webp_images:
                            new_src = src.rsplit(".", 1)[0] + ".webp"
                            
                            # Add loading="lazy" if not present
                            full_tag = f'<img {attrs_before}src="{new_src}"{attrs_after}>'
                            if "loading=" not in full_tag:
                                full_tag = full_tag.replace("<img ", '<img loading="lazy" ')
                            
                            return full_tag
                    
                    # If not replacing image, still check for lazy loading?
                    # Plan says "Add loading=lazy to off-screen images".
                    # For simplicity, adding to all images except maybe explicit header/hero if identified. 
                    # But safest provides significant gain is adding to all or most.
                    # Let's add lazy loading even if not converting to webp, as per task.md
                    
                    full_tag = match.group(0)
                    if "loading=" not in full_tag:
                         return full_tag.replace("<img ", '<img loading="lazy" ')
                    
                    return full_tag

                updated_content = img_tag_pattern.sub(replace_image, content)

                if content != updated_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    print(f"Updated {file}")

if __name__ == "__main__":
    base_dir = os.getcwd()
    images_dir = os.path.join(base_dir, "images")
    update_html_files(base_dir, images_dir)
