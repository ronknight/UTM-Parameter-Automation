import re

# Define UTM parameters
utm_source = "webjaguar"
utm_medium = "website"
utm_campaign = "character-navigation"

# Load HTML file
with open("masonry 110624 v3.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Function to add UTM parameters to a URL if they are not already present
def add_utm_params(url, content_name):
    # Check if the URL already has UTM parameters to avoid duplication
    if "utm_source=" in url or "utm_medium=" in url or "utm_campaign=" in url or "utm_content=" in url:
        return url  # Return original URL if UTM parameters already exist
    
    # Define UTM parameters with dynamic content name
    utm_content = f"{content_name}-link"
    # Add UTM parameters to URL
    if "?" in url:
        return f"{url}&utm_source={utm_source}&utm_medium={utm_medium}&utm_campaign={utm_campaign}&utm_content={utm_content}"
    else:
        return f"{url}?utm_source={utm_source}&utm_medium={utm_medium}&utm_campaign={utm_campaign}&utm_content={utm_content}"

# Single comprehensive pattern to match all link types
pattern = r'(<a[^>]*href=["\'])([^"\']+)(["\'][^>]*>)\s*(?:<span[^>]*class=["\']tag\s+([^"\']+)["\'][^>]*>([^<]+)</span>)\s*(</a>)'

def process_links(html_content):
    def replace_link(match):
        start_tag = match.group(1)
        url = match.group(2)
        end_tag = match.group(3)
        tag_class = match.group(4)
        original_text = match.group(5)  # The text inside the span
        closing_tag = match.group(6)
        
        # Use lowercase version for UTM parameters only
        content_name = tag_class.lower() if tag_class else original_text.lower().replace(' ', '-')
        
        # Add UTM parameters to the URL
        new_url = add_utm_params(url, content_name)
        
        # Reconstruct the link with original capitalization preserved
        return f'{start_tag}{new_url}{end_tag}<span class="tag {tag_class}">{original_text}</span>{closing_tag}'

    # Process all links in a single pass
    return re.sub(pattern, replace_link, html_content)

# Process the HTML content and update links with UTM parameters
updated_html = process_links(html_content)

# Write the updated HTML to a new file
with open("masonry_with_utm.html", "w", encoding="utf-8") as file:
    file.write(updated_html)

print("UTM parameters have been added to all character links, preserving original text capitalization.")

# Test pattern with a sample link to verify
test_html = """<a href="https://www.4sgm.com/lsearch.jhtm?cid=&noKeywords=true&keywords=&minPrice=&maxPrice=&facetNameValue=Licensed+Characters_value_Disney"> <span class="tag disney">Disney</span> </a>"""
result = process_links(test_html)
print("\nTest result:")
print(result)