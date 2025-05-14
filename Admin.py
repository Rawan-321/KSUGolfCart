
class Admin:
    def __init__(self,ID,password):
        self.__ID=ID
        self.__password=password


    def __str__(self):
        return (self.__ID+','+self.__password)

    def get_admin_ID(self):
        return self.__ID
    def set_admin_ID(self,ID):
        self.__ID=ID

    def get_admin_password(self):
        return self.__password

    def set_admin_ID(self,password):
        self.__password=password



    
