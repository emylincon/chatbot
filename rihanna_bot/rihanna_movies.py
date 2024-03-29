from imdb import IMDb, IMDbError
# https://imdbpy.readthedocs.io/


def selector(query):
    if query[:6] == 'search':     # search matrix in movies
        msg = query[7:].split(' in ')[0]
        return Movies().search(msg)
    elif query == 'show top movies':
        return Movies().top_movies()
    elif query[:len('show top ')] == 'show top ':    # show top 50 movies, show by year top 5 movies
        msg = query[len('show top '):].split()[0]
        if msg.isnumeric():
            return Movies().top_movies(end=int(msg))
        else:
            reply = 'I do not understand the query. use man help'
            return {'display': reply, 'say': reply}
    elif query[:len('show by year top ')] == 'show by year top ':
        msg = query[len('show by year top '):].split()[0]
        if msg.isnumeric():
            return Movies().top_movies(end=int(msg), order='year')
        else:
            return Movies().top_movies(order='year')
    elif query[:len('find person ')] == 'find person ':      # find person angelina in movies
        msg = query[len('find person '):].split(' in ')[0]
        return Movies().find_person(msg)
    elif query[:len('find people ')] == 'find people ':      # find people angelina in movies
        msg = query[len('find people '):].split(' in ')[0]
        return Movies().find_people(msg)
    else:
        reply = 'I do not understand the query. use man help'
        return {'display': reply, 'say': reply}


