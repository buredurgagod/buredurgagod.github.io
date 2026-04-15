with open('unsure_files.txt', 'r') as f:
    lines = [l.strip() for l in f if l.strip()]

content = """# Unused Files Review

The following files do not appear to be linked or accessed directly via any HTML templates, CSS or scripts in your project. Please review them and let me know if it's safe to mass-delete them, or if you'd like to retain specific ones.

## Potential Unused Favicons (5 files)
These might be dynamically needed by browsers or the manifest.json file differently:
"""
favicons = [l for l in lines if 'favicon' in l]
for f in favicons:
    content += f"- `{f}`\n"

content += "\n## Other Unreferenced Images (153 files)\n"
content += "These images seem entirely unused in the codebase (for example they may refer to an older hero element or alternate image format that is currently not being accessed). Here are the files:\n\n"
content += "```text\n"
images = [l for l in lines if 'images' in l and 'favicon' not in l]
for i in images:
    content += i + "\n"
content += "```\n"

with open('unused_files_review.md', 'w') as f:
    f.write(content)

