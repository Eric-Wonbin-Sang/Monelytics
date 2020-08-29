from Banks.BankOfAmerica import BankOfAmerica
from Banks.Venmo import Venmo

from General import Functions, Constants


class Profile:

    def __init__(self, **kwargs):

        self.nickname = kwargs.get("nickname")
        self.type = kwargs.get("type")
        self.owner = kwargs.get("owner")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")

        self.bank = self.get_bank()

    def get_bank(self):
        if self.type == "Bank Of America":
            return BankOfAmerica.BankOfAmerica(self, Constants.do_download)
        elif self.type == "Venmo":
            return Venmo.Venmo(self, Constants.do_download)
        raise UserWarning("Unknown Bank type requested - {}".format(self.type))

    def __str__(self):
        return "nick: {}  type: {}  owner: {}, username: {}, password: ****".format(
            self.nickname,
            self.type,
            self.owner,
            self.username
        )


def get_profile_list():
    return [Profile(**kwargs) for kwargs in Functions.parse_json(Constants.profile_list_json)]
