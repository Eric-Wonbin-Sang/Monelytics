from PastSystem.Banks.AbstractSystem import AbstractBank
from PastSystem.Banks.Venmo import VenmoStatement


class Venmo(AbstractBank.AbstractBank):

    def __init__(self, bank_folder_dir):
        super().__init__(
            bank_folder_dir=bank_folder_dir,
            bank_type="Venmo",
            statement_class=VenmoStatement.VenmoStatement
        )
