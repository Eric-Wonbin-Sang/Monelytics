
window.onload = function() {
    create_banks_and_accounts();
};

function create_banks_and_accounts() {

    var url = "http://127.0.0.1:5000/get_bank_and_account_info";

    const request = new XMLHttpRequest();
    request.open("GET", url);
    request.send();

    request.onload = (e) => {

        var bank_dick_list = JSON.parse(request.response);

        for(let i_b in bank_dick_list){

            var bank_type = bank_dick_list[i_b]["type"]
            var bank_owner = bank_dick_list[i_b]["owner"]
            var bank_username = bank_dick_list[i_b]["username:"]
            var bank_password = bank_dick_list[i_b]["password"]
            var account_dict_list = bank_dick_list[i_b]["account_list"]

            console.log(bank_type);
            console.log(bank_owner);
            console.log(bank_username);
            console.log(bank_password);

            for(let i_a in account_dict_list){

                var account_type = account_dict_list[i_a]["type"]
                var account_name = account_dict_list[i_a]["name"]
                var account_nickname = account_dict_list[i_a]["nickname"]
                var account_specific_type = account_dict_list[i_a]["specific_type"]
                var account_curr_balance = account_dict_list[i_a]["curr_balance"]

                console.log("\t", account_type);
                console.log("\t", account_name);
                console.log("\t", account_nickname);
                console.log("\t", account_specific_type);
                console.log("\t", account_curr_balance);
            }
            console.log("--------------");

        }
    }
    request.onerror = (e) => {
        console.log("error");
    }
}
