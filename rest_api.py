from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from NewPastSystem import main as past_system

app = Flask(__name__)
CORS(app)
api = Api(app)


class Test(Resource):

    def get(self):
        return {
            "test": "hello"
        }


class BankToAccount(Resource):

    bank_list = past_system.get_full_bank_list()

    def get(self):
        return [bank.to_dict() for bank in self.bank_list]


api.add_resource(Test, '/test')
api.add_resource(BankToAccount, '/get_bank_and_account_info')


if __name__ == '__main__':
    app.run(debug=True)
