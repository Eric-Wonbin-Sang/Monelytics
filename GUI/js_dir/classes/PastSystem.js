
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
    }

    get_banks_and_accounts_sidebar_div() {
        var banks_and_accounts_sidebar_div = document.getElementById("banks_and_accounts_sidebar");
        for(let i in this.bank_list){
            banks_and_accounts_sidebar_div.appendChild(this.bank_list[i].get_div());
        }
    }

    reset_all_active_account_buttons() {
        for (let i in this.bank_list) {
            this.bank_list[i].reset_active_account_buttons();
        }
    }
}
