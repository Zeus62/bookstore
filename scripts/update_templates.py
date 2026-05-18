import json
import re
import os

# Load en.json
with open('Book_Store/static/i18n/en.json', 'r', encoding='utf-8') as f:
    en_dict = json.load(f)

# Flatten dictionary
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

flat_en = flatten_dict(en_dict)

def replace_i18n(html_content):
    # 1. Replace <tag ... data-i18n="key">Text</tag>
    # Note: text between tags can be anything, but usually they just wrap the text.
    # We can replace the text content of the tag.
    def repl_inner(m):
        full_tag = m.group(1)
        key = m.group(2)
        rest_tag = m.group(3)
        old_text = m.group(4)
        close_tag = m.group(5)
        
        if key in flat_en:
            # remove data-i18n attribute and replace inner text
            # We want to keep the inner formatting if there are html tags inside? 
            # In our case it's usually just text.
            new_text = f"{{{{ _('{flat_en[key]}') }}}}"
            return f"{full_tag}{rest_tag}{new_text}{close_tag}"
        return m.group(0)

    html_content = re.sub(r'(<[^>]*?)\s*data-i18n="([^"]+)"([^>]*>)(.*?)(</[^>]+>)', repl_inner, html_content, flags=re.DOTALL)
    
    # 2. Replace data-i18n="key" in self-closing tags like <input ... data-i18n="key" value="old">
    def repl_value(m):
        before = m.group(1)
        key = m.group(2)
        after = m.group(3)
        
        if key in flat_en:
            # We also need to replace the value="old" attribute
            val_pattern = r'value="[^"]*"'
            new_after = re.sub(val_pattern, f'value="{{{{ _(\'{flat_en[key]}\') }}}}"', after)
            new_before = re.sub(val_pattern, f'value="{{{{ _(\'{flat_en[key]}\') }}}}"', before)
            if new_after != after or new_before != before:
                # We replaced value, so just drop data-i18n
                return f"{new_before}{new_after}"
        return m.group(0)
    
    html_content = re.sub(r'(<input[^>]*?)\s*data-i18n="([^"]+)"([^>]*>)', repl_value, html_content)
    
    # 3. Replace data-i18n-placeholder="key" placeholder="old"
    def repl_placeholder(m):
        before = m.group(1)
        key = m.group(2)
        after = m.group(3)
        if key in flat_en:
            ph_pattern = r'placeholder="[^"]*"'
            new_after = re.sub(ph_pattern, f'placeholder="{{{{ _(\'{flat_en[key]}\') }}}}"', after)
            new_before = re.sub(ph_pattern, f'placeholder="{{{{ _(\'{flat_en[key]}\') }}}}"', before)
            if new_after != after or new_before != before:
                return f"{new_before}{new_after}"
            else:
                return f'{before} placeholder="{{{{ _(\'{flat_en[key]}\') }}}}"{after}'
        return m.group(0)

    html_content = re.sub(r'(<[^>]*?)\s*data-i18n-placeholder="([^"]+)"([^>]*>)', repl_placeholder, html_content)

    # 4. Replace data-i18n-title="key" title="old"
    def repl_title(m):
        before = m.group(1)
        key = m.group(2)
        after = m.group(3)
        if key in flat_en:
            t_pattern = r'title="[^"]*"'
            new_after = re.sub(t_pattern, f'title="{{{{ _(\'{flat_en[key]}\') }}}}"', after)
            new_before = re.sub(t_pattern, f'title="{{{{ _(\'{flat_en[key]}\') }}}}"', before)
            if new_after != after or new_before != before:
                return f"{new_before}{new_after}"
            else:
                return f'{before} title="{{{{ _(\'{flat_en[key]}\') }}}}"{after}'
        return m.group(0)

    html_content = re.sub(r'(<[^>]*?)\s*data-i18n-title="([^"]+)"([^>]*>)', repl_title, html_content)

    return html_content

# Process all templates
template_dir = 'Book_Store/templates'
for filename in os.listdir(template_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = replace_i18n(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

print("Template processing complete.")
