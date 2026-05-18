import os, re
for root, _, files in os.walk('Book_Store/templates'):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = re.sub(r",\s*\*\*\{'data-i18n':\s*'[^']+'\}", '', content)
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
