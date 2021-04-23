
class Scenario {

    constructor(future_system, scenario_dict) {

        this.future_system = future_system;
        this.scenario_dict = scenario_dict;

        this.scenario_json_path = this.scenario_dict["scenario_json_path"];
        this.name = this.scenario_dict["name"];
        this.projection_dict_list = this.scenario_dict["projection_dict_list"];

        this.button = this.get_button();
        this.projection_list = this.get_projection_list();

    }

    get_projection_list() {
        var projection_list = [];
        for(let i in this.projection_dict_list){
            projection_list.push(new Projection(this, this.projection_dict_list[i]));
        }
        return projection_list;
    }

    get_button() {
        var button = create_elem("button", "scenario_button");
        button.innerHTML = this.name;
        var self = this;
        button.onclick = function() {
            self.future_system.reset_scenario_buttons();
            button.classList.toggle("active");
            self.update_graph();
            self.future_system.update_projections_div();
        }
        return button;
    }

    get_graph_rest_url() {
        return "http://127.0.0.1:5000/future_system/graph/" + this.name;
    }

    get_summary_div() {
        var summary_div = create_elem("div", "scenario_summary_div");

        var name_span = create_elem("span", "scenario_attrib");
        name_span.innerHTML = "name: " + this.name;
        summary_div.appendChild(name_span);

        var path_span = create_elem("span", "scenario_attrib");
        path_span.innerHTML = "path: " + this.scenario_json_path;
        summary_div.appendChild(path_span);

        return summary_div
    }

    update_graph() {
        var url = this.get_graph_rest_url();
        request = new XMLHttpRequest();
        request.open("GET", url);
        request.send();
        request.onload = (e) => {
            var analysis_content_div = document.getElementById("graph_div");

            var iframe = create_elem("iframe", "scenario_graph");
            iframe.setAttribute("src", JSON.parse(request.response)["result"]);

            analysis_content_div.innerHTML = "";
            analysis_content_div.appendChild(iframe);

        }
        request.onerror = (e) => {
            console.log("error");
        }
    }

    get_projection_div_list() {
        var div_list = [];
        for (let i in this.projection_list) {
            div_list.push(this.projection_list[i].get_div());
        }
        return div_list;
    }
}
