var ws = new WebSocket("ws://localhost:8000");
window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
var recognition = new window.SpeechRecognition();
var store = [''];
var s_g = -2;
var answer = '';
var answers = {};
const simonSays = "simon says";
var wordfile_dic = {'filename': ''};
document.getElementById("chat_input").onkeydown = check;
const VOICE_OBJ = new SpeechSynthesisUtterance();
// const voice = {
//     //   "name":  "Microsoft Hazel Desktop - English (Great Britain)",
//     //   "lang": "en-GB"
//     // };
//     //   VOICE_OBJ.voiceURI = voice.name;
//     //   VOICE_OBJ.lang = voice.lang;
// let xvoice = speechSynthesis.getVoices()[2];
let mm = window.speechSynthesis.getVoices();
console.log("voices: ->", mm);
let xvoice = {voiceURI: "Microsoft Susan - English (United Kingdom)", name: "Microsoft Susan - English (United Kingdom)", lang: "en-GB", localService: true, default: false};
VOICE_OBJ.voiceURI = xvoice.name;
VOICE_OBJ.lang = xvoice.lang;
// VOICE_OBJ.voice = xvoice;
VOICE_OBJ.rate = 0.7
// Close socket when window closes
$(window).on('beforeunload', function () {
    ws.close();
});
ws.onerror = function (event) {
    location.reload();
}
ws.onmessage = function (event) {
    var message_received = event.data;

    if (message_received.indexOf('{') >= 0) {
        var obj = JSON.parse(message_received);
        if (obj.hasOwnProperty('answer')) {
            answer = obj['answer'];
        }
        else if (obj.hasOwnProperty('answers')) {
            answers = {...answers, ...obj['answers']};
        }
        if (obj.hasOwnProperty('user_said')) {
            chat_add_message(obj['user_said'], true);
            chat_add_message(obj['display'], false);
            myVoice(obj['say']);
            unloading();
        } else {
            chat_add_message(obj['display'], false);
            myVoice(obj['say']);
            unloading();
        }
    } else if (message_received.indexOf(';') >= 0) {
        var speak = message_received.split(';')[0];
        var msg = message_received.split(';')[1];
        chat_add_message(speak, true);
        chat_add_message(msg, false);
        unloading();

    } else {
        chat_add_message(message_received, false);
        unloading();
    }


};

// Add a message to the chat history
function chat_add_message(message, isUser) {
    var class_suffix = isUser ? '_user' : '';
    var html = '\
        <div class="chat_line">\
            <div class="chat_bubble' + class_suffix + '">\
              <div class="chat_triangle' + class_suffix + '"></div>\
                ' + message + '\
            </div>\
        </div>\
        ';
    chat_add_html(html);
}

// Add HTML to the chat history
function chat_add_html(html) {
    $("#chat_log").append(html);
    chat_scrolldown();
}

// Scrolls the chat history to the bottom
function chat_scrolldown() {
    $("#chat_log").animate({scrollTop: $("#chat_log")[0].scrollHeight}, 500);
}

// If press ENTER, talk to chat and send message to server
$(function () {
    $('#chat_input').on('keypress', function (event) {
        let reply;
        if (event.which === 13 && $(this).val() != "") {
            var message = $(this).val();
            $(this).val("");
            chat_add_message(message, true);
            loading();
            store.push(message);
            s_g = -2;
            if (answer != '') {
                var resp = ['why', 'dunno', 'why?'];
                var ans = answer;
                answer = '';
                if (resp.indexOf(message.toLowerCase()) > 0) {
                    chat_add_message(ans, false);
                    myVoice(ans);
                    unloading();

                } else {
                    if (ans.slice(8,).toLowerCase().search(message.toLowerCase()) != -1) {
                        let reply = 'you are right. ';
                        chat_add_message(reply + ans, false);
                        myVoice(reply + ans);
                        unloading();
                    } else {
                        let reply = 'you are wrong. ';
                        chat_add_message(reply + ans, false);
                        myVoice(reply + ans);
                        unloading();
                    }
                }

            } else if (message === "clear") {
                location.reload();
            } else if (message.toLowerCase().slice(0, simonSays.length) == simonSays) {
                let reply = message.slice(simonSays.length + 1, message.length);
                let my_reply = reply.replace('[', '').replace(']', '');
                chat_add_message(my_reply, false);
                myVoice(my_reply);
                unloading();
            } else if (message.slice(0, "word create file ".length) == "word create file ") {
                var filename = message.slice('word create file '.length);
                wordfile_dic['filename'] = filename + '.docx';
                var word_text_form = '<b> Editing ' + filename + '.docx </b><div class="wordfile_div"><textarea id="wordfile" rows="10" cols="100"></textarea><br><button id="file_button" onclick="saveWordfile()">Save</button></div>';
                // send word_text_form to website/user
                chat_add_message(word_text_form, false);
                myVoice('add content to your word file');
                unloading();
            } else {
                // console.log(`ans = ${message.toLowerCase().slice(0, simonSays.length) == simonSays}`)
                ws.send(message);

            }

        }
    });
});

