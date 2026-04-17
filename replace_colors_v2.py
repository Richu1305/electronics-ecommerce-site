import os
import re

template_dir = r"c:\Users\richu\OneDrive\Desktop\Company\pythonproject\template"

# Colors to replace:
# #F5F5F7 (bg) -> #F8FAFC
# #1D1D1F (text/headers) -> #111827

replacements = [
    (re.compile(r'#F5F5F7', re.IGNORECASE), '#F8FAFC'),
    (re.compile(r'#1D1D1F', re.IGNORECASE), '#111827'),
    (re.compile(r'text-black bg-light', re.IGNORECASE), 'bg-dark'), # clean up any leftover classes
    (re.compile(r'text-black', re.IGNORECASE), 'text-white'), # clean up offcanvas headers
]

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for pattern, to_replace in replacements:
                new_content = pattern.sub(to_replace, new_content)
                
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
print("Done.")

