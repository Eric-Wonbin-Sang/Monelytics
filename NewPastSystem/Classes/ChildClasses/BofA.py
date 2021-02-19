
from NewPastSystem.Classes.ParentClasses import Bank


class BofA(Bank.Bank):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def __str__(self):
        return "BofA Bank - type: {}, id: {}\n\towner: {}\n\tusername: {}\n\tpassword: {}".format(
            self.type,
            self.id,
            self.owner,
            self.username,
            "*" * len(self.password)
        )
