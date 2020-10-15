from PastSystem.Banks.AbstractSystem import AbstractBank
from PastSystem.Banks.BankOfAmerica import BankOfAmericaStatement


class BankOfAmerica(AbstractBank.AbstractBank):

    def __init__(self, bank_folder_dir):

        super().__init__(
            bank_folder_dir=bank_folder_dir,
            bank_type="Bank Of America",
            statement_class=BankOfAmericaStatement.BankOfAmericaStatement
        )
