#!/usr/bin/env python3
"""
Fix blog post navigation menu and clean up redundant whitespace.
- Adds Blog link to navigation
- Adds mobile hamburger menu
- Removes empty divs and unnecessary line breaks from content
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

BASE_DIR = Path(__file__).parent.parent
POSTS_DIR = BASE_DIR / "post"


def clean_whitespace_in_content(content_div):
    """Remove redundant whitespace from blog content."""
    if not content_div:
        return
    
    original_html = str(content_div)
    
    # Remove empty divs that only contain other empty divs or line breaks
    def is_empty_or_whitespace_only(tag):
        """Check if a tag is empty or only contains whitespace/empty elements."""
        if not hasattr(tag, 'name') or tag.name is None:
            return False
        
        if tag.name not in ['div', 'span']:
            return False
        
        # Get all text content
        text_content = tag.get_text(strip=True)
        if text_content:
            return False
        
        # Check children
        children = list(tag.children)
        if not children:
            return True
        
        # Check if all children are empty/whitespace
        for child in children:
            if isinstance(child, NavigableString):
                if child.strip():
                    return False
            elif hasattr(child, 'name') and child.name:
                if child.name == 'br':
                    continue  # br tags are ok in empty divs
                elif child.name in ['div', 'span']:
                    if not is_empty_or_whitespace_only(child):
                        return False
                else:
                    # Has non-empty, non-whitespace element
                    return False
        
        return True
    
    # Remove empty divs and spans iteratively
    changed = True
    iterations = 0
    max_iterations = 15
    
    while changed and iterations < max_iterations:
        changed = False
        iterations += 1
        
        # Find all divs and spans, process in reverse order
        all_tags = content_div.find_all(['div', 'span'], recursive=True)
        for tag in reversed(all_tags):
            # Skip if tag has been removed
            if not tag.parent:
                continue
                
            if is_empty_or_whitespace_only(tag):
                tag.decompose()
                changed = True
    
    # Remove spans that only contain <br/> tags
    for span in content_div.find_all('span', recursive=True):
        children = list(span.children)
        # If span only has br tags or whitespace
        if len([c for c in children if hasattr(c, 'name') and c.name == 'br']) > 0:
            # Check if span has any actual content
            if not span.get_text(strip=True):
                span.decompose()
    
    # Remove unnecessary consecutive br tags (keep max 2)
    br_count = 0
    for element in content_div.descendants:
        if hasattr(element, 'name') and element.name == 'br':
            br_count += 1
            if br_count > 2:
                # Find previous br siblings
                prev_siblings = []
                sibling = element.previous_sibling
                count = 0
                while sibling and count < 5:
                    if hasattr(sibling, 'name') and sibling.name == 'br':
                        prev_siblings.append(sibling)
                        count += 1
                    sibling = sibling.previous_sibling if hasattr(sibling, 'previous_sibling') else None
                
                # If we have more than 2 consecutive brs, remove this one
                if len(prev_siblings) >= 1:
                    element.decompose()
                    br_count = 0
        elif hasattr(element, 'name') and element.name and element.name not in ['br', 'span']:
            # Reset count when we hit a real element
            br_count = 0


def add_blog_link_to_menu(nav_links_ul, soup, relative_path):
    """Add Blog link to navigation menu if it doesn't exist."""
    blog_path = f"{relative_path}blog/"
    
    # Check if Blog link already exists
    existing_blog = nav_links_ul.find('a', href=re.compile(r'blog'))
    if existing_blog:
        return False
    
    # Find the Shipments link or Contact link to insert before
    insert_after = None
    for link in nav_links_ul.find_all('a'):
        href = link.get('href', '')
        if 'shipments' in href.lower() or 'contact' in href.lower():
            insert_after = link.find_parent('li')
            break
    
    # Create Blog link
    blog_li = soup.new_tag('li')
    blog_a = soup.new_tag('a', href=blog_path)
    blog_a.string = 'Blog'
    blog_li.append(blog_a)
    
    if insert_after:
        insert_after.insert_after(blog_li)
    else:
        # Append at the end if no insertion point found
        nav_links_ul.append(blog_li)
    
    return True


