class User:

    def __init__(self, user_name, account, first_name, last_name, email, phone_num, password):
        self.user_name = user_name
        self.account = account
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_num = phone_num
        self.password = password
class Admin(User):

    def __init__(self, id, user_name, account, first_name, last_name, email, phone_num, password):
        User.__init__(self, user_name, account, first_name, last_name, email, phone_num, password)
        self.id = id

    def __str__(self):
        return "{} {}: {}, Employee ID: {}".format(self.first_name, self.last_name, self.user_name, self.id)

class Customer(User):

    def __init__(self, card_num = 0, card_date = 0, address = 0, points = 0, history = 0, user_name = "Guest", account = 0, first_name = 0, last_name = 0, email = 0, phone_num = 0, password = 0):
        User.__init__(self, user_name, account, first_name, last_name, email, phone_num, password)
        self.card_num = card_num
        self.card_date = card_date
        self.address = address
        self.points = points
        self.history = history
        
    def __str__(self):
        return "{} {}: {}, Rewards: {}".format(self.first_name, self.last_name, self.user_name, self.points)