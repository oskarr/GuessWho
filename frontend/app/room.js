const socket = io('');
(function(){
    socket.on('reply', (data) => {app.chat.push(new ChatMessage(data.from, data.message))})
    socket.on('characters', (data) => {app.characters = data.all; app.self = data.self;})

    roomid = window.location.href.split("/")
    roomid = roomid[roomid.length-1]
    roomid = roomid.split("?")[0].split("#")[0]

    socket.emit('update_user', Cookies.get("username"), Cookies.get("team"))
    socket.emit('joinroom', roomid)
    socket.emit('get_characters')
})()



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
