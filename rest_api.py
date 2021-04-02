from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from NewPastSystem import main as past_system

app = Flask(__name__)
CORS(app)
api = Api(app)

bank_list = past_system.get_full_bank_list()


class BankToAccount(Resource):
    def get(self):
        return [bank.to_dict() for bank in bank_list]


class AccountGraph(Resource):
    def get(self, bank_type, owner, account_name):
        temp_bank = None
        for bank in bank_list:
            if bank.type == bank_type and bank.owner == owner:
                temp_bank = bank
                break

        if temp_bank is None:
            return {
                "comment": "bank with type of {} and name of {} not found".format(
                    bank_type, owner
                ),
                "result": None,
            }

        temp_account = None
        for account in temp_bank.account_list:
            if account.name == account_name:
                temp_account = account

        if temp_account is None:
            return {
                "comment": "account with name of {} not found".format(
                    account_name
                ),
                "result": None,
            }

        div = temp_account.get_graph_div()
        print(type(div))
        print(div)
        return {
            "comment": "WORKED".format(
                account_name
            ),
            "result": div,
        }


api.add_resource(BankToAccount, '/get_bank_and_account_info')
api.add_resource(AccountGraph, '/get_graph/<bank_type>/<owner>/<account_name>')


if __name__ == '__main__':
    app.run(debug=True)
