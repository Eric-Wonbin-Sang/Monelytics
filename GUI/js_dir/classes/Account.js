
class Account {

    constructor(parent_bank, index, account_dict) {

        this.parent_bank = parent_bank;
        this.index = index;

        this.name = account_dict["name"];
        this.nickname = account_dict["nickname"];
        this.type = account_dict["type"];
        this.specific_type = account_dict["specific_type"];
        this.curr_balance = account_dict["curr_balance"];

        this.button = this.get_button();
    }

    get_button() {
        var button = create_elem("button", "account_button");

        var name_span = create_elem("span", "account_name_span");
        name_span.innerHTML = this.name;
        button.appendChild(name_span);

        var amount_span = create_elem("span", "account_amount_span");
        amount_span.innerHTML = get_dollar_str(this.curr_balance);
        button.appendChild(amount_span);

        var self = this;
        button.onclick = function() {
            if (self.button.classList.contains("active")) {
                self.button.classList.toggle("active");
            }
            else {
                self.parent_bank.past_system.reset_all_active_account_buttons();
                self.button.classList.toggle("active");
            }

            var url = "http://127.0.0.1:5000/get_graph/" + self.parent_bank.type + "/" + self.parent_bank.owner + "/" + self.name;
            request = new XMLHttpRequest();
            request.open("GET", url);
            request.send();
            request.onload = (e) => {
                var analysis_content_div = document.getElementById("analysis_content");
                analysis_content_div.innerHTML = DOMPurify.sanitize(JSON.parse(request.response)["result"]);
            }
            request.onerror = (e) => {
                console.log("error");
            }
        };
        return button;
    }

    get_div() {
        var account_div = document.createElement("div");
        account_div.setAttribute("class", "account_div");
        account_div.appendChild(this.button);
        return account_div;
    }
}
