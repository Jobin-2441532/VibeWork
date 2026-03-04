import os
import re
from bs4 import BeautifulSoup

d = r"C:\Users\JOBIN\Desktop\Freelance\frontend"
for f in os.listdir(d):
    if f.endswith(".html"):
        p = os.path.join(d, f)
        with open(p, "r", encoding="utf-8") as file:
            c = file.read()
            
        soup = BeautifulSoup(c, 'html.parser')
        
        btn1 = soup.find('button', id='themeToggle')
        if btn1:
            parent = btn1.parent
            if parent and parent.name == 'div' and parent.get('class') and 'gap-2' in parent.get('class'):
                parent.decompose()
            else:
                btn1.decompose()
                
        btn2 = soup.find('button', id='textSizeBtn')
        if btn2:
            btn2.decompose()

        c = soup.prettify(formatter="html")
        c = re.sub(r'//\s*Dark Mode Logic.*?//\s*Auth check', '// Auth check', c, flags=re.DOTALL)
        c = re.sub(r'//\s*Text Size Logic.*?//\s*Auth check', '// Auth check', c, flags=re.DOTALL)
        
        c = re.sub(r'<style>.*?</style>', '<style>\n    body {\n        background-color: #f3f4f6;\n    }\n  </style>', c, flags=re.DOTALL)
        
        with open(p, "w", encoding="utf-8") as file:
            file.write(c)
