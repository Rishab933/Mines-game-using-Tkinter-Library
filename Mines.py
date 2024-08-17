import random
from tkinter import *
import numpy as np
from PIL import Image, ImageTk

custom_msg_canvas = None


# something to do with upi id to make the system real

def create_array():  # This creates an array from 1 to 25 to randomly select one danger title

    a = np.arange(1, 26)
    danger = random.choice(a)

    return danger


def profit(i):  # This returns the odds that you have won on the bases of correct title chosen

    a = np.array(
        [1.03, 1.08, 1.12, 1.18, 1.24, 1.30, 1.37, 1.46, 1.55, 1.65, 1.77, 1.90, 2.06, 2.25, 2.47, 2.75, 3.09, 3.54,
         4.13, 4.95, 6.19, 8.25, 12.38, 24.75])

    return a[i]


def click(event):  # This defines the functionality of Bet, 1/2, 2x, Cash out, 25 titles button

    global d, bet_clicked, grid_button_clicked, custom_msg_canvas, f, custom_wallet_canvas

    text = event.widget.cget("text")
    if text == "Bet":
        f = list(range(1, 26))
        print("Bet Button working")
        current_balance_amt = balance.get()  # This part subtract the bet amount from the main balance
        B = bet_amount.get()
        if B > current_balance_amt:
            bet_amount.set(current_balance_amt)
            new_balance_amt = 0
            print(f"Updated balance is {new_balance_amt}")
            balance.set(new_balance_amt)
            Bet_Amount_entry.update()
            Top_bar_balance.update()
        else:
            new_balance_amt = round((current_balance_amt - B), 1)
            print(f"Updated balance is {new_balance_amt}")
            balance.set(new_balance_amt)
            Top_bar_balance.update()

        d = create_array()  # Create a new danger tile
        f.remove(d)
        bet_clicked = True
        grid_button_clicked = False
        Bet_button.config(text="Cash Out")
        Bet_button.config(state=DISABLED)  # disable Cash Out initially
        enable_grid_buttons()
        reset_button_colors()  # ensure buttons are reset before new round
        if custom_msg_canvas:
            custom_msg_canvas.destroy()
            custom_msg_canvas = None

    elif text == "Cash Out":  # Cash out function
        if grid_button_clicked:
            cash_out()

    elif text == "1/2":  # Half button to make the bet amount half
        if bet_clicked:
            event.widget.config(state=DISABLED)
        else:
            event.widget.config(state=NORMAL)
            print("1/2 Button is working")
            a = bet_amount.get()
            a = a / 2
            bet_amount.set(a)
            print(f"Updated Bet Amount is {a}")
            Bet_Amount_entry.update()

    elif text == "2x":  # 2x button to double the bet amount if bet amount is 0 then it
        if bet_clicked:
            event.widget.config(state=DISABLED)
        else:
            event.widget.config(state=NORMAL)
            print("2x Button is working")  # first set the bet amount to 0.1
            a = bet_amount.get()
            if a == 0.0:
                a = 0.1
                bet_amount.set(a)
                Bet_Amount_entry.update()
            else:
                a = a * 2
                bet_amount.set(a)
                print(f"Updated Bet Amount is {a}")
                Bet_Amount_entry.update()

    elif text == "Wallet":  # To display the wallet functionality
        print("Wallet Button working")
        show_custom_wallet()


    else:  # Here comes the functionality for the 25 tiles button
        if bet_clicked:
            event.widget.config(state=DISABLED)        ########################################
            if int(text) == d:
                print("Not safe")
                event.widget.config(bg="#FF0001", fg="#FF0001")
                Bet_button.config(text="Bet")
                disable_grid_buttons()
                bet_clicked = False
                n_mines.set(24)
                NUmber_of_gems.update()
            else:
                print("Safe")
                event.widget.config(bg="#00E701", fg="#00E701")

                if int(text) in f:  # This calculates and display the number of safe titles or gems
                    f.remove(int(text))  # that are yet to be chosen
                    x = len(f)
                    n_mines.set(x)
                    NUmber_of_gems.update()
                    check_all_safe_tiles_clicked()
                grid_button_clicked = True
                Bet_button.config(state=NORMAL)  # Enable Cash Out


def disable_grid_buttons():
    for button in grid_buttons:
        button.config(state=DISABLED)


def check_all_safe_tiles_clicked():
    a = n_mines.get()
    if a == 0:
        max_win()


def enable_grid_buttons():
    for button in grid_buttons:
        button.config(state=NORMAL)


