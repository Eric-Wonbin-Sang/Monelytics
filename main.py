from AccountParsers import Account
from StatementFiles import BofAStatement, VenmoStatement


def main():

    bofa_personal_account = Account.Account(name="Personal", id="5329")
    bofa_statement = BofAStatement.BofAStatement(
        account=bofa_personal_account,
        statement_path="C:\\Users\\ericw\\Desktop\\SourceFiles\\2020.12.01 - 2020.04.05 bofa 5329.csv"
    )
    bofa_personal_account.add_statement(bofa_statement)

    print(bofa_statement)

    # ----------------------------------------------------------------------

    venmo_account = Account.Account(name="Personal", id="5329")
    venmo_statement = VenmoStatement.VenmoStatement(
        account=venmo_account,
        statement_path="C:\\Users\\ericw\\Desktop\\SourceFiles\\2020.01.16 - 2020.03.31 venmo.csv"
    )
    venmo_account.add_statement(venmo_statement)

    print(venmo_account)
    

main()
