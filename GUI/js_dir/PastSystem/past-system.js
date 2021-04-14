
window.onload = function() {
    var url = "http://127.0.0.1:5000/past_system/get_bank_and_account_info";
    request = new XMLHttpRequest();
    request.open("GET", url);
    request.send();
    request.onload = (e) => {
        past_system = new PastSystem(request.response);
    }
    request.onerror = (e) => {
        console.log("error");
    }
}
