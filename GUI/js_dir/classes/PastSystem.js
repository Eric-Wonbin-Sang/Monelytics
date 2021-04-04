
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
            if (i == 0) {
                break;
            }
        }
        var url = "http://127.0.0.1:5000/graph_past_system/show_all";
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
    }

    get_banks_and_accounts_sidebar_div() {
        var banks_and_accounts_sidebar_div = document.getElementById("banks_and_accounts_sidebar");
        for(let i in this.bank_list){
            banks_and_accounts_sidebar_div.appendChild(this.bank_list[i].get_div());
        }
    }

    get_active_accounts_graph_rest_url() {

        var base_url = "http://127.0.0.1:5000/graph_past_system/";
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
        return base_url + url_suffix;
    }
}
