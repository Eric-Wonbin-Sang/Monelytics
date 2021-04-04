from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from NewPastSystem.Classes.ParentClasses import Bank, Account

from NewPastSystem import main as past_system

app = Flask(__name__)
CORS(app)
api = Api(app)

bank_list = past_system.get_full_bank_list()


class BankToAccount(Resource):
    def get(self):
        return [bank.to_dict() for bank in bank_list]


class GraphPastSystem(Resource):
    def get(self, bank_to_accounts_str):

        if bank_to_accounts_str == "show_all":
            return {
                "comment": "showing all",
                "result": Account.graph_accounts([account for bank in bank_list for account in bank.account_list]),
            }

        account_list = []
        for str_part in bank_to_accounts_str.split("BANK")[1:]:
            bank_and_owner, *account_name_list = str_part.split("|")[:-1]
            bank_str, owner_str = bank_and_owner.split("-")

            temp_bank = Bank.find_bank_by_type_and_owner(bank_str, owner_str, bank_list)
            if temp_bank is None:
                continue
            for account_name in account_name_list:
                temp_account = Bank.find_bank_account_by_name(account_name, temp_bank)
                if temp_account is None:
                    continue
                account_list.append(temp_account)

        return {
            "comment": "WORKED",
            "result": Account.graph_accounts(account_list),
        }


api.add_resource(BankToAccount, '/get_bank_and_account_info')
api.add_resource(GraphPastSystem, '/graph_past_system/<bank_to_accounts_str>')


if __name__ == '__main__':
    app.run(debug=True)
