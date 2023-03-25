import pyodbc
import os
import time
import MainAutoReg
import random
import datetime

connectionString = ("Driver={SQL Server};""Server=LAPTOP-MR4G4705\MYSEVERNAME;"
"Database=Olivie_Dvorik;""Trusted_Connection=yes")
connection = pyodbc.connect(connectionString, autocommit=True)
dbCursor = connection.cursor()

clear = lambda: os.system('cls')

def buyOlivie(id_user):
    status = True
    ingridients = []
    clear()
    for row in dbCursor.execute(f"SELECT * FROM [User] where [ID_User] = '{id_user}'"):
        balance = row.Balance_User
    nameIngridient, typeIngridient, costIngridient, countIngridient = [], [], [], []
    for row in dbCursor.execute("SELECT * FROM [Ingridient] INNER JOIN [Type_Ingridient] ON [Type_ID] = [ID_Type]"):
        nameIngridient.append(row.Name_Ingridient)
        costIngridient.append(row.Cost_Ingridient)
        countIngridient.append(row.Count_Ingridient)
        typeIngridient.append(row.Name_Type)

    print("Заказ оливье.\nОбратите внимание: АКЦИЯ - каждое 5 оливье в подарок!\nСписок ингридиентов: \n")
    for i in range(len(typeIngridient)):
        print(f"{i+1}. {typeIngridient[i]} - {nameIngridient[i]} - {costIngridient[i]} рублей.\n")

    choice = int(input("1. Выбрать ингрединенты для оливье.\n2. Назад. \n"))
    if choice == 2:
        clear()
        time.sleep(1)
        mainUser(id_user)
    elif choice == 1:
        try:
            countOlivie = int(input("\nВведите количество оливье: "))
        except:
             print("Введены неверные данные!")
             buyOlivie(id_user)
        while status == True:
            for count in range(len(typeIngridient)):
                countIngr = count+1
            print("Выберите ингридиент: ")
            try:
                chooseIngridient = int(input())
            except ValueError:
                print("Введены неверные данные!")
                buyOlivie(id_user)
            if (chooseIngridient <= countIngr and chooseIngridient > 0):
                    ingridients.append(chooseIngridient-1)
            else:
                print("Введены неверные данные!")
                buyOlivie(id_user)

            addnew = int(input("Добавить ещё один ингредиент?\n1. Да\n2. Нет\n"))
            match addnew:
                case 1:
                    status = True
                case 2:
                    status = False
                case _:
                    print("Введены неверные данные!")
                    buyOlivie(id_user)
        
        print("\nОтлично! Итоговый состав оливье: \n")

        summaOrder = 0
        summaOneForCheck = 0
        loyalityDiscount = 0
        for i in range(len(ingridients)):
            print(nameIngridient[ingridients[i-1]], " - ", costIngridient[ingridients[i-1]], "рублей \n")
            summaOrder += costIngridient[ingridients[i-1]]
            summaOneForCheck += costIngridient[ingridients[i-1]]

        for row in dbCursor.execute(f"select * from [User] inner join [Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = {id_user}"):
            loyalityDiscount = row.Discount
        if (countOlivie % 5 == 0):
            minusOlivie = countOlivie / 5
            summaOrder *= (countOlivie - minusOlivie)
        else:
            summaOrder *= countOlivie
        discountSum = summaOrder - (summaOrder * loyalityDiscount)
        print(f"Ваша скидка : {loyalityDiscount}%")
        if (countOlivie % 5 == 0):
            print(f"\nСумма к оплате: {discountSum} рублей. Также вы получили бесплатную еду!")
        else:
             print(f"\nСумма к оплате: {discountSum} рублей")
        
        foreignObj = random.randint(1, 6)
        foreignObjOrder = random.randint(1, 6)
        beetle = False
        
        if foreignObj == 5:
            beetle == True

        confirmation = int(input("\n1. Подтвердить заказ \n2. Отмена\n"))
        match confirmation:
            case 1:
                if foreignObj == 5 and foreignObjOrder == 5:
                    print("В ваше блюдо попал таракан! Извините. Предоставляем вам скидку 30%!")
                    discountSum *= 0.30
                    time.sleep(1)
                    print(f"\nСумма к оплате: {discountSum}")
                balance -= discountSum
                structureOrder = ""
                if balance >= 0:
                    dbCursor.execute(f"UPDATE [User] SET [Balance_User] = {balance} WHERE [ID_User] = {id_user}")
                    connection.commit()
                    for i in range(len(ingridients)):
                        dbCursor.execute(f"UPDATE [Ingridient] SET [Count_Ingridient] = {countIngridient[ingridients[i-1]] - countOlivie} WHERE [Name_Ingridient] = '{nameIngridient[ingridients[i-1]]}'")
                        structureOrder += typeIngridient[ingridients[i-1]] + "-" + nameIngridient[ingridients[i-1]]+";"
                        connection.commit()
                    time.sleep(1)
                    print("Заказ успешно выполнен!")
                    print("Формируем чек...")
                    time.sleep(3)
                    dbCursor.execute(f"INSERT INTO [Olivie_Buy] ([Structure_Olivie], [User_ID], [Count_Olivie], [Sum_Order], [Time_Order], [Foreign_Object]) values (?, ?, ?, ?, ?, ?)", structureOrder, id_user, countOlivie, discountSum, datetime.datetime.now(), beetle)
                    check_number = random.randint(1, 99999)
                    if beetle == True:
                        check_text = f"""
                        -------------------------------
                                Чек №{check_number}
                        -------------------------------
                        Оливье состоит из: {structureOrder}
                        Количество: {countOlivie} шт.
                        Цена за штуку: {summaOneForCheck} руб.
                        В оливье попал таракан... Для вас скидка 30%
                        -------------------------------
                        Итого: {discountSum} руб.
                        -------------------------------
                        Спасибо за покупку!
                        """
                    else:
                        check_text = f"""
                        -------------------------------
                                Чек №{check_number}
                        -------------------------------
                        Оливье состоит из: {structureOrder}
                        Количество: {countOlivie} шт.
                        Цена за штуку: {summaOneForCheck} руб.
                        -------------------------------
                        Итого: {discountSum} руб.
                        -------------------------------
                        Спасибо за покупку!
                        """
                    # Записываем текст чека в файл
                    file_name = f"check_{check_number}.txt"
                    with open(file_name, "w", encoding='cp1251') as f:
                        f.write(check_text)
                    print(f"Чек сохранен в файле {file_name}")
                    dbCursor.execute("SELECT SUM(Sum_Order) FROM Olivie_Buy WHERE user_id = ?", id_user) 
                    resultSumAllOrder = dbCursor.fetchone()[0]
                    if (resultSumAllOrder > 5000):
                        dbCursor.execute(f"UPDATE [User] SET [Loyality_ID] = 2 WHERE [ID_User] = {id_user}")
                        connection.commit()
                    elif (resultSumAllOrder > 15000):
                        dbCursor.execute(f"UPDATE [User] SET [Loyality_ID] = 3 WHERE [ID_User] = {id_user}")
                        connection.commit()
                    elif (resultSumAllOrder > 25000):
                        dbCursor.execute(f"UPDATE [User] SET [Loyality_ID] = 4 WHERE [ID_User] = {id_user}")
                        connection.commit()
                    status = False
                    time.sleep(2)
                    mainUser(id_user)
                else:
                    print("На счету недостаточно средств!")
                    status = False
                    time.sleep(2)
                    buyOlivie(id_user)
            case 2:
                print("Отмена заказа.")
                status = False
                time.sleep(2)
                mainUser(id_user)
            case _:
                print("Неверное значение!")


