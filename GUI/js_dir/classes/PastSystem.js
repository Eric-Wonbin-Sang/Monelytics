
class PastSystem {

    constructor(json_response) {

        this.json_response = json_response;
        this.bank_list = this.get_bank_list();
        
        this.get_banks_and_accounts_sidebar_div()
        this.initialize_ui();
    
    }

    get_bank_list() {
        var bank_list = [];
        var bank_dict_list = JSON.parse(this.json_response);
        for(let i_b in bank_dict_list){
            bank_list.push(new Bank(this, bank_dict_list[i_b]));
        }
        return bank_list;
    }

    initialize_ui() {
        for (let i in this.bank_list) {
            this.bank_list[i].button.click();
            // if (i == 0) {
            //     break;
            // }
        }
        this.update_graph();
        this.update_transactions();
    }

    get_banks_and_accounts_sidebar_div() {
        var banks_and_accounts_sidebar_div = document.getElementById("banks_and_accounts_sidebar");
        for(let i in this.bank_list){
            banks_and_accounts_sidebar_div.appendChild(this.bank_list[i].get_div());
        }
    }

    get_active_accounts_url_suffix() {

        var url_suffix = "";
        
        for (let b_i in this.bank_list) {
            var bank = this.bank_list[b_i];
            
            var account_name_list = [];
            for (let a_i in bank.account_list) {
                var account = this.bank_list[b_i].account_list[a_i];
                if (account.button.classList.contains("active")) {
                    account_name_list.push(account.name);
                }
            }

            if (account_name_list.length != 0) {
                url_suffix += "BANK" + bank.type + "-" + bank.owner + "|";
                for (let a_i in account_name_list) {
                    url_suffix += account_name_list[a_i] + "|";
                }
            }
        }

        if (url_suffix === "") {
            url_suffix = "show_all";
        }
        return url_suffix;
    }

    get_active_accounts_graph_rest_url() {
        var base_url = "http://127.0.0.1:5000/past_system/graph/";
        return base_url + this.get_active_accounts_url_suffix();
    }

    update_graph() {
        var url = this.get_active_accounts_graph_rest_url();
        request = new XMLHttpRequest();
        request.open("GET", url);
        request.send();
        request.onload = (e) => {
            var analysis_content_div = document.getElementById("graph_div");

            var iframe = create_elem("iframe", "accounts_graph");
            iframe.setAttribute("src", JSON.parse(request.response)["result"]);

            analysis_content_div.innerHTML = "";
            analysis_content_div.appendChild(iframe);

        }
        request.onerror = (e) => {
            console.log("error");
        }
    }

    get_active_accounts_transactions_rest_url() {
        var base_url = "http://127.0.0.1:5000/past_system/get_transactions/";
        return base_url + this.get_active_accounts_url_suffix();
    }

    update_transactions() {
        var url = this.get_active_accounts_transactions_rest_url();
        
        $.getJSON(url, function(data) {

            var table = create_elem("table", "transactions_table");

            var key_to_header_dict = {
                "date": "Date", 
                "parent_bank_type": "Bank", 
                "parent_bank_owner": "Owner", 
                "account_name": "Account Name", 
                "from": "From", 
                "amount": "Amount", 
                "description": "Description"
            };

            var temp_tr = create_elem("tr", "transactions_table_header_row");
            for (let key in key_to_header_dict) {
                var temp_th = create_elem("th", "transactions_table_header", key);
                temp_th.innerHTML = key_to_header_dict[key];
                temp_tr.appendChild(temp_th);
            }
            table.appendChild(temp_tr);

            var transaction_dict_list = data["result"];
            for (let i in transaction_dict_list) {

                var transaction_dict = transaction_dict_list[i];
                var key_to_data_dict = {
                    "date": transaction_dict["date"], 
                    "parent_bank_type": transaction_dict["parent_bank_type"], 
                    "parent_bank_owner": transaction_dict["parent_bank_owner"], 
                    "account_name": transaction_dict["account_name"], 
                    "from": transaction_dict["from"], 
                    "amount": get_dollar_str(transaction_dict["amount"]), 
                    "description": transaction_dict["description"]
                };

                var temp_tr = create_elem("tr", "transactions_table_data_row");
                for (let key in key_to_data_dict) {
                    var temp_td = create_elem("td", "transactions_table_data " + key);
                    temp_td.innerHTML = key_to_data_dict[key];
                    temp_tr.appendChild(temp_td);
                }
                table.appendChild(temp_tr);
            }

            var div = document.getElementById("transactions_div");
            div.innerHTML = "";
            div.appendChild(table);

        });
    }
}
