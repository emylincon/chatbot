var ws = new WebSocket("ws://localhost:8000");
	var store = [''];
	var s_g = -2;
	document.getElementById("chat_input").onkeydown = check;
    // Close socket when window closes
    $(window).on('beforeunload', function(){
       ws.close();
    });
    ws.onerror = function(event) {
        location.reload();
    }
    ws.onmessage = function(event)  {
        var message_received = event.data;

		if (message_received.indexOf('{') >= 0){
                var obj = JSON.parse(message_received);
                if (obj.hasOwnProperty('user_said')){
                    chat_add_message(obj['user_said'], true);
                    chat_add_message(obj['display'], false);
                    voice(obj['say']);
                }
                else{
                    chat_add_message(obj['display'], false);
                    voice(obj['say']);
                }
		}

		else if (message_received.indexOf(';') >=0) {
		   var speak = message_received.split(';')[0];
		   var msg = message_received.split(';')[1];
		   chat_add_message(speak, true);
		   chat_add_message(msg, false);

		}

		else{
		        chat_add_message(message_received, false);
		    }




    };
    // Add a message to the chat history
    function chat_add_message(message, isUser) {
        var class_suffix = isUser ? '_user' : '';
        var html = '\
        <div class="chat_line">\
            <div class="chat_bubble'+class_suffix+'">\
              <div class="chat_triangle'+class_suffix+'"></div>\
                '+message+'\
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
        $("#chat_log").animate({ scrollTop: $("#chat_log")[0].scrollHeight }, 500);
    }
    // If press ENTER, talk to chat and send message to server
    $(function() {
       $('#chat_input').on('keypress', function(event) {
          if (event.which === 13 && $(this).val() != ""){
             var message = $(this).val();
             $(this).val("");
             chat_add_message(message, true);
			 store.push(message);
			 s_g = -2;
             ws.send(message);
          }
       });
    });
    function myFunction() {
      ws.send("click");
    }
    function check(e) {
      var x = e.keyCode;

	  if (x == 40){      // handling up arrow key
		if (s_g == -2){
			s_g = store.length -1;
		}
		document.getElementById("chat_input").value = store[s_g];
		if (s_g != (store.length -1)){
            s_g = s_g + 1;
		}

		}
	  else if (x == 38){     // handling down arrow key
		if (s_g == -2){
			s_g = store.length -1;
		}
		document.getElementById("chat_input").value = store[s_g];
		if (s_g != 0){
            s_g = s_g -1;
		}

        }

    }
    function man_complete(word){
        document.getElementById("chat_input").value = word;
    }

    function open_link(link){
        window.open(link, "_blank");

    }

    function voice(text){
        const msg = new SpeechSynthesisUtterance();
        msg.volume = 1; // 0 to 1
        msg.rate = 1; // 0.1 to 10
        msg.pitch = 1.5; // 0 to 2
        msg.text  = text;


        const voice = {
        "name": "Tessa",
        "lang": "en-ZA"
      }; //47
        console.log(`Voice: ${voice.name} and Lang: ${voice.lang}`);
        msg.voiceURI = voice.name;
        msg.lang = voice.lang;


        speechSynthesis.speak(msg);
    }