def add_mobile_menu(soup, relative_path):
    """Add mobile hamburger menu to blog post."""
    nav = soup.find('nav')
    if not nav:
        return False
    
    # Check if mobile menu already exists (check both class and class_)
    if soup.find('button', class_='mobile-menu-toggle') or soup.find('button', {'class': 'mobile-menu-toggle'}):
        # Clean up duplicates
        buttons = soup.find_all('button', class_='mobile-menu-toggle')
        if len(buttons) > 1:
            for btn in buttons[1:]:
                btn.decompose()
        return False
    
    # Find the nav-links ul (without mobile-menu class)
    nav_links = nav.find('ul', class_='nav-links')
    if not nav_links or 'mobile-menu' in nav_links.get('class', []):
        return False
    
    # Check if mobile menu ul already exists
    existing_mobile_menu = nav.find('ul', class_='mobile-menu')
    if existing_mobile_menu:
        return False
    
    # Create mobile menu button
    menu_button = soup.new_tag('button')
    menu_button['class'] = 'mobile-menu-toggle'
    menu_button['aria-expanded'] = 'false'
    menu_button['aria-label'] = 'Toggle navigation menu'
    
    for i in range(3):
        span = soup.new_tag('span')
        span['class'] = 'hamburger-line'
        menu_button.append(span)
    
    # Insert button before nav-links
    nav_links.insert_before(menu_button)
    
    # Create mobile menu (clone of nav-links)
    mobile_menu = soup.new_tag('ul')
    mobile_menu['class'] = 'nav-links mobile-menu'
    
    # Clone all list items
    for li in nav_links.find_all('li', recursive=False):
        li_clone = BeautifulSoup(str(li), 'html.parser').li
        mobile_menu.append(li_clone)
    
    # Insert mobile menu after nav-links
    nav_links.insert_after(mobile_menu)
    
    # Check if overlay already exists
    existing_overlay = soup.find('div', class_='mobile-menu-overlay')
    if not existing_overlay:
        # Create overlay
        overlay = soup.new_tag('div')
        overlay['class'] = 'mobile-menu-overlay'
        body = soup.find('body')
        if body:
            body.append(overlay)
    
    return True


def add_mobile_menu_styles(soup):
    """Add CSS for mobile menu and improve spacing."""
    style_tag = soup.find('style')
    if not style_tag:
        return False
    
    style_content = style_tag.string or ""
    
    # Check if mobile menu styles already exist
    if 'mobile-menu-toggle' in style_content:
        # Check if spacing fix is already added
        if '.blog-content > div' in style_content:
            return False
        # Add spacing fix to existing styles
        spacing_css = """
        
        /* Reduce spacing between headers and paragraphs */
        .blog-content > div {
            margin-bottom: 0.5rem;
        }
        
        .blog-content > div > h1,
        .blog-content > div > h2,
        .blog-content > div > h3,
        .blog-content > div > h4,
        .blog-content > div > h5,
        .blog-content > div > h6 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
        }
        
        .blog-content > div > p {
            margin-top: 0;
            margin-bottom: 1rem;
        }
        
        .blog-content > div > p:first-child {
            margin-top: 0;
        }
        """
        style_tag.string += spacing_css
        return True
    
    mobile_menu_css = """
        
        /* Mobile Menu Toggle */
        .mobile-menu-toggle {
            display: none;
            flex-direction: column;
            gap: 4px;
            background: none;
            border: none;
            cursor: pointer;
            padding: 0.5rem;
            z-index: 1001;
        }
        
        .hamburger-line {
            width: 25px;
            height: 3px;
            background-color: var(--color-text);
            transition: all 0.3s ease;
        }
        
        /* Reduce spacing between headers and paragraphs */
        .blog-content > div {
            margin-bottom: 0.5rem;
        }
        
        .blog-content > div > h1,
        .blog-content > div > h2,
        .blog-content > div > h3,
        .blog-content > div > h4,
        .blog-content > div > h5,
        .blog-content > div > h6 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
        }
        
        .blog-content > div > p {
            margin-top: 0;
            margin-bottom: 1rem;
        }
        
        .blog-content > div > p:first-child {
            margin-top: 0;
        }
        
        @media (max-width: 768px) {
            .mobile-menu-toggle {
                display: flex;
            }
            
            body {
                overflow-x: hidden;
            }
            
            .nav-links:not(.mobile-menu) {
                display: none !important;
            }
            
            .nav-links.mobile-menu {
                position: fixed;
                top: 0;
                right: -100%;
                height: 100vh;
                width: 80%;
                max-width: 300px;
                background-color: var(--color-bg);
                flex-direction: column;
                align-items: flex-start;
                padding: 5rem 2rem 2rem;
                box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
                transition: right 0.3s ease;
                z-index: 1000;
                gap: 1.5rem;
                overflow-y: auto;
                margin: 0;
                list-style: none;
            }
            
            .nav-links.mobile-menu.active {
                right: 0;
            }
            
            .nav-links.mobile-menu li {
                width: 100%;
                border-bottom: 1px solid var(--color-bg-light);
                padding-bottom: 1rem;
            }
            
            .nav-links.mobile-menu a {
                font-size: 1.1rem;
                width: 100%;
                display: block;
            }
            
            .mobile-menu-overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 999;
            }
            
            .mobile-menu-overlay.active {
                display: block;
            }
            
            header {
                padding: 1rem 1.5rem;
            }
            
            .logo img {
                height: 48px;
            }
            
            nav {
                position: relative;
            }
        }
        
        @media (max-width: 480px) {
            header {
                padding: 0.75rem 1rem;
            }
            
            .logo img {
                height: 40px;
            }
        }
    """
    
    style_tag.string += mobile_menu_css
    return True


