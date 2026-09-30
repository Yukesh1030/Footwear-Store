import os
import re

files = ['ClientDashboard.html', 'ClientOrders.html', 'ClientWishlist.html', 'ClientMessages.html', 'ClientSettings.html']

for filename in files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Redirect buttons outside of sidebar
    # We want to add onclick="window.location.href='404.html'" to buttons.
    # Exclude buttons with id="mobileToggle", id="refreshOrders", id="chatSend", or inside sidebar.
    def button_replacer(m):
        full_match = m.group(0)
        # Check if it has an id that we shouldn't touch
        if 'id="mobileToggle"' in full_match or 'id="refreshOrders"' in full_match or 'id="chatSend"' in full_match:
            return full_match
        # Check if it's type="submit" because forms handle their own redirect
        if 'type="submit"' in full_match.lower():
            return full_match
        # Avoid already replaced
        if 'window.location.href' in full_match:
            return full_match
        
        # Insert onclick before the closing >
        return full_match[:-1] + ' onclick="window.location.href=\'404.html\'">'

    # We do a quick and dirty way to avoid sidebar by splitting the document
    if '<div class="sidebar"' in content:
        parts = content.split('</aside>')
        if len(parts) == 2:
            new_main = re.sub(r'<button\b[^>]*>', button_replacer, parts[1])
            content = parts[0] + '</aside>' + new_main
    else:
        content = re.sub(r'<button\b[^>]*>', button_replacer, content)

    # 2. Fix forms in ClientSettings.html
    if filename == 'ClientSettings.html':
        # Replace the Personal Information section to be a form
        old_personal = """<div class="form-grid">
                        <div class="form-group">
                            <label>Full Name</label>
                            <input type="text" class="form-control" value="Yukeshyuki18">
                        </div>
                        <div class="form-group">
                            <label>Email Address</label>
                            <input type="email" class="form-control" id="settingsEmailField" readonly>
                            <div class="setting-desc">Email cannot be changed directly for security reasons.</div>
                        </div>
                        <div class="form-group">
                            <label>Phone Number</label>
                            <input type="tel" class="form-control" placeholder="+91">
                        </div>
                    </div>
                    <div class="panel-footer"><button class="btn-primary" onclick="window.location.href='404.html'">Save Profile</button></div>"""
                    
        new_personal = """<form onsubmit="event.preventDefault(); if(this.checkValidity()) { window.location.href='404.html'; } else { this.reportValidity(); } return false;">
                        <div class="form-grid">
                            <div class="form-group">
                                <label>Full Name</label>
                                <input type="text" class="form-control" value="Yukeshyuki18" required>
                            </div>
                            <div class="form-group">
                                <label>Email Address</label>
                                <input type="email" class="form-control" id="settingsEmailField" readonly required>
                                <div class="setting-desc">Email cannot be changed directly for security reasons.</div>
                            </div>
                            <div class="form-group">
                                <label>Phone Number</label>
                                <input type="tel" class="form-control" placeholder="+91" required>
                            </div>
                        </div>
                        <div class="panel-footer"><button type="submit" class="btn-primary">Save Profile</button></div>
                    </form>"""
                    
        # Replace password section
        old_password = """<div class="form-group">
                            <label>Current Password</label>
                            <input type="password" class="form-control" placeholder="••••••••">
                        </div>
                        <div class="form-group">
                            <label>New Password</label>
                            <input type="password" class="form-control" placeholder="••••••••">
                        </div>
                        <button class="btn-primary" style="margin-bottom: 2rem;" onclick="window.location.href='404.html'">Update Password</button>"""
                        
        new_password = """<form onsubmit="event.preventDefault(); if(this.checkValidity()) { window.location.href='404.html'; } else { this.reportValidity(); } return false;" style="display:contents">
                        <div class="form-group">
                            <label>Current Password</label>
                            <input type="password" class="form-control" placeholder="••••••••" required>
                        </div>
                        <div class="form-group">
                            <label>New Password</label>
                            <input type="password" class="form-control" placeholder="••••••••" required>
                        </div>
                        <button type="submit" class="btn-primary" style="margin-bottom: 2rem; grid-column: 1 / -1;">Update Password</button>
                    </form>"""

        # We first run the naive replacements (since they might have been touched by button_replacer)
        # Then we'll do a more robust regex if exact string matching fails
        # Let's just use regex for password and personal info
        
        # Personal Info Regex
        content = re.sub(
            r'<div class="form-grid">\s*<div class="form-group">\s*<label>Full Name</label>.*?<div class="panel-footer"><button class="btn-primary"[^>]*>Save Profile</button></div>',
            new_personal,
            content,
            flags=re.DOTALL
        )
        
        # Password Regex
        content = re.sub(
            r'<div class="form-group">\s*<label>Current Password</label>.*?<button class="btn-primary"[^>]*>Update Password</button>',
            new_password,
            content,
            flags=re.DOTALL
        )
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filename}")
