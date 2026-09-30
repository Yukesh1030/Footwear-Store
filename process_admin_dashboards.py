import os
import re

files = ['AdminDashboard.html', 'AdminProducts.html', 'AdminOrders.html', 'AdminCustomers.html', 'AdminSettings.html']

for filename in files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add redirect to buttons outside of sidebar
    def button_replacer(m):
        full_match = m.group(0)
        # Check if it has an id that we shouldn't touch
        if 'id="' in full_match:
            return full_match
        # Check if it's type="submit" because forms handle their own redirect
        if 'type="submit"' in full_match.lower():
            return full_match
        # Avoid already replaced
        if 'window.location.href' in full_match:
            return full_match
        
        # Insert onclick before the closing >
        return full_match[:-1] + ' onclick="window.location.href=\'404.html\'">'

    if '<div class="sidebar"' in content:
        parts = content.split('</aside>')
        if len(parts) == 2:
            new_main = re.sub(r'<button\b[^>]*>', button_replacer, parts[1])
            content = parts[0] + '</aside>' + new_main
    else:
        content = re.sub(r'<button\b[^>]*>', button_replacer, content)

    # 2. Convert pseudo-forms into real forms
    # We will look for <div class="form-grid"> ... </div> \n <div class="panel-footer"><button ...>
    # Actually, in AdminProducts.html, it's <div style="padding: 0 2rem 1.5rem;">
    # Let's write a custom block replacer for each specific file where pseudo-forms exist.

    if filename == 'AdminProducts.html':
        # Add Product pseudo-form
        def add_product_form(m):
            block = m.group(0)
            # add required to inputs and selects
            block = re.sub(r'<input\b[^>]*>', lambda x: x.group(0)[:-1] + ' required>' if 'required' not in x.group(0) else x.group(0), block)
            block = re.sub(r'<select\b[^>]*>', lambda x: x.group(0)[:-1] + ' required>' if 'required' not in x.group(0) else x.group(0), block)
            # change button to type="submit" and remove onclick if any
            block = re.sub(r'<button class="btn-primary"[^>]*>', '<button type="submit" class="btn-primary">', block)
            
            return '<form onsubmit="event.preventDefault(); if(this.checkValidity()) { window.location.href=\'404.html\'; } else { this.reportValidity(); } return false;">\n' + block + '\n</form>'
            
        content = re.sub(r'<div class="form-grid">.*?<button class="btn-primary"[^>]*>Add Product</button>\s*</div>', add_product_form, content, flags=re.DOTALL)

    if filename == 'AdminSettings.html':
        def settings_form(m):
            block = m.group(0)
            # add required
            block = re.sub(r'<input\b(?!.*type="checkbox")[^>]*>', lambda x: x.group(0)[:-1] + ' required>' if 'required' not in x.group(0) else x.group(0), block)
            block = re.sub(r'<select\b[^>]*>', lambda x: x.group(0)[:-1] + ' required>' if 'required' not in x.group(0) else x.group(0), block)
            # button
            block = re.sub(r'<button class="btn-primary"[^>]*>', lambda x: '<button type="submit" class="btn-primary">' if 'onclick' in x.group(0) else x.group(0).replace('class=', 'type="submit" class='), block)
            return '<form onsubmit="event.preventDefault(); if(this.checkValidity()) { window.location.href=\'404.html\'; } else { this.reportValidity(); } return false;">\n' + block + '\n</form>'
            
        # We need to wrap each panel that has a form-grid and a button
        content = re.sub(r'<div class="form-grid">.*?<button class="btn-primary"[^>]*>.*?</button>\s*</div>', settings_form, content, flags=re.DOTALL)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filename}")
