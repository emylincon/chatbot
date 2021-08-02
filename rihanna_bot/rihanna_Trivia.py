import requests
from urllib.parse import unquote
import random


def selector(message: str):
    if message[:len('Trivia question')] == 'trivia question':
        return Question().request()


class Question:
    def __init__(self):
        self.url = "https://opentdb.com/api.php?amount=1&encode=url3986"
        self.question_id = random.randrange(100,9999)

    def get_question(self):
        response = requests.get(self.url)
        res_string = response.json()
        question = res_string # eval(unquote(str(res_string)))
        options = [*question['results'][0]['incorrect_answers'], question['results'][0]['correct_answer']]
        random.shuffle(options)
        question['results'][0]['options'] = options
        question['results'][0]['id'] = self.question_id
        self.question_id += 1
        return question

    def format_say(self, text):
        sentences = []
        if len(text) > 180:
            if text[180] == " " or text[179] == " ":
                sentences.append(text[:180])
                sentences.append(text[180:])
            else:
                for i in range(180, 1, -1):
                    if text[i] == " ":
                        sentences.append(text[:i])
                        sentences.append(text[i:])
        else:
            sentences.append(text)
        return sentences

    @staticmethod
    def format_question(question):
        question = question['results'][0]

        def gen_id():
            return f"td{random.randrange(1, 9999)}"

        response = f"""
        <table class="t02">
            <tbody>
                <tr>
                    <th>Category</th>
                    <th>Difficulty</th>
                </tr>
                <tr>
                    <td onclick="">{unquote(question['category'])}</td>
                    <td onclick="">{unquote(question['difficulty'])}</td>
                </tr>
            </tbody>
        </table>
        <div class="question">{unquote(question['question'])}</div>
        <table class="t02 t03" cellspacing="0">
            <tbody>
            """
        for option in question['options']:
            rd = gen_id()
            response += f"""<tr>
                    <td onclick="check_ans('{rd}', {question['id']})" id={rd}>{unquote(option)}</td>
                </tr>
            """
        response += """</tbody>
                </table>
                """
        return response

    def request(self):
        question = self.get_question()
        html = self.format_question(question)
        say = ""
        if question['results'][0]['difficulty'] == 'hard':
            say += "This is a difficult question. uhm. uhm.. "
        say += f"question says: {unquote(question['results'][0]['question'])}? "
        say += f"The options are: {unquote(', '.join(question['results'][0]['options']))} "
        print(len(say), say)
        return {'display': html, 'say': say,
                'answers': {question['results'][0]['id']: unquote(question['results'][0]['correct_answer'])}}


if __name__ == '__main__':
    print(Question().request())
