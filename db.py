import sqlite3
from sqlite3 import Error
# we create a connection object in main
import logging
logging.basicConfig(filename='ReservationLog.log',
                  filemode='a',
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                  level=logging.DEBUG)
#Admin info
# admin_ID="113311"
# password="ofcourse"

conn=sqlite3.connect("app.db")
c=conn.cursor()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
#### Tables

# c.execute("""CREATE TABLE users
#             ( user_ID TEXT PRIMARY KEY NOT NULL,
#             first_name TEXT NOT NULL,
#             last_name TEXT NOT NULL,
#             password TEXT NOT NULL,
#             email TEXT NOT NULL,
#             phone_number TEXT NOT NULL,
#             user_class TEXT NOT NULL)""")
#
#
# c.execute("""CREATE TABLE admin
#             ( admin_ID TEXT PRIMARY KEY NOT NULL,
#             password TEXT NOT NULL)""")
#
# c.execute("""CREATE TABLE golf_cart
#             ( plate_number TEXT PRIMARY KEY NOT NULL,
#             location TEXT NOT NULL)""")

# c.execute("""CREATE TABLE reservation(
#             start_time TEXT NOT NULL,
#             end_time TEXT NOT NULL,
#             date TEXT NOT NULL,
#             user_ID TEXT ,
#             plate_number TEXT,
#             FOREIGN KEY (user_ID) REFERENCES users (user_ID),
#             FOREIGN KEY (plate_number) REFERENCES golf_cart (plate_number)
#             )""")


def insert_user(user):
    with conn:
        c.execute("INSERT INTO users VALUES (:user_ID,:first_name,:last_name,:password,:email,"
                  ":phone_number,:user_class)",{"user_ID":user.get_ID(),"first_name":user.get_first_name(),
                   "last_name":user.get_last_name(),"password":user.get_password(),"email":user.get_email(),
                    "phone_number":user.get_phone_number(),"user_class":user.get_user_class()})

def insert_admin(admin):
    with conn:
        c.execute("INSERT INTO admin VALUES (:admin_ID,:password)", {"admin_ID": admin.get_admin_ID(),
        "password": admin.get_admin_password()})

def insert_golf_cart(golf_cart):
    with conn:
          c.execute("INSERT INTO golf_cart VALUES (:plate_number, :location)",
                    {"plate_number": golf_cart.get_plate_number(),
                     "location": golf_cart.get_location()})

def insertGolfCart(golf_cart):
    plate_number = golf_cart.get_plate_number()
    with conn:
        c.execute("SELECT plate_number FROM golf_cart WHERE plate_number = :plate_number",
                  {"plate_number": plate_number})
        existing_plate = c.fetchone()
        if existing_plate is None:
            c.execute("INSERT INTO golf_cart VALUES (:plate_number, :location)",{"plate_number": plate_number,
                       "location": golf_cart.get_location()})
            return True
        else:
            return False


def insert_reservation(reservation,user_ID,plate_number):
    cart=get_golf_cart_by_id(plate_number)
    with conn:
        c.execute("INSERT INTO reservation VALUES (:start_time,:end_time,:date,"
        ":user_ID,:plate_number)",{ "start_time":reservation.get_start_time(),
        "end_time":reservation.get_end_time(),"date":reservation.get_date(),
        "user_ID":user_ID,"plate_number":plate_number})
        logging.info(
            f'A reservation have been successfully made by user with ID:{user_ID} for the cart with Plate number:'
            f'{plate_number} and Location {cart[0][1]} and Start time={reservation.get_start_time()} and End time='
            f'{reservation.get_end_time()} and date'
            f'={reservation.get_date()}')

#get by key
def get_user_by_id(user_ID ):
    c.execute("SELECT * FROM users WHERE user_ID=:user_ID",{"user_ID":user_ID })
    return c.fetchall()

def get_admin_by_id(admin_ID ):
    c.execute("SELECT * FROM admin WHERE admin_ID=:admin_ID",{"admin_ID":admin_ID })
    return c.fetchall()

def get_golf_cart_by_id(plate_number ):
    c.execute("SELECT * FROM golf_cart WHERE plate_number=:plate_number",{"plate_number":plate_number })
    return c.fetchall()

def get_reservation_by_id(user_ID, plate_number):
    c.execute("SELECT * FROM reservation WHERE user_ID=:user_ID AND plate_number=:plate_number",
              {"user_ID": user_ID, "plate_number": plate_number})
    return c.fetchall()

def get_userClass_by_id(user_ID):
    c.execute("SELECT user_class FROM users WHERE user_ID=:user_ID",{"user_ID":user_ID})
    return c.fetchall()
def get_reservation_by_userID(user_ID):
    c.execute("SELECT * FROM reservation WHERE user_ID=:user_ID", {"user_ID": user_ID})
    return c.fetchall()
def get_reservation_by_plateNumber(plate_number):
    c.execute("SELECT * FROM reservation WHERE plate_number=:plate_number", {"plate_number": plate_number})
    return c.fetchall()

def get_available_golf_carts():
    with conn:
        c.execute("""
            SELECT g.*
            FROM golf_cart g
            LEFT JOIN reservation r ON g.plate_number = r.plate_number
            WHERE r.plate_number IS NULL
        """)

        available_carts = c.fetchall()

        return available_carts

def get_all_golf_Carts():
    with conn:
        c.execute("select * from golf_cart")
        return c.fetchall()


#remove object
def remove_users(users):
    with conn:
        c.execute("DELETE from users WHERE user_ID=:user_ID",{"user_ID":users.get_ID()})

def remove_admin(admin):
    with conn:
        c.execute("DELETE from admin WHERE admin_ID=:admin_ID",{"admin_ID":admin.get_admin_ID()})

def remove_golf_cart(golf_cart):
    with conn:
        c.execute("DELETE from golf_cart WHERE plate_number=:plate_number",{"plate_number":golf_cart.get_plate_number() })

def remove_reservation(reservation):
    with conn:
        c.execute("DELETE from reservation WHERE reservation_ID=:reservation_ID",{"reservation_ID":reservation.get_ID()})


