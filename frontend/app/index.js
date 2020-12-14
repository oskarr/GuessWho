function GET(param) {
    try {
        return window.location.href.split("?")[1].split("#")[0].split(param+"=")[1].split("&")[0]
    } catch {
        return ""
    }
    
}

app = new Vue({
    el: '#center',
    data: {
        uname: Cookies.get("username"),
        roomid: GET("room"),
        team: Cookies.get("team"),
    },
    methods: {// TODO add validation
        newroom: function () {
            Cookies.set("username", this.uname, {path: ""})
            Cookies.set("team", this.team, {path: ""})
            window.location.href = "/newroom"
        },
        joinroom: function () {
            Cookies.set("username", this.uname, {path: ""})
            Cookies.set("team", this.team, {path: ""})
            window.location.href = "/room/" + this.roomid
        },
        GET: GET,
    }
})