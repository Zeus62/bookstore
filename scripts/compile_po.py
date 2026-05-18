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

with open(os.path.join(json_dir, 'en.json'), 'r', encoding='utf-8') as f:
    en_dict = flatten_dict(json.load(f))

for lang in languages:
    json_path = os.path.join(json_dir, f'{lang}.json')
    if not os.path.exists(json_path):
        continue
    with open(json_path, 'r', encoding='utf-8') as f:
        lang_dict = flatten_dict(json.load(f))
        
    po_path = os.path.join(po_dir, lang, 'LC_MESSAGES', 'messages.po')
    os.makedirs(os.path.dirname(po_path), exist_ok=True)
    
    with open(po_path, 'w', encoding='utf-8') as f:
        f.write('msgid ""\n')
        f.write('msgstr ""\n')
        f.write('"Project-Id-Version: 1.0\\n"\n')
        f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        f.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        f.write('\n')
        
        for key, en_text in en_dict.items():
            trans_text = lang_dict.get(key, en_text)
            
            # Escape strings for PO file
            en_esc = en_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            trans_esc = trans_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            
            f.write(f'msgid "{en_esc}"\n')
            f.write(f'msgstr "{trans_esc}"\n\n')

print("PO files fully rewritten from JSON.")
