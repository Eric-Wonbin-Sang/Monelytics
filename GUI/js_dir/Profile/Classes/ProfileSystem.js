
class ProfileSystem {

    constructor(profile) {

        this.profile = profile;

        this.initialize_ui();

    }

    initialize_ui() {
        this.update_profile_photo_div();
        this.update_info_div();
    }

    update_profile_photo_div() {
        var div = document.getElementById("profile_photo_div");
        div.appendChild(this.profile.get_name_p());
        div.appendChild(this.profile.get_image());
    }

    update_info_div() {
        var div = document.getElementById("info_div");
        div.appendChild(this.profile.get_bank_logins_to_html());
    }
}
