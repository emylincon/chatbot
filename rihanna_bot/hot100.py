import requests
from bs4 import BeautifulSoup
import config
import random as r

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
hot_songs = {'The Box Roddy Ricch': {'artist': 'Roddy Ricch', 'rank': '1', 'last_week': '1', 'peak': '1', 'weeks on chart': '15', 'img': 'https://charts-static.billboard.com/img/2019/12/roddy-ricch-eqp-the-box-2k7-53x53.jpg', 'song': 'The Box'}, 'Blinding Lights The Weeknd': {'artist': 'The Weeknd', 'rank': '2', 'last_week': '4', 'peak': '2', 'weeks on chart': '16', 'img': 'https://charts-static.billboard.com/img/2019/12/the-weeknd-pqn-blinding-lights-gfd-53x53.jpg', 'song': 'Blinding Lights'}, "Don't Start Now Dua Lipa": {'artist': 'Dua Lipa', 'rank': '3', 'last_week': '2', 'peak': '2', 'weeks on chart': '20', 'img': 'https://charts-static.billboard.com/img/2019/11/dua-lipa-5k0-dont-start-now-7wb-53x53.jpg', 'song': "Don't Start Now"}, 'Life Is Good Future Featuring Drake': {'artist': 'Future Featuring Drake', 'rank': '4', 'last_week': '3', 'peak': '2', 'weeks on chart': '10', 'img': 'https://charts-static.billboard.com/img/2020/01/future-tsu-life-is-good-rko-53x53.jpg', 'song': 'Life Is Good'}, 'Circles Post Malone': {'artist': 'Post Malone', 'rank': '5', 'last_week': '5', 'peak': '1', 'weeks on chart': '29', 'img': 'https://charts-static.billboard.com/img/2019/09/post-malone-tp6-circles-sb0-53x53.jpg', 'song': 'Circles'}, 'Roxanne Arizona Zervas': {'artist': 'Arizona Zervas', 'rank': '6', 'last_week': '7', 'peak': '4', 'weeks on chart': '20', 'img': 'billboard.jpg', 'song': 'Roxanne'}, 'Adore You Harry Styles': {'artist': 'Harry Styles', 'rank': '7', 'last_week': '16', 'peak': '7', 'weeks on chart': '15', 'img': 'billboard.jpg', 'song': 'Adore You'}, 'Intentions Justin Bieber Featuring Quavo': {'artist': 'Justin Bieber Featuring Quavo', 'rank': '8', 'last_week': '10', 'peak': '8', 'weeks on chart': '6', 'img': 'billboard.jpg', 'song': 'Intentions'}, 'Someone You Loved Lewis Capaldi': {'artist': 'Lewis Capaldi', 'rank': '9', 'last_week': '15', 'peak': '1', 'weeks on chart': '45', 'img': 'billboard.jpg', 'song': 'Someone You Loved'}, 'everything i wanted Billie Eilish': {'artist': 'Billie Eilish', 'rank': '10', 'last_week': '14', 'peak': '8', 'weeks on chart': '19', 'img': 'billboard.jpg', 'song': 'everything i wanted'}, 'Hot Girl Bummer blackbear': {'artist': 'blackbear', 'rank': '11', 'last_week': '17', 'peak': '11', 'weeks on chart': '27', 'img': 'billboard.jpg', 'song': 'Hot Girl Bummer'}, 'Memories Maroon 5': {'artist': 'Maroon 5', 'rank': '12', 'last_week': '13', 'peak': '2', 'weeks on chart': '26', 'img': 'billboard.jpg', 'song': 'Memories'}, 'Myron Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '13', 'last_week': '-', 'peak': '13', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Myron'}, 'Say So Doja Cat': {'artist': 'Doja Cat', 'rank': '14', 'last_week': '19', 'peak': '14', 'weeks on chart': '11', 'img': 'billboard.jpg', 'song': 'Say So'}, 'Dance Monkey Tones And I': {'artist': 'Tones And I', 'rank': '15', 'last_week': '12', 'peak': '4', 'weeks on chart': '24', 'img': 'billboard.jpg', 'song': 'Dance Monkey'}, 'Heartless The Weeknd': {'artist': 'The Weeknd', 'rank': '16', 'last_week': '21', 'peak': '1', 'weeks on chart': '17', 'img': 'billboard.jpg', 'song': 'Heartless'}, 'The Bones Maren Morris': {'artist': 'Maren Morris', 'rank': '17', 'last_week': '23', 'peak': '17', 'weeks on chart': '26', 'img': 'billboard.jpg', 'song': 'The Bones'}, 'My Oh My Camila Cabello Featuring DaBaby': {'artist': 'Camila Cabello Featuring DaBaby', 'rank': '18', 'last_week': '26', 'peak': '18', 'weeks on chart': '15', 'img': 'billboard.jpg', 'song': 'My Oh My'}, 'Bean (Kobe) Lil Uzi Vert Featuring Chief Keef': {'artist': 'Lil Uzi Vert Featuring Chief Keef', 'rank': '19', 'last_week': '-', 'peak': '19', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Bean (Kobe)'}, 'Suicidal YNW Melly & Juice WRLD': {'artist': 'YNW Melly & Juice WRLD', 'rank': '20', 'last_week': '-', 'peak': '20', 'weeks on chart': '16', 'img': 'billboard.jpg', 'song': 'Suicidal'}, "Ballin' Mustard & Roddy Ricch": {'artist': 'Mustard & Roddy Ricch', 'rank': '21', 'last_week': '29', 'peak': '11', 'weeks on chart': '35', 'img': 'billboard.jpg', 'song': "Ballin'"}, '10,000 Hours Dan + Shay & Justin Bieber': {'artist': 'Dan + Shay & Justin Bieber', 'rank': '22', 'last_week': '27', 'peak': '4', 'weeks on chart': '24', 'img': 'billboard.jpg', 'song': '10,000 Hours'}, 'Godzilla Eminem Featuring Juice WRLD': {'artist': 'Eminem Featuring Juice WRLD', 'rank': '23', 'last_week': '32', 'peak': '3', 'weeks on chart': '9', 'img': 'billboard.jpg', 'song': 'Godzilla'}, 'BOP DaBaby': {'artist': 'DaBaby', 'rank': '24', 'last_week': '35', 'peak': '11', 'weeks on chart': '25', 'img': 'billboard.jpg', 'song': 'BOP'}, 'Stupid Love Lady Gaga': {'artist': 'Lady Gaga', 'rank': '25', 'last_week': '30', 'peak': '5', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'Stupid Love'}, 'Yessirskiii Lil Uzi Vert & 21 Savage': {'artist': 'Lil Uzi Vert & 21 Savage', 'rank': '26', 'last_week': '-', 'peak': '26', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Yessirskiii'}, 'Baby Pluto Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '27', 'last_week': '6', 'peak': '6', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': 'Baby Pluto'}, 'Woah Lil Baby': {'artist': 'Lil Baby', 'rank': '28', 'last_week': '31', 'peak': '15', 'weeks on chart': '19', 'img': 'billboard.jpg', 'song': 'Woah'}, 'Falling Trevor Daniel': {'artist': 'Trevor Daniel', 'rank': '29', 'last_week': '42', 'peak': '25', 'weeks on chart': '18', 'img': 'billboard.jpg', 'song': 'Falling'}, 'RITMO (Bad Boys For Life) The Black Eyed Peas X J Balvin': {'artist': 'The Black Eyed Peas X J Balvin', 'rank': '30', 'last_week': '47', 'peak': '30', 'weeks on chart': '17', 'img': 'billboard.jpg', 'song': 'RITMO (Bad Boys For Life)'}, 'Lose You To Love Me Selena Gomez': {'artist': 'Selena Gomez', 'rank': '31', 'last_week': '38', 'peak': '1', 'weeks on chart': '22', 'img': 'billboard.jpg', 'song': 'Lose You To Love Me'}, 'No Guidance Chris Brown Featuring Drake': {'artist': 'Chris Brown Featuring Drake', 'rank': '32', 'last_week': '46', 'peak': '5', 'weeks on chart': '41', 'img': 'billboard.jpg', 'song': 'No Guidance'}, 'High Fashion Roddy Ricch Featuring Mustard': {'artist': 'Roddy Ricch Featuring Mustard', 'rank': '33', 'last_week': '43', 'peak': '20', 'weeks on chart': '12', 'img': 'billboard.jpg', 'song': 'High Fashion'}, 'You should be sad Halsey': {'artist': 'Halsey', 'rank': '34', 'last_week': '41', 'peak': '26', 'weeks on chart': '10', 'img': 'billboard.jpg', 'song': 'You should be sad'}, 'Homesick Kane Brown': {'artist': 'Kane Brown', 'rank': '35', 'last_week': '44', 'peak': '35', 'weeks on chart': '18', 'img': 'billboard.jpg', 'song': 'Homesick'}, 'I Hope Gabby Barrett': {'artist': 'Gabby Barrett', 'rank': '36', 'last_week': '50', 'peak': '36', 'weeks on chart': '12', 'img': 'billboard.jpg', 'song': 'I Hope'}, 'P2 Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '37', 'last_week': '11', 'peak': '11', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': 'P2'}, 'Blueberry Faygo Lil Mosey': {'artist': 'Lil Mosey', 'rank': '38', 'last_week': '53', 'peak': '38', 'weeks on chart': '6', 'img': 'billboard.jpg', 'song': 'Blueberry Faygo'}, 'Homemade Jake Owen': {'artist': 'Jake Owen', 'rank': '39', 'last_week': '60', 'peak': '39', 'weeks on chart': '8', 'img': 'billboard.jpg', 'song': 'Homemade'}, 'Heart On Ice Rod Wave': {'artist': 'Rod Wave', 'rank': '40', 'last_week': '58', 'peak': '40', 'weeks on chart': '19', 'img': 'billboard.jpg', 'song': 'Heart On Ice'}, 'That Way Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '41', 'last_week': '20', 'peak': '20', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'That Way'}, 'Lo Mein Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '42', 'last_week': '8', 'peak': '8', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': 'Lo Mein'}, 'I Love Me Demi Lovato': {'artist': 'Demi Lovato', 'rank': '43', 'last_week': '18', 'peak': '18', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': 'I Love Me'}, 'Good As Hell Lizzo': {'artist': 'Lizzo', 'rank': '44', 'last_week': '49', 'peak': '3', 'weeks on chart': '30', 'img': 'billboard.jpg', 'song': 'Good As Hell'}, 'Lotus Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '45', 'last_week': '-', 'peak': '45', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Lotus'}, 'BEST ON EARTH Russ & BIA': {'artist': 'Russ & BIA', 'rank': '46', 'last_week': '62', 'peak': '46', 'weeks on chart': '15', 'img': 'billboard.jpg', 'song': 'BEST ON EARTH'}, 'Slide H.E.R. Featuring YG': {'artist': 'H.E.R. Featuring YG', 'rank': '47', 'last_week': '61', 'peak': '47', 'weeks on chart': '13', 'img': 'billboard.jpg', 'song': 'Slide'}, 'WHATS POPPIN Jack Harlow': {'artist': 'Jack Harlow', 'rank': '48', 'last_week': '73', 'peak': '48', 'weeks on chart': '6', 'img': 'billboard.jpg', 'song': 'WHATS POPPIN'}, 'What She Wants Tonight Luke Bryan': {'artist': 'Luke Bryan', 'rank': '49', 'last_week': '78', 'peak': '49', 'weeks on chart': '13', 'img': 'billboard.jpg', 'song': 'What She Wants Tonight'}, 'Dior Pop Smoke': {'artist': 'Pop Smoke', 'rank': '50', 'last_week': '55', 'peak': '30', 'weeks on chart': '5', 'img': 'billboard.jpg', 'song': 'Dior'}, 'Sum 2 Prove Lil Baby': {'artist': 'Lil Baby', 'rank': '51', 'last_week': '52', 'peak': '16', 'weeks on chart': '10', 'img': 'billboard.jpg', 'song': 'Sum 2 Prove'}, 'Silly Watch Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '52', 'last_week': '9', 'peak': '9', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': 'Silly Watch'}, 'Nobody But You Blake Shelton Duet With Gwen Stefani': {'artist': 'Blake Shelton Duet With Gwen Stefani', 'rank': '53', 'last_week': '69', 'peak': '43', 'weeks on chart': '10', 'img': 'billboard.jpg', 'song': 'Nobody But You'}, 'Wassup Lil Uzi Vert Featuring Future': {'artist': 'Lil Uzi Vert Featuring Future', 'rank': '54', 'last_week': '-', 'peak': '54', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Wassup'}, "Oprah's Bank Account Lil Yachty, Drake & DaBaby": {'artist': 'Lil Yachty, Drake & DaBaby', 'rank': '55', 'last_week': '89', 'peak': '55', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': "Oprah's Bank Account"}, 'More Hearts Than Mine Ingrid Andress': {'artist': 'Ingrid Andress', 'rank': '56', 'last_week': '85', 'peak': '56', 'weeks on chart': '12', 'img': 'billboard.jpg', 'song': 'More Hearts Than Mine'}, 'B.S. Jhene Aiko Featuring H.E.R.': {'artist': 'Jhene Aiko Featuring H.E.R.', 'rank': '57', 'last_week': '24', 'peak': '24', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': 'B.S.'}, "Chasin' You Morgan Wallen": {'artist': 'Morgan Wallen', 'rank': '58', 'last_week': '70', 'peak': '58', 'weeks on chart': '8', 'img': 'billboard.jpg', 'song': "Chasin' You"}, 'Slow Dance In A Parking Lot Jordan Davis': {'artist': 'Jordan Davis', 'rank': '59', 'last_week': '77', 'peak': '59', 'weeks on chart': '11', 'img': 'billboard.jpg', 'song': 'Slow Dance In A Parking Lot'}, 'Strawberry Peels Lil Uzi Vert Featuring Young Thug & Gunna': {'artist': 'Lil Uzi Vert Featuring Young Thug & Gunna', 'rank': '60', 'last_week': '-', 'peak': '60', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Strawberry Peels'}, 'P*$$y Fairy (OTW) Jhene Aiko': {'artist': 'Jhene Aiko', 'rank': '61', 'last_week': '40', 'peak': '40', 'weeks on chart': '9', 'img': 'billboard.jpg', 'song': 'P*$$y Fairy (OTW)'}, 'Moon Relate Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '62', 'last_week': '-', 'peak': '62', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Moon Relate'}, 'What A Man Gotta Do Jonas Brothers': {'artist': 'Jonas Brothers', 'rank': '63', 'last_week': '63', 'peak': '16', 'weeks on chart': '9', 'img': 'billboard.jpg', 'song': 'What A Man Gotta Do'}, 'Tusa Karol G & Nicki Minaj': {'artist': 'Karol G & Nicki Minaj', 'rank': '64', 'last_week': '75', 'peak': '42', 'weeks on chart': '16', 'img': 'billboard.jpg', 'song': 'Tusa'}, 'Catch Brett Young': {'artist': 'Brett Young', 'rank': '65', 'last_week': '86', 'peak': '65', 'weeks on chart': '8', 'img': 'billboard.jpg', 'song': 'Catch'}, 'I Can Show You Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '66', 'last_week': '-', 'peak': '66', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'I Can Show You'}, 'We Back Jason Aldean': {'artist': 'Jason Aldean', 'rank': '67', 'last_week': '81', 'peak': '62', 'weeks on chart': '16', 'img': 'billboard.jpg', 'song': 'We Back'}, 'Trap This Way (This Way) Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '68', 'last_week': '-', 'peak': '68', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Trap This Way (This Way)'}, 'I Wish Grandpas Never Died Riley Green': {'artist': 'Riley Green', 'rank': '69', 'last_week': '82', 'peak': '66', 'weeks on chart': '12', 'img': 'billboard.jpg', 'song': 'I Wish Grandpas Never Died'}, 'Si Veo A Tu Mama Bad Bunny': {'artist': 'Bad Bunny', 'rank': '70', 'last_week': '56', 'peak': '32', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'Si Veo A Tu Mama'}, 'death bed Powfu Featuring beabadoobee': {'artist': 'Powfu Featuring beabadoobee', 'rank': '71', 'last_week': '-', 'peak': '71', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'death bed'}, 'Leaders Lil Uzi Vert Featuring NAV': {'artist': 'Lil Uzi Vert Featuring NAV', 'rank': '72', 'last_week': '-', 'peak': '72', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Leaders'}, 'Heatin Up Lil Baby & Gunna': {'artist': 'Lil Baby & Gunna', 'rank': '73', 'last_week': '57', 'peak': '18', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'Heatin Up'}, 'Sunday Best Surfaces': {'artist': 'Surfaces', 'rank': '74', 'last_week': '99', 'peak': '74', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'Sunday Best'}, 'Grace Lil Baby & 42 Dugg': {'artist': 'Lil Baby & 42 Dugg', 'rank': '75', 'last_week': '98', 'peak': '48', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'Grace'}, 'No Auto Lil Uzi Vert Featuring Lil Durk': {'artist': 'Lil Uzi Vert Featuring Lil Durk', 'rank': '76', 'last_week': '-', 'peak': '76', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'No Auto'}, 'The Other Side SZA X Justin Timberlake': {'artist': 'SZA X Justin Timberlake', 'rank': '77', 'last_week': '80', 'peak': '61', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'The Other Side'}, 'Yummy Justin Bieber': {'artist': 'Justin Bieber', 'rank': '78', 'last_week': '67', 'peak': '2', 'weeks on chart': '11', 'img': 'billboard.jpg', 'song': 'Yummy'}, 'B.I.T.C.H. Megan Thee Stallion': {'artist': 'Megan Thee Stallion', 'rank': '79', 'last_week': '59', 'peak': '31', 'weeks on chart': '6', 'img': 'billboard.jpg', 'song': 'B.I.T.C.H.'}, 'La Dificil Bad Bunny': {'artist': 'Bad Bunny', 'rank': '80', 'last_week': '54', 'peak': '33', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'La Dificil'}, "I Hope You're Happy Now Carly Pearce & Lee Brice": {'artist': 'Carly Pearce & Lee Brice', 'rank': '81', 'last_week': '91', 'peak': '65', 'weeks on chart': '11', 'img': 'billboard.jpg', 'song': "I Hope You're Happy Now"}, 'Homecoming Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '82', 'last_week': '22', 'peak': '22', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': 'Homecoming'}, 'Come This Way Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '83', 'last_week': '-', 'peak': '83', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Come This Way'}, 'To Die For Sam Smith': {'artist': 'Sam Smith', 'rank': '84', 'last_week': '96', 'peak': '46', 'weeks on chart': '5', 'img': 'billboard.jpg', 'song': 'To Die For'}, 'Emotionally Scarred Lil Baby': {'artist': 'Lil Baby', 'rank': '85', 'last_week': '64', 'peak': '31', 'weeks on chart': '3', 'img': 'billboard.jpg', 'song': 'Emotionally Scarred'}, 'Does To Me Luke Combs Featuring Eric Church': {'artist': 'Luke Combs Featuring Eric Church', 'rank': '86', 'last_week': '-', 'peak': '86', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Does To Me'}, 'Got The Guap Lil Uzi Vert Featuring Young Thug': {'artist': 'Lil Uzi Vert Featuring Young Thug', 'rank': '87', 'last_week': '-', 'peak': '87', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Got The Guap'}, 'Supalonely BENEE Featuring Gus Dapperton': {'artist': 'BENEE Featuring Gus Dapperton', 'rank': '88', 'last_week': '-', 'peak': '88', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Supalonely'}, 'Money Spread Lil Uzi Vert Featuring Young Nudy': {'artist': 'Lil Uzi Vert Featuring Young Nudy', 'rank': '89', 'last_week': '-', 'peak': '89', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Money Spread'}, 'Cardigan Don Toliver': {'artist': 'Don Toliver', 'rank': '90', 'last_week': '-', 'peak': '90', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Cardigan'}, "Beer Can't Fix Thomas Rhett Featuring Jon Pardi": {'artist': 'Thomas Rhett Featuring Jon Pardi', 'rank': '91', 'last_week': '-', 'peak': '91', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': "Beer Can't Fix"}, 'Vete Bad Bunny': {'artist': 'Bad Bunny', 'rank': '92', 'last_week': '66', 'peak': '33', 'weeks on chart': '16', 'img': 'billboard.jpg', 'song': 'Vete'}, 'Know Your Worth Khalid x Disclosure': {'artist': 'Khalid x Disclosure', 'rank': '93', 'last_week': '94', 'peak': '57', 'weeks on chart': '6', 'img': 'billboard.jpg', 'song': 'Know Your Worth'}, 'Futsal Shuffle 2020 Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '94', 'last_week': '48', 'peak': '5', 'weeks on chart': '11', 'img': 'billboard.jpg', 'song': 'Futsal Shuffle 2020'}, 'Prices Lil Uzi Vert': {'artist': 'Lil Uzi Vert', 'rank': '95', 'last_week': '25', 'peak': '25', 'weeks on chart': '2', 'img': 'billboard.jpg', 'song': 'Prices'}, 'Go Stupid Polo G Featuring NLE Choppa & Stunna 4 Vegas': {'artist': 'Polo G Featuring NLE Choppa & Stunna 4 Vegas', 'rank': '96', 'last_week': '90', 'peak': '60', 'weeks on chart': '5', 'img': 'billboard.jpg', 'song': 'Go Stupid'}, 'Before You Go Lewis Capaldi': {'artist': 'Lewis Capaldi', 'rank': '97', 'last_week': '-', 'peak': '71', 'weeks on chart': '7', 'img': 'billboard.jpg', 'song': 'Before You Go'}, 'Savage Megan Thee Stallion': {'artist': 'Megan Thee Stallion', 'rank': '98', 'last_week': '-', 'peak': '98', 'weeks on chart': '1', 'img': 'billboard.jpg', 'song': 'Savage'}, 'Come Thru Summer Walker & Usher': {'artist': 'Summer Walker & Usher', 'rank': '99', 'last_week': '-', 'peak': '42', 'weeks on chart': '12', 'img': 'billboard.jpg', 'song': 'Come Thru'}, 'Make No Sense YoungBoy Never Broke Again': {'artist': 'YoungBoy Never Broke Again', 'rank': '100', 'last_week': '-', 'peak': '57', 'weeks on chart': '18', 'img': 'billboard.jpg', 'song': 'Make No Sense'}}


def selector(query):
    if query == 'hot 100 chart':
        return Music().chart()
    else:
        return {'display': 'nothing to show', 'say': 'nothing to show'}


class Music:
    def __init__(self):
        url = 'https://www.billboard.com/charts/hot-100'
        page = requests.get(url, headers=config.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.main_li = soup.find_all("li", {"class": "chart-list__element display--flex"})

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

    def chart(self):
        songs = self.get_songs
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
        for song in songs.values():
            display += f"<tr>\
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
        req = 'https://www.billboard.com/charts/the-billboard-hot-100'
        page = requests.get(req, headers=config.header)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.main_div = self.soup.find_all("div", {"class": "chart-list-item piano-content-overlay__gated-item"})

    @property
    def get_songs(self):
        songs = {}
        for div in self.main_div:
            songs[div.get('data-artist') + ' ' + div.get('data-title') + ' The Billboard Hot 100'] \
                = {'rank': div.get('data-rank'), 'artist': div.get('data-artist'), 'song': div.get('data-title')}
        return songs

    @property
    def songs_images(self):
        img_list = self.soup.find_all('img', {'class': 'chart-list-item__image'})
        songs = self.get_songs
        for img in img_list:
            title = img.get('alt')
            if title in songs:
                image = img.get('src')
                if image[:4] != 'data':
                    songs[title]['img'] = image
                else:
                    try:
                        songs[title]['img'] = img.get('data-src')
                    except Exception:
                        songs[title]['img'] = 'billboard.jpg'
        return songs

    def random_song(self):
        try:
            songs = self.get_songs
            return r.choice(list(songs))[:-22]
        except Exception:
            return r.choice(list(dict_songs))[:-22]

    def playlist(self, no=5):
        if no > 10:
            no = 10
        try:
            songs = self.get_songs
            items = list(songs)[:no]
            plays = ''
            for item in items:
                plays += item[:-22] + ','
            return plays[:-1]
        except Exception:
            items = list(dict_songs)[:no]
            plays = ''
            for item in items:
                plays += item + ','
            return plays[:-1]

# a = Music().chart()
# print(a)