from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from PastSystem.Classes.ParentClasses import Bank, Account

from Classes import Profile

app = Flask(__name__)
CORS(app)
api = Api(app)

profile_list = Profile.get_profile_list()
main_profile = profile_list[0]
bank_list = main_profile.bank_list
scenario_list = main_profile.scenario_list


# PAST SYSTEM -------------------------------------------------

class BankToAccount(Resource):

    def get(self):
        return [bank.to_dict() for bank in bank_list]


class GraphPastSystem(Resource):

    def get(self, bank_to_accounts_str):
        if bank_to_accounts_str == "show_all":
            return {
                "comment": "showing all",
                "result": Account.graph_accounts(main_profile, [account for bank in bank_list for account in bank.account_list]),
            }

        account_list = bank_to_accounts_str_to_account_list(bank_to_accounts_str)

        return {
            "comment": "WORKED",
            "result": Account.graph_accounts(main_profile, account_list),
        }


class TransactionDictList(Resource):

    def get(self, bank_to_accounts_str):
        if bank_to_accounts_str == "show_all":
            return {
                "comment": "showing all",
                "result": Account.get_all_account_transaction_dict_list([account for bank in bank_list for account in bank.account_list]),
            }

        account_list = bank_to_accounts_str_to_account_list(bank_to_accounts_str)

        return {
            "comment": "WORKED",
            "result": Account.get_all_account_transaction_dict_list(account_list),
        }


def bank_to_accounts_str_to_account_list(bank_to_accounts_str):
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
    return account_list


# FUTURE SYSTEM -------------------------------------------------

class GetScenarioInfo(Resource):

    def get(self):
        return {
            "comment": "WORKED",
            "result": [scenario.to_dict() for scenario in scenario_list]
        }


class GraphFutureSystem(Resource):

    def get(self, scenario_name):

        for scenario in scenario_list:
            if scenario.name == scenario_name:
                return {
                    "comment": "WORKED",
                    "result": scenario.create_graph()
                }
        return {
            "comment": "FAILED",
            "result": None
        }


# Account Info ------------------------------------

class GetProfileInfo(Resource):

    def get(self, profile_name):

        for profile in profile_list:
            if profile.name == profile_name:
                return {
                    "comment": "SUCCESS",
                    "result": main_profile.to_dict()
                }
        return {
            "comment": "FAILED",
            "result": None
        }


api.add_resource(BankToAccount,         '/past_system/get_bank_and_account_info')
api.add_resource(GraphPastSystem,       '/past_system/graph/<bank_to_accounts_str>')
api.add_resource(TransactionDictList,   '/past_system/get_transactions/<bank_to_accounts_str>')

api.add_resource(GetScenarioInfo,       '/future_system/get_scenarios')
api.add_resource(GraphFutureSystem,     '/future_system/graph/<scenario_name>')

api.add_resource(GetProfileInfo,     '/profile/<profile_name>/get_info')


if __name__ == '__main__':
    app.run(debug=True)
