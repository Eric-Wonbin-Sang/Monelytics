
class FutureSystem {

    constructor(json_response) {

        this.json_response = json_response;
        this.scenario_list = this.get_scenario_list();
        
        // this.get_banks_and_accounts_sidebar_div()
        this.initialize_ui();
    
    }

    get_scenario_list() {
        var scenario_list = [];
        var scenario_dict_list = JSON.parse(this.json_response)["result"];
        for(let i in scenario_dict_list){
            scenario_list.push(new Scenario(this, scenario_dict_list[i]));
        }
        return scenario_list;
    }

    initialize_ui() {
        for (let i in this.scenario_list) {
            this.scenario_list[i].update_graph();
            if (i == 0) {
                break;
            }
        }
        // this.update_scenario_selection_div(this.scenario_list[0]);
        this.update_projections_div(this.scenario_list[0]);
    }

    update_scenario_selection_div(curr_scenario) {

        var dropdown_div = document.getElementById("scenarios_dropdown");

        var button = create_elem("button", "scenario_button");
        button.innerHTML  = curr_scenario.name
        button.onclick = function() {
            document.getElementById("scenarios_a_div").classList.toggle("show");
        }
        dropdown_div.appendChild(button);

        var scenarios_a_div = create_elem("div", null, "scenarios_a_div");
        for (let i in this.scenario_list) {
            var scenario = this.scenario_list[i];
            var a_elem = create_elem("a");
            a_elem.innerHTML = scenario.name;
            a_elem.href = "#";
            scenarios_a_div.appendChild(a_elem);
        }
        dropdown_div.appendChild(scenarios_a_div);

        dropdown_div.appendChild(curr_scenario.get_summary_div());

    }

    update_projections_div(curr_scenario) {
        var div = document.getElementById("projections_div");
        var projection_div_list = curr_scenario.get_projection_div_list();
        for (let i in projection_div_list) {
            div.appendChild(projection_div_list[i]);
        }
    }
}
