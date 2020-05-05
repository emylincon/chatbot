import datetime
import time
import trans_
import config

clock_ = 0


def rihanna_time():
    global clock_

    _time = str(datetime.datetime.now()).split()[1].split('.')[0]
    reply = f'The Time is {_time}'
    if config.lang_code != 'en':
        reply = trans_.translate_sentence_code(reply, config.lang_code)
        config.lang_code = 'en'
    return {'display': clock(), 'say': reply}
    # if clock_ == 0:
    #     clock_ = 1
    #     return {'display': clock(), 'say': reply}
    # else:
    #     return {'display': reply, 'say': reply}


def rihanna_date():
    reply = time.ctime()
    return {'display': reply, 'say': reply}


# https://www.youtube.com/watch?v=94TKO4eKfIA    clock display

def clock():
    clock_display = """<div class="clock_div">
                            <div class="clock">
                                <div class="hour">
                                    <div class="hr" id="hr">
                                    </div>
                                </div>
                                <div class="min">
                                    <div class="mn" id="mn">
                                    </div>
                                </div>
                                <div class="sec">
                                    <div class="sc" id="sc">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <script>keep_clock();</script>
                    """
    return clock_display
