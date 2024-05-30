from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, Time, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import sqlalchemy
import re
import pandas as pd
from sqlalchemy import func
from datetime import datetime
import random


engine = create_engine('mysql+pymysql://root@localhost/musicshop')
Base = sqlalchemy.orm.declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Database tables as Python classes
class Brand(Base):
    __tablename__ = 'brand'

    brand_id = Column(Integer, primary_key=True)
    name_of_brand = Column(String(20), nullable=False)
    rating = Column(Numeric(20), nullable=False)

class Category(Base):
    __tablename__ = 'Category'

    category_id = Column(Integer, primary_key=True)
    categ_name = Column(String(20), nullable=False)

class DeliveryMethod(Base):
    __tablename__ = 'delivery_method'

    del_method_id = Column(Integer, primary_key=True)
    aditional_price = Column(Numeric(10, 2), nullable=False)
    name_ = Column(String(10), nullable=False)
    time_for_del = Column(String(10), nullable=False)

class Payment(Base):
    __tablename__ = 'Payment'

    payment_id = Column(Integer, primary_key=True)
    pay_method = Column(String(100), nullable=False)

class DeliveryCompany(Base):
    __tablename__ = 'delivery_company'

    emp_no = Column(Integer, primary_key=True)
    name_ = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    phone_no = Column(String(16), nullable=False)

class Discount(Base):
    __tablename__ = 'Discount'

    disc_id = Column(Integer, primary_key=True)
    dis_amount = Column(Numeric(3, 3), nullable=False)
    sum_to_get = Column(Numeric(10, 2), nullable=False)
    name_ = Column(String(100), nullable=False)

class Customer(Base):
    __tablename__ = 'Customer'

    cus_id = Column(Integer, primary_key=True)
    name_ = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    phone_no = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    disc_id = Column(Integer, ForeignKey('Discount.disc_id'))

    discount = relationship("Discount")

class Type(Base):
    __tablename__ = 'Type_'

    type_id = Column(Integer, primary_key=True)
    type_name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('Category.category_id'))

    category = relationship("Category")

