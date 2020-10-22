import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict
import random as r


def selector(msg):
    if msg[:len('sensor details for the lab')] == "sensor details for the lab":
        kind = msg[len('sensor details for the lab')+1:]
        return Sensor().get_response(kind=kind)
    else:
        res = 'sorry sensors are offline'
        return {'say': res, 'display': res}
        

class TextSimilarity:
    def get_cosine_sim(self, *strs):
        vectors = [t for t in self.get_vectors(*strs)]
        return cosine_similarity(vectors)
    @staticmethod
    def get_vectors(*strs):
        text = [t for t in strs]
        vectorizer = CountVectorizer(text)
        vectorizer.fit(text)
        return vectorizer.transform(text).toarray()

class Sensor:
    def __init__(self):
        self.api = 'http://lsbu-sensors.herokuapp.com/'
        self.similar = TextSimilarity()
        self.unit = {'temp': 'degrees celsius', 'hum': 'percent', 'heat': 'degrees celsius'}
        self.symbol = {'temp': '°C', 'hum': '%', 'heat': '°C'}
        self.kinds = {'temp': 'temperature', 'hum': 'humidity', 'heat': 'heat_index'}
        self.keys = OrderedDict([('temp', 'temp'), ('hum', 'hum'), ('heat', 'heat'), ('heat index', 'heat'),
                                 ('feels like', 'heat'), ('temperature', 'temp'), ('humidity', 'hum'), ('humid', 'hum')])

    def get_data(self):
        return requests.get(self.api+'get-data').json()

    def find_similar(self, kind):
        keys = list(self.keys.keys())
        res = self.similar.get_cosine_sim(kind, *keys)[0][1:]
        max_no = max(res)
        ind_max = list(res).index(max_no)
        return self.keys[keys[ind_max]]

    def get_response(self, kind):
        key = self.find_similar(kind=kind)
        data = self.get_data()
        say = f'the {self.kinds[key].replace("_", " ")} in the lab is {round(data["actual"]["sensor"][self.kinds[key]], 2)} {self.unit[key]}'
        display = self.create_html(kind=key, data=data)
        return {'say': say, 'display': display}

    def create_html(self, kind, data):
        pid = r.randrange(1000, 9999)
        title = {'temp': 'temperature', 'hum': 'humidity', 'heat': 'feels like'}
        data_stat = data["data_stat"][self.kinds[kind]]
        pred_stat = {'arima': data["pred_stat"]['arima'][kind], 'lstm': data["pred_stat"]['lstm'][kind]}


        style = """
        .box{
            position: relative;
            background: #fff;
            padding: 20px 40px 40px;
            text-align: center;
            overflow: hidden;
            border-radius: 20px;
        }
        .box .hum{
            background: linear-gradient(45deg,#036eb7, #64eaff);
        }
        .box .temp{
            background: linear-gradient(45deg,#E91E63, #ED55FF);
        }
        .box .heat{
            background: linear-gradient(45deg,#086D35, #00FF72);
        }
        .box h2{
            position: relative;
            margin: 0;
            padding: 0;
            font-size: 55px;
            color: #fff;
            z-index: 1;
            opacity: 0.4;
        }
        
        .box h3{
            margin: 0;
            padding: 0;
            font-size: 20px;
            color: #fff;
            text-transform: uppercase;
        }
        table .tg-0lax{
            font-weight: bold;
        }
        table .tg tr:hover {
          background-color:#f5f5f5;
          color: black;
        }
        """
        div = f"""
        <div class="box {kind}">
                <h2>{title[kind].title()}</h2>
                <h2>{round(data["actual"]["sensor"][self.kinds[kind]], 2)} {self.symbol[kind]}</h2>
                    <h3>data stat</h3>

                    <table class="tg">
                        <tbody>
                            <tr>
                                <td class="tg-0pky">Count</td>
                                <td class="tg-0lax" id="temp-count-data">{data["actual"]["sensor"]["id"]}</td>
                                <td class="tg-0la" id="temp-count-arrow"> <img style="height: 20px;" src='img/sense/{data_stat["count"]["arrow"]}.png'> {data_stat["count"]["%"]}%</td>
                            </tr>
                            <tr>
                                <td class="tg-0pky">Mean</td>
                                <td class="tg-0lax" id="temp-mean-data">{data_stat['mean']['data']}</td>
                                <td class="tg-0la" id="temp-mean-arrow"> <img style="height: 20px;" src='img/sense/{data_stat["mean"]["arrow"]}.png'> {data_stat['mean']['%']}%</td>
                            </tr>
                            <tr>
                                <td class="tg-0pky">STD</td>
                                <td class="tg-0lax" id="temp-std-data">{data_stat['std']['data']}</td>
                                <td class="tg-0la" id="temp-std-arrow"> <img style="height: 20px;" src='img/sense/{data_stat["std"]["arrow"]}.png'> {data_stat['std']['%']}%</td>
                            </tr>
                            <tr>
                                <td class="tg-0pky">Min</td>
                                <td class="tg-0lax" id="temp-min-data">{data_stat['min']['data']}</td>
                                <td class="tg-0la" id="temp-min-arrow"> <img style="height: 20px;" src='img/sense/{data_stat["min"]["arrow"]}.png'> {data_stat['min']['%']}%</td>
                            </tr>
                            <tr>
                                <td class="tg-0pky">Max</td>
                                <td class="tg-0lax" id="temp-max-data">{data_stat['max']['data']}</td>
                                <td class="tg-0la" id="temp-max-arrow"> <img style="height: 20px;" src='img/sense/{data_stat["max"]["arrow"]}.png'> {data_stat['max']['%']}%</td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <br>
                    <h3>Prediction Models</h3>
                    <br>
                    <table class="tg">
                        <thead>
                          <tr>
                            <th class="tg-0pky">Model</th>
                            <th class="tg-0lax">RMSE</th>
                            <th class="tg-0lax">Last Trained</th>
                          </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="tg-0pky">ARIMA</td>
                                <td class="tg-0lax" id="temp-arima-rmse"> <img style="height: 20px;" src='img/sense/{pred_stat['arima']['arrow']}.png'> {pred_stat['arima']['rmse']}</td>
                                <td class="tg-0lax" id="temp-arima-date"> {pred_stat['arima']['date']}</td>
                            </tr>
                            <tr>
                                <td class="tg-0pky">LSTM</td>
                                <td class="tg-0lax" id="temp-lstm-rmse"><img style="height: 20px;" src='img/sense/{pred_stat['lstm']['arrow']}.png'> {pred_stat['lstm']['rmse']}</td>
                                <td class="tg-0lax" id="temp-lstm-date"> {pred_stat['lstm']['date']}</td>
                            </tr>
                        </tbody>
                    </table>

                    <br>
                    <div class="pie">
                        <canvas id="Pie-{pid}"></canvas>
                    </div>
            </div>
        """
        script = "<script>"
        script += f"var pie1 = document.getElementById('Pie-{pid}').getContext('2d');"
        script += """
                dataPie = {
                datasets: [{"""
        script += f"data: {[pred_stat['lstm']['accuracy'], pred_stat['lstm']['loss']]},"
        script += """
                    backgroundColor: [
                        'rgba(0, 255, 0, 0.8)',
                        'rgba(255, 0, 0, 0.8)',
                    ],
                    borderColor: [
                        'rgba(255, 255, 255, 1)',
                        'rgba(255, 255, 255, 1)',
                    ],
                }],
            
                // These labels appear in the legend and in the tooltips when hovering different arcs
                labels: [
                    'Accuracy',
                    'Loss',
                ]
            };
            
            var PieHum = new Chart(pie1, {
                type: 'doughnut',
                data: dataPie,
                options: {
                    legend: {
                        display: false,
            
                     },
                    title: {
                        fontSize: 20,
                        text: "Model Accuracy",
                        display: true,
                        fontStyle: 'bold',
                        fontColor: 'white'
                    },
                }
            });
            </script>
        """
        return div+script

#
# print(selector('sensor details for the lab temperature'))