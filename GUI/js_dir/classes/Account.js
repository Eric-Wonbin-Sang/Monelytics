
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

            self.button.classList.toggle("active")
            
            var url = self.parent_bank.past_system.get_active_accounts_graph_rest_url();
            request = new XMLHttpRequest();
            request.open("GET", url);
            request.send();
            request.onload = (e) => {
                var analysis_content_div = document.getElementById("analysis_content");

                var iframe = create_elem("iframe", "accounts_graph");
                iframe.setAttribute("src", JSON.parse(request.response)["result"]);

                analysis_content_div.innerHTML = "";
                analysis_content_div.appendChild(iframe);

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
