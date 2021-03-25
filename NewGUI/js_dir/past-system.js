
function get_p_elem(some_text) {
    var p_elem = document.createElement("p");
    var node = document.createTextNode(some_text);
    p_elem.appendChild(node);
    return p_elem;
}

class Bank {

    constructor(bank_dict) {
        this.type = bank_dict["type"];
        this.owner = bank_dict["owner"];
        this.username = bank_dict["username:"];
        this.password = bank_dict["password"];
        this.dict_list = bank_dict["account_list"];

        this.account_list = this.get_account_list();
        this.button = this.get_button();
    }

    get accounts_total() {
        var total = 0;
        for (let i in this.account_list) {
            total += this.account_list[i].curr_balance;
        }
        return total;
    }

    get_account_list() {
        var account_list = [];
        for(let i_a in this.dict_list) {
            account_list.push(new Account(this.dict_list[i_a]));
        }
        return account_list;
    }

    get_button() {
        var button = document.createElement("button");
        button.setAttribute("class", "collapsible");

        var type_span = document.createElement("span");
        type_span.setAttribute("class", "bank_type_span");
        type_span.innerHTML = this.type + " (" + this.owner.split(" ")[0] + ")";

        var total_span = document.createElement("span");
        total_span.setAttribute("class", "bank_total_span");
        
        var total = this.accounts_total;
        if (total == 0 & this.account_list.length == 0) {
            total_span.innerHTML = "No Accounts!";
        }
        else {
            total_span.innerHTML = "$" + new String(this.accounts_total);
        }

        button.appendChild(type_span);
        button.appendChild(total_span);

        button.onclick = function() {

            var account_div = this.nextElementSibling;
            if (account_div != null) {

                button.classList.toggle("active");

                if (account_div.style.maxHeight){
                    account_div.style.maxHeight = null;
                } else {
                    account_div.style.maxHeight = account_div.scrollHeight + "px";
                } 
            }
        };

        return button;
    }

    get_div() {
        var bank_div = document.createElement("div");
        bank_div.setAttribute("class", "bank_div");

        if (this.dict_list.length == 0) {
            var account_div = document.createElement("div");
            account_div.setAttribute("class", "account_div");
            account_div.setAttribute("id", 0);
            account_div.appendChild(get_p_elem("No Accounts!"));
            bank_div.appendChild(account_div);
        }

        bank_div.appendChild(this.button);

        for(let i_a in this.account_list) {
            bank_div.appendChild(this.account_list[i_a].get_div());
        }
        return bank_div;
    }

}

class Account {

    constructor(account_dict) {
        this.name = account_dict["name"];
        this.nickname = account_dict["nickname"];
        this.type = account_dict["type"];
        this.specific_type = account_dict["specific_type"];
        this.curr_balance = account_dict["curr_balance"];
    }

    get_div() {
        var account_div = document.createElement("div");
        account_div.setAttribute("class", "account_div");

        account_div.appendChild(get_p_elem("Account: " + this.name));
        account_div.appendChild(get_p_elem("Nickname: " + this.nickname));
        account_div.appendChild(get_p_elem("Type: " + this.type));
        account_div.appendChild(get_p_elem("Spec Type: " + this.specific_type));
        
        return account_div;
    }
}

function get_bank_list(json_response) {
    var bank_list = [];
    var bank_dict_list = JSON.parse(json_response);
    for(let i_b in bank_dict_list){
        bank_list.push(new Bank(bank_dict_list[i_b]));
    }
    return bank_list;
}

function get_banks_and_accounts_sidebar_div(bank_list) {
    var banks_and_accounts_sidebar_div = document.getElementById("banks_and_accounts_sidebar");
    for(let i in bank_list){
        banks_and_accounts_sidebar_div.appendChild(bank_list[i].get_div());
    }
}

window.onload = function() {
    var url = "http://127.0.0.1:5000/get_bank_and_account_info";
    request = new XMLHttpRequest();
    request.open("GET", url);
    request.send();
    request.onload = (e) => {

        var json_response = request.response
        var bank_list = get_bank_list(json_response);

        get_banks_and_accounts_sidebar_div(bank_list);

        for (let i in bank_list) {
            bank_list[i].button.click();
            if (i == 0) {
                break;
            }
        }
    }
    request.onerror = (e) => {
        console.log("error");
    }
}
