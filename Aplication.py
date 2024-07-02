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

class InstrumentSalesView(Base):
    __tablename__ = 'InstrumentSalesRanking'
    __table_args__ = {'autoload_with': engine}

    Inst_id = Column(Integer, primary_key=True)
    ins_name = Column(String(255))
    total_amount_sold = Column(Integer)
    sales_rank = Column(Integer)

person = Person()

def show_instrument_sales_view():
    results = session.query(InstrumentSalesView).all()

    if results:
        print(f"{'Instrument ID':<15}{'Instrument Name':<30}{'Total Amount Sold':<20}{'Sales Rank':<10}")
        print("="*75)
        for row in results:
            print(f"{row.Inst_id:<15}{row.ins_name:<30}{row.total_amount_sold:<20}{row.sales_rank:<10}")
    else:
        print("No data available in the view.")

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

def get_cus_info(client_no):
    # Query the database to find the customer with matching details
    customer = session.query(Customer).filter_by(cus_id = client_no).first()

    if customer:
        return customer.name_, customer.surname, customer.phone_no, customer.address, customer.disc_id 
    else:
        return None  # Return None if no matching customer is found    
    
def register_customer():
    name = validate_input("Enter your name: ", r'^[A-Za-z]+$', "John")
    person.set_name(name)
    surname = validate_input("Enter your surname: ", r'^[A-Za-z]+$', "Doe")
    person.set_surname(surname)
    phone_no = '+48-' + validate_input("Enter your phone number (e.g., 123-456-789): ", r'^\d{3}-\d{3}-\d{3}$', "123-456-7890")
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

def loggining_customer():
       # Get the list of available customer IDs from the Customer table
    available_cus_ids = [cus.cus_id for cus in session.query(Customer).all()]

    # Construct the pattern for validating customer IDs
    pattern = '^(' + '|'.join(str(cus_id) for cus_id in available_cus_ids) + ')$'

    client_no = validate_input("Please enter your customer id: ", pattern, "There is no person with such customer id" )

    name, surname, phone, address, disc = get_cus_info(client_no)

    person.set_cus_id(client_no), person.set_name(name), person.set_surname(surname), person.set_phone_no(phone), person.set_address(address), person.set_disc_id(disc)

    return

def show_instruments():
    results = session.query(Instrument).filter(Instrument.amount_on_store > 0).all()

    if results:
        print(f"{'Instrument Number':<15}{'Instrument Name':<30}{'Amount On Store':<20}{'Price':<10}")
        print("="*75)
        for row in results:
            print(f"{row.Inst_id:<15}{row.ins_name:<30}{row.amount_on_store:<20}{row.price:<10}")
    else:
        print("No data available in the view.")

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
        show_instruments()
        available_inst_ids = [inst.Inst_id for inst in session.query(Instrument).all()]

        pattern = '^(' + '|'.join(str(inst_id) for inst_id in available_inst_ids) + ')$'

        inst_no = validate_input("Enter the instrument number which u want to order: ", pattern, "Invalid input. Please enter a valid instrument number.")
        inst_id = inst_no
        amount = int(validate_input("Enter the amount: ", r'^\d+$', "Invalid input. Please enter a valid amount."))
        total_price += insert_sale_instr(tran_id, inst_id, amount)
        
        show_total_price(tran_id)
        
        choice = validate_input("Choose an option: '1)Resign and comeback to menu', '2)Order more', '3)Continue order process': ", r'^(1|2|3)$', "Invalid input. Please choose a valid option.")
        if choice == '1':
            session.query(SaleInstr).filter_by(tran_id=tran_id).delete()
            session.commit()
            print("Transaction cancelled.")
            break
        elif choice == '2':
            continue
        elif choice == '3':
            payment_methods = session.query(Payment).all()
            print("Payment methods:")
            for method in payment_methods:
                print(method.pay_method)
            chosen_method = validate_input("Choose a payment method 1)Bank Transfer 2)PayPal 3)Credit Card : ", r'^(1|2|3)$', "Invalid input. Please choose option(1-3).")
            payment_id = chosen_method
            if not payment_id:
                print("Payment method not found.")
                continue
            ccus_id = person.get_cus_id()  
            
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
            chosen_method_name = validate_input("Choose a delivery method: 1)Standard|2)Express|3)Inpost ", r'^(1|2|3)$', "Invalid input. Please choose option(1-3).")
            del_method_id = chosen_method_name

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

    # Check if the discount card information exists for the provided customer ID
    if discount_card:
        # Display the discount card information
        print("Discount Card Information:")
        print(f"Customer ID: {cus_id}")
        print(f"Discount Percentage: {discount_card.dis_amount * 100} %")
        print(f"Name of a card: {discount_card.name_}")
    else:
        print("Discount card information not found for the provided customer ID.")

