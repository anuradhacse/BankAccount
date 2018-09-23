import tkinter as tk
from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

win = tk.Tk()
# Set window size here to '440x640' pixels
win.geometry('440x640')
# Set window title here to 'FedUni Banking'
win.winfo_toplevel().title('FedUni Banking')

# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()

# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, textvariable=pin_number_var, show='*')

# The balance label and associated variable
balance_var = tk.StringVar()
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry_var = tk.StringVar()
amount_entry = tk.Entry(win, textvariable=amount_entry_var)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(win, height=10, width=48)

# The bank account object we will work with
account = BankAccount()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    account_pin_entry.delete(0, 'end')


def handle_pin_button(event):
    global pin_number_var
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''
    # Limit to 4 chars in length
    if(len(pin_number_var.get()) > 3 ):
        messagebox.showerror('Invalid Pin Number', ' Enter a four digit PIN number.')
        account_pin_entry.delete(0, 'end')
    else:
        # Set the new pin number on the pin_number_var
        pin_number_var.set(pin_number_var.get() + event.widget['text'])
        print("Pin Number var " + pin_number_var.get())

def log_in(event):
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global account_num_entry

    # Create the filename from the entered account number with '.txt' on the end
    filename = account_number_var.get() + '.txt'

    valid_account = True

    # Try to open the account file for reading
    try:
        account_file = open(filename, 'r')
    except FileNotFoundError:
        messagebox.showerror('Login failed', ' Invalid Account Id.')
        valid_account = False

    if valid_account:
        account_number   = account_file.readline()
        pin_number = account_file.readline()[:-1]
        # Read third and fourth lines (balance and interest rate)
        account_balance  = account_file.readline().rstrip()
        account_interest = account_file.readline().rstrip()
        # Section to read account transactions from file - start an infinite 'do-while' loop here
        # Attempt to read a line from the account file, break if we've hit the end of the file. If we
        # read a line then it's the transaction type, so read the next line which will be the transaction amount.
        # and then create a tuple from both lines and add it to the account's transaction_list
        while True:
            line = account_file.readline()          # Attempt to read a line

            if not line:                            # If we failed, then exit
                print('End of file!')
                break

            # If we did NOT fail, then the 'line' we read will be the transaction
            # type, so the line below it will be the transaction amount.
            amount = account_file.readline()
            account.transaction_list += (line, amount)

        #add a '\n' to last item in the tuple
        account.transaction_list[-1] += '\n'
        print(account.transaction_list)
        # Close the file now we're finished with it
        account_file.close()

        #raise exception if the PIN entered doesn't match account PIN read
        if (pin_number_var.get() == pin_number):
            account.account_number = account_number
            account.pin_number = pin_number
            account.balance = account_balance
            account.interest_rate = account_interest

            messagebox.showinfo('Success', 'Log in successful!')

            # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
            remove_all_widgets()
            create_account_screen()
        else:
            messagebox.showerror('Login failed', ' Invalid Pin Number.')




# ---------- Button Handlers for Account Screen ----------

def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account

    # Save the account with any new transactions
    
    # Reset the bank acount object

    # Reset the account number and pin to blank

    # Remove all widgets and display the login screen again
    

