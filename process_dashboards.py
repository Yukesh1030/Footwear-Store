import os
import re

files_to_process = [
    'AdminDashboard.html', 'AdminProducts.html', 'AdminOrders.html', 'AdminCustomers.html', 'AdminSettings.html',
    'ClientDashboard.html', 'ClientOrders.html', 'ClientWishlist.html', 'ClientMessages.html', 'ClientSettings.html'
]

for filename in files_to_process:
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Replace non-sidebar links
    # To do this safely, we will find all <a> tags and check their class.
    # The sidebar links usually have class "menu-item" or "logout-btn".
    # The logo is usually inside <div class="sidebar-header"> or something similar, or it points to a dashboard html.
    
    def link_replacer(m):
        tag = m.group(0)
        # Check if it's a sidebar link
        if 'class="menu-item' in tag or 'class="logout-btn' in tag or 'assets/Brand-logo.webp' in tag or 'Brand-logo' in tag:
            return tag
        # Replace href with 404.html
        return re.sub(r'href=["\'].*?["\']', 'href="404.html"', tag)
        
    # We also need to skip the Brand-logo anchor, which usually wraps the logo image, but the regex above won't catch it unless we check the inner HTML, which is hard with simple regex.
    # Actually, we can just find <a ...> ... </a>
    def full_link_replacer(m):
        full_match = m.group(0)
        # If it's the brand logo, skip
        if 'Brand-logo' in full_match:
            return full_match
        # If it's a sidebar link, skip
        if 'menu-item' in full_match or 'logout-btn' in full_match:
            return full_match
        # Otherwise, replace href in the opening tag
        opening_tag = m.group(1)
        new_opening = re.sub(r'href=["\'].*?["\']', 'href="404.html"', opening_tag)
        return new_opening + m.group(2) + m.group(3)
        
    content = re.sub(r'(<a\b[^>]*>)(.*?)(</a>)', full_link_replacer, content, flags=re.IGNORECASE|re.DOTALL)

    # Step 2: Form validation
    if '<form' in content.lower():
        def form_replacer(m):
            tag = m.group(0)
            if 'onsubmit=' not in tag.lower():
                tag = tag[:-1] + ' onsubmit="event.preventDefault(); if(this.checkValidity()) { window.location.href=\'404.html\'; } else { this.reportValidity(); } return false;">'
            return tag
        content = re.sub(r'<form\b[^>]*>', form_replacer, content, flags=re.IGNORECASE)
        
        # Add required to inputs
        def input_replacer(m):
            tag = m.group(0).lower()
            if 'type="hidden"' in tag or 'type="submit"' in tag or 'type="button"' in tag or 'type="radio"' in tag or 'type="checkbox"' in tag:
                return m.group(0)
            if 'required' not in tag:
                # Insert required before closing bracket
                orig_tag = m.group(0)
                if orig_tag.endswith('/>'):
                    return orig_tag[:-2] + ' required/>'
                else:
                    return orig_tag[:-1] + ' required>'
            return m.group(0)
            
        content = re.sub(r'<input\b[^>]*>', input_replacer, content, flags=re.IGNORECASE)
        content = re.sub(r'<select\b[^>]*>', input_replacer, content, flags=re.IGNORECASE)
        content = re.sub(r'<textarea\b[^>]*>', input_replacer, content, flags=re.IGNORECASE)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filename}")
