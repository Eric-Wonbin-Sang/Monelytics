
function create_elem(html_type, some_class=null, some_id=null) {
    var html_elem = document.createElement(html_type);
    if (some_class != null) {
        html_elem.setAttribute("class", some_class);
    }
    if (some_id != null) {
        html_elem.setAttribute("id", some_id);
    }
    return html_elem;
}

function get_p_elem(some_text) {
    var p_elem = document.createElement("p");
    var node = document.createTextNode(some_text);
    p_elem.appendChild(node);
    return p_elem;
}

function get_dollar_str(num) {
    if (num < 0) {
        return "-$" + num.toLocaleString().substring(1);
    }
    return "$" + num.toLocaleString();
}

window.onload = function() {
    var url = "http://127.0.0.1:5000/get_bank_and_account_info";
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