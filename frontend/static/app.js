const socket = io('');
socket.on('reply', (data) => {
    console.log("Reply:")
    console.log(data)
    chat.messages.push(data)
});



chat = new Vue({
    el: '#chat',
    data: {
        messages: [],
        draftmessage: "",
    },
    methods: {
        sendmessage: function() {
            console.log(this.draftmessage)
            socket.emit("chat_message", this.draftmessage)
            console.log(this.draftmessage)
        }
    }
})
