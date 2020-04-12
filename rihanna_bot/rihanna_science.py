import wolframalpha
import config


# https://www.wolframalpha.com/


def selector(query):
    if query[:len('solve ')] == 'solve ':
        msg = query[len('solve '):]
        if msg[-len('show working'):] == 'show working':
            msg = msg.replace('show working', '')
            return Science(query=msg).answer_format()
        else:
            return Science(query=msg).answer_text()
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
            for step in result_list:
                if step['subpod']['plaintext']:
                    reply += step['subpod']['plaintext'] + '\n'
            return {'display': reply.replace('\n', '<br>'), 'say': reply.replace('-', 'minus')}
        except Exception as e:
            return {'display': str(e), 'say': str(e)}

    def answer_format(self):
        try:
            say = ''
            display = ''
            result_list = self.result['pod']
            for step in result_list:
                if step['subpod']['plaintext']:
                    say += step['subpod']['plaintext'] + '\n'
                if step['@title'] == 'Solution':
                    display += '<div>' \
                               f'<font color="blue">Result: </font>' \
                               f'<img src="{step["subpod"]["img"]["@src"]}" alt=f"{step["subpod"]["plaintext"]}">' \
                               '</div>'
                else:
                    display += '<div>' \
                               f'<img src="{step["subpod"]["img"]["@src"]}" alt=f"{step["subpod"]["plaintext"]}">' \
                               '</div>'
            return {'display': display, 'say': say.replace('-', 'minus')}
        except Exception as e:
            return {'display': str(e), 'say': str(e)}

    def joke(self):

        result_list = self.result['pod']
        ans = ''
        _ans = ''
        for step in result_list:
            _ans += step['subpod']['plaintext']
            if step['@title'] == 'Result':
                ans += step['subpod']['plaintext']
        if ans != '':
            ans = ans.split('A: ')
            answer = 'Answer: ' + ans[1]
            question = ans[0].replace('Q', 'Question')
            if '(' in answer:
                answer = answer[:answer.index('(')]
            return {'display': question, 'say': question, 'answer': answer}
        else:
            return {'display': _ans.replace('\n', '<br>'), 'say': _ans}

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
            reply = 'bug has been detected in universal'
            return {'display': reply, 'say': reply}
    # f'{self.default()["say"]}'

    def default(self):
        # this does not work if there is no result or solution title in result
        reply = next(self.result.results).text
        return {'display': reply, 'say': reply}


# a = Science('movies').universal()
# print(a)
