import os
import pyperclip

file_list = [
    'server.py',
    'app.py',
    'media_sequence.py',
    # 'templates/index.html',
    # 'static/script.js',
    # 'static/media_control.js',
    # 'static/canvas.js'
]

all_texts = ''
for file in file_list:
    all_texts += f'\n# {file}\n'
    file_path = os.path.join(os.path.dirname(__file__), file)
    with open(file_path, 'r', encoding='utf-8') as f:
        all_texts += f.read() + '\n'

# all_texts += """
# I want perfect code.
# """
all_texts += """
I want perfect code.
"""
print(all_texts)
print(len(all_texts.split('\n')))

pyperclip.copy(all_texts)
