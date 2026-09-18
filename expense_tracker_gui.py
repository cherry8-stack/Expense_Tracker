'''
creating a simple expense tracker with basic functionlities 
and good UI using customtkinter
'''
import customtkinter as ctk
import json
from datetime import datetime
from CTkMessagebox import CTkMessagebox

# JSON for saving data
def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)

def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

expenses = load_expenses()

# Window
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Expense Tracker")
app.geometry("1100x650")
app.resizable(False, False)

# Welcome screen
welcome = ctk.CTkFrame(app, fg_color="#F8F8F5")
welcome.pack(fill="both", expand=True)

ctk.CTkLabel(
    welcome, text="✦   ✧   ✦",
    font=("Arial", 22), text_color="#9CCFE8"
).place(relx=.5, rely=.32, anchor="center")

greeting = ctk.CTkLabel(
    welcome, text="Hey buddy ☺️",
    font=("Arial", 42, "bold"), text_color="#4B6584"
)

subtitle = ctk.CTkLabel(
    welcome, text="Welcome to your Expense Tracker",
    font=("Arial", 18), text_color="#829AB1"
)

dots = ctk.CTkLabel(
    welcome, text="•  •  •",
    font=("Arial", 20), text_color="#A7C7E7"
)

def start():
    greeting.place(relx=.5, rely=.45, anchor="center")
    app.after(400, lambda: subtitle.place(relx=.5, rely=.54, anchor="center"))
    app.after(900, lambda: dots.place(relx=.5, rely=.64, anchor="center"))
    app.after(1800, dashboard)

