from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, Time, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import sqlalchemy
import re
import pandas as pd
from sqlalchemy import func



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
    additional_price = Column(Numeric(10, 2), nullable=False)
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
    delivery_address = Column(String(40), nullable=False)
    delivery_status = Column(String(10), nullable=False)
    sale_id = Column(Integer, ForeignKey('SaleOrder.sale_id'), nullable=False)
    del_method_id = Column(Integer, ForeignKey('delivery_method.del_method_id'), nullable=False)
    emp_no = Column(Integer, ForeignKey('delivery_company.emp_no'), nullable=False)

    sale_order = relationship("SaleOrder")
    delivery_method = relationship("DeliveryMethod")
    delivery_company = relationship("DeliveryCompany")

def validate_input(prompt, pattern, example):
    while True:
        value = input(prompt)
        if re.match(pattern, value):
            return value
        else:
            print(f"Invalid input. Example of valid input: {example}")

# Registration function
def register_customer():
    name = validate_input("Enter your name: ", r'^[A-Za-z]+$', "John")
    surname = validate_input("Enter your surname: ", r'^[A-Za-z]+$', "Doe")
    phone_no = validate_input("Enter your phone number (e.g., 123-456-7890): ", r'^\d{3}-\d{3}-\d{4}$', "123-456-7890")
    address = validate_input("Enter your address: ", r'^[A-Za-z0-9\s,]+$', "123 Main St")

    new_customer = Customer(name_=name, surname=surname, phone_no=phone_no, address=address, disc_id=1)

    session.add(new_customer)
    session.commit()

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
    print(f"Total price for transaction {tran_id}: {total}")
    return total

def print_menu():
    print("Welcome to the Music Shop!")
    print("1. Register")
    print("2. Show list of instruments")
    print("3. Make an order")
    print("4. Show current discount card")
    print("5. Exit")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
           register_customer()
        elif choice == "2":
            print("Showing list of instruments...")
            show_instruments()
        elif choice == "3":
            
            print("Making an order...")
        elif choice == "4":
            
            print("Showing current discount card...")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
get_instrument_id('Buffet Clarinet')
if __name__ == "__main__":
    main()


