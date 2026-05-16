import json
import os
import re

languages = ['en', 'ar', 'fr', 'de']
json_dir = 'Book_Store/static/i18n'
po_dir = 'Book_Store/translations'

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# First get mapping from en.json (value -> key) since our .po msgid are values from en.json
en_path = os.path.join(json_dir, 'en.json')
with open(en_path, 'r', encoding='utf-8') as f:
    en_dict = flatten_dict(json.load(f))

# We need a reverse map from english string to json key
en_to_key = {v: k for k, v in en_dict.items()}

for lang in languages:
    json_path = os.path.join(json_dir, f'{lang}.json')
    po_path = os.path.join(po_dir, lang, 'LC_MESSAGES', 'messages.po')
    
    if not os.path.exists(json_path) or not os.path.exists(po_path):
        continue
        
    with open(json_path, 'r', encoding='utf-8') as f:
        lang_dict = flatten_dict(json.load(f))
        
    with open(po_path, 'r', encoding='utf-8') as f:
        po_content = f.read()
    
    # We will iterate through each msgid in the po file and if we find it in our reverse map,
    # we replace the next msgstr "" with msgstr "translated_value"
    
    new_po_lines = []
    lines = po_content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('msgid '):
            # Extract the msgid string
            msgid = line[6:].strip('"')
            new_po_lines.append(line)
            
            # The next line should be msgstr
            if i + 1 < len(lines) and lines[i+1].startswith('msgstr ""'):
                i += 1
                if msgid in en_to_key:
                    key = en_to_key[msgid]
                    if key in lang_dict:
                        # Escape quotes in translated text
                        translated_text = lang_dict[key].replace('"', '\\"')
                        new_po_lines.append(f'msgstr "{translated_text}"')
                    else:
                        new_po_lines.append('msgstr ""')
                else:
                    new_po_lines.append('msgstr ""')
            else:
                pass # it might not be a simple msgstr line, handle it normally
        else:
            new_po_lines.append(line)
        i += 1
        
    with open(po_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_po_lines))

print("Translations migrated successfully.")
