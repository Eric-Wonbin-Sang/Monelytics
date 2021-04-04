class Bank {

    constructor(past_system, bank_dict) {

        this.past_system = past_system;

        this.type = bank_dict["type"];
        this.owner = bank_dict["owner"];
        this.username = bank_dict["username:"];
        this.password = bank_dict["password"];
        this.dict_list = bank_dict["account_list"];

        this.account_list = this.get_account_list();
        this.button = this.get_button();
    }

    get_accounts_total() {
        var total = 0;
        for (let i in this.account_list) {
            total += this.account_list[i].curr_balance;
        }
        return total;
    }

    get_total_balance_str() {
        var total = this.get_accounts_total();
        if (total == 0 & this.account_list.length == 0) {
            return "No Accounts";
        }
        return get_dollar_str(total);
    }

    get_account_list() {
        var account_list = [];
        for(let i_a in this.dict_list) {
            account_list.push(new Account(this, i_a, this.dict_list[i_a]));
        }
        return account_list;
    }

    get_button() {
        var button = create_elem("button", "bank_collapsible");

        var type_span = create_elem("span", "bank_type_span");
        type_span.innerHTML = this.type + " (" + this.owner.split(" ")[0] + ")";
        button.appendChild(type_span);

        var total_span = create_elem("span", "bank_total_span");
        total_span.innerHTML = this.get_total_balance_str();
        button.appendChild(total_span);

        button.onclick = function() {

            var account_div = this.nextElementSibling;
            if (account_div.innerHTML != "") {

                button.classList.toggle("active");

                if (account_div.style.maxHeight) {
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
        bank_div.appendChild(this.button);

        var account_list_div = document.createElement("div");
        account_list_div.setAttribute("class", "all_accounts_div");

        for(let i_a in this.account_list) {
            account_list_div.appendChild(this.account_list[i_a].get_div());
        }

        bank_div.appendChild(account_list_div);
        return bank_div;
    }

    reset_active_account_buttons() {
        for (let i in this.account_list) {
            if (this.account_list[i].button.classList.contains("active")) {
                this.account_list[i].button.classList.toggle("active");
            }
        }
    }
}
