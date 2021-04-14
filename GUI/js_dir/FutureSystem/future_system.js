
window.onload = function() {
    var url = "http://127.0.0.1:5000/future_system/get_scenarios";
    request = new XMLHttpRequest();
    request.open("GET", url);
    request.send();
    request.onload = (e) => {
        system = new FutureSystem(request.response);
    }
    request.onerror = (e) => {
        console.log("error");
    }
}
