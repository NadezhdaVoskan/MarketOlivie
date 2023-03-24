import pyodbc
import os
import time
import MainAutoReg

connectionString = ("Driver={SQL Server};""Server=LAPTOP-MR4G4705\MYSEVERNAME;"
"Database=Olivie_Dvorik;""Trusted_Connection=yes")
connection = pyodbc.connect(connectionString, autocommit=True)
dbCursor = connection.cursor()

clear = lambda: os.system('cls')


def buySupplier(id_user):
    clear()
    for row in dbCursor.execute(f"SELECT * FROM [User] where [ID_User] = '{id_user}'"):
        balance = row.Balance_User
    nameIngridient, typeIngridient, costIngridient, countIngridient = [], [], [], []
    for row in dbCursor.execute("SELECT * FROM [Ingridient] INNER JOIN [Type_Ingridient] ON [Type_ID] = [ID_Type]"):
        nameIngridient.append(row.Name_Ingridient)
        costIngridient.append(row.Cost_Ingridient)
        typeIngridient.append(row.Name_Type)
        countIngridient.append(row.Count_Ingridient)

    print("Список ингридиентов: \n")
    for i in range(len(typeIngridient)):
        print(f"{i+1}. {typeIngridient[i]} - {nameIngridient[i]} - {countIngridient[i]} шт. - {costIngridient[i]} рублей.\n")

    choice = int(input("1. Выбрать продукт для поставки \n2. Назад \n"))
    if choice == 2:
        clear()
        time.sleep(1)
        mainAdmin(id_user)
    elif choice == 1:
                
        try:
            idIngridient = int(input("Выберите ингридиент для поставки: \n"))
        except ValueError:
            print("Введены неверные данные! Попробуйте заново!")
            time.sleep(2)
            buySupplier(id_user)
        for count in range(len(nameIngridient)):
                countIngridients = count+1
        if (idIngridient > 0 and idIngridient <= countIngridients):

            try:
                count = int(input("Введите количество поставки: \n"))
            except ValueError:
                print("Введены неверные данные")
                time.sleep(2)
                buySupplier(id_user)

            currentNameIngr, currentCountIngr,currentCostIngr, currentTypeIngr = [], [], [], []
            for row in dbCursor.execute(f"SELECT * FROM [Ingridient] INNER JOIN [Type_Ingridient] ON [Type_ID] = [ID_Type] WHERE [ID_Ingridient] = {idIngridient}"):
                currentNameIngr = row.Name_Ingridient
                currentCountIngr = row.Count_Ingridient
                currentCostIngr = row.Cost_Ingridient
                currentTypeIngr = row.Name_Type

            endCount = currentCountIngr + count
            sum = count * currentCostIngr

            status = True
            print((f"Поставка {currentTypeIngr} - {currentNameIngr}, кол-во: {count} шт. {sum} рублей\n"))
            while (status == True):
                confirmation = int(input("1. Подтвердить заказ \n2. Отмена\n"))
                match confirmation:
                    case 1:
                        balance -= sum
                        if balance >= 0:
                            dbCursor.execute(f"UPDATE [User] SET [Balance_User] = {balance} WHERE [ID_User] = {id_user}")
                            connection.commit()
                            dbCursor.execute(f"UPDATE [Ingridient] SET [Count_Ingridient] = {endCount} WHERE [ID_Ingridient] = {idIngridient}")
                            connection.commit()
                            time.sleep(1)
                            print("Заказ успешно выполнен!")
                            status = False
                            time.sleep(2)
                            buySupplier(id_user)
                        else:
                            print("На счету недостаточно средств!")
                            status = False
                            time.sleep(2)
                            buySupplier(id_user)
                    case 2:
                        print("Отмена заказа.")
                        status = False
                        time.sleep(2)
                        buySupplier(id_user)
                    case _:
                        print("Неверное значение!")
        else: 
            raise ValueError


def historyPurchase(id_user):
    userId, phoneUser = [], []
    for row in dbCursor.execute("select * from [User]"):
        userId.append(row.ID_User)
        phoneUser.append(row.Phone_User)
    print("Список существующих пользователей:")
    for i in range(len(phoneUser)):
        print(f"{i+1} - {phoneUser[i]}")
    phone = input("\nВведите номер пользователя без пробелов для просмотра: +7")
    if (len(phone) > 10 or len(phone) <= 9 or phone.isdigit() == False):
            print("Неправильно введен номер!\n")
    else:
        phoneRequest = "+7" + phone
        for row in dbCursor.execute(f"SELECT ID_User FROM dbo.[User] WHERE Phone_User = '{phoneRequest}'"):
            idUser = row.ID_User
        print("\nСписок покупок пользователя:\n ")
        dbCursor.execute(f"SELECT Structure_Olivie, Count_Olivie, Sum_Order, Time_Order FROM [Olivie_Buy] WHERE User_ID = '{idUser}'")
        for row in dbCursor:
            print("Покупка:", row.Structure_Olivie, "Количество:", row.Count_Olivie, "Цена:", row.Sum_Order, "Время:",  str(row.Time_Order)[:-7], "\n") 
    time.sleep(2)
    choose = int(input("Для выхода в главное меню нажмите 0: "))
    if choose == 0:
         mainAdmin(id_user)
    else:
        print("Произошла ошибка!")

def cardsLoyality(id_user):
    userId, phoneUser = [], []
    for row in dbCursor.execute("select * from [User]"):
        userId.append(row.ID_User)
        phoneUser.append(row.Phone_User)
    print("Список существующих пользователей:")
    for i in range(len(phoneUser)):
        print(f"{i+1} - {phoneUser[i]}")
    phone = input("\nВведите номер пользователя без пробелов для просмотра: +7")
    if (len(phone) > 10 or len(phone) <= 9 or phone.isdigit() == False):
            print("Неправильно введен номер!\n")
    else:
        phoneRequest = "+7" + phone
        for row in dbCursor.execute(f"SELECT ID_User FROM dbo.[User] WHERE Phone_User = '{phoneRequest}'"):
            idUser = row.ID_User

    for row in dbCursor.execute(f"select * from [User] inner join [Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = {idUser}"):
        nameLoyality = row.Name_Loyality
        discountLoyality = row.Discount
        discount = discountLoyality * 100
    print(f"\nПрограмма лояльности пользователя: {nameLoyality}, скидка: 0.{str(discount)[:-2]}%\n")
    time.sleep(2)
    choose = int(input("Для выхода в главное меню нажмите 0: "))
    if choose == 0:
         mainAdmin(id_user)
    else:
        print("Произошла ошибка!")

def mainAdmin(id_user):
    clear()
    print("Добро пожаловать на панель админа!")

    for row in dbCursor.execute(f"SELECT * FROM [User] where [ID_User] = '{id_user}'"):
        balance = row.Balance_User
    print(f"Ваш баланс: {balance}")

    choice = int(input("Выберите действие:\n1. Поставка \n2. История покупок \n3. Карты лояльности \n4. Выйти из аккаунта\n\n"))

    if choice == 1:
       return buySupplier(id_user)
    elif choice == 2:
       return historyPurchase(id_user)
    elif choice == 3:
       return cardsLoyality(id_user)
    elif choice == 4:
       return MainAutoReg.main()
    else:
       raise TypeError

