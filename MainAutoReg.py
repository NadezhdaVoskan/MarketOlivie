import pyodbc
import maskpass
import random
import time
import Admin
import User
import os

connectionString = ("Driver={SQL Server};""Server=LAPTOP-MR4G4705\MYSEVERNAME;"
"Database=Olivie_Dvorik;""Trusted_Connection=yes")
connection = pyodbc.connect(connectionString, autocommit=True)
dbCursor = connection.cursor()

clear = lambda: os.system('cls')


def registration():
    status = True
    print("\nРегистрация\n")
    print("Пожалуйста, введите:")
    while status == True:
        phone = str(input("Номер телефона без пробелов: +7 "))
        if (len(phone) > 10 or len(phone) <= 9 or phone.isdigit() == False):
            print("Неправильно введен номер!\n")
        else:
            status = False
            phoneRequest = "+7" + phone
            try:
                password = maskpass.askpass(prompt="Введите пароль:", mask="*")
            except: TypeError
            balance = random.randint(20, 500)
            dbCursor.execute(f"INSERT INTO [User] ([Role_ID], [Loyality_ID], [Phone_User], [Password_User], [Balance_User]) values (?, ?, ?, ?, ?)", 2, 1, phoneRequest, password, balance)
            connection.commit()
            print("Успешная регистрация!")
            time.sleep(2)
            main()

def authorization():
    status = True
    print("\nАвторизация\n")
    print("Пожалуйста, введите:")
    while status == True:
        phone = str(input("Номер телефона без пробелов: +7"))
        if (len(phone) > 10 or len(phone) <= 9 or phone.isdigit() == False):
            print("Неправильно введен номер!\n")
        else:
            phone_user, password_user, id_user, role_user = "","","",""
            status = False
            phoneRequest = "+7" + phone
            password = maskpass.askpass(prompt="Введnите пароль:", mask="*")
            for row in dbCursor.execute(f"SELECT * FROM [User] where [Phone_User] = '{phoneRequest}'"):
                phone_user = row.Phone_User
                password_user = row.Password_User
                id_user = row.ID_User
                role_user = row.Role_ID
            if phoneRequest == phone_user and password == password_user and role_user == 1:
                print("Вошел админ!")
                Admin.mainAdmin(id_user)
            elif phoneRequest == phone_user and password == password_user and role_user == 2:
                print("Вошел покупатель!")
                for row in dbCursor.execute(f"SELECT Balance_User FROM dbo.[User] WHERE [ID_User] = '{id_user}'"):
                    balance = row.Balance_User
                balanceAdd = random.randint(20, 500)
                balance += balanceAdd
                dbCursor.execute(f"UPDATE [User] SET [Balance_User] = {balance} WHERE [ID_User] = {id_user}")
                connection.commit()
                User.mainUser(id_user)
            else:
                print("Введены неверные данные! Попробуйте заново!")
                time.sleep(1)
                authorization()
            
    

def main():

    clear()
    print("\n'Оливьешный дворик'")
    choice = int(input("Добро пожаловать!\n\n Выберите действие:\n1. Авторизация \n2. Регистрация \n3. Выйти\n\n"))
    if choice == 1:
       return authorization()
    elif choice == 2:
       return registration()
    elif choice == 3:
       return exit()
    else:
       raise TypeError
    
main()
    

    