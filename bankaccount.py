class BankAccount():

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number = '0'
        self.pin_number = ''
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []
        

    def deposit(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        try:
            deposit_amount = float(amount)
            amount = str(deposit_amount) + '\n'
            self.transaction_list += ('Deposit\n', amount)
            self.balance = float(self.balance) + deposit_amount
            return "deposited"
        except (TypeError,ValueError):
            return

    def withdraw(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        try:
            withdraw_amount = float(amount)
            amount = str(withdraw_amount) + '\n'
            self.transaction_list += ('Withdraw\n', amount)
            if float(self.balance) < withdraw_amount:
                raise ValueError("Withdraw amount is more than the balance!")

            self.balance = float(self.balance) - withdraw_amount
            return "withdraw"
        except (TypeError,ValueError) as errorMsg:
            if "Withdraw amount" in str(errorMsg):
                return "Withdraw amount is more than the balance!"
            return "Please enter a valid amount!"
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''
        return ''.join(self.transaction_list)


    def export_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        filename = self.account_number[:-1] + '.txt'
        try:
            account_file = open(filename, 'w')
        except FileNotFoundError:
            # messagebox.showerror('Unexpected Error', ' Error occurred while saving the file.')
            return ' Error occurred while saving the file.'

        account_file.write(self.account_number)
        account_file.write(self.pin_number + '\n')
        account_file.write(str(self.balance) + '\n')
        account_file.write(str(self.interest_rate) + '\n')
        account_file.write(self.get_transaction_string()[:-1])
        account_file.close()
        return 'success'