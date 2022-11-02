import csv, sqlite3, os
from sqlite3 import Error
from os import path
from Users import User, Admin, Customer

class DbManager:

    def __init__(self):
        self.menu = None
        self.conn = self.connect()
        self.cur = self.conn.cursor()

    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(":memory:")
            return conn
        except Error as e:
            print(e)
        return conn

    def disconnect(self):
        self.conn.close()

    def create_menu_table(self, data_file):
        data_file = data_file
        sql_menu = """CREATE TABLE menu_table (
                  category          VARCHAR(50),
                  item_name         VARCHAR(50),
                  description       VARCHAR(150),
                  price             VARCHAR(50),
                  prep_time         INT,
                  available         INT
                  );"""
        self.cur.execute(sql_menu)
        menu_items = self.insert_menu(data_file)
        sql_menu_ins = """INSERT INTO menu_table VALUES (?,?,?,?,?,?)"""
        i = 1
        for line in range(1,len(menu_items)):
            self.cur.execute(sql_menu_ins, menu_items[i])
            i += 1
        self.conn.commit()  

    def create_user_table(self, data_file):
        users = []
        data_file = data_file
        sql_user = """CREATE TABLE users_table (
                  user_name             VARCHAR(50),
                  account_type          VARCHAR(50),
                  first_name            VARCHAR(150),
                  last_name             VARCHAR(50),
                  email                 VARCHAR(50),
                  phone_number          VARCHAR(50),
                  password              VARCHAR(50),
                  employee_id           VARCHAR(50),
                  credit_card_number    VARCHAR(50),
                  credit_card_exp_date  VARCHAR(50),
                  billing_address       VARCHAR(50),
                  reward_points         INT,
                  order_history         INT
                  );"""
        self.cur.execute(sql_user)
        user_list = self.insert_user(data_file)
        sql_user_ins = """INSERT INTO users_table VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        i = 1
        for line in range(1,len(user_list)):
            self.cur.execute(sql_user_ins, user_list[i])
            i+=1
        self.conn.commit()  

    def insert_menu(self, menu):
        self.menu = menu
        menu_lines = []
        with open(menu) as m:     
            for line in m:
                l = line.split('\t')
                menu_lines.append(l)
        return menu_lines

    def insert_user(self, user):
        self.user = user
        user_lines = []
        with open(user) as u:     
            for line in u:
                l = line.split('\t')
                user_lines.append(l)
        return user_lines
        
    def display_daily_menu(self, category):
        category_name = category
        sql_query = """SELECT item_name, description, price FROM menu_table
                    WHERE category = ? AND available = 1"""
        self.cur.execute(sql_query, (category_name,))
        print("{}: ".format(category_name))            
        for row in self.cur.fetchall():
            print("\t{}\t(${})\n\t   {}".format(row[0], row[2], row[1]))
        self.conn.commit
        
    def set_food_price(self, name, price):
        item_nme = name
        item_price = price
        sql_query = f"""UPDATE menu_table
                    SET price = {item_price}
                    WHERE item_name = ?"""
        self.cur.execute(sql_query, (item_nme,))
        self.conn.commit

    def set_food_category(self, name, category):
        item_name = name
        item_cat = category
        sql_query = f"""UPDATE menu_table
                    SET category = {item_cat}
                    WHERE item_name = ?"""
        self.cur.execute(sql_query, (item_name,))
        self.conn.commit

    def set_food_description(self, name, description):
        item_name = name
        item_desc = description
        sql_query = f"""UPDATE menu_table
                    SET description = {item_desc}
                    WHERE item_name = ?"""
        self.cur.execute(sql_query, (item_name,))
        self.conn.commit

    def set_food_availability(self, name, availability):
        item_name = name
        item_avail = availability
        sql_query = f"""UPDATE menu_table
                    SET available = {item_avail}
                    WHERE item_name = ?"""
        self.cur.execute(sql_query, (item_name,))
        self.conn.commit

    def set_food_name(self, old_name, new_name):
        item_name = old_name
        item_new_name = new_name
        sql_query = f"""UPDATE menu_table
                    SET item_name = {item_new_name}
                    WHERE item_name = ?"""
        self.cur.execute(sql_query, (item_name,))
        self.conn.commit

    def get_food_price(self, name):
        item_name = name
        exist_check = self.is_food_exist(item_name)
        if exist_check == True:
            sql_query = """SELECT price FROM menu_table
                        WHERE item_name == ?"""
            self.cur.execute(sql_query, (item_name,))
            item_price = self.cur.fetchone()
            return item_price[0]
        else:
            return -1.0
            
    def set_food_prep(self, name, prep):
        item_nme = name
        item_prep = prep
        sql_query = f"""UPDATE menu_table
                    SET prep_time = {item_prep}
                    WHERE item_name = ?"""
        self.cur.execute(sql_query, (item_nme,))
        self.conn.commit

    def get_food_time(self, name):
        item_name = name
        exist_check = self.is_food_exist(item_name)
        if exist_check == True:
            sql_query = """SELECT prep_time FROM menu_table
                        WHERE item_name == ?"""
            self.cur.execute(sql_query, (item_name,))
            item_time = self.cur.fetchone()
            return item_time[0]
        else:
            return -1

    def is_food_exist(self, name):
        item_name = name
        sql_query = """SELECT item_name FROM menu_table
                    WHERE item_name = ?"""
        self.cur.execute(sql_query, (item_name,))
        result = self.cur.fetchall()
        if len(result) == 0:
            return False
        else:
            return True

    def is_food_available(self, name):
        item_nme = name
        sql_query = """SELECT available FROM menu_table
                    WHERE item_name = ?"""
        self.cur.execute(sql_query, (item_nme,))
        result = self.cur.fetchone()
        if result[0] == 1:
            return True
        else:
            return False
    
    def update_customer_rewards(self, name, value):
        user_name = name
        reward_val = value
        sql_query = f"""UPDATE users_table
                    SET reward_points = {reward_val}
                    WHERE user_name = ?"""
        self.cur.execute(sql_query, (user_name,))
        self.conn.commit

    def update_customer_history(self, name, value):
        user_name = name
        history_val = value
        sql_query = f"""UPDATE users_table
                    SET order_history = {history_val}
                    WHERE user_name = ?"""
        self.cur.execute(sql_query, (user_name,))
        self.conn.commit    

    def is_user_exist(self, user_name):
        username = user_name
        sql_query = """SELECT user_name FROM users_table
                    WHERE user_name = ?"""
        self.cur.execute(sql_query, (username,))
        result = self.cur.fetchall()
        if len(result) == 0:
            return False
        else:
            return True        

    def delete_user(self, user_name):
        username = user_name
        sql_query = """DELETE FROM users_table
                    WHERE user_name = ?"""
        self.cur.execute(sql_query, (username,))
        self.conn.commit

    def update_admin(self, user):
        admin = user
        sql_query = f"""UPDATE users_table
                    SET phone_number = {0}, email = {1}
                    WHERE user_name = {2}""".format(admin.phone_num, admin.email, admin.user_name)
        self.cur.execute(sql_query)
        self.conn.commit

    def get_admin(self, user_name):
        admin = user_name
        exist_check = self.is_user_exist(admin)
        if exist_check == True:
            sql_query = """SELECT 
                            employee_id,
                            user_name,
                            account_type,
                            first_name,
                            last_name,
                            email,
                            phone_number,
                            password
                        FROM users_table
                        WHERE user_name = ? AND account_type = 'admin'"""
            self.cur.execute(sql_query, (admin,))
            result = self.cur.fetchone()
            if result != None:
                curr_admin = Admin(*(result))
                return curr_admin
            else:
                return 0

    def update_customer(self, user):
        cust = user
        exist_check = self.is_user_exist(cust.user_name)
        if exist_check == True:
            sql_query = f"""UPDATE users_table
                        SET 
                            credit_card_number = {0},
                            credit_card_exp_date = {1},
                            billing_address = {2},
                            phone_number = {3}, 
                            email = {4}
                        WHERE user_name = {5}
                        """.format(cust.card_num, cust.card_date, cust.address, cust.phone_num, cust.email, cust.user_name)
            self.cur.execute(sql_query)
            self.conn.commit   
        else:
            data_tuple = (cust.user_name, 'customer', cust.first_name, cust.last_name, cust.email, cust.phone_num, cust.password, 
                            None,  cust.card_num, cust.card_date, cust.address, 0, 0)
            sql_query = """INSERT INTO users_table VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            self.cur.execute(sql_query, data_tuple)
            self.conn.commit   


    def get_customer(self, user_name):
        cust = user_name
        exist_check = self.is_user_exist(cust)
        if exist_check == True:
            sql_query = """SELECT 
                            credit_card_number, 
                            credit_card_exp_date,
                            billing_address,
                            reward_points,
                            order_history,
                            user_name,
                            account_type,
                            first_name,
                            last_name,
                            email,
                            phone_number,
                            password
                        FROM users_table
                        WHERE user_name = ? AND account_type = 'customer'"""
            self.cur.execute(sql_query, (cust,))
            result = self.cur.fetchone()
            if result != None:
                curr_cust = Customer(*result)
                return curr_cust
            else:
                return 0
                        