#!/usr/bin/env python3
"""
Fix jQuery UI CSS file paths by removing encoded quotes from URLs
"""

import os
import re

def fix_jquery_ui_css():
    css_file = "static/jquery-ui/jquery-ui.css"
    
    if not os.path.exists(css_file):
        print(f"❌ CSS file not found: {css_file}")
        return False
    
    print(f"🔧 Fixing jQuery UI CSS file: {css_file}")
    
    # Read the file
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count problematic URLs before fixing (including in comments)
    # Look for patterns like %22images%2Fui-icons_*.png%22
    encoded_pattern = r'%22images%2F[^%]+\.png%22'
    problematic_urls = len(re.findall(encoded_pattern, content))
    print(f"Found {problematic_urls} encoded image URLs")
    
    # Also look for the exact patterns from the error
    quote_pattern = r'"images/ui-icons_[^"]+\.png"'
    quoted_urls = len(re.findall(quote_pattern, content))
    print(f"Found {quoted_urls} properly quoted image URLs")
    
    if problematic_urls == 0:
        print("✅ No problematic encoded URLs found")
        if quoted_urls > 0:
            print("✅ File has properly formatted URLs")
        return True
    
    print("🔧 Fixing encoded URLs in comments and CSS...")
    
    # Fix the comment line first (line 4) - remove the entire problematic parameter section
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'iconsHover=url(%22images%2F' in line:
            print(f"Fixing line {i+1} with encoded URLs")
            # Remove all the icon parameters from the theme URL
            line = re.sub(r'&icons[^&]*=url\(%22images%2F[^&]*', '', line)
            lines[i] = line
            break
    
    content = '\n'.join(lines)
    
    # Fix any remaining encoded URLs in CSS rules
    content = re.sub(r'url\(%22([^%]+)%22\)', r'url("\1")', content)
    content = content.replace('%2F', '/')
    
    # Verify the fixes
    remaining_problems = len(re.findall(encoded_pattern, content))
    if remaining_problems > 0:
        print(f"⚠️  Still found {remaining_problems} problematic URLs after fixing")
        return False
    
    # Write the fixed content back
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {problematic_urls} URLs in {css_file}")
    return True

if __name__ == "__main__":
    success = fix_jquery_ui_css()
    if not success:
        exit(1)
    print("🎉 jQuery UI CSS file has been fixed!")
