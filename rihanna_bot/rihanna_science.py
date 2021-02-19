import wolframalpha
import config
import json
import pandas as pd
import random


# https://www.wolframalpha.com/


def selector(query):
    if query[:len('solve ')] == 'solve ':
        msg = query[len('solve '):]
        if msg[-len('show working'):] == 'show working':
            msg = msg.replace('show working', '')
            return Science(query=msg).answer_format()
        else:
            return Science(query=msg).answer_format()
    elif 'joke' in query:
        return Science(query).joke()
    else:
        return Science(query).universal()


def default_response(chat):
    if chat == '':
        return 'I am sorry. I am not allowed to answer that question'
    else:
        try:
            return Science(chat).default()
        except Exception:
            return 'I am sorry. I am not allowed to answer that question'


class Science:
    def __init__(self, query):
        self.client = wolframalpha.Client(config.wolf_id)
        self.result = self.client.query(query)
        self.query = query

    def answer_text(self):
        try:
            reply = ''
            result_list = self.result['pod']

            # print(json.dumps(result_list, indent=4))
            for step in result_list:
                if step['@numsubpods'] == '1':
                    if step['subpod']['plaintext']:
                        reply += step['subpod']['plaintext'] + '\n'
                else:
                    for pod in step['subpod']:
                        if pod['plaintext']:
                            reply += pod['plaintext'] + '\n'

                # if step['subpod']['plaintext']:
                #     reply += step['subpod']['plaintext'] + '\n'
            if len(reply) > 50:
                say = 'please find the displayed result'
            else:
                say = reply[:]
            return {'display': reply.replace('\n', '<br>'), 'say': say.replace('-', 'minus')}
        except Exception as e:
            reply = f'bug (Science.answer_text): {e}'
            return {'display': reply, 'say': str(e)}

    def answer_format(self):
        try:
            say = ''
            display = ''
            result_list = self.result['pod']
            # print(json.dumps(result_list, indent=4))
            for step in result_list:
                display += '<div style="color: white; background-color: black;">' \
                           f'{step["@title"]}' \
                           '</div>'
                if step['@numsubpods'] == '1':
                    if step['subpod']['plaintext']:
                        say += step['subpod']['plaintext'] + '\n'
                    if step['@title'] == 'Solution':
                        display += '<div>' \
                                   f'<font color="blue">Result: </font>' \
                                   f'<img src="{step["subpod"]["img"]["@src"]}" alt=f"{step["subpod"]["plaintext"]}">' \
                                   '</div>'
                    else:
                        display += '<div style="padding: 5px; align-items: center;">' \
                                   f'<img src="{step["subpod"]["img"]["@src"]}" alt=f"{step["subpod"]["plaintext"]}">' \
                                   '</div>'
                else:
                    for pod in step['subpod']:
                        if pod['plaintext']:
                            say += pod['plaintext'] + '\n'
                        if pod.get('@title') == 'Solution':
                            display += '<div>' \
                                       f'<font color="blue">Result: </font>' \
                                       f'<img src="{pod["img"]["@src"]}" alt=f"{pod["plaintext"]}">' \
                                       '</div>'
                        else:
                            display += '<div style="padding: 5px; align-items: center; margin: 0 auto;">' \
                                       f'<img src="{pod["img"]["@src"]}" alt=f"{pod["plaintext"]}">' \
                                       '</div>'
            if len(say) > 50:
                say = 'please find the displayed result'
            return {'display': display, 'say': say.replace('-', 'minus')}
        except Exception as e:
            reply = f'bug (Science.answer_format): {e}'
            return {'display': reply, 'say': str(e)}

    def joke(self):
        def default():
            rand = ['my jokes are not that funny', 'what do you think i am? some kinda comedian?',
                    'i dont understand human humor']
            reply = random.choice(rand)
            return {'display': reply, 'say': reply}
        result_list = self.result['pod']
        # pd.set_option('max_columns', None)
        df = pd.DataFrame(result_list)
        try:
            tx = df[df['@title'].str.match('Result')].to_dict('records')
            result = tx[0]['subpod']['plaintext']
            if 'A: ' in result:
                ans = result.split('A: ')
                answer = 'Answer: ' + ans[1]
                question = ans[0].replace('Q', 'Question')
                if '(' in answer:
                    answer = answer[:answer.index('(')]
                return {'display': question, 'say': question, 'answer': answer}
            else:
                return {'display': result.replace('\n', '<br>'), 'say': result}
        except IndexError:
            return default()

    def universal(self):
        try:
            result_list = self.result['pod']
            reply = "<table width='250px'>"

            for pod in result_list:
                if pod['@numsubpods'] == '1':
                    reply += f"<tr bgcolor='#FDF0ED'>" \
                    f"<th align='center'><font color='black'>{pod['@title']}</font></th>" \
                    "</tr>" \
                    "<tr>" \
                    f"<td align='center'><img src='{pod['subpod']['img']['@src']}' alt='{pod['subpod']['plaintext']}'></td>" \
                    "</tr>"
                else:
                    reply += f"<tr bgcolor='#FDF0ED'>" \
                             f"<th align='center'><font color='black'>{pod['@title']}</font></th>" \
                             f"</tr>"
                    for subpod in pod['subpod']:
                        reply += "<tr><td>"
                        reply += "<div style = 'width:250px; word-wrap: break-word'>" \
                                 f"<b><font color='blue'>{subpod['@title']}</font></b>" \
                                 f"<br><img src='{subpod['img']['@src']}' alt='{subpod['plaintext']}'>" \
                                 "</div></td>" \
                                 "</tr>"
            reply += "</table>"

            return {'display': reply, 'say': f'Find displayed the requested result for {self.query}: '}
        except Exception:
            reply = 'bug has been detected in Science.universal'
            return {'display': reply, 'say': reply}
    # f'{self.default()["say"]}'

    def default(self):
        # this does not work if there is no result or solution title in result
        reply = next(self.result.results).text
        return {'display': reply, 'say': reply}


# a = Science('movies').universal()
# print(a)

# a = Science('joke').joke()
# print(a)

# print(selector('solve x^4 - 4x^3 + 8x + 1'))

# print(selector('solve x^4 - 4x^3 + 8x + 1 show working'))