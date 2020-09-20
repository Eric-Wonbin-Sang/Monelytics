from Banks.AbstractSystem import AbstractBank
from Banks.BankOfAmerica import BankOfAmericaStatement, BankOfAmericaTransaction


class BankOfAmerica(AbstractBank.AbstractBank):

    def __init__(self, bank_folder_dir):

        super().__init__(
            bank_folder_dir=bank_folder_dir,
            bank_type="Bank Of America",
            statement_class=BankOfAmericaStatement.BankOfAmericaStatement,
            transaction_class=BankOfAmericaTransaction.BankOfAmericaTransaction
        )