def registration_menu():
    while True:
        print("Welcome to the Music Shop!")
        print("Complete logging:)")
        choice = validate_input("Registration/logging (1/2)", r'^(1|2)$', 'Please choose 1(Registration) or 2(Logging)')
        if choice == '1':
            register_customer()
            print("Registration completted succsesfully")
            break
        elif choice == '2':
            loggining_customer()
            print("Loggining completted succsesfully")
            break

def add_invoice(path):
    dot_index = path.rfind('.')
    extension = path[dot_index + 1:]
    
    if extension == 'xlsx':
        df = pd.read_excel(path)
        session = Session()  # Assuming you have defined and configured your SQLAlchemy session
        
        for index, row in df.iterrows():
            name = row['ins_name']
            amount = row['amount']
            price = row['price']
            brand_name = row['name_of_brand']
            type_name = row['type_name']
            category_name = row.get('category_name', None)  # Optional category_name
            
            instrument = session.query(Instrument).filter_by(ins_name=name).first()
            
            if instrument:
                instrument.amount_on_store += amount
            else:
                brand = session.query(Brand).filter_by(name_of_brand=brand_name).first()
                
                if not brand:
                    brand = Brand(name_of_brand=brand_name, rating=5)
                    session.add(brand)
                    session.commit()  # Commit brand creation
                
                type = session.query(Type).filter_by(type_name=type_name).first()
                
                if not type:
                    if category_name:
                        category = session.query(Category).filter_by(categ_name=category_name).first()
                        
                        if not category:
                            category = Category(categ_name=category_name)
                            session.add(category)
                            session.commit()  # Commit category creation
                        
                        type = Type(type_name=type_name, category_id=category.category_id)
                        session.add(type)
                    else:
                        type = Type(type_name=type_name)
                        session.add(type)
                    
                    session.commit()  # Commit type creation
                
                # Now we should have the type_id
                new_inst = Instrument(
                    price=price,
                    ins_name=name,
                    amount_on_store=amount,
                    brand_id=brand.brand_id,
                    type_id=type.type_id  # Assign the fetched or created type_id
                )
                session.add(new_inst)
            
            # Batch commit for better performance
            if index % 100 == 0:
                session.commit()
        
        session.commit()  # Final commit for any remaining changes
        session.close()   # Close the session

def print_menu():
    print("1. Make an order")
    print("2. Show current discount card")
    print("3. Show instrument ranking")
    print("4. Log out")
    print("5. Exit")

def main():
    registration_menu()
    while True:
        print_menu()
        choice = validate_input("Enter your choice: ", r'^(1|2|3|4|5|6)$', 'Choose option from 1- 4')
        if choice == "1":
            create_new_transaction()
            print("Order completed")
        elif choice == "2":
            print("Showing current discount card...")
            show_discount_card_info()
        elif choice == "3":
            print("Showing instrument ranking...")
            show_instrument_sales_view()
        elif choice == "4":
            registration_menu()
        elif choice == "5":
            print("Exiting...")
            break
        elif choice =="6":
            add_invoice('Instrument_Invoice.xlsx')

if __name__ == "__main__":
    main()