def add_mobile_menu_script(soup):
    """Add JavaScript for mobile menu functionality."""
    # Check if script already exists
    if soup.find('script', string=re.compile('mobile-menu-toggle')):
        return False
    
    script_content = """
    document.addEventListener('DOMContentLoaded', function() {
        const menuToggle = document.querySelector('.mobile-menu-toggle');
        const mobileMenu = document.querySelector('.mobile-menu');
        const overlay = document.querySelector('.mobile-menu-overlay');
        
        if (menuToggle && mobileMenu) {
            menuToggle.addEventListener('click', function() {
                const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
                
                menuToggle.setAttribute('aria-expanded', !isExpanded);
                mobileMenu.classList.toggle('active');
                
                if (overlay) {
                    overlay.classList.toggle('active');
                }
                
                // Prevent body scroll when menu is open
                if (!isExpanded) {
                    document.body.style.overflow = 'hidden';
                } else {
                    document.body.style.overflow = '';
                }
            });
            
            // Close menu when clicking overlay
            if (overlay) {
                overlay.addEventListener('click', function() {
                    menuToggle.setAttribute('aria-expanded', 'false');
                    mobileMenu.classList.remove('active');
                    overlay.classList.remove('active');
                    document.body.style.overflow = '';
                });
            }
            
            // Close menu when clicking a link
            const menuLinks = mobileMenu.querySelectorAll('a');
            menuLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    menuToggle.setAttribute('aria-expanded', 'false');
                    mobileMenu.classList.remove('active');
                    if (overlay) {
                        overlay.classList.remove('active');
                    }
                    document.body.style.overflow = '';
                });
            });
            
            // Close menu on window resize if it becomes desktop view
            window.addEventListener('resize', function() {
                if (window.innerWidth > 768) {
                    menuToggle.setAttribute('aria-expanded', 'false');
                    mobileMenu.classList.remove('active');
                    if (overlay) {
                        overlay.classList.remove('active');
                    }
                    document.body.style.overflow = '';
                }
            });
        }
    });
    """
    
    script_tag = soup.new_tag('script')
    script_tag.string = script_content
    body = soup.find('body')
    if body:
        body.append(script_tag)
    
    return True


def fix_blog_post(post_path):
    """Fix a single blog post file."""
    print(f"\nProcessing: {post_path.name}")
    
    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return False
    
    # Calculate relative path to root
    depth = len(post_path.parent.relative_to(BASE_DIR).parts)
    relative_path = "../" * depth if depth > 0 else ""
    
    # Fix navigation menu
    nav_links = soup.find('ul', class_='nav-links')
    menu_updated = False
    if nav_links:
        # Add Blog link
        if add_blog_link_to_menu(nav_links, soup, relative_path):
            print("  ✅ Added Blog link to navigation")
            menu_updated = True
        
        # Add mobile menu
        if add_mobile_menu(soup, relative_path):
            print("  ✅ Added mobile hamburger menu")
            menu_updated = True
            
            # Add mobile menu styles
            if add_mobile_menu_styles(soup):
                print("  ✅ Added mobile menu styles")
            
            # Add mobile menu script
            if add_mobile_menu_script(soup):
                print("  ✅ Added mobile menu JavaScript")
    
    # Clean up whitespace in content
    blog_content = soup.find('div', class_='blog-content')
    if blog_content:
        before_html_length = len(str(blog_content))
        before_text_length = len(blog_content.get_text(strip=True))
        
        clean_whitespace_in_content(blog_content)
        
        after_html_length = len(str(blog_content))
        after_text_length = len(blog_content.get_text(strip=True))
        
        # Check if we reduced HTML size (removed empty elements)
        if before_html_length != after_html_length:
            reduction = before_html_length - after_html_length
            print(f"  ✅ Cleaned up whitespace (HTML size: {before_html_length} → {after_html_length}, reduced by {reduction} chars)")
            menu_updated = True
        elif before_text_length != after_text_length:
            print(f"  ✅ Cleaned up whitespace (text length: {before_text_length} → {after_text_length})")
            menu_updated = True
    
    # Save if changes were made
    if menu_updated:
        try:
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"  ✅ Saved changes")
            return True
        except Exception as e:
            print(f"  ❌ Error saving file: {e}")
            return False
    
    return False


def main():
    """Main function to fix all blog posts."""
    if not POSTS_DIR.exists():
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    print("=" * 60)
    print("Fixing blog post menus and whitespace")
    print("=" * 60)
    
    post_dirs = [d for d in POSTS_DIR.iterdir() if d.is_dir()]
    print(f"\nFound {len(post_dirs)} blog posts")
    
    fixed_count = 0
    for post_dir in sorted(post_dirs):
        post_file = post_dir / "index.html"
        if post_file.exists():
            if fix_blog_post(post_file):
                fixed_count += 1
        else:
            print(f"\n⚠️  No index.html found in {post_dir.name}")
    
    print(f"\n{'=' * 60}")
    print(f"✅ Fixed {fixed_count} blog posts")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()

