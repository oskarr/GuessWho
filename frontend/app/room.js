const socket = io('');
(function(){
    socket.on('reply', (data) => {app.chat.push(new ChatMessage(data.from, data.message))});
    socket.on('room', (data) => {app.chat.push(new ChatMessage(data.from, data.message))});
    roomid = window.location.href.split("/")
    roomid = roomid[roomid.length-1]
    roomid = roomid.split("?")[0].split("#")[0]
    socket.emit('username', Cookies.get("username"))
    socket.emit('joinroom', roomid)
})()



class ChatMessage {
    constructor(sid, message) {
      this.from = sid;
      this.content = message;
    }
  }




app = new Vue({
    el: '#app',
    data: {
        chat: [],
        draftmessage: "",
    },
    methods: {
        chatkeydown: function(event) {
            if(event.keyCode == 13) {
                this.chat.push(new ChatMessage(socket.id, this.draftmessage))
                socket.emit("chat_message", this.draftmessage)
                this.draftmessage = ""
            }
        },
        roomkeydown: function(event) {
            if(event.keyCode == 13) {
                socket.emit("room", {action: "connect", roomid: this.draftroom})
            }
        },
    }
})
