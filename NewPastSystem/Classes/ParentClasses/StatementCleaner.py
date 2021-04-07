import os


class StatementCleaner:

    def __init__(self, account, type_to_statement_class_dict):

        self.account = account
        self.type_to_statement_class_dict = type_to_statement_class_dict

        self.statement_list = self.get_statement_list()

        print("STATEMENT CLEANER -", account.type, account.name)
        for statement in self.statement_list:
            if statement.clean_statement_file_name is not None:
                print("\t", end="")
                file_path = account.clean_statement_files_path + "/" + statement.clean_statement_file_name
                if not os.path.exists(file_path):
                    statement.statement_df.to_csv(file_path, index=True, header=True)
                    print(statement.clean_statement_file_name, "created!")
                else:
                    print(statement.clean_statement_file_name, "exists!")
            else:
                # print("Empty Statement")
                pass

    def get_statement_list(self):
        statement_list = []
        for path in os.listdir(self.account.statement_source_files_path):
            file_path = self.account.statement_source_files_path + "/" + path
            if self.account.type in self.type_to_statement_class_dict:
                statement_list.append(
                    self.type_to_statement_class_dict[self.account.type](
                        parent_account=self.account,
                        file_path=file_path
                    )
                )
            else:
                print("UNKNOWN ACCOUNT TYPE {}".format(self.account.type))

        # filtering and sorting
        statement_list = [statement for statement in statement_list if not statement.is_empty]
        statement_list.sort(key=lambda statement: statement.last_transaction_date)

        return statement_list

    def remove_latest_statement_files(self):
        latest_statement = self.statement_list[-1]
        if latest_statement:
            latest_statement.source_statement_file_path
            latest_statement.clean_statement_file_path