# Main dashboard
def dashboard():
    welcome.destroy()

    main = ctk.CTkFrame(app, fg_color="#F8FBFF")
    main.pack(fill="both", expand=True)

    side = ctk.CTkFrame(main, width=220, fg_color="#EEF7FC")
    side.pack(side="left", fill="y")
    side.pack_propagate(False)

    ctk.CTkLabel(
        side, text="EXPENSE\nTRACKER",
        font=("Arial", 24, "bold"), text_color="#4B6584"
    ).pack(pady=(40, 50))

    content = ctk.CTkFrame(main, fg_color="#F8FBFF")
    content.pack(side="left", fill="both", expand=True)

    def clear():
        for widget in content.winfo_children():
            widget.destroy()

    # Dashboard 
    def show_dashboard():
        clear()

        hour = datetime.now().hour

        if hour < 12:
            greeting_text = "Good morning, buddy ☺️"
        elif hour < 17:
            greeting_text = "Good afternoon, buddy ☺️"
        else:
            greeting_text = "Good evening, buddy ☺️"

        heading = ctk.CTkLabel(
            content,
            text=greeting_text,
            font=("Arial", 30, "bold"),
            text_color="#4B6584"
        )

        heading.pack(
        anchor="w",
        padx=40,
        pady=(35, 5)
        )

        

        ctk.CTkLabel(
            content, text="Here's your spending overview.",
            font=("Arial", 16), text_color="#829AB1"
        ).pack(anchor="w", padx=40)

        total = sum(e["Amount"] for e in expenses)
        count = len(expenses)
        average = total / count if count else 0

        cards = ctk.CTkFrame(content, fg_color="transparent")
        cards.pack(fill="x", padx=40, pady=30)

        data = [
            ("TOTAL SPENDING", f"₹ {total}", "#E4F3FA"),
            ("TOTAL EXPENSES", str(count), "#EEE8FA"),
            ("AVERAGE EXPENSE", f"₹ {average:.2f}", "#E8F5ED")
        ]

        for title, value, color in data:
            card = ctk.CTkFrame(cards, fg_color=color, corner_radius=20)
            card.pack(side="left", fill="both", expand=True, padx=8)

            ctk.CTkLabel(
                card, text=title,
                font=("Arial", 14, "bold"), text_color="#588995"
            ).pack(anchor="w", padx=22, pady=(20, 5))

            ctk.CTkLabel(
                card, text=value,
                font=("Arial", 30, "bold"), text_color="#355070"
            ).pack(anchor="w", padx=22)

        recent = ctk.CTkFrame(content, fg_color="white", corner_radius=20)
        recent.pack(fill="both", expand=True, padx=40, pady=(0, 35))

        ctk.CTkLabel(
            recent, text="Recent Expenses",
            font=("Arial", 22, "bold"), text_color="#4B6584"
        ).pack(anchor="w", padx=25, pady=20)

        if not expenses:
            ctk.CTkLabel(
                recent, text="No expenses recorded yet.",
                text_color="#829AB1"
            ).pack(anchor="w", padx=25)
        else:
            for e in expenses[-5:][::-1]:
                ctk.CTkLabel(
                    recent,
                    text=f"{e['category']}    ₹ {e['Amount']}    {e['Description']}",
                    text_color="#4B6584"
                ).pack(anchor="w", padx=25, pady=5)

    # Add expense
    def show_add():
        clear()

        ctk.CTkLabel(
            content, text="Add Expense 💰",
            font=("Arial", 30, "bold"), text_color="#4B6584"
        ).pack(anchor="w", padx=40, pady=(35, 5))

        ctk.CTkLabel(
            content, text="Record a new expense.",
            font=("Arial", 16), text_color="#829AB1"
        ).pack(anchor="w", padx=40)

        form = ctk.CTkFrame(content, fg_color="white", corner_radius=20)
        form.pack(fill="x", padx=40, pady=30)

        entries = []

        for label, placeholder in [
            ("Category", "Food, Travel, Shopping..."),
            ("Amount", "Enter amount"),
            ("Description", "What did you spend on?")
        ]:
            ctk.CTkLabel(
                form, text=label,
                font=("Arial", 15, "bold"), text_color="#4B6584"
            ).pack(anchor="w", padx=30, pady=(20, 5))

            entry = ctk.CTkEntry(
                form, placeholder_text=placeholder,
                height=45, corner_radius=12
            )
            entry.pack(fill="x", padx=30)
            entries.append(entry)

        message = ctk.CTkLabel(
            form, text="", text_color="#5B8E7D",
            font=("Arial", 15, "bold")
        )
        message.pack(pady=10)

        def add():
            category, amount, description = [e.get() for e in entries]

            if not category or not amount or not description:
                CTkMessagebox(
                    title="Missing Information",
                    message="Please fill in all the fields."
                )
                return

            try:
                amount = int(amount)
            except ValueError:
                CTkMessagebox(
                    title="Invalid Amount",
                    message="Please enter a valid number."
                )
                return

            expenses.append({
                "category": category,
                "Amount": amount,
                "Description": description,
                "Datetime": datetime.now().strftime("%d-%m-%Y %I:%M %p")
            })

            save_expenses()

            for e in entries:
                e.delete(0, "end")

            message.configure(text="✓ Expense added successfully!")

        ctk.CTkButton(
            form, text="Save Expense ✨",
            height=50, corner_radius=15,
            fg_color="#9CCFE8", text_color="#355070",
            command=add
        ).pack(pady=25)

    # View expenses
    def show_expenses():
        clear()

        ctk.CTkLabel(
            content, text="Your Expenses 📋",
            font=("Arial", 30, "bold"), text_color="#4B6584"
        ).pack(anchor="w", padx=40, pady=(35, 5))

        frame = ctk.CTkScrollableFrame(
            content, fg_color="white", corner_radius=20
        )
        frame.pack(fill="both", expand=True, padx=40, pady=30)

        if not expenses:
            ctk.CTkLabel(
                frame, text="No expenses recorded yet.",
                text_color="#829AB1"
            ).pack(pady=40)
            return

        for i, e in enumerate(expenses, 1):
            card = ctk.CTkFrame(
                frame, fg_color="#F8FBFF", corner_radius=15
            )
            card.pack(fill="x", padx=10, pady=7)

            ctk.CTkLabel(
                card,
                text=f"Expense {i}   |   {e['category']}   |   ₹ {e['Amount']}",
                font=("Arial", 15, "bold"),
                text_color="#4B6584"
            ).pack(anchor="w", padx=20, pady=(12, 3))

            ctk.CTkLabel(
                card,
                text=f"{e['Description']}   •   {e['Datetime']}",
                text_color="#5D6D7E"
            ).pack(anchor="w", padx=20, pady=(0, 12))

    # Summary
    def show_summary():
        clear()

        ctk.CTkLabel(
            content, text="Expense Summary 📊",
            font=("Arial", 30, "bold"), text_color="#4B6584"
        ).pack(anchor="w", padx=40, pady=(35, 5))

        frame = ctk.CTkFrame(content, fg_color="white", corner_radius=20)
        frame.pack(fill="both", expand=True, padx=40, pady=30)

        if not expenses:
            ctk.CTkLabel(
                frame, text="No expenses recorded yet.",
                text_color="#829AB1"
            ).pack(pady=50)
            return

        total = sum(e["Amount"] for e in expenses)
        categories = {}

        for e in expenses:
            categories[e["category"]] = categories.get(
                e["category"], 0
            ) + e["Amount"]

        highest = max(expenses, key=lambda e: e["Amount"])
        lowest = min(expenses, key=lambda e: e["Amount"])

        lines = [
            f"Total expenses: {len(expenses)}",
            f"Total spending: ₹ {total}",
            "",
            "Spending by category:"
        ]

        lines += [f"{c}: ₹ {a}" for c, a in categories.items()]

        lines += [
            "",
            f"Highest expense: ₹ {highest['Amount']} ({highest['category']})",
            f"Lowest expense: ₹ {lowest['Amount']} ({lowest['category']})"
        ]

        ctk.CTkLabel(
            frame,
            text="\n".join(lines),
            justify="left",
            font=("Arial", 16),
            text_color="#4B6584"
        ).pack(anchor="w", padx=30, pady=30)

    # Delete
    def show_delete():
        clear()

        ctk.CTkLabel(
            content, text="Delete Expense 🗑️",
            font=("Arial", 30, "bold"), text_color="#4B6584"
        ).pack(anchor="w", padx=40, pady=(35, 5))

        frame = ctk.CTkFrame(content, fg_color="white", corner_radius=20)
        frame.pack(fill="both", expand=True, padx=40, pady=30)

        if not expenses:
            ctk.CTkLabel(
                frame, text="No expenses recorded yet.",
                text_color="#829AB1"
            ).pack(pady=50)
            return

        for i, e in enumerate(expenses, 1):
            ctk.CTkLabel(
                frame,
                text=f"{i}.  {e['category']}   ₹ {e['Amount']}   {e['Description']}",
                text_color="#4B6584"
            ).pack(anchor="w", padx=30, pady=5)

        number = ctk.CTkEntry(
            frame, placeholder_text="Enter expense number",
            height=45, corner_radius=12
        )
        number.pack(pady=25)

        def delete():
            try:
                n = int(number.get())
                if n < 1 or n > len(expenses):
                    raise ValueError
            except ValueError:
                CTkMessagebox(
                    title="Invalid Number",
                    message="Please enter a valid expense number."
                )
                return

            del expenses[n - 1]
            save_expenses()
            show_delete()

        ctk.CTkButton(
            frame, text="Delete Expense",
            height=45, corner_radius=12,
            fg_color="#D8A7B1", text_color="#5A3540",
            command=delete
        ).pack()

    # Navigation
    buttons = [
        ("⌂  Dashboard", show_dashboard),
        ("＋  Add Expense", show_add),
        ("☷  Expenses", show_expenses),
        ("◉  Summary", show_summary),
        ("⌫  Delete", show_delete)
    ]

    for text, command in buttons:
        ctk.CTkButton(
            side, text=text, height=45,
            corner_radius=15,
            fg_color="transparent",
            text_color="#4B6584",
            hover_color="#DCEEF7",
            command=command
        ).pack(fill="x", padx=20, pady=7)

    show_dashboard()

app.after(300, start)
app.mainloop()