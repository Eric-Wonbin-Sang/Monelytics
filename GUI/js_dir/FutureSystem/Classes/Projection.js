
class Projection {

    constructor(parent_scenario, projection_dict) {

        this.parent_scenario = parent_scenario;
        this.projection_dict = projection_dict;

        this.name = this.projection_dict["name"];
        this.start_datetime = this.projection_dict["start_datetime"];
        this.end_datetime = this.projection_dict["end_datetime"];
        this.frequency = this.projection_dict["frequency"];
        this.amount = this.projection_dict["amount"];

    }

    get_div() {

        var div = create_elem("div", "projection_div");

        var key_to_label_dict = {
            "name": "Name",
            "start_datetime": "Start",
            "end_datetime": "End",
            "frequency": "Frequency",
            "amount": "Amount",
        };
        
        for (let key in this.projection_dict) {
            var label_div = create_elem("div", "projection_label_div");
            var value_div = create_elem("div", "projection_value_div");
            
            var attribute_div = create_elem("div", "projection_atrtibute");
            var span = create_elem("span", "projection_atrtibute_name");
            span.innerHTML = key_to_label_dict[key];
            var input = create_elem("input", "projection_atrtibute_value");
            input.value = this.projection_dict[key];

            label_div.appendChild(span);
            value_div.appendChild(input);
            attribute_div.appendChild(label_div);
            attribute_div.appendChild(value_div);
            div.appendChild(attribute_div);

        }
        return div;
    }
}
