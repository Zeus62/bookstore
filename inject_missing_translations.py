import json
import os

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

en_path = os.path.join(json_dir, 'en.json')
with open(en_path, 'r', encoding='utf-8') as f:
    en_dict = flatten_dict(json.load(f))

# The English values will be our msgids
msgids = list(set(en_dict.values()))

for lang in languages:
    json_path = os.path.join(json_dir, f'{lang}.json')
    po_path = os.path.join(po_dir, lang, 'LC_MESSAGES', 'messages.po')
    
    if not os.path.exists(json_path) or not os.path.exists(po_path):
        continue
        
    with open(json_path, 'r', encoding='utf-8') as f:
        lang_dict = flatten_dict(json.load(f))
        
    # We need a reverse map from english string to lang string
    # english string -> key -> lang string
    en_to_key = {v: k for k, v in en_dict.items()}
    
    with open(po_path, 'r', encoding='utf-8') as f:
        po_content = f.read()
    
    # parse existing msgids
    existing_msgids = set()
    for line in po_content.split('\n'):
        if line.startswith('msgid '):
            existing_msgids.add(line[6:].strip('"'))
            
    # append missing msgids
    new_lines = []
    for msgid in msgids:
        if msgid not in existing_msgids:
            key = en_to_key[msgid]
            translation = lang_dict.get(key, "")
            
            # Escape strings
            msgid_esc = msgid.replace('"', '\\"')
            translation_esc = translation.replace('"', '\\"')
            
            new_lines.append(f'msgid "{msgid_esc}"')
            new_lines.append(f'msgstr "{translation_esc}"')
            new_lines.append('')
            
    if new_lines:
        with open(po_path, 'a', encoding='utf-8') as f:
            f.write('\n' + '\n'.join(new_lines))

print("Missing translations injected successfully.")
