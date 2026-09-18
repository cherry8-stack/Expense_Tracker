import json
from datetime import datetime
def save_expenses():
    with open("expenses.json","w") as file :
        json.dump(expenses,file)
def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
expenses=load_expenses()
while True:
    print("\n\n====================")
    print("  Expense tracker")
    print("====================")
    print("\n1.Add expense")
    print("2.View expense")
    print("3.View total spending")
    print("4.Exit")


    
    choice=int(input("\nEnter the choice : "))


    if choice==1:

        try:
            while True:
                print("\nchoose a category :")
                print("1.Food")
                print("2.Travel")
                print("3.Education")
                print("4.Shopping")
                print("5.Other")
                choose_category=input("Enter the choice : ")
                if choose_category=="1":
                    category="Food"
                    break
                elif choose_category=="2":
                    category="Travel"
                    break
                elif choose_category=="3":
                    category="Education"
                    break
                elif choose_category=="4":
                    category="Shopping"
                    break
                elif choose_category=="5":
                    category="Other"
                    break
                else:
                    print("invalid choice")
                    continue

            amount=int(input("Enter the amount : "))
            if amount<0:
                print("amount must be greater than 0")
                continue
            while True:
                description=input("Enter the description : ").strip()
                if description:
                    print(description)
                    break
                print("Description should contain something.Please try again.")
            date_time=datetime.now().strftime("%d-%m-%Y %I:%M %p")
            expense={
                "category":category,
                "Amount":amount,
                "Description":description,
                "Datetime":date_time
            }
                
            expenses.append(expense)
            save_expenses()
            print("successfully added")
        except:
            print("Enter the valid input")   


    elif choice==2:
        print("\n-----Expense-----")
        if not expenses:
            print("No expenses recorded yet")
        else:
            for i,expense in enumerate(expenses,start=1):
                print("\n-------------------------------")
                print("Expense :",i)
                print("category :",expense["category"])
                print("Amount :",expense["Amount"])
                print("Description :",expense["Description"])
                print("Date and time :",expense["Datetime"])
                print("-------------------------------")
                

    elif choice==3:
        total=0
        print("\n----Total spending----")
        if not expenses:
            print("NO expenses recoeded yet.")
        for expense in expenses:
            total=total+expense["Amount"]
        print("\nTotal spending",total)

    elif choice==4:
        print("\n----delete expense----")
        if not expense:
            print("No expense recorded yet.")
        else:
            for i,expense in enumerate(expenses,start=1):
                print(i,expense["category"],expense["Amount"])
            expense_number=int(input("Enter the expense to delete :"))
            del expenses[expense_number-1]
            save_expenses()
            print("\nExpense deleted successfully")


    elif choice==5:
        print("\n----Expense summary----")
        if not expense:
            print("\nNo expense recorded yet.")
        else:
            print(f"Total number of expenses :{len(expenses)}")
            total=0
            for expense in expenses:
                total=total+expense["Amount"]
            print("Total spending",total)
            category_total={}
            for expense in expenses:
                category=expense["category"]
                amount=expense["Amount"]
                if category in category_total:
                    category_total[category]=category_total[category]+amount
                else:
                    category_total[category]=amount
            print("\nSpending by category")
            for category in category_total:
                print(category,":",category_total[category])

            highest=max(expenses,key=lambda expense:expense["Amount"])
            print("\nHighest expense :",highest["Amount"])
            print("category :",highest["category"])

            lowest=min(expenses,key=lambda expense:expense["Amount"])
            print("\nLowest expense :",lowest["Amount"])
            print("category :",lowest["category"])
 
    


    
    elif choice==6:
        print("Exit")
    else:
        print("invalid choice")






