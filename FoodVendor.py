import sqlite3, os
from sqlite3 import Error
from os import path
from DbManager import DbManager
from Users import User, Admin, Customer
import datetime

class FoodVendor:

    def initialize(self):
        self.receipt_number = 1000
        self.db = DbManager()
        self.db.create_menu_table('menu.tsv')
        self.db.create_user_table('user.tsv')

    def admin_login(self):
        user_name = input("Please enter your user_name: ")
        user_pwd = input("Please enter password: ")
        iter = 1
        exist_chk = self.db.is_user_exist(user_name)
        while iter < 4:
            if exist_chk == True:
                admin_user = self.db.get_admin(user_name)
                if admin_user != 0:
                    return admin_user
                    break
                else:
                    print("\nAdmin account not found or password mismatch! Please check your username and password.")
                    user_name = input("Please enter your user_name: ")
                    user_pwd = input("Please enter password: ")
                    exist_chk = self.db.is_user_exist(user_name)
                    iter += 1
            elif iter == 3:
                print("You have reached the maximum number of login attempts. Goodbye!")
            else:
                print("\nAdmin account not found or password mismatch! Please check your username and password.")
                user_name = input("Please enter your user_name: ")
                user_pwd = input("Please enter password: ")
                exist_chk = self.db.is_user_exist(user_name)
                iter += 1

    def update_admin_profile(self, user):
        admin_user = user
        print("Current user profile for {}:\n".format(admin_user.user_name))
        print("Phone number:", admin_user.phone_num)
        print("Email address:", admin_user.email)
        new_phone = input("\nPlease enter the new phone number (no space or dash):")
        new_email = input("Please enter the new email address:")
        admin_user.phone_num = new_phone
        admin_user.email = new_email
        self.db.update_admin(admin_user)

    def customer_login(self):
        cust_name = input("Please enter your user_name: ")
        cust_pwd = input("Please enter password: ")
        iter = 1
        exist_chk = self.db.is_user_exist(cust_name)
        while iter < 4:
            if exist_chk == True:
                cust_user = self.db.get_customer(cust_name)
                if cust_user != 0:
                    return cust_user
                    break
                else:
                    print("\nAdmin account not found or password mismatch! Please check your username and password.")
                    cust_name = input("Please enter your user_name: ")
                    user_pwd = input("Please enter password: ")
                    exist_chk = self.db.is_user_exist(cust_name)
                    iter += 1
            elif iter == 3:
                print("You have reached the maximum number of login attempts. Goodbye!")
            else:
                print("\nAdmin account not found or password mismatch! Please check your username and password.")
                cust_name = input("Please enter your user_name: ")
                user_pwd = input("Please enter password: ")
                exist_chk = self.db.is_user_exist(cust_name)
                iter += 1

    def update_customer_profile(self, user):
        cust_user = user
        print("Current user profile for {}:\n".format(cust_user.user_name))
        print("Credit card number:", cust_user.card_num)
        print("Expiration date:", cust_user.card_date)
        print("Billing address:", cust_user.address)
        print("Phone number:", cust_user.phone_num)
        print("Email address:", cust_user.email)
        new_card_num = ("\nPlease enter the new credit card number (no space or dash):")
        new_exp_date = ("Please enter the new expiration date (MMYY):")
        new_address = ("Please enter the new billing address:")
        new_phone = input("Please enter the new phone number (no space or dash):")
        new_email = input("Please enter the new email address:")
        cust_user.card_num = new_card_num
        cust_user.card_date = new_exp_date
        cust_user.address = new_address
        cust_user.phone_num = new_phone
        cust_user.email = new_email
        self.db.update_customer(cust_user)

    def create_account(self):
        username = input("Please enter the user_name of the new account:\n")
        exist_chk = self.db.is_user_exist(username)
        while exist_chk == True:
            print(username, "is not available, please choose a different username:")
            username = input()
            exist_chk = self.db.is_user_exist(username)
        new_pwd = input("Please enter new password:")
        account_query = input("Is this a customer account (Y/N)?")
        if account_query == 'Y':
            account_type = "customer"
            new_fname = input("Please enter first name:")
            new_lname = input("Please enter last name:")
            new_email = input("Please enter email address:")
            new_phone = input("Please enter phone number:")
            new_card_num = input("Please enter credit card number (no space or dash):")
            new_card_exp = input("Please enter expiration date (MMYY):")
            new_address = input("Please enter billing address:")
            new_user = Customer(new_card_num, new_card_exp, new_address, 0, 0, username, 'customer',
                                new_fname, new_lname, new_email, new_phone, new_pwd)
            self.db.update_customer(new_user)
        else:
            account_type = 'admin'
            new_fname = input("Please enter first name:")
            new_lname = input("Please enter last name:")
            new_email = input("Please enter email address:")
            new_phone = input("Please enter phone number:")
            new_id = input("Please enter employee ID:")
            new_user = Admin(new_id, username, 'admin', new_fname, new_lname, new_email, new_phone, new_pwd)
            self.db.update_admin(new_user)

    def delete_account(self):
            user_del = input("Please enter the user_name of the account to be deleted:")
            exist_chk = self.db.is_user_exist(user_del)
            if exist_chk == True:
                del_query = input("Account of {} will be removed. Are you sure (Y/N)?".format(user_del))
                if del_query == 'Y' and user_del != self.user:
                    self.db.delete_user(user_del)
                    print("Account of {} removed.".format(user_del))
            else:
                print("User does not currently exist.")

    def create_receipt(self, list, user, reward = 0):
        f = open('FoodVendorReceipt{}.txt'.format(self.receipt_number), 'a')
        f.write('{:^21}'.format('FOOD VENDOR'))
        f.write(str(print(user)))
        f.write('Receipt #:' + str(self.receipt_number) + '\n')
        self.receipt_number += 1
        now = datetime.now()
        s1 = now.strftime("%A, %m/%d/%Y, %I:%M:%S %p")
        f.write(s1)
        itr = 0
        sub_total = 0
        total_prep = 0
        items_format = '{name:25}${price:5.2f}'
        for item in range(len(list)):
            f.write(items_format.format(name=item[itr][0], price = item[itr][1]))
            total_prep += self.db.get_food_time(item[itr][0])
            itr += 1
            sub_total += item[itr][1]
        price_format = '${price:25}'
        if user.user_name == 'Guest':
            f.write("Total: ", price_format.format(price=sub_total))
            cc_nums = "{}{}{}{}".format(user.card_num[-4], user.card_num[-3], user.card_num[-2], user.card_num[-1])
            f.write("Credit Card: XXXXXXXXXXXX" + cc_nums)
            f.write("Your order will be ready in : {} mins".format(total_prep))
            f.write("Thank you for your order!")
        else:
            f.write("Subtotal: ", price_format.format(price=sub_total))
            reward_disc = (reward / 10)
            f.write("Reward: -${}".format(price_format(price = reward_disc)))
            total = sub_total - reward_disc
            f.write("Total: ", price_format.format(price=total))
            cc_nums = "{}{}{}{}".format(user.card_num[-4], user.card_num[-3], user.card_num[-2], user.card_num[-1])
            f.write("Credit Card: XXXXXXXXXXXX" + cc_nums)
            add_reward = total % 5
            new_reward_amnt = (reward - (reward * 10)) + add_reward
            f.write("You've earned {} in this order!\n".format(add_reward))
            f.write("Your order will be ready in : {} mins".format(total_prep))
            f.write("Thank you for your order!")
        f.close()

    def print_order_history(self, user):
        order = str(user.history)
        file = 'FoodVendorReceipt' + order
        f = open('{}.txt'.format(file), 'r')
        print("Order History:")
        print(f.read())
        print("End of order history.")

    def insert_food_item(self):
        print('Please choose a food category:')
        print('    Sandwiches - Enter 1')
        print('    Salads - Enter 2')
        print('    Drinks - Enter 3')
        print('    Mexican food - Enter 4')
        print('    Vegetarian - Enter 5')
        print('    Return to previous menu - Enter 6')
        option = int(input())
        while option != 6:
            side_opt = input('Is this a side option (Y/N)?')
            item = input('Please enter the name of food item:')
            item_desc = input('Please enter the description of food item:')
            item_price = input('Please enter the price of food item:')
            item_prep = input('Please enter the prep time of food item (in minutes):')
            item_avail = input('Do you want to make this item available in daily menu (Y/N)?')
            if option == 1:
                item_cat = 'Sandwiches'
                if side_opt == 'Y':
                    item_cat = 'Sandwiches' + '_option'
            elif option == 2:
                item_cat = 'Salads'
                if side_opt == 'Y':
                    item_cat = 'Salads' + '_option'
            elif option == 3:
                item_cat = 'Drinks'
            elif option == 4:
                item_cat = 'Mexican Food'
                if side_opt == 'Y':
                    item_cat = 'Mexican Food' + '_option'
            elif option == 5:
                item_cat = 'Vegetarian'
                if side_opt == 'Y':
                    item_cat = 'Vegetarian' + '_option'
            else:
                option = int(input())
        self.db.set_food_price(self, item, item_price)
        self.db.set_food_category(self, item, item_cat)
        self.db.set_food_description(self, item, item_desc)
        self.db.set_food_availability(self, item, item_avail)
        self.db.set_food_prep(self, item, item_prep)

    def order_food(self, user):
        ordered_items = []
        order_iter = 0
        username = user.user_name
        print("\nDaily Menu\n")
        print('Choose a category:')
        print('\tSandwiches - Enter 1')
        print('\tSalads - Enter 2')
        print('\tVegetarian - Enter 3')
        print('\tMexican Food - Enter 4')
        print('\tDrink - Enter 5')
        print('\tCheck-out or exit - Enter 6')
        selection = int(input())
        while selection != 6:
            if selection == 1:
                item_cat = 'Sandwiches'
            elif selection == 2:
                item_cat = 'Salads'
            elif selection == 3:
                item_cat = 'Vegetarian'
            elif selection == 4:
                item_cat = 'Mexican Food'
            elif selection == 5:
                item_cat = 'Drinks'
            self.db.display_daily_menu(item_cat)
            item_sel = input("""Enter the name of item you'd like to order, or "None" to return to last menu.""")
            if item_sel != "None":
                item_exist = self.db.is_food_exist(item_sel)
                item_avail = self.db.is_food_available(item_sel)
                if item_exist == True and item_avail == True:
                    print("{} added to order.\n".format(item_sel))
                    ordered_items.append((order_iter, item_sel))
                    order_iter += 1
                    if selection != 5:
                        print("Would you like to add any of these options to your order?")
                        item_option = item_cat + "_option"
                        self.db.display_daily_menu(item_option)
                        option_sel = input("""Enter the name of option item you'd like to order, or "None" to return to last menu. """)
                        if option_sel == 'None':
                            print()
                        else:
                            option_exist = self.db.is_food_exist(option_sel)
                            option_avail = self.db.is_food_available(option_sel)
                            if option_exist == True and option_avail == True:
                                print("{} added to order.".format(option_sel))
                                ordered_items.append((order_iter, option_sel))
                                order_iter += 1
            print("\n\nDaily Menu\n")
            print('Choose a category:')
            print('\tSandwiches - Enter 1')
            print('\tSalads - Enter 2')
            print('\tVegetarian - Enter 3')
            print('\tMexican Food - Enter 4')
            print('\tDrink - Enter 5')
            print('\tCheck-out or exit - Enter 6')
            selection = int(input())
        if selection == 6 and order_iter == 0:
            print("No food ordered. Goodbye")
        elif username != 'Guest':
            #todo fix the below
            reward_use = input("You currently have 30 Reward Points. Please enter the number of Reward Points you want to redeem. ")
            print("Your order has been placed. Please take your receipt.")
        else:
            card_num = input("Please enter the credit card number (no space or dash):")
            card_exp_date = input("Please enter the expiration date (MMYY):")
            billing_add = input("Please enter the billing address:")
            phone_num = input("Please enter the phone number (no space or dash):")
            email = input("Please enter the email address:")
            print("Your order has been placed. Please take your receipt.")
            self.create_receipt(ordered_items, user)

    def print_main_menu(self):
        print("Welcome to Food Vendor!")
        print("Choose an option to begin.")
        print("\tCustomer login - Enter 1")
        print("\tPlace order as a guest - Enter 2")
        print("\tManage system (admin sign-in required) - Enter 3")
        print("\tLeave Food Vendor - Enter 4")

    def main_menu(self):
        self.print_main_menu()
        menu_sel = int(input())
        while menu_sel >= 0 and menu_sel <= 4:
            if menu_sel == 1:
                user = input("Please input your username")
                self.member_menu(user)
                self.print_main_menu()
                menu_sel = int(input())
            elif menu_sel == 2:
                self.order_food(Customer())
                self.print_main_menu()
                menu_sel = int(input())
            elif menu_sel == 3:
                user = input("Please input your username")
                self.admin_menu(user)
                self.print_main_menu()
                menu_sel = int(input())
            elif menu_sel == 4:
                print("See you next time!")
                break
            elif menu_sel > 4:
                print("Please enter a valid option (1 - 3):")
                menu_sel = int(input())
            elif menu_sel < 0:
                print("Please enter a valid option (1 - 3):")
                menu_sel = int(input())

    def print_member_menu(self):
        print("Welcome back, {}!".format(self.user.first_name))
        print("You have {} points in reward, don't forget to use them!".format(self.user.points))
        print("What would you like to do?")
        print("\tPlace an order - Enter 1")
        print("\tView last order history - Enter 2")
        print("\tUpdate profile - Enter 3")
        print("\tLogout and return to main menu - Enter 4")

    def member_menu(self, user):
        user = user
        self.print_member_menu()
        menu_sel = int(input())
        while menu_sel >= 0 and menu_sel <= 4:
            if menu_sel == 1:
                self.order_food(user)
                self.print_member_menu()
                menu_sel = int(input())
            elif menu_sel == 2:
                self.print_order_history(user)
                self.print_member_menu()
                menu_sel = int(input())
            elif menu_sel == 3:
                self.update_customer_profile(user)
                self.print_member_menu()
                menu_sel = int(input())
            elif menu_sel == 4:
                break
            elif menu_sel > 4:
                print("Please enter a valid option (1 - 3):")
                menu_sel = int(input())
            elif menu_sel < 0:
                print("Please enter a valid option (1 - 3):")
                menu_sel = int(input())

    def print_admin_user(self, user):
        print(user)
        print("Admin menu - What would you like to do?")
        print("\tManage user accounts - Enter 1")
        print("\tManage food menu - Enter 2")
        print("\tLogout and return to main menu - Enter 3")

    def admin_menu(self, user):
        user = user
        self.print_admin_user(user)
        menu_sel = int(input())
        while menu_sel >= 0 and menu_sel <= 3:
            if menu_sel == 1:
                self.manage_accounts(user)
                self.print_admin_user(user)
                menu_sel = int(input())
            elif menu_sel == 2:
                self.manage_menu()
                self.print_admin_user(user)
                menu_sel = int(input())
            elif menu_sel == 3:
                break
                self.print_admin_user(user)
                menu_sel = int(input())
            elif menu_sel > 3:
                print("Please enter a valid option (1 - 3):")
                self.print_admin_user(user)
                menu_sel = int(input())
            elif menu_sel < 0:
                print("Please enter a valid option (1 - 3):")
                self.print_admin_user(user)
                menu_sel = int(input())

    def print_manage_menu(self):
        print("Manage Food menu - choose an option:")
        print("\tInsert new food item - Enter 1")
        print("\tUpdate food price  - Enter 2")
        print("\tUpdate food description  - Enter 3")
        print("\tUpdate food availability for daily menu - Enter 4")
        print("\tReturn to employee menu - Enter 5")

    def manage_menu(self):
        self.print_manage_menu()
        menu_sel = int(input())
        while menu_sel >= 0 and menu_sel <= 5:
            if menu_sel == 1:
                self.insert_food_item()
            elif menu_sel == 2:
                item_price = input("Enter price of item:")
                self.db.set_food_price(item_name, item_price)
                self.print_manage_menu()
                menu_sel = int(input())
            elif menu_sel == 3:
                item_desc = input("Enter Description of item:")
                self.db.set_food_description(item_name, item_desc)
                self.print_manage_menu()
                menu_sel = int(input())
            elif menu_sel == 4:
                item_name = input("Enter name of item:")
                item_avail = input("Set this item as available in daily menu (Y/N)?")
                if item_avail == 'N':
                    item_avail = 0
                else:
                    item_avail = 1
                self.db.set_food_availability(item_name, item_avail)
                self.print_manage_menu()
                menu_sel = int(input())
            elif menu_sel == 5:
                break
            elif menu_sel > 5:
                print("Please enter a valid option (1 - 5):")
                menu_sel = int(input())
            elif menu_sel < 0:
                print("Please enter a valid option (1 - 5):")
                menu_sel = int(input())

    def print_manage_accounts(self):
        print("Manage accounts - choose an option:")
        print("\tUpdate your profile - Enter 1")
        print("\tUpdate customer profile  - Enter 2")
        print("\tCreate an account  - Enter 3")
        print("\tDelete an account - Enter 4")
        print("\tReturn to employee menu - Enter 5")

    def manage_accounts(self, user):
        self.print_manage_accounts()
        menu_sel = int(input())
        user = user
        while menu_sel >= 0 and menu_sel <= 5:
            if menu_sel == 1:
                username = user.user_name
                user_exist = self.db.is_user_exist(username)
                if user_exist == True:
                    self.update_admin_profile(username)
                menu_sel = int(input())
            elif menu_sel == 2:
                cust = input("Enter customer username:")
                user_exist = self.db.is_user_exist(cust)
                if user_exist == True:
                        self.update_customer_profile(cust)
                self.print_manage_accounts()
                menu_sel = int(input())
            elif menu_sel == 3:
                self.create_account()
                self.print_manage_accounts()
                menu_sel = int(input())
            elif menu_sel == 4:
                self.delete_account()
                self.print_manage_accounts()
                menu_sel = int(input())
            elif menu_sel == 5:
                break
            elif menu_sel > 5:
                print("Please enter a valid option (1 - 5):")
                self.print_manage_accounts()
                menu_sel = int(input())
            elif menu_sel < 0:
                print("Please enter a valid option (1 - 5):")
                self.print_manage_accounts()
                menu_sel = int(input())

if __name__ == '__main__':
    vendor = FoodVendor()
    vendor.initialize()

    vendor.main_menu()


    vendor.db.disconnect()
