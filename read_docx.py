import sys
import zipfile
import xml.etree.ElementTree as ET

def get_docx_text(path):
    try:
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = ET.XML(xml_content)
        
        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = WORD_NAMESPACE + 'p'
        TEXT = WORD_NAMESPACE + 't'
        
        paragraphs = []
        for paragraph in tree.iter(PARA):
            texts = [node.text for node in paragraph.iter(TEXT) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        
        return '\n'.join(paragraphs)
    except Exception as e:
        return str(e)

with open('docx_output.txt', 'w', encoding='utf-8') as out_f:
    for f in [
        r'c:\Users\JOBIN\Desktop\Freelance\Freelancing_Marketplace_PRD.docx',
        r'c:\Users\JOBIN\Desktop\Freelance\Freelancing_Marketplace_Design_Document.docx',
        r'c:\Users\JOBIN\Desktop\Freelance\Freelancing_Marketplace_Tech_Stack_Document.docx'
    ]:
        out_f.write(f"========== {f} ==========\n")
        out_f.write(get_docx_text(f))
        out_f.write("\n\n")