def perform_deposit(event):
    '''Function to add a deposit for the amount in the amount entry to the
       account's transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Get the cash amount to deposit. Note: We check legality inside account's deposit method
    deposit_amount = amount_entry.get()
    try:
        deposit_amount = float(deposit_amount)
    except ValueError:
        messagebox.showerror('Transaction Error', ' Please Enter a valid amount.')
        amount_entry.delete(0, 'end')
        return

    if deposit_amount < 0:
        messagebox.showerror('Transaction Error', ' Cannot deposit negetive amount of money.')
    else:
        amount = str(deposit_amount) + '\n'
        account.transaction_list += ('Deposit\n', amount)
        #show the new deposit in the text field
        transaction_text_widget.config(state='normal')

        # Try to increase the account balance and append the deposit to the account file
        # Deposit funds
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        transaction_text_widget.delete('1.0', 'end')
        transaction_text_widget.insert('insert', account.get_transaction_string())
        transaction_text_widget.config(state='disabled')

        # Change the balance label to reflect the new balance
        account.balance = float(account.balance) + float(deposit_amount)
        balance_var.set('Balance: $' + str(account.balance))

        # Clear the amount entry
        amount_entry.delete(0, 'end')

        # Update the interest graph with our new balance
        plot_interest_graph()

def perform_withdrawal():
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    
        # Get the cash amount to deposit. Note: We check legality inside account's withdraw method
        
        # Withdraw funds        

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.

        # Change the balance label to reflect the new balance

        # Clear the amount entry

        # Update the interest graph with our new balance

    # Catch and display any returned exception as a messagebox 'showerror'
        

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()[0:-1]

def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''

    # YOUR CODE to generate the x and y lists here which will be plotted
    x = []
    y = []
    monthly_interest = float(account.interest_rate) / 12
    multiply_factor = 1 + (monthly_interest) #insterest rate is in format 0.33 not like 33%. So we don
    total = float(account.balance)
    for month in range(1, 13):
        total = total * multiply_factor
        x.append(month)
        y.append(total)

    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5,2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()
    
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')


# ---------- UI Screen Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''    
    
    # ----- Row 0 -----

    # 'FedUni Banking' label here. Font size is 32.
    title = tk.Label(win, text='FedUni Banking', font=(None, 32))
    title.grid(row=0, column=0, columnspan=4)

    # ----- Row 1 -----

    # Acount Number / Pin label here
    account_pin_label = tk.Label(win, text='Acount Number/PIN')
    account_pin_label.grid(row=1, column=0, columnspan=1, sticky='nsew')

    # Account number entry here
    account_number_entry.grid(row=1, column=1, columnspan=1, sticky='nsew')

    # Account pin entry here
    account_pin_entry.grid(row=1, column=2, columnspan=1, sticky='nsew')

    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    b_one = tk.Button(win, text='1')
    b_one.grid(row=2, column=0, sticky='nsew')
    b_one.bind('<Button-1>', handle_pin_button)

    b_two = tk.Button(win, text='2')
    b_two.grid(row=2, column=1, sticky='nsew')
    b_two.bind('<Button-1>', handle_pin_button)

    b_three = tk.Button(win, text='3')
    b_three.grid(row=2, column=2, sticky='nsew')
    b_three.bind('<Button-1>', handle_pin_button)

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    b_four = tk.Button(win, text='4')
    b_four.grid(row=3, column=0, sticky='nsew')
    b_four.bind('<Button-1>', handle_pin_button)

    b_five = tk.Button(win, text='5')
    b_five.grid(row=3, column=1, sticky='nsew')
    b_five.bind('<Button-1>', handle_pin_button)

    b_six = tk.Button(win, text='6')
    b_six.grid(row=3, column=2, sticky='nsew')
    b_six.bind('<Button-1>', handle_pin_button)

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    b_seven = tk.Button(win, text='7')
    b_seven.grid(row=4, column=0, sticky='nsew')
    b_seven.bind('<Button-1>', handle_pin_button)

    b_eight = tk.Button(win, text='8')
    b_eight.grid(row=4, column=1, sticky='nsew')
    b_eight.bind('<Button-1>', handle_pin_button)

    b_nine = tk.Button(win, text='9')
    b_nine.grid(row=4, column=2, sticky='nsew')
    b_nine.bind('<Button-1>', handle_pin_button)

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    b_cancel = tk.Button(win, text='Cancel/Clear', bg='red', activebackground='red')
    b_cancel.grid(row=5, column=0, sticky='nsew')
    b_cancel.bind('<Button-1>', clear_pin_entry)

    # Button 0 here
    b_zero = tk.Button(win, text='0')
    b_zero.grid(row=5, column=1, sticky='nsew')
    b_zero.bind('<Button-1>', handle_pin_button)

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    b_login = tk.Button(win, text='Login', bg='green', activebackground='green')
    b_login.grid(row=5, column=2, sticky='nsew')
    b_login.bind('<ButtonPress-1>', log_in)

    # ----- Set column & row weights -----

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.grid_rowconfigure(0, weight=2)
    win.grid_rowconfigure(1, weight=1)
    win.grid_rowconfigure(2, weight=1)
    win.grid_rowconfigure(3, weight=1)
    win.grid_rowconfigure(4, weight=1)
    win.grid_rowconfigure(5, weight=1)

def create_account_screen():
    '''Function to create the account screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var
    
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    title = tk.Label(win, text='FedUni Banking', font=(None, 24))
    title.grid(row=0, column=0, columnspan=4)

    # ----- Row 1 -----

    # Account number label here
    account_number_label = tk.Label(win, text='Account Number: ' + account.account_number)
    account_number_label.grid(row=1, column=0, columnspan=1)

    # Balance label here
    balance_var.set('Balance: $' + account.balance)
    balance_label.grid(row=1, column=1, columnspan=1)

    # Log out button here
    b_logout = tk.Button(win, text='Log Out')
    b_logout.grid(row=1, column=2, columnspan=2,  sticky='nsew')
    b_logout.bind('<Button-1>', save_and_log_out())

    # ----- Row 2 -----

    # Amount label here
    amount_label = tk.Label(win, text='Amount($) ')
    amount_label.grid(row=2, column=0, columnspan=1)

    # Amount entry here
    amount_entry.grid(row=2, column=1, columnspan=1)

    # Deposit button here
    b_deposit = tk.Button(win, text='Deposit')
    b_deposit.grid(row=2, column=2, columnspan=1,  sticky='nsew')
    b_deposit.bind('<Button-1>', perform_deposit)

    # Withdraw button here
    b_withdraw = tk.Button(win, text='Withdraw')
    b_withdraw.grid(row=2, column=3, columnspan=1, sticky='nsew')
    b_withdraw.bind('<Button-1>', perform_withdrawal())

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    text_scrollbar = tk.Scrollbar(win, command=transaction_text_widget.yview)
    text_scrollbar.grid(row=3, column=3, sticky='nse')


    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    transaction_text_widget.grid(row=3, column=0, columnspan=4, sticky='nsew')

    #add transaction details to transaction Text widget
    for item in account.transaction_list:
        transaction_text_widget.insert('end', item)

    transaction_text_widget.config(state='disabled')
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited

    # Now add the scrollbar and set it to change with the yview of the text widget
    transaction_text_widget['yscrollcommand'] = text_scrollbar.set

    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()

    # ----- Set column & row weights -----
    win.grid_columnconfigure(2, weight=2)
    win.grid_columnconfigure(3, weight=2)

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(1, weight=1)
    win.grid_rowconfigure(2, weight=1)
    win.grid_rowconfigure(3, weight=1)
    win.grid_rowconfigure(4, weight=2)

# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
# create_account_screen()
win.mainloop()
