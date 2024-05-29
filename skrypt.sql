
CREATE OR replace TABLE brand (
    brand_id INTEGER NOT NULL AUTO_INCREMENT,
    name_of_brand VARCHAR(20) NOT NULL,
    rating NUMERIC(28) NOT NULL,
    PRIMARY KEY (brand_id)
);

CREATE OR replace TABLE Category (
    category_id INTEGER NOT NULL AUTO_INCREMENT,
    categ_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (category_id)
);

CREATE OR replace TABLE Customer (
    cus_id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    phone_no VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    buying_no NVARCHAR(10) NOT NULL,
    Discount_disc_id INTEGER NOT NULL,
    disc_id INTEGER NOT NULL,
    PRIMARY KEY (cus_id)
);

CREATE OR replace TABLE delivary_method (
    del_method_id INTEGER NOT NULL AUTO_INCREMENT,
    aditional_price FLOAT NOT NULL,
    name_of_method VARCHAR(10) NOT NULL,
    time_for_del VARCHAR(10) NOT NULL,
    PRIMARY KEY (del_method_id)
);

CREATE OR Replace TABLE Payment (
    payment_id INTEGER NOT NULL AUTO_INCREMENT,
    pay_method VARCHAR(100) NOT NULL,
    PRIMARY KEY (payment_id)
);

CREATE OR replace TABLE delivery_company (
    emp_no INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    phone_no VARCHAR(16) NOT NULL,
    PRIMARY KEY (emp_no)
);

CREATE OR replace TABLE Discount (
    disc_id INTEGER NOT NULL AUTO_INCREMENT,
    dis_amount NUMERIC(28) NOT NULL,
    sum_to_get DECIMAL(10,2) NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (disc_id),
    UNIQUE (disc_id)
);

CREATE OR replace TABLE Type_ (
    type_id INTEGER NOT NULL AUTO_INCREMENT,
    type_name VARCHAR(100) NOT NULL,
    Category_category_id INTEGER NOT NULL,
    PRIMARY KEY (type_id),
    FOREIGN KEY (Category_category_id) REFERENCES Category(category_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE OR replace TABLE Instrument (
    Inst_id INTEGER NOT NULL AUTO_INCREMENT,
    price DECIMAL(10,2) NOT NULL,
    ins_name VARCHAR(255) NOT NULL,
    amount_on_store NUMERIC(28) NOT NULL,
    brand_brand_id INTEGER NOT NULL,
    Type_type_id INTEGER NOT NULL,
    PRIMARY KEY (Inst_id),
    FOREIGN KEY (brand_brand_id) REFERENCES brand(brand_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (Type_type_id) REFERENCES Type_(type_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE OR replace TABLE SaleOrder (
    sale_id INTEGER NOT NULL AUTO_INCREMENT,
    Sale_date DATETIME NOT NULL,
    Instrument_Inst_id INTEGER NOT NULL,
    date_s DATE NOT NULL,
    time_s DATETIME NOT NULL,
    total_price BIT NOT NULL,
    Payment_payment_id INTEGER NOT NULL,
    Customer_cus_id INTEGER NOT NULL,
    PRIMARY KEY (sale_id),
    FOREIGN KEY (Instrument_Inst_id) REFERENCES Instrument(Inst_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (Payment_payment_id) REFERENCES Payment(payment_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (Customer_cus_id) REFERENCES Customer(cus_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE OR replace TABLE SaleInstr (
    transaction_id INTEGER NOT NULL AUTO_INCREMENT,
    amount INTEGER NOT NULL,
    SaleOrder_sale_id INTEGER NOT NULL,
    Instrument_Inst_id INTEGER NOT NULL,
    total_price BIT NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (Instrument_Inst_id) REFERENCES Instrument(Inst_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (SaleOrder_sale_id) REFERENCES SaleOrder(sale_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE OR replace TABLE Delivery (
    delivary_id INTEGER NOT NULL AUTO_INCREMENT,
    delivery_adress VARCHAR(40) NOT NULL,
    delivary_status VARCHAR(10) NOT NULL,
    SaleOrder_sale_id INTEGER NOT NULL,
    delivary_method_del_method_id INTEGER NOT NULL,
    delivery_company_emp_no INTEGER NOT NULL,
    emp_no INTEGER NOT NULL,
    PRIMARY KEY (delivary_id),
    FOREIGN KEY (delivary_method_del_method_id) REFERENCES delivary_method(del_method_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (delivery_company_emp_no) REFERENCES delivery_company(emp_no) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (SaleOrder_sale_id) REFERENCES SaleOrder(sale_id) ON DELETE NO ACTION ON UPDATE NO ACTION
); 
