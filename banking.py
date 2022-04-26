import random
import sqlite3

class Cards:
    
    def __init__(self):
        self.card_num = "400000" + str(random.randint(100000000, 999999999))
        self.copy_card_num = self.card_num
        self.card_num = [int(x) for x in str(self.card_num)]
        self.card_num = [x * 2 if y % 2 == 0 else x for y, x in enumerate(self.card_num)]
        self.card_num = [x - 9 if x > 9 else x for x in self.card_num]
        self.pom = 0
        for x in self.card_num:
            self.pom = self.pom + x

        self.copy_card_num = self.copy_card_num + ("0" if self.pom % 10 == 0 else str(10 - self.pom % 10))
        self.card_num = self.copy_card_num
        self.card_pin = random.randint(1000, 9999)

    def genereate_card(self):
        return self.card_pin, self.card_num


pom = False
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
try:
    cur.execute('CREATE TABLE card("id" INTEGER PRIMARY KEY AUTOINCREMENT, "number" TEXT, "pin" TEXT, "balance" INTEGER DEFAULT 0)')
    conn.commit()
except sqlite3.OperationalError:
    pass

while True:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    choosen_option = int(input())

    if choosen_option == 1:
        cards = Cards()
        lookin1, lookin2 = cards.genereate_card()
        print("Your card has been created")
        print("Your card number:")
        print(lookin2)
        print("Your card PIN:")
        print(lookin1)
        cur.execute('INSERT INTO card ("number", "pin") VALUES (?,?)' , (lookin2, lookin1))
        conn.commit()

    elif choosen_option == 2:
        print("Enter your card number:")
        excard_num = input()
        print("Enter your PIN:")
        excard_pin = input()

        cur.execute('SELECT number, pin FROM card WHERE number = (?) AND pin = (?)', (excard_num, excard_pin))

        if cur.fetchone() is not None:

            print("You have successfully logged in!")
            print()
            while True:
                print("1. Balance")
                print("2. Add income")
                print("3. Do transfer")
                print("4. Close account")
                print("5. Log out")
                print("0. Exit")
                choosen_option = int(input())

                if choosen_option == 1:
                    cur.execute('SELECT balance FROM card WHERE number = (?) AND pin = (?)', (excard_num, excard_pin))
                    print(cur.fetchone()[0])

                elif choosen_option == 2:
                    add_income = int(input())
                    cur.execute('UPDATE card SET balance = balance + (?) WHERE number = (?) AND pin = (?)', (add_income, excard_num, excard_pin))
                    conn.commit()

                elif choosen_option == 3:
                    print("Enter card number:")
                    card_number = input()

                    copy_of_card_number = card_number

                    pom_last_dig = int(copy_of_card_number) % 10
                    copy_of_card_number = int(copy_of_card_number) // 10

                    copy_of_card_number = [int(x) for x in str(copy_of_card_number)]
                    copy_of_card_number = [x * 2 if y % 2 == 0 else x for y, x in enumerate(copy_of_card_number)]
                    copy_of_card_number = [x - 9 if x > 9 else x for x in copy_of_card_number]
                    pom = 0
                    for x in copy_of_card_number:
                        pom = pom + x

                    copy_of_card_number = [str(x) for x in copy_of_card_number]
                    copy_of_card_number = "".join(copy_of_card_number)
                    copy_of_card_number = copy_of_card_number + ("0" if pom % 10 == 0 else str(10 - pom % 10))
                    if pom % 10 == 0:
                        pom_last_dig2 = 0
                    else:
                        pom_last_dig2 = 10 - pom % 10
                    if pom_last_dig == pom_last_dig2:
                        cur.execute('SELECT balance FROM card WHERE number = (?) AND pin = (?)',
                                    (excard_num, excard_pin))
                        if excard_num != card_number:
                            cur.execute('SELECT number FROM card WHERE number = (?)', [card_number])
                            if cur.fetchone() is not None:
                                print("Enter how much money you want to transfer:")
                                transfer = int(input())
                                cur.execute('SELECT balance FROM card WHERE number = (?)', [excard_num])
                                if cur.fetchone()[0] >= transfer:
                                    cur.execute('UPDATE card SET balance = balance + (?) WHERE number = (?)',
                                                (transfer, card_number, ))
                                    conn.commit()
                                    cur.execute('UPDATE card SET balance = balance - (?) WHERE number = (?)',
                                                (transfer, excard_num,))
                                    conn.commit()
                                    print("Success!")
                                else:
                                    print("Not enough money!")
                            else:
                                print("Such a card does not exist.")
                        else:
                            print("You can't transfer money to the same account!")
                    else:
                        print("Probably you made a mistake in the card number. Please try again!")

                elif choosen_option == 4:
                    cur.execute('DELETE FROM card WHERE number = (?) AND pin = (?)', (excard_num, excard_pin))
                    conn.commit()
                    print("Account successfully closed")
                    break

                elif choosen_option == 5:
                    print("You have successfully logged out")
                    break

                else:
                    pom = True
                    break

        else:
            print("Wrong card number or PIN!")

        if pom is True:
            break
    else:
        break