function myFunction() {
    ws.send("click");
}

function check(e) {
    var x = e.keyCode;

    if (x === 40) {      // handling up arrow key
        if (s_g === -2) {
            s_g = store.length - 1;
        }
        document.getElementById("chat_input").value = store[s_g];
        if (s_g != (store.length - 1)) {
            s_g = s_g + 1;
        }

    } else if (x === 38) {     // handling down arrow key
        if (s_g == -2) {
            s_g = store.length - 1;
        }
        document.getElementById("chat_input").value = store[s_g];
        if (s_g != 0) {
            s_g = s_g - 1;
        }

    }

}

function check_ans(myId, ques_id){
        let node = document.querySelector(`#${myId}`);
        if(node.innerText === answers[ques_id]){
            node.classList.add('green');
            voice("Correct!");
        }
        else{
            node.classList.add('red');
            voice("Wrong Option");
        }
    }

function man_complete(word) {
    document.getElementById("chat_input").value = word;
}

function open_link(link) {
    window.open(link, "_blank");

}

function myVoice(myLongText){

var utterance = new SpeechSynthesisUtterance(myLongText);

//modify it as you normally would
var voiceArr = speechSynthesis.getVoices();
utterance.voice = voiceArr[2];

//pass it into the chunking function to have it played out.
//you can set the max number of characters by changing the chunkLength property below.
//a callback function can also be added that will fire once the entire text has been spoken.
speechUtteranceChunker(utterance, {
    chunkLength: 180
}, function () {
    //some code to execute when done
    console.log('done');
});
}

function voice(text) {
    VOICE_OBJ.text = text;
    speechSynthesis.speak(VOICE_OBJ);
    //   VOICE_OBJ.volume = 1; // 0 to 1
    //   VOICE_OBJ.rate = 1; // 0.1 to 1
    //   VOICE_OBJ.pitch = 1.5; // 0 to 2
    //   const voice = {
    //   "name":  "Microsoft Hazel Desktop - English (Great Britain)",
    //   "lang": "en-GB"
    // };
    //   VOICE_OBJ.voiceURI = voice.name;
    //   VOICE_OBJ.lang = voice.lang;

}

function man_mySelect(word) {
    var sen = word.slice(0, -1);
    var ind = word.slice(-1);
    var sel = document.getElementById("mySelect" + ind).value;
    document.getElementById("chat_input").value = sen + sel;

}

function mouseFunction(e) {
    var body = document.querySelector('body');
    var heart = document.createElement("span");
    heart.className = 'love';
    var x = e.offsetX;
    var y = e.offsetY;
    heart.style.left = x + 'px';
    heart.style.top = y + 'px';
    var size = Math.random() * 100;
    heart.style.width = 20 + size + 'px';
    heart.style.height = 20 + size + 'px';
    body.appendChild(heart);

    setTimeout(function () {
        heart.remove();
    }, 2000)
}

function putMouse() {
    document.addEventListener("mousemove", mouseFunction);
}

function removeMouse() {
    document.removeEventListener("mousemove", mouseFunction);
}

function loading() {
    const load = document.createElement('div');
    load.className = 'ring';
    load.classId = 'ring';
    load.innerHTML = `
			active<div class='ringer'></div>
		  `;
    document.getElementById('loading').appendChild(load);
}

function listening() {
    const load = document.createElement('div');
    load.className = 'ring';
    load.classId = 'ring';
    load.innerHTML = `
			listening<div class='ringer'></div>
		  `;
    document.getElementById('loading').appendChild(load);
}