class Instrument(Base):
    __tablename__ = 'Instrument'

    Inst_id = Column(Integer, primary_key=True)
    price = Column(Numeric(10, 2), nullable=False)
    ins_name = Column(String(255), nullable=False)
    amount_on_store = Column(Integer, nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.brand_id'))
    type_id = Column(Integer, ForeignKey('Type_.type_id'))

    brand = relationship("Brand")
    type = relationship("Type")

class SaleInstr(Base):
    __tablename__ = 'SaleInstr'

    tran_id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    Inst_id = Column(Integer, ForeignKey('Instrument.Inst_id'), primary_key=True)
    total_price = Column(Numeric(10, 2), nullable=False)

    instrument = relationship("Instrument")

class SaleOrder(Base):
    __tablename__ = 'SaleOrder'

    sale_id = Column(Integer, primary_key=True)
    tran_id = Column(Integer, ForeignKey('SaleInstr.tran_id'), nullable=False)
    date_s = Column(Date, nullable=False)
    time_s = Column(Time, nullable=False)
    total_price = Column(Numeric(10, 2))
    payment_id = Column(Integer, ForeignKey('Payment.payment_id'), nullable=False)
    cus_id = Column(Integer, ForeignKey('Customer.cus_id'), nullable=False)

    sale_instr = relationship("SaleInstr")
    payment = relationship("Payment")
    customer = relationship("Customer")

class Delivery(Base):
    __tablename__ = 'Delivery'

    delivery_id = Column(Integer, primary_key=True)
    delivery_adres = Column(String(40), nullable=False)
    delivery_status = Column(String(10), nullable=False)
    sale_id = Column(Integer, ForeignKey('SaleOrder.sale_id'), nullable=False)
    del_method_id = Column(Integer, ForeignKey('delivery_method.del_method_id'), nullable=False)
    emp_no = Column(Integer, ForeignKey('delivery_company.emp_no'), nullable=False)

    sale_order = relationship("SaleOrder")
    delivery_method = relationship("DeliveryMethod")
    delivery_company = relationship("DeliveryCompany")

class Person:
    def __init__(self):
        self.__name = ""
        self.__surname = ""
        self.__phone_no = ""
        self.__address = ""
        self.__disc_id = 1
        self.__ccus_id = None

    def get_cus_id(self):
        return self.__ccus_id
    
    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_phone_no(self):
        return self.__phone_no

    def get_address(self):
        return self.__address

    def get_disc_id(self):
        return self.__disc_id
    
    def set_cus_id(self,cus_id):
        self.__ccus_id = cus_id

    def set_name(self, name):
        self.__name = name

    def set_surname(self, surname):
        self.__surname = surname

    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

    def set_address(self, address):
        self.__address = address

    def set_disc_id(self, disc_id):
        self.__disc_id = disc_id

person = Person()

def validate_input(prompt, pattern, example):
    while True:
        value = input(prompt)
        if re.match(pattern, value):
            return value
        else:
            print(f"Invalid input. Example of valid input: {example}")

def fetch_cus_id(name, surname, phone_no, address):
    # Query the database to find the customer with matching details
    customer = session.query(Customer).filter_by(
        name_=name, surname=surname, phone_no=phone_no, address=address).first()

    if customer:
        return customer.cus_id  # Return the cus_id if a customer is found
    else:
        return None  # Return None if no matching customer is found

# Registration function
def register_customer():
    name = validate_input("Enter your name: ", r'^[A-Za-z]+$', "John")
    person.set_name(name)
    surname = validate_input("Enter your surname: ", r'^[A-Za-z]+$', "Doe")
    person.set_surname(surname)
    phone_no = validate_input("Enter your phone number (e.g., 123-456-7890): ", r'^\d{3}-\d{3}-\d{4}$', "123-456-7890")
    person.set_phone_no(phone_no)
    address = validate_input("Enter your address: ", r'^[A-Za-z0-9\s,]+$', "123 Main St")
    person.set_phone_no(phone_no)

    new_customer = Customer(name_=name, surname=surname, phone_no=phone_no, address=address, disc_id=1)

    session.add(new_customer)
    session.commit()
    ccus_id = fetch_cus_id(name, surname, phone_no, address)
    if ccus_id is None:
        print("Customer not found in the database.")
        return None
    
    person.set_cus_id(ccus_id)
    print("Registration successful!")

def show_instruments():
    # Define the SQL query to fetch the instruments data
    query = """
    SELECT ins_name AS 'Instrument Name', amount_on_store AS 'Amount on Store', price AS 'Price'
    FROM Instrument
    WHERE amount_on_store > 0;
    """
    
    # Execute the query and fetch the data into a pandas DataFrame
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    
    # Display the DataFrame
    print(df)

def insert_sale_instr(tran_id, inst_id, amount):
    instrument = session.query(Instrument).filter_by(Inst_id=inst_id).first()
    if instrument:
        total_price = instrument.price * amount
        sale_instr = SaleInstr(tran_id=tran_id, Inst_id=inst_id, amount=amount, total_price=total_price)
        session.add(sale_instr)
        session.commit()
        return total_price
    else:
        print(f"Instrument with ID {inst_id} not found.")
        return None

def get_instrument_id(name):
    instrument = session.query(Instrument).filter_by(ins_name=name).first()
    if instrument:
        print(instrument.Inst_id)
        return instrument.Inst_id
    else:
        print(f"Instrument {name} not found.")
        return None
    
def show_total_price(tran_id):
    total = session.query(func.sum(SaleInstr.total_price)).filter_by(tran_id=tran_id).scalar()
    print(f"Total price for transaction : {total}")
    return total

def create_new_transaction():
    tran_id = session.query(func.max(SaleInstr.tran_id)).scalar()
    tran_id = 1 if tran_id is None else tran_id + 1
    total_price = 0

    while True:
        name = validate_input("Enter the instrument name: ", r'^[A-Za-z\s]+$', "Invalid input. Please enter a valid instrument name.")
        inst_id = get_instrument_id(name)
        if not inst_id:
            continue
        amount = int(validate_input("Enter the amount: ", r'^\d+$', "Invalid input. Please enter a valid amount."))
        total_price += insert_sale_instr(tran_id, inst_id, amount)
        
        show_total_price(tran_id)
        
        choice = validate_input("Choose an option: 'Resign and comeback to menu', 'Order more', 'Continue order process': ", r'^(Resign and comeback to menu|Order more|Continue order process)$', "Invalid input. Please choose a valid option.")
        if choice == 'Resign and comeback to menu':
            session.query(SaleInstr).filter_by(tran_id=tran_id).delete()
            session.commit()
            print("Transaction cancelled.")
            break
        elif choice == 'Order more':
            continue
        elif choice == 'Continue order process':
            payment_methods = session.query(Payment).all()
            print("Payment methods:")
            for method in payment_methods:
                print(method.pay_method)
            chosen_method = validate_input("Choose a payment method : ", r'^(Bank Transfer|PayPal||Credit Card)$', "Invalid input. Please choose a valid payment method.")
            payment_id = session.query(Payment.payment_id).filter(Payment.pay_method == chosen_method).scalar()
            if not payment_id:
                print("Payment method not found.")
                continue
            ccus_id = person.get_cus_id()  # Implement this function to fetch emp_no
            
            # Get current date and time
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            
            # Create a new SaleOrder instance and insert it into the database
            new_order = SaleOrder(tran_id=tran_id, date_s=current_date, time_s=current_time, total_price=total_price, payment_id=payment_id, cus_id=ccus_id)
            session.add(new_order)
            session.commit()
            
            delivery_methods = session.query(DeliveryMethod).all()
            print("Delivery methods:")
            for method in delivery_methods:
                print(f"Name: {method.name_}, Time for delivery: {method.time_for_del}, Additional Price: {method.aditional_price}")
            chosen_method_name = validate_input("Choose a delivery method: ", r'^(Standard|Express|Inpost)$', "Invalid input. Please choose a valid delivery method.")
            chosen_method = session.query(DeliveryMethod).filter(DeliveryMethod.name_ == chosen_method_name).first()
            if chosen_method:
                del_method_id = chosen_method.del_method_id
            else:
                print("Delivery method not found.")
                continue
            sale_order = session.query(SaleOrder).filter_by(tran_id=tran_id).first()
            if not sale_order:
                print("SaleOrder not found.")
                return

            # Take a random emp_no from all DeliveryCompany
            delivery_companies = session.query(DeliveryCompany).all()
            if not delivery_companies:
                print("No delivery companies found.")
                return
            random_delivery_company = random.choice(delivery_companies)
            emp_no = random_delivery_company.emp_no

            # Get del_method_id from the previously chosen delivery method
            if not del_method_id:
                print("Delivery method not found.")
                return

            # Ask for delivery address
            delivery_adress = validate_input("Enter delivery address: ", r'^[A-Za-z0-9\s,]+$', "123 Main St")

            # Insert new row into the Delivery table
            new_delivery = Delivery(delivery_adres=delivery_adress, delivery_status='registered', sale_id=sale_order.sale_id, del_method_id=del_method_id, emp_no=emp_no)
            session.add(new_delivery)
            session.commit()
            
            print('Your order is succesfuly regestrated')
            
            break

def show_discount_card_info():
    # Get the list of available customer IDs from the Customer table
    available_cus_ids = [cus.cus_id for cus in session.query(Customer).all()]

    # Construct the pattern for validating customer IDs
    pattern = '^(' + '|'.join(str(cus_id) for cus_id in available_cus_ids) + ')$'

    # Get the customer ID using validate_input with the constructed pattern
    cus_id = validate_input("Enter the customer ID: ", pattern, "Invalid customer ID. Please enter a valid customer ID.")

    # Query the Customer table to retrieve the customer's discount ID
    customer = session.query(Customer).filter_by(cus_id=cus_id).first()

    # Check if the customer exists
    if customer:
        # Get the discount ID for the customer
        discount_id = customer.disc_id

        # Query the Discount table to retrieve the discount card information for the customer's discount ID
        discount_card = session.query(Discount).filter_by(disc_id=discount_id).first()

    print("Showing list of instruments...")
    # Check if the discount card information exists for the provided customer ID
    if discount_card:
        # Display the discount card information
        print("Discount Card Information:")
        print(f"Customer ID: {cus_id}")
        print(f"Discount Percentage: {discount_card.dis_amount * 100} %")
        print(f"Name of a card: {discount_card.name_}")
    else:
        print("Discount card information not found for the provided customer ID.")


def print_menu():
    print("Welcome to the Music Shop!")
    print("1. Show list of instruments")
    print("2. Make an order")
    print("3. Show current discount card")
    print("4. Exit")

def main():
    while True:
        print("Hi,first of all complete registration:)")
        register_customer()
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            show_instruments()
        elif choice == "2":
            create_new_transaction()
            print("Making an order...")
        elif choice == "3":
            print("Showing current discount card...")
            show_discount_card_info()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


