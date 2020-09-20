
class AbstractStatement:

    def __init__(self, parent_account, statement_file_path):

        self.parent_account = parent_account
        self.statement_file_path = statement_file_path

    def __str__(self):
        return self.statement_file_path
