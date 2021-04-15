
window.onload = function() {
    var url = "http://127.0.0.1:5000/profile/Eric%20Sang/get_info";
    request = new XMLHttpRequest();
    request.open("GET", url);
    request.send();
    request.onload = (e) => {
        temp = new ProfileSystem(new Profile(JSON.parse(request.response)["result"]));
    }
    request.onerror = (e) => {
        console.log("error");
    }
}