def cash_out():
    global bet_clicked
    print("Cash Out Button working")
    reveal_danger_button()
    disable_safe_buttons()
    Bet_button.config(text="Bet")
    bet_clicked = False
    reset_button_colors()  # Reset colors after cash out
    x = n_mines.get()
    print(f"x = {x}")
    a = 24 - x
    print(a)
    if a == 0:
        max_win()
    else:
        print(f"Number of gems {a}")
        print(f"You made a profit of {profit(a - 1)}")  # Profit generated
        v = profit(a - 1)
        p = bet_amount.get()
        r = p * v
        a = r - p
        edge = 0.02 * a
        final_payout = round((r - edge), 1)
        print(f"You have made a profit of {final_payout}")
        show_custom_message("", f"{v}x", f"{final_payout}")
        b = n_mines.get()
        b = 24
        n_mines.set(b)
        NUmber_of_gems.update()
        current_balance = balance.get()
        new_balance = round((current_balance + final_payout), 1)
        balance.set(new_balance)
        Top_bar_balance.update()


def reveal_danger_button():
    danger_button = get_button_with_text(str(d))
    if danger_button:
        danger_button.config(bg="red")


def get_button_with_text(text):
    for button in grid_buttons:
        if button.cget("text") == text:
            return button
    return None


def disable_safe_buttons():
    for button in grid_buttons:
        if button.cget("text") != str(d):
            button.config(state=DISABLED)


def reset_button_colors():
    for button in grid_buttons:
        button.config(bg="#2F4553", fg="#BDBDBD")  # Reset to default colors


def max_win():
    global bet_clicked, custom_msg_canvas
    a = 24
    n_mines.set(a)
    NUmber_of_gems.update()
    v = 24.75
    print("Max win odd : 24.75")
    b = bet_amount.get()
    p = b * v
    net_p = p - b
    edge = 0.02 * net_p
    final_payout = round((p - edge), 1)
    print(f"Max win : {p}")
    disable_safe_buttons()
    Bet_button.config(text="Bet")
    bet_clicked = False
    reset_button_colors()
    show_custom_message("", f"{v}x", f"{final_payout}")
    current_balance = balance.get()
    new_balance = round((current_balance + final_payout), 1)
    balance.set(new_balance)
    Top_bar_balance.update()


def show_custom_message(title, message1, message2):
    global custom_msg_canvas
    custom_msg_canvas = Canvas(root, width=130, height=80, bg="#1A2C38", highlightthickness=5,
                               highlightbackground="#00E701")
    custom_msg_canvas.place(x=430, y=261)
    custom_msg_canvas.create_line(55, 50, 88, 50, width=3, fill="#2F4553")
    custom_msg_label = Label(custom_msg_canvas, text=message1, font=("Arial", 20, "bold"), bg="#1A2C38", fg="#00E701")
    custom_msg_label.place(x=70, y=28, anchor="center")
    custom_msg_label = Label(custom_msg_canvas, text=message2, font=("Arial", 10, "bold"), bg="#1A2C38", fg="#00E701")
    custom_msg_label.place(x=70, y=68, anchor="center")


