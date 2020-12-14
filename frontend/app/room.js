

ROOM_ID = window.location.href.split("/")
ROOM_ID = ROOM_ID[ROOM_ID.length-1]
ROOM_ID = ROOM_ID.split("?")[0].split("#")[0]

if(Cookies.get("username") == "undefined" || Cookies.get("team") == "undefined") {
    window.location.href = "../?room="+ROOM_ID+"&err=newuser"
}

const socket = io('');
(function(){
    socket.on('reply', (data) => {app.chat.push(new ChatMessage(data.from, data.message))})
    socket.on('characters', (data) => {app.characters = data.all; app.self = data.self;})

    socket.emit('update_user', Cookies.get("username"), Cookies.get("team"))
    socket.emit('joinroom', ROOM_ID)
    socket.emit('get_characters')
})()

function copyLink() {
    var copyText = document.getElementById('linkbox');
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand('copy');
}

class ChatMessage {
    constructor(sid, message) {
      this.from = sid;
      this.content = message;
    }

    fromSelf() {
        return this.from == socket.id
    }
  }




app = new Vue({
    el: '#app',
    data: {
        chat: [],
        characters: {},
        self: {},
        draftmessage: "",
        url: window.location.href
    },
    methods: {
        chatkeydown: function(event) {
            if(event.keyCode == 13) {
                this.chat.push(new ChatMessage(socket.id, this.draftmessage))
                socket.emit("chat_message", this.draftmessage)
                this.draftmessage = ""
            }
        }
    }
})
