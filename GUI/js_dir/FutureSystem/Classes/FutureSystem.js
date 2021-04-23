
class FutureSystem {

    constructor(json_response) {

        this.json_response = json_response;
        this.scenario_list = this.get_scenario_list();
        
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

    reset_scenario_buttons() {
        for (let i in this.scenario_list) {
            if (this.scenario_list[i].button.classList.contains("active")) {
                this.scenario_list[i].button.classList.toggle("active");
            }
        }
    }

    get_curr_scenario() {
        for (let i in this.scenario_list) {
            if (this.scenario_list[i].button.classList.contains("active")) {
                return this.scenario_list[i];
            }
        }
    }

    get_add_scenario_button() {
        var button = create_elem("button", "add_scenario_button");
        button.innerHTML = "+";
        button.onclick = function() {

        }
        return button;
    }

    initialize_ui() {
        for (let i in this.scenario_list) {
            this.scenario_list[i].button.classList.toggle("active");
            if (i == 0) {
                break;
            }
        }
        this.get_curr_scenario().update_graph();
        this.update_scenarios_sidebar_div();
        this.update_projections_div();
    }

    update_scenarios_sidebar_div() {
        var div = document.getElementById("scenarios_sidebar");
        for (let i in this.scenario_list) {
            div.appendChild(this.scenario_list[i].button);
        }
        div.appendChild(this.get_add_scenario_button());
    }

    update_projections_div() {

        var curr_scenario = this.get_curr_scenario();

        var div = document.getElementById("projections_div");
        div.innerHTML = "";
        var projection_div_list = curr_scenario.get_projection_div_list();
        for (let i in projection_div_list) {
            div.appendChild(projection_div_list[i]);
        }
    }
}