function unloading() {
    var x;
    x = document.getElementById('loading');
    if (x.innerHTML) {
        x.innerHTML = '';
    }

}

function keep_clock() {
    var deg = 6;
    var hrs = document.querySelectorAll("#hr");
    var mns = document.querySelectorAll("#mn");
    var scs = document.querySelectorAll("#sc");

    setInterval(
        () => {
            let day = new Date();
            let hh = day.getHours() * 30;
            let mm = day.getMinutes() * deg;
            let ss = day.getSeconds() * deg;
            for (i = 0; i < hrs.length; ++i) {
                hrs[i].style.transform = `rotateZ(${hh + (mm / 12)}deg)`;
                mns[i].style.transform = `rotateZ(${mm}deg)`;
                scs[i].style.transform = `rotateZ(${ss}deg)`;
            }

        }
    )

}

function saveWordfile() {
    wordfile_dic['content'] = document.getElementById("wordfile").value;
    var send_me = `word file send ${JSON.stringify(wordfile_dic)}`;
    var notify = `<p style='color: white; background-color:black; width:250px;'>${wordfile_dic['filename']} Saved!</p>`;

    var elements = document.getElementsByClassName("wordfile_div");
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].innerHTML) {
            elements[i].innerHTML = notify;
        }
    }
    // send send_me to python for processing
    ws.send(send_me);
    wordfile_dic = {'filename': ''};

}

function Speak_now() {
    recognition.start();

    let finalTranscript = '';


    recognition.interimResults = true;
    recognition.maxAlternatives = 10;
    // recognition.continuous = true;
    voice('listening');
    listening();
    recognition.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex, len = event.results.length; i < len; i++) {
            let transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }
        //console.log('trans: '+finalTranscript);
        if (finalTranscript != '') {

            if (finalTranscript.toLowerCase().slice(0, simonSays.length) == simonSays) {
                let reply = finalTranscript.slice(simonSays.length + 1, finalTranscript.length);
                let my_reply = reply.replaceAll('*', '');
                chat_add_message(reply, false);
                voice(my_reply);
                unloading();
            } else {
                unloading();
                chat_add_message(finalTranscript, true);
                loading();
                ws.send(finalTranscript);
            }

        }
    }

}

var speechUtteranceChunker = function (utt, settings, callback) {
    settings = settings || {};
    var newUtt;
    var txt = (settings && settings.offset !== undefined ? utt.text.substring(settings.offset) : utt.text);
    if (utt.voice && utt.voice.voiceURI === 'native') { // Not part of the spec
        newUtt = utt;
        newUtt.text = txt;
        newUtt.addEventListener('end', function () {
            if (speechUtteranceChunker.cancel) {
                speechUtteranceChunker.cancel = false;
            }
            if (callback !== undefined) {
                callback();
            }
        });
    }
    else {
        var chunkLength = (settings && settings.chunkLength) || 160;
        var pattRegex = new RegExp('^[\\s\\S]{' + Math.floor(chunkLength / 2) + ',' + chunkLength + '}[.!?,]{1}|^[\\s\\S]{1,' + chunkLength + '}$|^[\\s\\S]{1,' + chunkLength + '} ');
        var chunkArr = txt.match(pattRegex);

        if (chunkArr[0] === undefined || chunkArr[0].length <= 2) {
            //call once all text has been spoken...
            if (callback !== undefined) {
                callback();
            }
            return;
        }
        var chunk = chunkArr[0];
        newUtt = new SpeechSynthesisUtterance(chunk);
        var x;
        for (x in utt) {
            if (utt.hasOwnProperty(x) && x !== 'text') {
                newUtt[x] = utt[x];
            }
        }
        newUtt.addEventListener('end', function () {
            if (speechUtteranceChunker.cancel) {
                speechUtteranceChunker.cancel = false;
                return;
            }
            settings.offset = settings.offset || 0;
            settings.offset += chunk.length - 1;
            speechUtteranceChunker(utt, settings, callback);
        });
    }

    if (settings.modifier) {
        settings.modifier(newUtt);
    }
    console.log(newUtt); //IMPORTANT!! Do not remove: Logging the object out fixes some onend firing issues.
    //placing the speak invocation inside a callback fixes ordering and onend issues.
    setTimeout(function () {
        speechSynthesis.speak(newUtt);
    }, 0);
};