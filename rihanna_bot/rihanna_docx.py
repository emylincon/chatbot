from docx import Document
from os import path
import os

# https://www.youtube.com/watch?v=26vNgM_wSAE


def selector(query):
    pass


class WordFile:
    def __init__(self, filename):
        self.path = r'C:\Users\emyli\PycharmProjects\Chatbot_Project\wordfiles'
        self.filename = filename

    def create(self, content=None, content_styled=None, heading=None):
        # content = just text, content_styled = [[{'content':'i ..', 'style':'bold' or'italic' or None]},{}...], ..]
        if path.exists(f'{self.path}\{self.filename}'):
            reply = f'{self.filename} exists in directory'
            return {'display': reply, 'say': reply}
        doc = Document()
        if heading:
            doc.add_heading(heading, 0)
        if content:
            doc.add_paragraph(content)
            doc.save(f'{self.path}\{self.filename}')
            reply = f'Word document {self.filename} has been created'
            return {'display': reply, 'say': reply}
        elif content_styled:
            for para in content_styled:
                p = doc.add_paragraph('')
                for run in para:
                    if run['style'] == 'bold':
                        p.add_run(run['content']).bold = True
                    elif run['style'] == 'italic':
                        p.add_run(run['content']).italic = True
                    else:
                        p.add_run(run['content'])
            doc.save(f'{self.path}\{self.filename}')
            reply = f'Word document {self.filename} has been created'
            return {'display': reply, 'say': reply}
        else:
            reply = 'no content specified'
            return {'display': reply, 'say': reply}

    def read(self):
        if path.exists(f'{self.path}\{self.filename}'):
            display_content = ''
            say_content = ''
            doc = Document(f'{self.path}\{self.filename}')
            for para in doc.paragraphs:
                #print(para.font)
                if para.style.name == 'Title':
                    display_content += f'<h1>{para.text}</h1>'
                    say_content += para.text + '\n'
                else:
                    say_content += para.text + '\n'
                    p = '<p>'
                    for run in para.runs:
                        if run.font.bold:
                            p += f'<b>{run.text}</b>'
                        elif run.font.italic:
                            p += f'<em>{run.text}</em>'
                        else:
                            p += f'{run.text}'
                    p += '</p>'
                    display_content += p
            return {'display': display_content, 'say': say_content}

        else:
            reply = f'file {self.filename} does not exist'
            return {'display': reply, 'say': reply}

    def delete(self):
        if path.exists(f'{self.path}\{self.filename}'):
            os.remove(f'{self.path}\{self.filename}')
            reply = f'Word document {self.filename} has been deleted'
            return {'display': reply, 'say': reply}
        else:
            reply = f'file {self.filename} does not exist'
            return {'display': reply, 'say': reply}


# WordFile('emeka.docx').delete()
# con = [
#         [{'content':'i love people', 'style':'bold'}, {'content':' they are very nice', 'style':None}],
#         [{'content':'i love people', 'style':'italic'}, {'content':' they are very nice', 'style':None}],
#        [{'content': 'i love people', 'style': 'bold'}, {'content': ' they are very nice', 'style': 'bold'}],
#        [{'content': 'i love people', 'style': None}, {'content': ' they are very nice', 'style': 'italic'}]
#        ]
# a = WordFile('emeka.docx').create(content_styled=con, heading='life is good')
#
# print(a)

# a = WordFile('emeka.docx').read()
# print(a)
