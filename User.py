
class User:
    def __init__(self,ID,first_name,last_name,password,email,phone_number,user_class):
        self.__first_name=first_name
        self.__last_name=last_name
        self.__ID=ID
        self.__password=password
        self.__email=email
        self.__phone_number=phone_number
        self.__user_class=user_class

    def __str__(self):
        return f"{self.__first_name},{self.__last_name},{self.__ID},{self.__password},{self.__email},{self.__phone_number},{self.__user_class}"

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_ID(self):
        return self.__ID

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number

    def get_user_class(self):
        return self.__user_class

    # Setter methods
    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_ID(self, ID):
        self.__ID = ID

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_user_class(self, user_class):
        self.__user_class = user_class


