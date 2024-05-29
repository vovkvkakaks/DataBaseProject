CREATE OR replace TABLE brand (
    brand_id INTEGER NOT NULL AUTO_INCREMENT,
    name_of_brand VARCHAR(20) NOT NULL,
    rating NUMERIC(20) NOT NULL,
    PRIMARY KEY (brand_id)
);

CREATE OR replace TABLE Category (
    category_id INTEGER NOT NULL AUTO_INCREMENT,
    categ_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (category_id)
);



CREATE OR replace TABLE delivery_method (
    del_method_id INTEGER NOT NULL AUTO_INCREMENT,
    aditional_price DOUBLE(10,2) NOT NULL,
    name_ VARCHAR(10) NOT NULL,
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
    name_ VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    phone_no VARCHAR(16) NOT NULL,
    PRIMARY KEY (emp_no)
);

CREATE OR replace TABLE Discount (
    disc_id INTEGER NOT NULL AUTO_INCREMENT,
    dis_amount DOUBLE(3,3) NOT NULL,
    sum_to_get DOUBLE(10,2) NOT NULL,
    name_ VARCHAR(100) NOT NULL,
    PRIMARY KEY (disc_id)
);

CREATE OR replace TABLE Customer (
    cus_id INTEGER NOT NULL AUTO_INCREMENT,
    name_ VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    phone_no VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    disc_id INTEGER NOT NULL,
    PRIMARY KEY (cus_id),
    FOREIGN KEY (disc_id) REFERENCES discount(disc_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE OR replace TABLE Type_ (
    type_id INTEGER NOT NULL AUTO_INCREMENT,
    type_name VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (type_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE OR replace TABLE Instrument (
    Inst_id INTEGER NOT NULL AUTO_INCREMENT,
    price DECIMAL(10,2) NOT NULL,
    ins_name VARCHAR(255) NOT NULL,
    amount_on_store INTEGER(5) NOT NULL,
    brand_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    PRIMARY KEY (Inst_id, ins_name),
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (type_id) REFERENCES Type_(type_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE OR replace TABLE SaleInstr (
    tran_id INTEGER NOT NULL Auto_increment ,
    amount INTEGER NOT NULL,
    Inst_id INTEGER NOT NULL,
    total_price DOUBLE(10,2) NOT NULL,
    PRIMARY KEY (tran_id,Inst_id),
    FOREIGN KEY (Inst_id) REFERENCES Instrument(Inst_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE OR replace TABLE SaleOrder (
    sale_id INTEGER NOT NULL AUTO_INCREMENT,
    tran_id INTEGER NOT NULL,
    date_s DATE NOT NULL,
    time_s TIME NOT NULL,
    total_price DOUBLE(10,2) ,
    payment_id INTEGER NOT NULL,
    cus_id INTEGER NOT NULL,
    PRIMARY KEY (sale_id),
    FOREIGN KEY (tran_id) REFERENCES SaleInstr(tran_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (payment_id) REFERENCES Payment(payment_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (cus_id) REFERENCES Customer(cus_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);



CREATE OR replace TABLE Delivery (
    delivary_id INTEGER NOT NULL AUTO_INCREMENT,
    delivery_adres VARCHAR(40) NOT NULL,
    delivery_status VARCHAR(10) NOT NULL,
    sale_id INTEGER NOT NULL,
    del_method_id INTEGER NOT NULL,
    emp_no INTEGER NOT NULL,
    PRIMARY KEY (delivary_id),
    FOREIGN KEY (del_method_id) REFERENCES delivery_method(del_method_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (emp_no) REFERENCES delivery_company(emp_no) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (sale_id) REFERENCES SaleOrder(sale_id) ON DELETE NO ACTION ON UPDATE NO ACTION
); 

ALTER TABLE SaleOrder ADD CONSTRAINT unique_tran_id UNIQUE (tran_id);
