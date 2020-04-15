import requests
from bs4 import BeautifulSoup
import config
import random as r
from multiprocessing.pool import ThreadPool
import billboard
import datetime
from rihanna_bot.ri_youtube import Youtube
from rihanna_bot.hot100_data import *
from rihanna_bot.similarity import sim_main
dict_songs = {
    'Future Featuring Drake Life Is Good The Billboard Hot 100': {'rank': '4', 'artist': 'Future Featuring Drake',
                                                                  'song': 'Life Is Good',
                                                                  'img': 'https://charts-static.billboard.com/img/2020/01/future-tsu-life-is-good-rko-53x53.jpg'},
    'Post Malone Circles The Billboard Hot 100': {'rank': '5', 'artist': 'Post Malone', 'song': 'Circles',
                                                  'img': 'https://charts-static.billboard.com/img/2019/09/post-malone-tp6-circles-sb0-53x53.jpg'},
    'Arizona Zervas Roxanne The Billboard Hot 100': {'rank': '6', 'artist': 'Arizona Zervas', 'song': 'Roxanne',
                                                     'img': 'https://charts-static.billboard.com/img/2019/11/arizona-zervas-egt-roxanne-5y8-53x53.jpg'},
    'Harry Styles Adore You The Billboard Hot 100': {'rank': '7', 'artist': 'Harry Styles', 'song': 'Adore You',
                                                     'img': 'https://charts-static.billboard.com/img/2019/12/harry-styles-psx-adore-you-n45-53x53.jpg'},
    'Justin Bieber Featuring Quavo Intentions The Billboard Hot 100': {'rank': '8',
                                                                       'artist': 'Justin Bieber Featuring Quavo',
                                                                       'song': 'Intentions',
                                                                       'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lewis Capaldi Someone You Loved The Billboard Hot 100': {'rank': '9', 'artist': 'Lewis Capaldi',
                                                              'song': 'Someone You Loved',
                                                              'img': 'https://charts-static.billboard.com/img/2019/03/lewis-capaldi-s2h-someone-you-loved-em0-53x53.jpg'},
    'Billie Eilish everything i wanted The Billboard Hot 100': {'rank': '10', 'artist': 'Billie Eilish',
                                                                'song': 'everything i wanted',
                                                                'img': 'https://charts-static.billboard.com/img/2019/11/billie-eilish-acb-everything-i-wanted-mj1-53x53.jpg'},
    'blackbear Hot Girl Bummer The Billboard Hot 100': {'rank': '11', 'artist': 'blackbear', 'song': 'Hot Girl Bummer',
                                                        'img': 'https://charts-static.billboard.com/img/2019/09/blackbear-nbm-hot-girl-bummer-nvt-53x53.jpg'},
    'Maroon 5 Memories The Billboard Hot 100': {'rank': '12', 'artist': 'Maroon 5', 'song': 'Memories',
                                                'img': 'https://charts-static.billboard.com/img/2019/09/maroon-5-vhb-memories-cnj-53x53.jpg'},
    'Lil Uzi Vert Myron The Billboard Hot 100': {'rank': '13', 'artist': 'Lil Uzi Vert', 'song': 'Myron',
                                                 'img': 'https://charts-static.billboard.com/img/2020/03/lil-uzi-vert-mre-myron-3z3-53x53.jpg'},
    'Doja Cat Say So The Billboard Hot 100': {'rank': '14', 'artist': 'Doja Cat', 'song': 'Say So',
                                              'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Tones And I Dance Monkey The Billboard Hot 100': {'rank': '15', 'artist': 'Tones And I', 'song': 'Dance Monkey',
                                                       'img': 'https://charts-static.billboard.com/img/2019/08/tones-and-i-e8g-dance-monkey-945-53x53.jpg'},
    'The Weeknd Heartless The Billboard Hot 100': {'rank': '16', 'artist': 'The Weeknd', 'song': 'Heartless',
                                                   'img': 'https://charts-static.billboard.com/img/2019/12/the-weeknd-qji-heartless-6te-53x53.jpg'},
    'Maren Morris The Bones The Billboard Hot 100': {'rank': '17', 'artist': 'Maren Morris', 'song': 'The Bones',
                                                     'img': 'https://charts-static.billboard.com/img/2019/03/maren-morris-knd-the-bones-u43-53x53.jpg'},
    'Camila Cabello Featuring DaBaby My Oh My The Billboard Hot 100': {'rank': '18',
                                                                       'artist': 'Camila Cabello Featuring DaBaby',
                                                                       'song': 'My Oh My',
                                                                       'img': 'https://charts-static.billboard.com/img/2019/12/camila-cabello-p0o-my-oh-my-7oy-53x53.jpg'},
    'Lil Uzi Vert Featuring Chief Keef Bean (Kobe) The Billboard Hot 100': {'rank': '19',
                                                                            'artist': 'Lil Uzi Vert Featuring Chief Keef',
                                                                            'song': 'Bean (Kobe)',
                                                                            'img': 'https://charts-static.billboard.com/img/2020/03/lil-uzi-vert-mre-bean-kobe-hyb-53x53.jpg'},
    'YNW Melly & Juice WRLD Suicidal The Billboard Hot 100': {'rank': '20', 'artist': 'YNW Melly & Juice WRLD',
                                                              'song': 'Suicidal',
                                                              'img': 'https://charts-static.billboard.com/img/2019/12/ynw-melly-000-suicidal-ptj-53x53.jpg'},
    "Mustard & Roddy Ricch Ballin' The Billboard Hot 100": {'rank': '21', 'artist': 'Mustard & Roddy Ricch',
                                                            'song': "Ballin'",
                                                            'img': 'https://charts-static.billboard.com/img/2019/07/mustard-000-ballin-3hx-53x53.jpg'},
    'Dan + Shay & Justin Bieber 10,000 Hours The Billboard Hot 100': {'rank': '22',
                                                                      'artist': 'Dan + Shay & Justin Bieber',
                                                                      'song': '10,000 Hours',
                                                                      'img': 'https://charts-static.billboard.com/img/2019/10/dan-shay-aqf-10000-hours-e1h-53x53.jpg'},
    'Eminem Featuring Juice WRLD Godzilla The Billboard Hot 100': {'rank': '23',
                                                                   'artist': 'Eminem Featuring Juice WRLD',
                                                                   'song': 'Godzilla',
                                                                   'img': 'https://charts-static.billboard.com/img/2020/02/eminem-c16-godzilla-r12-53x53.jpg'},
    'DaBaby BOP The Billboard Hot 100': {'rank': '24', 'artist': 'DaBaby', 'song': 'BOP',
                                         'img': 'https://charts-static.billboard.com/img/2019/10/dababy-sfn-bop-3fy-53x53.jpg'},
    'Lady Gaga Stupid Love The Billboard Hot 100': {'rank': '25', 'artist': 'Lady Gaga', 'song': 'Stupid Love',
                                                    'img': 'https://charts-static.billboard.com/img/2020/03/lady-gaga-lkc-stupid-love-arb-53x53.jpg'},
    'Lil Uzi Vert & 21 Savage Yessirskiii The Billboard Hot 100': {'rank': '26', 'artist': 'Lil Uzi Vert & 21 Savage',
                                                                   'song': 'Yessirskiii',
                                                                   'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Uzi Vert Baby Pluto The Billboard Hot 100': {'rank': '27', 'artist': 'Lil Uzi Vert', 'song': 'Baby Pluto',
                                                      'img': 'https://charts-static.billboard.com/img/2020/03/lil-uzi-vert-mre-baby-pluto-sy4-53x53.jpg'},
    'Lil Baby Woah The Billboard Hot 100': {'rank': '28', 'artist': 'Lil Baby', 'song': 'Woah',
                                            'img': 'https://charts-static.billboard.com/img/2019/11/lil-baby-nwx-woah-h7f-53x53.jpg'},
    'Trevor Daniel Falling The Billboard Hot 100': {'rank': '29', 'artist': 'Trevor Daniel', 'song': 'Falling',
                                                    'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'The Black Eyed Peas X J Balvin RITMO (Bad Boys For Life) The Billboard Hot 100': {'rank': '30',
                                                                                       'artist': 'The Black Eyed Peas X J Balvin',
                                                                                       'song': 'RITMO (Bad Boys For Life)',
                                                                                       'img': 'https://charts-static.billboard.com/img/2019/10/the-black-eyed-peas-kvc-ritmo-bad-boys-for-life-2fu-53x53.jpg'},
    'Selena Gomez Lose You To Love Me The Billboard Hot 100': {'rank': '31', 'artist': 'Selena Gomez',
                                                               'song': 'Lose You To Love Me',
                                                               'img': 'https://charts-static.billboard.com/img/2019/11/selena-gomez-nxt-lose-you-to-love-me-ygt-53x53.jpg'},
    'Chris Brown Featuring Drake No Guidance The Billboard Hot 100': {'rank': '32',
                                                                      'artist': 'Chris Brown Featuring Drake',
                                                                      'song': 'No Guidance',
                                                                      'img': 'https://charts-static.billboard.com/img/2019/06/chris-brown-abf-no-guidance-yi0-53x53.jpg'},
    'Roddy Ricch Featuring Mustard High Fashion The Billboard Hot 100': {'rank': '33',
                                                                         'artist': 'Roddy Ricch Featuring Mustard',
                                                                         'song': 'High Fashion',
                                                                         'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Halsey You should be sad The Billboard Hot 100': {'rank': '34', 'artist': 'Halsey', 'song': 'You should be sad',
                                                       'img': 'https://charts-static.billboard.com/img/2020/01/halsey-iqm-you-should-be-sad-gqk-53x53.jpg'},
    'Kane Brown Homesick The Billboard Hot 100': {'rank': '35', 'artist': 'Kane Brown', 'song': 'Homesick',
                                                  'img': 'https://charts-static.billboard.com/img/2018/09/kane-brown-k3k-53x53.jpg'},
    'Gabby Barrett I Hope The Billboard Hot 100': {'rank': '36', 'artist': 'Gabby Barrett', 'song': 'I Hope',
                                                   'img': 'https://charts-static.billboard.com/img/2019/03/gabby-barrett-l86-i-hope-mnv-53x53.jpg'},
    'Lil Uzi Vert P2 The Billboard Hot 100': {'rank': '37', 'artist': 'Lil Uzi Vert', 'song': 'P2',
                                              'img': 'https://charts-static.billboard.com/img/2016/04/lil-uzi-vert-mre-87x87.jpg'},
    'Lil Mosey Blueberry Faygo The Billboard Hot 100': {'rank': '38', 'artist': 'Lil Mosey', 'song': 'Blueberry Faygo',
                                                        'img': 'https://charts-static.billboard.com/img/2018/09/lil-mosey-j5a-53x53.jpg'},
    'Jake Owen Homemade The Billboard Hot 100': {'rank': '39', 'artist': 'Jake Owen', 'song': 'Homemade',
                                                 'img': 'https://charts-static.billboard.com/img/2019/06/jake-owen-17q-homemade-uhu-53x53.jpg'},
    'Rod Wave Heart On Ice The Billboard Hot 100': {'rank': '40', 'artist': 'Rod Wave', 'song': 'Heart On Ice',
                                                    'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Uzi Vert That Way The Billboard Hot 100': {'rank': '41', 'artist': 'Lil Uzi Vert', 'song': 'That Way',
                                                    'img': 'https://charts-static.billboard.com/img/2016/04/lil-uzi-vert-mre-87x87.jpg'},
    'Lil Uzi Vert Lo Mein The Billboard Hot 100': {'rank': '42', 'artist': 'Lil Uzi Vert', 'song': 'Lo Mein',
                                                   'img': 'https://charts-static.billboard.com/img/2020/03/lil-uzi-vert-mre-lo-mein-92d-53x53.jpg'},
    'Demi Lovato I Love Me The Billboard Hot 100': {'rank': '43', 'artist': 'Demi Lovato', 'song': 'I Love Me',
                                                    'img': 'https://charts-static.billboard.com/img/2020/03/demi-lovato-sad-i-love-me-fqg-53x53.jpg'},
    'Lizzo Good As Hell The Billboard Hot 100': {'rank': '44', 'artist': 'Lizzo', 'song': 'Good As Hell',
                                                 'img': 'https://charts-static.billboard.com/img/2016/04/lizzo-w3u-good-as-hell-lpw-53x53.jpg'},
    'Lil Uzi Vert Lotus The Billboard Hot 100': {'rank': '45', 'artist': 'Lil Uzi Vert', 'song': 'Lotus',
                                                 'img': 'https://charts-static.billboard.com/img/2020/03/lil-uzi-vert-mre-lotus-7at-53x53.jpg'},
    'Russ & BIA BEST ON EARTH The Billboard Hot 100': {'rank': '46', 'artist': 'Russ & BIA', 'song': 'BEST ON EARTH',
                                                       'img': 'https://charts-static.billboard.com/img/2019/11/russ-rhp-best-on-earth-ykk-53x53.jpg'},
    'H.E.R. Featuring YG Slide The Billboard Hot 100': {'rank': '47', 'artist': 'H.E.R. Featuring YG', 'song': 'Slide',
                                                        'img': 'https://charts-static.billboard.com/img/2019/10/her-6td-slide-jvj-53x53.jpg'},
    'Jack Harlow WHATS POPPIN The Billboard Hot 100': {'rank': '48', 'artist': 'Jack Harlow', 'song': 'WHATS POPPIN',
                                                       'img': 'https://charts-static.billboard.com/img/2020/02/jack-harlow-ft9-whats-poppin-ddu-53x53.jpg'},
    'Luke Bryan What She Wants Tonight The Billboard Hot 100': {'rank': '49', 'artist': 'Luke Bryan',
                                                                'song': 'What She Wants Tonight',
                                                                'img': 'https://charts-static.billboard.com/img/2007/02/luke-bryan-kl4-53x53.jpg'},
    'Pop Smoke Dior The Billboard Hot 100': {'rank': '50', 'artist': 'Pop Smoke', 'song': 'Dior',
                                             'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Baby Sum 2 Prove The Billboard Hot 100': {'rank': '51', 'artist': 'Lil Baby', 'song': 'Sum 2 Prove',
                                                   'img': 'https://charts-static.billboard.com/img/2017/11/lil-baby-nwx-53x53.jpg'},
    'Lil Uzi Vert Silly Watch The Billboard Hot 100': {'rank': '52', 'artist': 'Lil Uzi Vert', 'song': 'Silly Watch',
                                                       'img': 'https://charts-static.billboard.com/img/2016/04/lil-uzi-vert-mre-87x87.jpg'},
    'Blake Shelton Duet With Gwen Stefani Nobody But You The Billboard Hot 100': {'rank': '53',
                                                                                  'artist': 'Blake Shelton Duet With Gwen Stefani',
                                                                                  'song': 'Nobody But You',
                                                                                  'img': 'https://charts-static.billboard.com/img/2019/12/blake-shelton-m3d-nobody-but-you-29g-53x53.jpg'},
    'Lil Uzi Vert Featuring Future Wassup The Billboard Hot 100': {'rank': '54',
                                                                   'artist': 'Lil Uzi Vert Featuring Future',
                                                                   'song': 'Wassup',
                                                                   'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    "Lil Yachty, Drake & DaBaby Oprah's Bank Account The Billboard Hot 100": {'rank': '55',
                                                                              'artist': 'Lil Yachty, Drake & DaBaby',
                                                                              'song': "Oprah's Bank Account",
                                                                              'img': 'https://charts-static.billboard.com/img/2020/03/lil-yachty-0f9-oprahs-bank-account-hhw-53x53.jpg'},
    'Ingrid Andress More Hearts Than Mine The Billboard Hot 100': {'rank': '56', 'artist': 'Ingrid Andress',
                                                                   'song': 'More Hearts Than Mine',
                                                                   'img': 'https://charts-static.billboard.com/img/2019/07/ingrid-andress-000-more-hearts-than-mine-qra-53x53.jpg'},
    'Jhene Aiko Featuring H.E.R. B.S. The Billboard Hot 100': {'rank': '57', 'artist': 'Jhene Aiko Featuring H.E.R.',
                                                               'song': 'B.S.',
                                                               'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    "Morgan Wallen Chasin' You The Billboard Hot 100": {'rank': '58', 'artist': 'Morgan Wallen', 'song': "Chasin' You",
                                                        'img': 'https://charts-static.billboard.com/img/2016/08/morgan-wallen-ur7-87x87.jpg'},
    'Jordan Davis Slow Dance In A Parking Lot The Billboard Hot 100': {'rank': '59', 'artist': 'Jordan Davis',
                                                                       'song': 'Slow Dance In A Parking Lot',
                                                                       'img': 'https://charts-static.billboard.com/img/2019/05/jordan-davis-err-slow-dance-in-a-parking-lot-1s8-53x53.jpg'},
    'Lil Uzi Vert Featuring Young Thug & Gunna Strawberry Peels The Billboard Hot 100': {'rank': '60',
                                                                                         'artist': 'Lil Uzi Vert Featuring Young Thug & Gunna',
                                                                                         'song': 'Strawberry Peels',
                                                                                         'img': 'https://charts-static.billboard.com/img/2020/03/lil-uzi-vert-mre-strawberry-peels-9ed-53x53.jpg'},
    'Jhene Aiko P*$$y Fairy (OTW) The Billboard Hot 100': {'rank': '61', 'artist': 'Jhene Aiko',
                                                           'song': 'P*$$y Fairy (OTW)',
                                                           'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Uzi Vert Moon Relate The Billboard Hot 100': {'rank': '62', 'artist': 'Lil Uzi Vert', 'song': 'Moon Relate',
                                                       'img': 'https://charts-static.billboard.com/img/2016/04/lil-uzi-vert-mre-87x87.jpg'},
    'Jonas Brothers What A Man Gotta Do The Billboard Hot 100': {'rank': '63', 'artist': 'Jonas Brothers',
                                                                 'song': 'What A Man Gotta Do',
                                                                 'img': 'https://charts-static.billboard.com/img/2020/01/jonas-brothers-r3d-what-a-man-gotta-do-nnf-53x53.jpg'},
    'Karol G & Nicki Minaj Tusa The Billboard Hot 100': {'rank': '64', 'artist': 'Karol G & Nicki Minaj',
                                                         'song': 'Tusa',
                                                         'img': 'https://charts-static.billboard.com/img/2019/11/karol-g-etl-tusa-3rn-53x53.jpg'},
    'Brett Young Catch The Billboard Hot 100': {'rank': '65', 'artist': 'Brett Young', 'song': 'Catch',
                                                'img': 'https://charts-static.billboard.com/img/2019/06/brett-young-9rw-catch-97n-53x53.jpg'},
    'Lil Uzi Vert I Can Show You The Billboard Hot 100': {'rank': '66', 'artist': 'Lil Uzi Vert',
                                                          'song': 'I Can Show You',
                                                          'img': 'https://charts-static.billboard.com/img/2016/04/lil-uzi-vert-mre-87x87.jpg'},
    'Jason Aldean We Back The Billboard Hot 100': {'rank': '67', 'artist': 'Jason Aldean', 'song': 'We Back',
                                                   'img': 'https://charts-static.billboard.com/img/2019/09/jason-aldean-sa0-we-back---7nx-53x53.jpg'},
    'Lil Uzi Vert Trap This Way (This Way) The Billboard Hot 100': {'rank': '68', 'artist': 'Lil Uzi Vert',
                                                                    'song': 'Trap This Way (This Way)',
                                                                    'img': 'https://charts-static.billboard.com/img/2020/03/lil-uzi-vert-mre-trap-this-way-this-way-rej-53x53.jpg'},
    'Riley Green I Wish Grandpas Never Died The Billboard Hot 100': {'rank': '69', 'artist': 'Riley Green',
                                                                     'song': 'I Wish Grandpas Never Died',
                                                                     'img': 'https://charts-static.billboard.com/img/2019/08/riley-green-000-i-wish-grandpas-never-died-kk6-53x53.jpg'},
    'Bad Bunny Si Veo A Tu Mama The Billboard Hot 100': {'rank': '70', 'artist': 'Bad Bunny',
                                                         'song': 'Si Veo A Tu Mama',
                                                         'img': 'https://charts-static.billboard.com/img/2016/10/bad-bunny-157-53x53.jpg'},
    'Powfu Featuring beabadoobee death bed The Billboard Hot 100': {'rank': '71',
                                                                    'artist': 'Powfu Featuring beabadoobee',
                                                                    'song': 'death bed',
                                                                    'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Uzi Vert Featuring NAV Leaders The Billboard Hot 100': {'rank': '72', 'artist': 'Lil Uzi Vert Featuring NAV',
                                                                 'song': 'Leaders',
                                                                 'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Baby & Gunna Heatin Up The Billboard Hot 100': {'rank': '73', 'artist': 'Lil Baby & Gunna',
                                                         'song': 'Heatin Up',
                                                         'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Surfaces Sunday Best The Billboard Hot 100': {'rank': '74', 'artist': 'Surfaces', 'song': 'Sunday Best',
                                                   'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Baby & 42 Dugg Grace The Billboard Hot 100': {'rank': '75', 'artist': 'Lil Baby & 42 Dugg', 'song': 'Grace',
                                                       'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Uzi Vert Featuring Lil Durk No Auto The Billboard Hot 100': {'rank': '76',
                                                                      'artist': 'Lil Uzi Vert Featuring Lil Durk',
                                                                      'song': 'No Auto',
                                                                      'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'SZA X Justin Timberlake The Other Side The Billboard Hot 100': {'rank': '77', 'artist': 'SZA X Justin Timberlake',
                                                                     'song': 'The Other Side',
                                                                     'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Justin Bieber Yummy The Billboard Hot 100': {'rank': '78', 'artist': 'Justin Bieber', 'song': 'Yummy',
                                                  'img': 'https://charts-static.billboard.com/img/2020/01/justin-bieber-4oh-yummy-vs5-53x53.jpg'},
    'Megan Thee Stallion B.I.T.C.H. The Billboard Hot 100': {'rank': '79', 'artist': 'Megan Thee Stallion',
                                                             'song': 'B.I.T.C.H.',
                                                             'img': 'https://charts-static.billboard.com/img/2019/01/megan-thee-stallion-fnn-87x87.jpg'},
    'Bad Bunny La Dificil The Billboard Hot 100': {'rank': '80', 'artist': 'Bad Bunny', 'song': 'La Dificil',
                                                   'img': 'https://charts-static.billboard.com/img/2016/10/bad-bunny-157-53x53.jpg'},
    "Carly Pearce & Lee Brice I Hope You're Happy Now The Billboard Hot 100": {'rank': '81',
                                                                               'artist': 'Carly Pearce & Lee Brice',
                                                                               'song': "I Hope You're Happy Now",
                                                                               'img': 'https://charts-static.billboard.com/img/2019/10/carly-pearce-rdp-i-hope-youre-happy-now-1s8-53x53.jpg'},
    'Lil Uzi Vert Homecoming The Billboard Hot 100': {'rank': '82', 'artist': 'Lil Uzi Vert', 'song': 'Homecoming',
                                                      'img': 'https://charts-static.billboard.com/img/2020/03/lil-uzi-vert-mre-homecoming-px6-53x53.jpg'},
    'Lil Uzi Vert Come This Way The Billboard Hot 100': {'rank': '83', 'artist': 'Lil Uzi Vert',
                                                         'song': 'Come This Way',
                                                         'img': 'https://charts-static.billboard.com/img/2016/04/lil-uzi-vert-mre-87x87.jpg'},
    'Sam Smith To Die For The Billboard Hot 100': {'rank': '84', 'artist': 'Sam Smith', 'song': 'To Die For',
                                                   'img': 'https://charts-static.billboard.com/img/2020/02/sam-smith-ik0-to-die-for-e6v-53x53.jpg'},
    'Lil Baby Emotionally Scarred The Billboard Hot 100': {'rank': '85', 'artist': 'Lil Baby',
                                                           'song': 'Emotionally Scarred',
                                                           'img': 'https://charts-static.billboard.com/img/2017/11/lil-baby-nwx-53x53.jpg'},
    'Luke Combs Featuring Eric Church Does To Me The Billboard Hot 100': {'rank': '86',
                                                                          'artist': 'Luke Combs Featuring Eric Church',
                                                                          'song': 'Does To Me',
                                                                          'img': 'https://charts-static.billboard.com/img/2019/11/luke-combs-m9g-does-to-me-9ea-53x53.jpg'},
    'Lil Uzi Vert Featuring Young Thug Got The Guap The Billboard Hot 100': {'rank': '87',
                                                                             'artist': 'Lil Uzi Vert Featuring Young Thug',
                                                                             'song': 'Got The Guap',
                                                                             'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'BENEE Featuring Gus Dapperton Supalonely The Billboard Hot 100': {'rank': '88',
                                                                       'artist': 'BENEE Featuring Gus Dapperton',
                                                                       'song': 'Supalonely',
                                                                       'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lil Uzi Vert Featuring Young Nudy Money Spread The Billboard Hot 100': {'rank': '89',
                                                                             'artist': 'Lil Uzi Vert Featuring Young Nudy',
                                                                             'song': 'Money Spread',
                                                                             'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Don Toliver Cardigan The Billboard Hot 100': {'rank': '90', 'artist': 'Don Toliver', 'song': 'Cardigan',
                                                   'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    "Thomas Rhett Featuring Jon Pardi Beer Can't Fix The Billboard Hot 100": {'rank': '91',
                                                                              'artist': 'Thomas Rhett Featuring Jon Pardi',
                                                                              'song': "Beer Can't Fix",
                                                                              'img': 'https://charts-static.billboard.com/img/2019/06/thomas-rhett-2w0-beer-cant-fix-1ze-53x53.jpg'},
    'Bad Bunny Vete The Billboard Hot 100': {'rank': '92', 'artist': 'Bad Bunny', 'song': 'Vete',
                                             'img': 'https://charts-static.billboard.com/img/2016/10/bad-bunny-157-53x53.jpg'},
    'Khalid x Disclosure Know Your Worth The Billboard Hot 100': {'rank': '93', 'artist': 'Khalid x Disclosure',
                                                                  'song': 'Know Your Worth',
                                                                  'img': 'https://charts-static.billboard.com/img/2020/02/khalid-p0u-know-your-worth-afz-53x53.jpg'},
    'Lil Uzi Vert Futsal Shuffle 2020 The Billboard Hot 100': {'rank': '94', 'artist': 'Lil Uzi Vert',
                                                               'song': 'Futsal Shuffle 2020',
                                                               'img': 'https://charts-static.billboard.com/img/2019/12/lil-uzi-vert-mre-futsal-shuffle-2020-h3e-53x53.jpg'},
    'Lil Uzi Vert Prices The Billboard Hot 100': {'rank': '95', 'artist': 'Lil Uzi Vert', 'song': 'Prices',
                                                  'img': 'https://charts-static.billboard.com/img/2016/04/lil-uzi-vert-mre-87x87.jpg'},
    'Polo G Featuring NLE Choppa & Stunna 4 Vegas Go Stupid The Billboard Hot 100': {'rank': '96',
                                                                                     'artist': 'Polo G Featuring NLE Choppa & Stunna 4 Vegas',
                                                                                     'song': 'Go Stupid',
                                                                                     'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'Lewis Capaldi Before You Go The Billboard Hot 100': {'rank': '97', 'artist': 'Lewis Capaldi',
                                                          'song': 'Before You Go',
                                                          'img': 'https://charts-static.billboard.com/img/2017/04/lewis-capaldi-s2h-53x53.jpg'},
    'Megan Thee Stallion Savage The Billboard Hot 100': {'rank': '98', 'artist': 'Megan Thee Stallion',
                                                         'song': 'Savage',
                                                         'img': 'https://charts-static.billboard.com/img/2020/03/megan-thee-stallion-fnn-savage-2lf-53x53.jpg'},
    'Summer Walker & Usher Come Thru The Billboard Hot 100': {'rank': '99', 'artist': 'Summer Walker & Usher',
                                                              'song': 'Come Thru',
                                                              'img': 'https://www.billboard.com/assets/1585328969/images/charts/bb-placeholder-new.jpg?4118ff5c23d0f1304dc5'},
    'YoungBoy Never Broke Again Make No Sense The Billboard Hot 100': {'rank': '100',
                                                                       'artist': 'YoungBoy Never Broke Again',
                                                                       'song': 'Make No Sense',
                                                                       'img': 'https://charts-static.billboard.com/img/2017/06/youngboy-never-broke-again-cu3-53x53.jpg'}}


def selector(query):
    if query == 'hot 100 chart':
        return Music2().chart()
    elif query == 'hot 100 billboard playlist':
        return billboard_playlist()
    elif query[:len('billboard most popular ')] == 'billboard most popular ':
        msg = query[len('billboard most popular '):]
        if '-' in msg:
            return BillboardMusic().most_popular(msg.strip())
        else:
            chart = sim_main(msg)
            if chart == 0:
                reply = 'sorry i could not find chart'
                return {'display': reply, 'say': reply}
            else:
                return BillboardMusic().most_popular(chart)
    elif query[:len('billboard play most popular ')] == 'billboard play most popular ':
        msg = query[len('billboard play most popular '):]
        if '-' in msg:
            return BillboardMusic().play_most_popular(msg.strip())
        else:
            chart = sim_main(msg)
            if chart == 0:
                reply = 'sorry i could not find chart'
                return {'display': reply, 'say': reply}
            else:
                return BillboardMusic().play_most_popular(chart)
    elif query[:len('billboard chart ')] == 'billboard chart ':
        msg = query[len('billboard chart '):]
        if '-' in msg:
            return BillboardMusic().chart_songs(msg.strip())
        else:
            chart = sim_main(msg)
            if chart == 0:
                reply = 'sorry i could not find chart'
                return {'display': reply, 'say': reply}
            else:
                return BillboardMusic().chart_songs(chart)
    else:
        return {'display': 'nothing to show', 'say': 'nothing to show'}


class Music:
    def __init__(self):
        url = 'https://www.billboard.com/charts/hot-100'
        page = requests.get(url, headers=config.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.main_li = soup.find_all("li", {"class": "chart-list__element display--flex"})
        self.songs = {**self.get_songs}

    @property
    def get_songs(self):
        songs = {}
        for li in self.main_li:
            song = li.find("span",
                           {"class": "chart-element__information__song text--truncate color--primary"}).get_text()
            artist = li.find("span",
                             {"class": "chart-element__information__artist text--truncate color--secondary"}).get_text()
            rank = li.find("span",
                           {"class": "chart-element__rank__number"}).get_text()
            last_week = li.find("span",
                                {"class": "chart-element__meta text--center color--secondary text--last"}).get_text()
            peak = li.find("span",
                           {"class": "chart-element__meta text--center color--secondary text--peak"}).get_text()
            weeks_on_chat = li.find("span",
                                    {
                                        "class": "chart-element__meta text--center color--secondary text--week"}).get_text()
            img = li.find("span", {"class": "chart-element__image flex--no-shrink"}).get('style')
            if img != '':
                img = img.split("'")[1]
            else:
                img = 'billboard.jpg'
            songs[song + ' ' + artist] = {"artist": artist, "rank": rank, "last_week": last_week, "peak": peak,
                                          "duration": weeks_on_chat, "img": img, 'song': song}
        return songs

    def random_song(self):
        try:
            return r.choice(list(self.get_songs))
        except Exception:
            return r.choice(list(hot_songs))

    def playlist(self, no=5):
        if no > 10:
            no = 10
        try:
            songs = self.get_songs
            items = list(songs)[:no]
            plays = ''
            for item in items:
                plays += item + ','
            return plays[:-1]
        except Exception:
            items = list(hot_songs)[:no]
            plays = ''
            for item in items:
                plays += item + ','
            return plays[:-1]

    @staticmethod
    def find(search):
        vid_url = 'https://www.youtube.com/watch?v='
        url = "https://www.youtube.com/results?search_query="
        req = url + search
        page = requests.get(req, headers=config.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        load = soup.find("div", {"id": "img-preload"})
        if load:
            li = load.find_all("img")
            try:
                return vid_url+li[0].get("src").split('/')[4]
            except IndexError:
                return url+search
        else:
            return url + search

    def get_vids(self):
        print('processing, please wait...')
        result_list = {}
        pool = ThreadPool(processes=len(self.songs))
        for i in self.songs:
            result_list[i] = pool.apply_async(self.find, (i,))
        songs = self.songs
        for i in result_list:
            songs[i]['url'] = result_list[i].get()
        return songs

    def chart(self):
        global hot_songs
        try:
            diff = datetime.datetime.now() - date
            if diff.days > 7:
                hot_songs = self.get_vids()
                print(hot_songs)
            else:
                self.songs = hot_songs
        except AttributeError:
            self.songs = hot_songs
        display = "<table id='t01'>\
                      <tr>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Rank</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Song</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Artist</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Last Week</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Peak</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Duration</p></th>\
                        <th></th>\
                      </tr>\
                    "
        for song in self.songs.values():
            display += f"<tr onclick='open_link(" + f'"{song["url"]}"' + f")'>\
                            <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{song['rank']}</p></td>\
                            <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{song['song']}</p></td>\
                            <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{song['artist']}</p></td>\
                            <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{song['last_week']}</p></td>\
                            <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{song['peak']}</p></td>\
                            <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{song['duration']}</p></td>\
                            <td><img src='{song['img']}' alt='{song['artist']} image' width='60px'></td>\
                        </tr> \
                       "
        display += '</table>'
        return {'display': display, 'say': 'find displayed the hot 100 chart list'}


class Music2:
    def __init__(self):
        try:
            diff = datetime.datetime.now() - date
            if diff.days > 7:
                url = 'https://www.billboard.com/charts/hot-100'
                page = requests.get(url, headers=config.header)
                soup = BeautifulSoup(page.content, 'html.parser')
                self.main_li = soup.find_all("li", {"class": "chart-list__element display--flex"})
                self.songs = {**self.get_songs}
                self.songs = self.get_vids()
                path = r'C:\Users\emyli\PycharmProjects\Chatbot_Project\rihanna_bot\hot100_data.py'
                file = open(path, 'w', encoding='utf-8')
                file.write('import datetime\n')
                file.write(f'hot_songs = {self.songs}\n')
                now = datetime.datetime.now()
                file.write(f'date = datetime.datetime'
                           f'{(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)}\n')
                file.close()
            else:
                self.songs = hot_songs
        except AttributeError:
            self.songs = hot_songs

    @property
    def get_songs(self):
        songs = {}
        for li in self.main_li:
            song = li.find("span",
                           {"class": "chart-element__information__song text--truncate color--primary"}).get_text()
            artist = li.find("span",
                             {"class": "chart-element__information__artist text--truncate color--secondary"}).get_text()
            rank = li.find("span",
                           {"class": "chart-element__rank__number"}).get_text()
            last_week = li.find("span",
                                {"class": "chart-element__meta text--center color--secondary text--last"}).get_text()
            peak = li.find("span",
                           {"class": "chart-element__meta text--center color--secondary text--peak"}).get_text()
            weeks_on_chat = li.find("span",
                                    {
                                        "class": "chart-element__meta text--center color--secondary text--week"}).get_text()
            img = li.find("span", {"class": "chart-element__image flex--no-shrink"}).get('style')
            if img != '':
                img = img.split("'")[1]
            else:
                img = 'billboard.jpg'
            songs[song + ' ' + artist] = {"artist": artist, "rank": rank, "last_week": last_week, "peak": peak,
                                          "duration": weeks_on_chat, "img": img, 'song': song}
        return songs

    def random_song(self):
        try:
            return r.choice(list(self.get_songs))
        except Exception:
            return r.choice(list(hot_songs))

    def playlist(self, no=5):
        if no > 10:
            no = 10
        try:
            songs = self.get_songs
            items = list(songs)[:no]
            plays = ''
            for item in items:
                plays += item + ','
            return plays[:-1]
        except Exception:
            items = list(hot_songs)[:no]
            plays = ''
            for item in items:
                plays += item + ','
            return plays[:-1]

    @staticmethod
    def find(search):
        vid_url = 'https://www.youtube.com/watch?v='
        url = "https://www.youtube.com/results?search_query="
        req = url + search
        page = requests.get(req, headers=config.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        load = soup.find("div", {"id": "img-preload"})
        if load:
            li = load.find_all("img")
            try:
                return vid_url+li[0].get("src").split('/')[4]
            except IndexError:
                return url+search
        else:
            return url + search

    def get_vids(self):
        print('processing, please wait...')
        result_list = {}
        vid_url = 'https://www.youtube.com/watch?v='
        url = "https://www.youtube.com/results?search_query="
        pool = ThreadPool(processes=30)
        songs = self.songs
        for i in self.songs:
            if i in hot_songs:
                songs[i]['url'] = hot_songs[i]['url']
            else:
                # pool.apply_async(self.get_data, (i,))
                result_list[i] = pool.apply_async(Youtube().get_data, (i,))

        for i in result_list:
            if type(result_list[i]).__name__ == 'dict':
                songs[i]['url'] = vid_url + result_list[i]['videoID']
            else:
                print(i)
                item = result_list[i].get()
                if item:
                    songs[i]['url'] = vid_url + item['videoID']
                else:
                    songs[i]['url'] = url + i
        return songs

    def chart(self):
        display = "<table id='t01'>\
                      <tr>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Rank</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Song</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Artist</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Last Week</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Peak</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Duration</p></th>\
                        <th></th>\
                      </tr>\
                    "
        for song in self.songs.values():
            display += f"<tr onclick='open_link(" + f'"{song["url"]}"' + f")'>\
                            <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{song['rank']}</p></td>\
                            <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{song['song']}</p></td>\
                            <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{song['artist']}</p></td>\
                            <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{song['last_week']}</p></td>\
                            <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{song['peak']}</p></td>\
                            <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{song['duration']}</p></td>\
                            <td><img src='{song['img']}' alt='{song['artist']} image' width='60px'></td>\
                        </tr> \
                       "
        display += '</table>'
        return {'display': display, 'say': 'find displayed the hot 100 chart list'}

    def billboard_playlist(self):
        playlist = ''
        for song in self.songs.values():
            if 'v=' in song['url']:
                vid = song['url'].split('v=')[1]
                playlist += vid + ','

        display = f'<iframe width="560" height="315"\
                                src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                  f'playlist={playlist[playlist.index(",")+1:-1]}&loop=1" frameborder="0" allowfullscreen>\
                </iframe>'
        say = f"playing Billboard Hot 100 chart video playist from youtube"
        reply = {'display': display, 'say': say}
        return reply


# most popular song in the uk
class BillboardMusic:
    def __init__(self):
        self.charts = billboard.charts()
        self.chart = billboard.ChartData

    def most_popular(self, query):
        try:
            song = self.chart(query).entries[0].__dict__
            reply = f'{query.replace("-", " ")}: {song["title"]} by {song["artist"]}'
            return {'display': reply, 'say': reply}
        except Exception:
            reply = 'bug has been detected in billboard most popular'
            return {'display': reply, 'say': reply}

    def play_most_popular(self, query):
        try:
            song_details = self.chart(query).entries[0].__dict__
            song = song_details['title'] + ' ' + song_details['artist']
            return Youtube().search_youtube(song)
        except Exception:
            reply = 'bug has been detected in billboard play most popular'
            return {'display': reply, 'say': reply}

    def chart_songs(self, query):
        # try:
        chart_details = self.chart(query).entries
        display = "<table id='t01'>\
                              <tr>\
        <td><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Rank</p></td>"
        for i in chart_details[0].__dict__:
            if (i != 'rank') and (i != 'image') and (i != 'isNew') and (chart_details[0].__dict__[i]):
                display += f"<th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>{i.title()}</p></th>"

        display += "<th></th>\
                     </tr>"
        for song in chart_details:
            display += f"<tr>\
                        <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{song.rank}</p></td>"
            for item in song.__dict__:
                if (item != 'rank') and (item != 'image') and (item != 'isNew') and (chart_details[0].__dict__[item]):
                    d = song.__dict__
                    display += f"<td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{d[item]}</p></td>"
            if song.image and (requests.get(song.image).status_code == 200):
                display += f"<td><img src='{song.image}' alt='{song.artist} image' width='60px'></td>\
                        </tr>"
            else:
                display += f"<td><img src='billboard.jpg' alt='{song.artist} image' width='60px'></td>\
                                        </tr>"
        display += '</table>'
        return {'display': display, 'say': 'find chart below'}
        # except Exception:
        #     reply = 'bug has been detected in billboard chart songs'
        #     return {'display': reply, 'say': reply}


# a = Music2().chart()
# print(a)

# most popular song in italy, canada, germany, france, uk, us
# most popular rap song, pop song, rock song, latin song
# https://github.com/guoguo12/billboard-charts
#
# a = BillboardMusic().chart_songs('hot-100')
# print(a)