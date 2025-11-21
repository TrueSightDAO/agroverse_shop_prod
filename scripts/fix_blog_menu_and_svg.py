#!/usr/bin/env python3
"""
Fix duplicate menu display and remove empty SVG elements in blog posts.
"""

from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent.parent
POSTS_DIR = BASE_DIR / "post"


def is_empty_svg(svg_tag):
    """Check if an SVG tag is empty or only contains empty elements."""
    if not svg_tag or svg_tag.name != 'svg':
        return False
    
    # Get all children
    children = list(svg_tag.children)
    
    # If no children, it's empty
    if not children:
        return True
    
    # Check if all children are empty (whitespace, empty paths, etc.)
    for child in children:
        if isinstance(child, str):
            if child.strip():
                return False
        elif hasattr(child, 'name'):
            if child.name == 'path':
                # Check if path has no d attribute or empty d
                d_attr = child.get('d', '')
                if d_attr and d_attr.strip():
                    return False
            elif child.name in ['g', 'circle', 'rect', 'line', 'polyline', 'polygon']:
                # These could have content, but if they're empty, continue
                if child.get_text(strip=True):
                    return False
            else:
                # Other elements might have content
                if child.get_text(strip=True):
                    return False
    
    return True


def fix_blog_post(post_path):
    """Fix menu display and remove empty SVGs."""
    print(f"\nProcessing: {post_path.name}")
    
    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return False
    
    changes_made = False
    
    # Fix 1: Remove duplicate menus (keep only one desktop and one mobile)
    nav = soup.find('nav')
    if nav:
        nav_links_list = nav.find_all('ul', class_='nav-links')
        
        desktop_menus = [m for m in nav_links_list if 'mobile-menu' not in m.get('class', [])]
        mobile_menus = [m for m in nav_links_list if 'mobile-menu' in m.get('class', [])]
        
        # Keep only one desktop menu
        if len(desktop_menus) > 1:
            for menu in desktop_menus[1:]:
                menu.decompose()
                changes_made = True
                print(f"  ✅ Removed duplicate desktop menu")
        
        # Keep only one mobile menu
        if len(mobile_menus) > 1:
            for menu in mobile_menus[1:]:
                menu.decompose()
                changes_made = True
                print(f"  ✅ Removed duplicate mobile menu")
        
        # Ensure proper classes on remaining menus
        nav_links_list = nav.find_all('ul', class_='nav-links')
        for menu in nav_links_list:
            classes = menu.get('class', [])
            if 'mobile-menu' in classes:
                # This is the mobile menu - should be hidden on desktop
                if 'nav-links' not in classes:
                    classes.insert(0, 'nav-links')
            else:
                # This is the desktop menu - should be visible on desktop
                if 'mobile-menu' in classes:
                    classes.remove('mobile-menu')
            menu['class'] = classes
    
    # Fix 2: Remove empty SVG elements
    svg_count = 0
    all_svgs = soup.find_all('svg')
    for svg in all_svgs:
        if is_empty_svg(svg):
            svg.decompose()
            svg_count += 1
            changes_made = True
    
    if svg_count > 0:
        print(f"  ✅ Removed {svg_count} empty SVG element(s)")
    
    # Fix 3: Ensure CSS properly hides mobile menu on desktop and desktop menu on mobile
    style_tag = soup.find('style')
    if style_tag:
        style_content = style_tag.string or ""
        
        # Check if we need to add/update the CSS rules
        needs_update = False
        
        # Check if mobile menu hide rule exists
        if '.nav-links.mobile-menu' not in style_content or ('display: none' not in style_content and 'display:none' not in style_content):
            needs_update = True
        
        if needs_update:
            # Find insertion point (before mobile menu toggle styles or media query)
            insertion_point = None
            if '/* Mobile Menu Toggle */' in style_content:
                insertion_point = style_content.find('/* Mobile Menu Toggle */')
            elif '@media (max-width: 768px)' in style_content:
                insertion_point = style_content.find('@media (max-width: 768px)')
            elif '.mobile-menu-toggle' in style_content:
                insertion_point = style_content.find('.mobile-menu-toggle')
            
            if insertion_point:
                # Insert CSS rules
                insertion = """
        
        /* Hide mobile menu on desktop, show desktop menu */
        .nav-links.mobile-menu {
            display: none;
        }
        
        .nav-links:not(.mobile-menu) {
            display: flex;
        }
        
        """
                style_tag.string = style_content[:insertion_point] + insertion + style_content[insertion_point:]
                changes_made = True
                print(f"  ✅ Added CSS to properly show/hide menus")
    
    # Save if changes were made
    if changes_made:
        try:
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"  ✅ Saved changes")
            return True
        except Exception as e:
            print(f"  ❌ Error saving: {e}")
            return False
    
    print(f"  ℹ️  No changes needed")
    return False


def main():
    """Main function."""
    print("=" * 60)
    print("Fixing duplicate menus and empty SVGs in blog posts")
    print("=" * 60)
    
    post_dirs = [d for d in POSTS_DIR.iterdir() if d.is_dir()]
    
    fixed_count = 0
    for post_dir in sorted(post_dirs):
        post_file = post_dir / "index.html"
        if post_file.exists():
            if fix_blog_post(post_file):
                fixed_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ Fixed {fixed_count} blog posts")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()