def show_custom_wallet():
    global custom_wallet_canvas, img_tk
    custom_wallet_canvas = Canvas(root, width=400, height=330, bg="#1A2C38", borderwidth=0, highlightthickness=0)
    custom_wallet_canvas.place(x=250, y=140)
    custom_wallet_canvas.create_rectangle(0, 295, 400, 330, fill="#0F212E", outline="")
    x = balance.get()
    print(f"Your wallet balance is {x}")

    l1 = Label(custom_wallet_canvas, text="Wallet", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2")
    l1.place(x=10, y=10)

    b1 = Button(custom_wallet_canvas, text="x", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2", borderwidth=0,
                highlightthickness=0, command=destroy_wallet_canvas)
    b1.place(x=378, y=6)

    i = Image.open("img.png")
    i = i.resize((360, 150))
    img_tk = ImageTk.PhotoImage(i)
    l2 = Label(custom_wallet_canvas, image=img_tk, bg="#1A2C38")
    l2.place(x=18, y=38)

    if x == 0.0:
        st = "Your wallet is currently empty."
        l4 = Label(custom_wallet_canvas,
                   text="Make a deposit via crypto or local currency if it is available in your \n"
                        "region", font="Arial 8 bold", bg="#1A2C38", fg="#A6AFC7")
        l4.place(x=20, y=220)
    else:
        st = f"Your wallet balance is {x}"
    print(st)
    l3 = Label(custom_wallet_canvas, text=st, font="Arial 18 bold", bg="#1A2C38", fg="#CBCFD2")
    l3.place(x=20, y=190)

    b2 = Button(custom_wallet_canvas, text="Deposit", width=16, height=1, font="Arial 11 bold", bg="#1475E1",
                fg="#CBCFD2", borderwidth=0,
                highlightthickness=0, command=deposit)
    new_balance = balance.get()
    st = f"Your wallet balance is {new_balance}"
    print(st)
    l3.config(text=st)
    b2.place(x=35, y=260)
    b3 = Button(custom_wallet_canvas, text="Withdraw", width=16, height=1, font="Arial 11 bold", bg="#1475E1",
                fg="#CBCFD2", borderwidth=0,
                highlightthickness=0, command=withdraw)
    b3.place(x=215, y=260)


def deposit():
    print("Deposit button is clicked")
    global custom_deposit_canvas, amt_entry, deposit_amt, l2
    custom_deposit_canvas = Canvas(root, width=400, height=330, bg="#1A2C38", borderwidth=0, highlightthickness=0)
    custom_deposit_canvas.place(x=250, y=140)
    l1 = Label(custom_deposit_canvas, text="Wallet / Deposit", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2")
    l1.place(x=10, y=10)
    b1 = Button(custom_deposit_canvas, text="x", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2", borderwidth=0,
                highlightthickness=0, command=destroy_deposit_canvas)
    b1.place(x=378, y=6)
    l3 = Label(custom_deposit_canvas, text="Enter UPI ID :", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2")
    l3.place(x=20, y=125)
    UPI = StringVar()
    UPI_entry = Entry(custom_deposit_canvas, textvariable=UPI, font="arial 15 bold", fg="white", bg="#0F212E",
                      width=32,
                      borderwidth=1, highlightthickness=1, highlightbackground="white")
    UPI_entry.place(x=20, y=150)
    l4 = Label(custom_deposit_canvas, text="Amount :", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2")
    l4.place(x=20, y=185)
    deposit_amt = DoubleVar()  # This remains a DoubleVar
    amt_entry = Entry(custom_deposit_canvas, textvariable=deposit_amt, font="arial 15 bold", fg="white", bg="#0F212E",
                      width=32,
                      borderwidth=1, highlightthickness=1, highlightbackground="white")
    amt_entry.place(x=20, y=210)
    b3 = Button(custom_deposit_canvas, text="Confirm", font="arial 12 bold", fg="#CBCFD2", bg="#1475E1", width=8,
                borderwidth=0, highlightthickness=0, command=confirm_deposit)
    b3.place(x=165, y=270)
    x = balance.get()
    st = f"Your current \nwallet balance is {x}"
    l2 = Label(custom_deposit_canvas, text=st, font="Arial 15 bold", bg="#1A2C38", fg="#CBCFD2", padx=25)
    l2.place(x=80, y=50)


def destroy_deposit_canvas():
    global custom_deposit_canvas
    print("x button is working")
    custom_deposit_canvas.destroy()
    show_custom_wallet()


def confirm_deposit():
    global amt_entry, deposit_amt, balance, l2
    print("Confirm button working")
    try:
        deposit_amount = deposit_amt.get()
    except ValueError:
        print("Invalid amount entered")
        l2.config(text="Invalid deposit amount.\n Please enter a number.")
        return
    print(f"Deposit amount: {deposit_amount}")
    current_balance = balance.get()
    print(f"Current balance: {current_balance}")

    new_balance = current_balance + deposit_amount
    balance.set(new_balance)
    print(f"New balance: {new_balance}")
    Top_bar_balance.update()
    s = f"Your current \nwallet balance is {new_balance}"
    l2.config(text=s)
    deposit_amt.set(0)
    amt_entry.update()
    destroy_wallet_canvas()


def withdraw():
    global custom_withdraw_canvas, amt_entry, withdraw_amt, l2
    print("Withdraw button is clicked")
    custom_withdraw_canvas = Canvas(root, width=400, height=330, bg="#1A2C38", borderwidth=0, highlightthickness=0)
    custom_withdraw_canvas.place(x=250, y=140)
    l1 = Label(custom_withdraw_canvas, text="Wallet / Withdraw", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2")
    l1.place(x=10, y=10)
    b1 = Button(custom_withdraw_canvas, text="x", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2", borderwidth=0,
                highlightthickness=0, command=destroy_withdraw_canvas)
    b1.place(x=378, y=6)
    l3 = Label(custom_withdraw_canvas, text="Enter UPI ID :", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2")
    l3.place(x=20, y=125)
    UPI = StringVar()
    UPI_entry = Entry(custom_withdraw_canvas, textvariable=UPI, font="arial 15 bold", fg="white", bg="#0F212E",
                      width=32,
                      borderwidth=1, highlightthickness=1, highlightbackground="white")
    UPI_entry.place(x=20, y=150)
    l4 = Label(custom_withdraw_canvas, text="Amount :", font="Arial 10 bold", bg="#1A2C38", fg="#CBCFD2")
    l4.place(x=20, y=185)
    withdraw_amt = DoubleVar()
    amt_entry = Entry(custom_withdraw_canvas, textvariable=withdraw_amt, font="arial 15 bold", fg="white", bg="#0F212E",
                      width=28,
                      borderwidth=1, highlightthickness=1, highlightbackground="white")
    amt_entry.place(x=20, y=210)
    custom_withdraw_canvas.create_rectangle(330, 209.5, 376, 240, fill="white", outline="")
    b2 = Button(custom_withdraw_canvas, text="Max", font="arial 12 bold", fg="white", bg="#0F212E", width=4,
                borderwidth=0, highlightthickness=0, pady=1.49, command=max_withdraw)
    b2.place(x=331, y=211)
    b3 = Button(custom_withdraw_canvas, text="Confirm", font="arial 12 bold", fg="#CBCFD2", bg="#1475E1", width=8,
                borderwidth=0, highlightthickness=0, command=confirm_withdraw)
    b3.place(x=165, y=270)
    x = balance.get()
    st = StringVar()
    if x == 0.0:
        st = "Sorry your wallet is empty!\n Can't withdraw"
    else:
        st = f"Your wallet balance \navailable to withdraw is : {x}"
    l2 = Label(custom_withdraw_canvas, text=st, font="Arial 15 bold", bg="#1A2C38", fg="#CBCFD2")
    l2.place(x=80, y=50)


def destroy_withdraw_canvas():
    global custom_withdraw_canvas
    print("x button is working")
    custom_withdraw_canvas.destroy()
    show_custom_wallet()


def max_withdraw():
    global amt_entry, withdraw_amt
    print("max button working")
    x = balance.get()
    withdraw_amt.set(x)
    amt_entry.update()


def confirm_withdraw():
    global amt_entry, withdraw_amt, balance, l2
    print("Confirm button working")
    try:
        withdraw_amount = float(amt_entry.get())
    except ValueError:
        print("Invalid amount entered")
        l2.config(text="Invalid withdrawal amount.\n Please enter a number.")
        return
    print(f"Withdraw amount: {withdraw_amount}")
    current_balance = balance.get()
    print(f"Current balance: {current_balance}")
    if withdraw_amount > current_balance:
        print("Withdrawal amount exceeds current balance")
        l2.config(text="Insufficient \nfunds for withdrawal.", padx=25)
        return
    new_balance = current_balance - withdraw_amount
    balance.set(new_balance)
    print(f"New balance: {new_balance}")
    Top_bar_balance.update()
    if new_balance > 0:
        s = f"Your wallet balance \navailable to withdraw is: {new_balance}"
    else:
        s = "Sorry, your wallet is empty!\nCan't withdraw"
    l2.config(text=s)
    withdraw_amt.set(0)
    amt_entry.update()
    destroy_wallet_canvas()


def destroy_wallet_canvas():
    global custom_wallet_canvas
    print("x button is working of wallet canvas")
    custom_wallet_canvas.destroy()


root = Tk()
root.title("MINES")
root.geometry("800x600+400+100")
root.resizable(False, False)
root.configure(bg="#213743")

Top_bar = Frame(root, bg="#1A2C38", height=50, relief=SOLID)
Top_bar.pack(side=TOP, fill=X)

content_frame = Frame(Top_bar, bg="#1A2C38")
content_frame.place(relwidth=1, relheight=1)

Top_bar_lable = Label(content_frame, text="MINES", fg="white", bg="#1A2C38", font="palatino 18")
Top_bar_lable.place(x=10, y=(35 - 18) // 2)

balance = DoubleVar()
balance.set(0)  #############################################
Top_bar_balance = Label(content_frame, bg="#0F212E", width=10, height=1, textvariable=balance, fg="white", font=8,
                        padx=10, pady=3.49)
Top_bar_balance.place(x=325, y=(35 - 20) // 2)

Top_bar_wallet = Button(content_frame, text="Wallet", width=4, height=1, fg="white", bg="#1475E1", padx=10, pady=6.89,
                        borderwidth=0, highlightthickness=0)
Top_bar_wallet.bind('<Button-1>', click)
Top_bar_wallet.place(x=457, y=(34.5 - 19) // 2)

can_widget = Canvas(root, width=800, height=800, bg="#1A2C38", borderwidth=0, highlightthickness=0)
can_widget.pack(padx=20, pady=15)
can_widget.create_rectangle(0, 0, 200, 476, outline="")  #-->left
can_widget.create_rectangle(0, 476, 759, 518, fill="#0F212E", outline="")  #-->bottom
can_widget.create_rectangle(200, 0, 759, 472, fill="#0F212E", outline="")  #-->right

can_widget.create_rectangle(12, 35, 190, 68, fill="#2F4553", outline="")  #bet amount
can_widget.create_rectangle(12.5, 35.5, 125, 67, fill="#0F212E", outline="")  #bet amount

Bet_Amount_label = Label(can_widget, text="Bet Amount", fg="#BDBDBD", bg="#1A2C38", font="arial 9 bold")
can_widget.create_window((45, 20), window=Bet_Amount_label)

bet_amount = DoubleVar()
bet_amount.set(0)

Bet_Amount_entry = Entry(can_widget, textvariable=bet_amount, font="arial 10 bold", fg="white", bg="#0F212E", width=15,
                         borderwidth=0, highlightthickness=0)
can_widget.create_window((69, 53), window=Bet_Amount_entry)

Bet_Amount_half = Button(can_widget, text="1/2", font="arial 8 bold", fg="#BDBDBD", bg="#2F4553", borderwidth=0)
can_widget.create_window((140, 52), window=Bet_Amount_half)
Bet_Amount_half.bind('<Button-1>', click)

can_widget.create_line(159, 40, 159, 62, fill="#0F212E")

Bet_Amount_double = Button(can_widget, text="2x", font="arial 8 bold", fg="#BDBDBD", bg="#2F4553", borderwidth=0)
can_widget.create_window((175, 52), window=Bet_Amount_double)
Bet_Amount_double.bind('<Button-1>', click)

Mines_label = Label(can_widget, text="Mines", fg="#BDBDBD", bg="#1A2C38", font="arial 9 bold")
can_widget.create_window((30, 83), window=Mines_label)

can_widget.create_rectangle(12, 95, 190, 125, fill="#2F4553", outline="")
can_widget.create_rectangle(12.5, 95.5, 189, 124, fill="#0F212E", outline="")

NUmber_of_mines = Label(can_widget, text="1", fg="white", bg="#0F212E", font="arial 9 bold")
can_widget.create_window((25, 110), window=NUmber_of_mines)

Gems_label = Label(can_widget, text="Gems", fg="#BDBDBD", bg="#1A2C38", font="arial 9 bold")
can_widget.create_window((30, 139), window=Gems_label)

can_widget.create_rectangle(12, 150, 190, 180, fill="#2F4553", outline="")
can_widget.create_rectangle(12.5, 150.5, 189, 179, fill="#0F212E", outline="")

n_mines = IntVar()
n_mines.set(24)
NUmber_of_gems = Label(can_widget, textvariable=n_mines, fg="white", bg="#0F212E", font="arial 9 bold")
can_widget.create_window((25, 165), window=NUmber_of_gems)

Bet_button = Button(can_widget, text="Bet", font="arial 8 bold", fg="black", bg="#00E701", borderwidth=0, width=24,
                    height=2)
can_widget.create_window((100, 210), window=Bet_button)
Bet_button.bind('<Button-1>', click)


def create_buttons(canvas, x_start, y_start, text, font, bd, bg, click, borderwidth, highlightthickness, rows, cols,
                   x_step, y_step, relief):
    global grid_buttons
    grid_buttons = []
    for row in range(rows):
        for col in range(cols):
            b = Button(canvas, text=text, width=4, height=1, borderwidth=borderwidth, font=font,
                       highlightthickness=highlightthickness, bd=bd, bg=bg, relief=relief)
            b.bind("<Button-1>", click)
            a = int(text)
            a = a + 1
            text = a
            canvas.create_window((x_start + col * x_step, y_start + row * y_step), window=b)
            grid_buttons.append(b)
    disable_grid_buttons()


create_buttons(can_widget, x_start=260, y_start=56, text="1", font="arial 30", bd=1, bg="#2F4553", click=click, rows=5,
               cols=5, x_step=110, y_step=90, borderwidth=0, highlightthickness=0, relief=SOLID)

bet_clicked = False
grid_button_clicked = False

root.mainloop()
