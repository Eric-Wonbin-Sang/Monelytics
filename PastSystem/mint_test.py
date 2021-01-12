import mintapi
import pandas
import pprint

# pandas.set_option('display.max_columns', None)
pandas.options.display.max_columns = None
pandas.options.display.max_seq_items = None
pretty = pprint.PrettyPrinter()


def main():

    username = None
    password = None

    mint = mintapi.Mint(
        username,  # Email used to log in to Mint
        password,  # Your password used to log in to mint

        # Optional parameters
        mfa_method='sms',  # Can be 'sms' (default), 'email', or 'soft-token'.
        # if mintapi detects an MFA request, it will trigger the requested method
        # and prompt on the command line.
        headless=False,  # Whether the chromedriver should work without opening a
        # visible window (useful for server-side deployments)
        mfa_input_callback=None,  # A callback accepting a single argument (the prompt)
        # which returns the user-inputted 2FA code. By default
        # the default Python `input` function is used.
        session_path=None,  # Directory that the Chrome persistent session will be written/read from.
        # To avoid the 2FA code being asked for multiple times, you can either set
        # this parameter or log in by hand in Chrome under the same user this runs
        # as.
        imap_account=None,  # account name used to log in to your IMAP server
        imap_password=None,  # account password used to log in to your IMAP server
        imap_server=None,  # IMAP server host name
        imap_folder='INBOX',  # IMAP folder that receives MFA email
        wait_for_sync=False,  # do not wait for accounts to sync
        wait_for_sync_timeout=300,  # number of seconds to wait for sync
    )

    # mint.get_accounts()

    # Get extended account detail at the expense of speed - requires an
    # additional API call for each account
    # print(mint.get_accounts(True))

    # Get budget information
    # pretty.pprint(mint.get_budgets())

    # Get transactions
    transaction_df = mint.get_transactions()  # as pandas dataframe
    pretty.pprint(transaction_df)
    # mint.get_transactions_csv(include_investment=False)  # as raw csv data
    # mint.get_transactions_json(include_investment=False, skip_duplicates=False)

    # Get transactions for a specific account
    # accounts = mint.get_accounts(True)
    # for account in accounts:
    #     print(account)
    #     # mint.get_transactions_csv(id=account["id"])
    #     print(mint.get_transactions_json(id=account["id"]))

    # Get net worth
    print(mint.get_net_worth())

    # Get credit score
    print(mint.get_credit_score())

    # Get bills
    # print(mint.get_bills())

    # Get investments (holdings and transactions)
    # print(mint.get_invests_json())

    # Close session and exit cleanly from selenium/chromedriver
    mint.close()

    # Initiate an account refresh
    # print(mint.initiate_account_refresh())


main()
