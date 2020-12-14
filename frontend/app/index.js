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
        files: undefined,
    },
    methods: {// TODO add validation
        setcookies: function() {
            Cookies.set("username", this.uname, {path: ""})
            Cookies.set("team", this.team, {path: ""})
        },
        newroom: function () {
            this.setcookies()
            window.location.href = "/newroom"
        },
        joinroom: function () {
            this.setcookies()
            window.location.href = "/room/" + this.roomid
        },
        GET: GET,
        handleFiles: function(e) {
            console.log(e.target.files)
        }
    }
})