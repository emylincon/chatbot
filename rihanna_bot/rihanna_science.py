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
        return Science(query).answer_format()


class Science:
    def __init__(self, query):
        self.client = wolframalpha.Client(config.wolf_id)
        self.result = self.client.query(query)

    def answer_text(self):
        try:
            reply = ''
            result_list = self.result['pod']
            for step in result_list:
                if step['subpod']['plaintext']:
                    reply += step['subpod']['plaintext'] + '\n'
            return {'display': reply.replace('\n', '<br>'), 'say': reply.replace('-', 'minus')}
        except Exception as e:
            return {'display': help()+str(e), 'say': str(e)}

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


# a =Science('tell me a dirty joke').joke()
# print(a)