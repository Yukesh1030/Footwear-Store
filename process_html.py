import os
import re

files_to_process = ['index.html', 'Shop.html', 'Collections.html', 'About.html', 'Contact.html']

for filename in files_to_process:
    if not os.path.exists(filename):
        print(f"Skipping {filename}, not found.")
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Replace links outside <nav> and <footer>
    # We can split the text into chunks: nav, footer, and other.
    # To do this safely, we find all indices of <nav>, </nav>, <footer>, </footer>
    
    parts = []
    current_pos = 0
    
    # We will use re.finditer to find all <nav, </nav>, <footer, </footer>
    tags = list(re.finditer(r'<(/?nav|/?footer)\b[^>]*>', content, flags=re.IGNORECASE))
    
    inside_nav = False
    inside_footer = False
    
    new_content = ""
    
    for match in tags:
        start, end = match.span()
        tag_text = match.group(0).lower()
        
        # Text before the tag
        chunk = content[current_pos:start]
        
        # Process the chunk if we are NOT inside nav and NOT inside footer
        if not inside_nav and not inside_footer:
            # Replace hrefs in <a> tags
            # Regex to find <a ... href="something" ...>
            # We want to replace the href value with 404.html
            chunk = re.sub(r'(<a\b[^>]*href=["\'])(.*?)(["\'])', lambda m: m.group(1) + "404.html" + m.group(3) if not m.group(2).startswith('#') and not m.group(2).startswith('javascript:') else m.group(0), chunk, flags=re.IGNORECASE)
            
        new_content += chunk
        new_content += match.group(0) # add the tag itself
        
        if '<nav' in tag_text: inside_nav = True
        elif '</nav' in tag_text: inside_nav = False
        elif '<footer' in tag_text: inside_footer = True
        elif '</footer' in tag_text: inside_footer = False
        
        current_pos = end

    # Process the remaining content
    chunk = content[current_pos:]
    if not inside_nav and not inside_footer:
        chunk = re.sub(r'(<a\b[^>]*href=["\'])(.*?)(["\'])', lambda m: m.group(1) + "404.html" + m.group(3) if not m.group(2).startswith('#') and not m.group(2).startswith('javascript:') else m.group(0), chunk, flags=re.IGNORECASE)
    new_content += chunk

    # Step 2: Form validation
    # If there is a form, we add an id to it if it doesn't have one, and append a script.
    if '<form' in new_content.lower():
        # Let's just add an onsubmit inline attribute to all forms.
        # onsubmit="event.preventDefault(); if(this.checkValidity()) { window.location.href='404.html'; } else { alert('Please fill all required fields correctly.'); } return false;"
        
        def form_replacer(m):
            tag = m.group(0)
            if 'onsubmit=' not in tag.lower():
                # insert onsubmit before the closing >
                tag = tag[:-1] + ' onsubmit="event.preventDefault(); if(this.checkValidity()) { window.location.href=\'404.html\'; } else { this.reportValidity(); } return false;">'
            return tag
            
        new_content = re.sub(r'<form\b[^>]*>', form_replacer, new_content, flags=re.IGNORECASE)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Processed {filename}")