def historyPurchase(id_user):
    clear()
    print("Ваш список покупок: \n")
    dbCursor.execute(f"SELECT Structure_Olivie, Count_Olivie, Sum_Order, Time_Order FROM [Olivie_Buy] WHERE User_ID = '{id_user}'")
    for row in dbCursor:
        print("Покупка:", row.Structure_Olivie, "Количество:", row.Count_Olivie, "Цена:", row.Sum_Order, "Время:",  str(row.Time_Order)[:-7], "\n") 
    time.sleep(2)
    choose = int(input("Для выхода в главное меню нажмите 0"))
    if choose == 0:
         mainUser(id_user)
    else:
        print("Произошла ошибка!")


def cardLoyalty(id_user):
    clear()
    for row in dbCursor.execute(f"select * from [User] inner join [Loyality] on [Loyality_ID] = [ID_Loyality] where [ID_User] = {id_user}"):
        nameLoyality = row.Name_Loyality
        discountLoyality = row.Discount
        discount = discountLoyality * 100
    print(f"Ваша программа лояльности: {nameLoyality}, скидка: {discount}%\n")
    time.sleep(2)
    choose = int(input("Для выхода в главное меню нажмите 0: "))
    if choose == 0:
         mainUser(id_user)
    else:
        print("Произошла ошибка!")

def mainUser(id_user):
    clear()
    print("Добро пожаловать на панель покупателя!")

    for row in dbCursor.execute(f"SELECT * FROM [User] INNER JOIN [Loyality] ON [Loyality_ID] = [ID_Loyality] WHERE [ID_User] = '{id_user}'"):
        balance = row.Balance_User
    print(f"Ваш баланс: {balance}")

    choice = int(input("Выберите действие:\n1. Заказать оливье \n2. История покупок \n3. Карта лояльности \n4. Выйти из аккаунта\n\n"))

    if choice == 1:
       return buyOlivie(id_user)
    elif choice == 2:
       return historyPurchase(id_user)
    elif choice == 3:
       return cardLoyalty(id_user)
    elif choice == 4:
       return MainAutoReg.main()
    else:
       raise TypeError
    