class Movies:
    def __init__(self):
        self.movie = IMDb()
        self.movie_link = 'https://openloadmovies.ac'

    def get_link(self, data):
        link = '#'
        if data['kind'] == 'movie':
            # link = self.movie_link + self.format_string(data['title'].lower().replace(' ', '-')) + f"-{data['year']}"
            link = f"{self.movie_link}/movies/{self.format_string(data['title'].lower().replace(' ', '-'))}-{data['year']}"
        elif data['kind'] == 'tv series':
            link = f"{self.movie_link}/tvseries/{self.format_string(data['title'].lower().replace(' ', '-'))}"
        return link

    def search(self, query):
        movie_list = self.movie.search_movie(query)
        display = "<table id='t01'>"
        for movie in movie_list:
            data = movie.data
            try:
                link = self.get_link(data=data)
                year = data['year']
            except KeyError:
                link = f"{self.movie_link}/?s={self.format_string(data['title'].lower())}"
                year = '-'
            display += f"<tr onclick='open_link(" + f'"{link}"' + f")'>\
                        <td><img src='{data['cover url']}' alt='{data['title']}'></td>\
                        <td><p style='font-size:15px; color:#5985E9; font-family:verdana;'>{data['title']}</p></td>\
                        <td><p style='font-size:15px; color:#5985E9; font-family:verdana;'>{year}</p></td>\
                        </tr>"
        display += '</table>'
        say = 'Find returned search results'
        reply = {'display': display, 'say': say}
        return reply

    @staticmethod
    def format_string(string):
        d = "!?\|:;@'][<>"

        for c in d:
            if c in string:
                string = string.replace(c, '')
        return string

    def top_movies(self, end=250, order='rank'):
        try:
            display = '<h1 style="align:center;">Top Movies</h1>'
            if order == 'rank':
                movie_list = self.movie.get_top250_movies()[:end]
            else:
                d_list = self.movie.get_top250_movies()
                movie_list = {i.data['year']: i for i in d_list}
                movie_list = {k: v for k, v in sorted(movie_list.items(), reverse=True)}
                movie_list = list(movie_list.values())[:end]
            display += "<table id='t01'>\
                          <tr>\
                            <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'><b>Rank</b></p></th>\
                            <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'><b>Movie</b></p></th>\
                            <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'><b>Year</b></p></th>\
                            <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'><b>Rating</b></p></th>\
                          </tr>\
                        "
            for movie in movie_list:
                data = movie.data
                link = self.get_link(data=data)
                display += f"<tr onclick='open_link(" + f'"{link}"' + f")'>\
                                <td><p style='font-size:12px; color:#5985E9; font-family:verdana;'>{data['top 250 rank']}</p></td>\
                                <td><p style='font-size:12px; color:#5985E9; font-family:verdana;'>{data['title']}</p></td>\
                                <td><p style='font-size:12px; color:#5985E9; font-family:verdana;'>{data['year']}</p></td>\
                                <td><p style='font-size:12px; color:#5985E9; font-family:verdana;'>{data['rating']}</p></td>\
                            </tr> \
                           "
            return {'display': display, 'say': 'find displayed the top movies'}
        except IMDbError as e:
            reply = f'bug detected in top movies: {e}'
            return {'display': reply, 'say': reply}

    def find_people(self, query):
        people = self.movie.search_person(query)
        if len(people) > 5:
            people = people[:5]
        all_people = [self.movie.get_person(p.personID).data for p in people]
        display = f'<h1 style="text-align:center;">Result for {query}</h1>'
        display += '<table style="width:800px;" border="0">'
        style = "style='font-size:12px; color:#5985E9; font-family:verdana; "
        p_style = "style='font-size:12px; color:#5985E9; font-family:verdana; margin:0; padding:0; margin-bottom:0; margin-top:0;'"
        for person in all_people:
            bio = f'<button type="button" class="collapsible">BIO</button>\
                            <div class="content">\
                             {" ".join(person["mini biography"])} </div>'
            try:
                birth_place = person['birth info']['birth place']
            except KeyError:
                birth_place = '-'
            try:
                birth_name = person['birth name']
            except KeyError:
                birth_name = person['name']
            try:
                height = person['height']
            except KeyError:
                height = '-'
            try:
                birth_date = person['birth date']
            except KeyError:
                birth_date = '-'
            try:
                nick_name = ' '.join(person['akas'])
            except KeyError:
                nick_name = '-'
            display += f"<tr>\
                        <td><div style='float:left; margin:0; padding:0; margin-bottom:0; margin-top:0;'><img src='{person['headshot']}'><br></div>" \
                       f"<div style='float:left; margin:0; padding:0; margin-bottom:0; margin-top:0;'><p {p_style}><b>Birth Name</b>: {birth_name}</p>" \
                       f"<p {p_style}><b>Known Name</b>:{person['name']}</p>" \
                       f"<p {p_style}><b>Height</b>: {height}</p>" \
                       f"<p {p_style}><b>BirthDay</b>: {birth_date}</p>" \
                       f"<p {p_style}>BirthPlace: {birth_place}</p>" \
                       f"<p {p_style}><b>Other Names</b>: {nick_name}</p>" \
                       f"</div></td>\
                        </tr>" \
                       f"<tr>" \
                       f"<td>{bio}</td>" \
                       f"</tr>" \
                       f"<tr>" \
                       f"<td><b>Filmography</b>"
            for item in person['filmography']:
                display += f'<button type="button" class="collapsible">{item.capitalize()}</button>'
                display += ' <div class="content">'
                sub_table = "<table id='t01'><tr>"
                for t in person['filmography'][item][0].data:
                    sub_table += f'<th>{t.capitalize()}</th>'
                sub_table += '</tr>'
                for sub_item in person['filmography'][item]:
                    sub_table += '<tr>'
                    for it in sub_item.data:
                        sub_table += f"<td>{sub_item.data[it]}</td>"
                    sub_table += '</tr>'
                sub_table += '</table></div>'
                display += sub_table
            display += '</td></tr>'
            try:
                display += '<tr><td>'
                display += f'<button type="button" class="collapsible">In Development</button>'
                display += ' <div class="content">'
                s_table = "<table id='t01'><tr>"
                for item in person['in development'][0].data:
                    s_table += f'<th>{item.capitalize()}</th>'
                s_table += '</tr>'
                for item in person['in development']:
                    s_table += '<tr>'
                    for it in item.data:
                        s_table += f"<td>{item.data[it]}</td>"
                    s_table += '</tr>'
                s_table += '</table></div>'
                display += s_table
                display += '</td></tr>'
            except KeyError:
                display += ''
            try:
                display += '<tr><td>'
                display += f'<button type="button" class="collapsible">Salary History</button>'
                display += ' <div class="content">'
                for salary in person['salary history']:
                    sa = salary.split('(qv)::')
                    display += f'<br><b>{sa[0].replace("_", " ")}</b>: {sa[1]}'
                display += '</div>'
                display += '</td></tr>'
            except KeyError:
                display += ''
        display += '</table>'

        script = '<script>\
                    var coll = document.getElementsByClassName("collapsible");\
                    var i;\
                    for (i = 0; i < coll.length; i++) {\
                      coll[i].addEventListener("click", function() {\
                        this.classList.toggle("active");\
                        var content = this.nextElementSibling;\
                        if (content.style.maxHeight){\
                          content.style.maxHeight = null;\
                        } else {\
                          content.style.maxHeight = content.scrollHeight + "px";\
                        } \
                      });\
                    }\
                    </script>'
        display += script
        say = f'find displayed the results for {query}'
        return {'display': display, 'say': say}

    def find_person(self, query):
        people = self.movie.search_person(query)[:1]
        all_people = [self.movie.get_person(p.personID).data for p in people]
        display = '<table style="width:800px;" border="0">'
        p_style = "style='font-size:13px; font-family:verdana; margin:0; padding:0; margin-bottom:0; margin-top:0;'"
        for person in all_people:
            bio = f'<button type="button" class="collapsible">BIO</button>\
                            <div class="content">\
                             {" ".join(person["mini biography"]).replace("(qv)", "").replace("_", "")} </div>'
            try:
                birth_place = person['birth info']['birth place']
            except KeyError:
                birth_place = '-'
            try:
                birth_name = person['birth name']
            except KeyError:
                birth_name = person['name']
            try:
                height = person['height']
            except KeyError:
                height = '-'
            try:
                birth_date = person['birth date']
            except KeyError:
                birth_date = '-'
            try:
                nick_name = ' '.join(person['akas'])
            except KeyError:
                nick_name = '-'
            display += f"<tr>\
                        <td><div style='float:left; margin:0; padding:0; margin-bottom:0; margin-top:0;'><img src='{person['headshot']}'><br></div>" \
                       f"<div style='float:left; margin:0; padding:0; margin-bottom:0; margin-top:0;'><p {p_style}><b>Birth Name</b>: {birth_name}</p>" \
                       f"<p {p_style}><b>Known Name</b>:{person['name']}</p>" \
                       f"<p {p_style}><b>Height</b>: {height}</p>" \
                       f"<p {p_style}><b>BirthDay</b>: {birth_date}</p>" \
                       f"<p {p_style}><b>BirthPlace</b>: {birth_place}</p>" \
                       f"<p {p_style}><b>Other Names</b>: {nick_name}</p>" \
                       f"</div></td>\
                        </tr>" \
                       f"<tr>" \
                       f"<td>{bio}</td>" \
                       f"</tr>" \
                       f"<tr>" \
                       f"<td><b>Filmography</b>"
            for item in person['filmography']:
                display += f'<button type="button" class="collapsible">{item.capitalize()}</button>'
                display += ' <div class="content">'
                sub_table = "<table id='t01'><tr>"
                for t in person['filmography'][item][0].data:
                    sub_table += f'<th>{t.capitalize()}</th>'
                sub_table += '</tr>'
                for sub_item in person['filmography'][item]:
                    sub_table += '<tr>'
                    for it in sub_item.data:
                        sub_table += f"<td>{sub_item.data[it]}</td>"
                    sub_table += '</tr>'
                sub_table += '</table></div>'
                display += sub_table
            display += '</td></tr>'
            try:
                display += '<tr><td>'
                display += f'<button type="button" class="collapsible">In Development</button>'
                display += ' <div class="content">'
                s_table = "<table id='t01'><tr>"
                for item in person['in development'][0].data:
                    s_table += f'<th>{item.capitalize()}</th>'
                s_table += '</tr>'
                for item in person['in development']:
                    s_table += '<tr>'
                    for it in item.data:
                        s_table += f"<td>{item.data[it]}</td>"
                    s_table += '</tr>'
                s_table += '</table></div>'
                display += s_table
                display += '</td></tr>'
            except KeyError:
                pass
            try:
                display += '<tr><td>'
                display += f'<button type="button" class="collapsible">Salary History</button>'
                display += ' <div class="content">'
                for salary in person['salary history']:
                    sa = salary.split('(qv)::')
                    display += f'<br><b>{sa[0].replace("_", " ")}</b>: {sa[1]}'
                display += '</div>'
                display += '</td></tr>'
            except KeyError:
                pass
        display += '</table>'

        script = '<script>\
                    var coll = document.getElementsByClassName("collapsible");\
                    var i;\
                    for (i = 0; i < coll.length; i++) {\
                      coll[i].addEventListener("click", function() {\
                        this.classList.toggle("active");\
                        var content = this.nextElementSibling;\
                        if (content.style.maxHeight){\
                          content.style.maxHeight = null;\
                        } else {\
                          content.style.maxHeight = content.scrollHeight + "px";\
                        } \
                      });\
                    }\
                    </script>'
        display += script
        say = f'find displayed the results for {query}'
        return {'display': display, 'say': say}


# a = Movies().find_people('angelina')
# print(a['display'])
# Movies().search('venom')