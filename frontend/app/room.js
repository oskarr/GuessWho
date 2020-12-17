

ROOM_ID = window.location.href.split("/")
ROOM_ID = ROOM_ID[ROOM_ID.length-1]
ROOM_ID = ROOM_ID.split("?")[0].split("#")[0]

if([undefined, "undefined"].indexOf(Cookies.get("username")) != -1 || [undefined, "undefined"].indexOf(Cookies.get("team")) != -1) {
    window.location.href = "../?room="+ROOM_ID+"&err=newuser"
}

const socket = io('');
(function(){
    socket.on('reply', (data) => {app.chat.push(new ChatMessage(data.from, data.message))})
    socket.on('characters', (data) => {
        console.log("Recieved characters");
        if (data.self == null) {
            app.newGameLabel = "Ny omgång"
        }
        app.teamcharacters = data.all;
        app.oppcharacters = data.opponent;
        app.self = data.self;
    })

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
        teamcharacters: {},
        oppcharacters: {},
        self: undefined,
        draftmessage: "",
        url: window.location.href,
        newGameLabel: "Ny omgång",
    },
    methods: {
        chatkeydown: function(event) {
            if(event.keyCode == 13) {
                this.chat.push(new ChatMessage(socket.id, this.draftmessage))
                socket.emit("chat_message", this.draftmessage)
                this.draftmessage = ""
            }
        },
        updateCharacters: function() {
            socket.emit('update_characters', this.teamcharacters)
        },
        selectCharacter: function() {
            for(character of this.oppcharacters) {
                if (character.active == false)
                    socket.emit('select_character', character)
            }
        },
        newGame: function() {
            socket.emit('new_game'),
            this.newGameLabel = "Väntar på andra laget..."
        }
    }
})
