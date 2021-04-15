
class Profile {
    
    constructor(data_dict) {

        this.data_dict = data_dict;

        this.name = this.data_dict["name"];
        this.source_dir = this.data_dict["source_dir"];
        this.photo_path = this.data_dict["photo_path"];
        this.bank_logins_dict_list = this.data_dict["bank_logins_dict_list"];

    }

    get_name_p() {
        var p = create_elem("p", "profile_name_p");
        p.innerHTML = this.name;
        return p;
    }

    get_image() {
        var image = create_elem("img", "profile_image");
        image.src = this.photo_path;
        return image;
    }

    get_bank_logins_to_html() {

        var bank_logins_div = create_elem("div", "bank_logins_div");

        for (let i in this.bank_logins_dict_list) {
            var bank_logins_dict = this.bank_logins_dict_list[i];

            var bank_login_div = create_elem("div", "bank_login_div");

            var type_p = create_elem("p", "type_p");
            type_p.innerHTML = bank_logins_dict["type"];

            var label_to_value_dict = {
                "Owner": bank_logins_dict["owner"],
                "Username": bank_logins_dict["username"],
                "Password": bank_logins_dict["password"]
            };

            var bank_login_table = create_elem("table", "bank_login_table");
            
            for (let label in label_to_value_dict) {
                var tr = create_elem("tr", "bank_login_table_row");

                var td_label = create_elem("td", "bank_login_table_label");
                td_label.innerHTML = label;

                var td_value = create_elem("td", "bank_login_table_value");
                td_value.innerHTML = label_to_value_dict[label];

                tr.appendChild(td_label);
                tr.appendChild(td_value);
                bank_login_table.appendChild(tr);
            }

            bank_login_div.appendChild(type_p);
            bank_login_div.appendChild(bank_login_table);
            bank_logins_div.appendChild(bank_login_div);
        }
        return bank_logins_div;
    }
}
