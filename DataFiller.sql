
INSERT INTO Category (categ_name) VALUES
('Strings'),
('Percussion'),
('Wind'),
('Keyboard');

-- Insert data into Type_ table
INSERT INTO Type_ (type_name, category_id) VALUES
('Acoustic Guitar', 1),
('Electric Guitar', 1),
('Drums', 2),
('Flute', 3),
('Piano', 4);

-- Insert data into Brand table
INSERT INTO Brand (name_of_brand, rating) VALUES
('Yamaha', 4.5),
('Fender', 4.7),
('Gibson', 4.8),
('Roland', 4.6),
('Kawai', 4.4);

-- Insert data into Instrument table

-- Insert data into Payment table
INSERT INTO Payment (pay_method) VALUES
('Credit Card'),
('PayPal'),
('Bank Transfer');

-- Insert additional data into Category table
INSERT INTO Category (categ_name) VALUES
('Brass'),
('Electronic'),
('Woodwind'),
('Folk'),
('Bowed Strings');

-- Insert additional data into Type_ table
INSERT INTO Type_ (type_name, category_id) VALUES
('Trumpet', 5),
('Synthesizer', 6),
('Clarinet', 7),
('Banjo', 8),
('Violin', 9);

-- Insert additional data into Brand table
INSERT INTO Brand (name_of_brand, rating) VALUES
('Bach', 4.6),
('Moog', 4.9),
('Buffet', 4.5),
('Deering', 4.7),
('Stradivarius', 5.0);

-- Insert additional data into Instrument table
INSERT INTO Instrument (price, ins_name, amount_on_store, brand_id, type_id) VALUES
(799.99, 'Yamaha Acoustic Guitar', 10, 1, 1),
(899.99, 'Fender Electric Guitar', 8, 2, 2),
(499.99, 'Roland Drums', 5, 4, 3),
(299.99, 'Yamaha Flute', 15, 1, 4),
(1599.99, 'Kawai Piano', 2, 5, 5),
(899.99, 'Bach Trumpet', 7, 6, 6),
(1199.99, 'Moog Synthesizer', 4, 7, 7),
(599.99, 'Buffet Clarinet', 12, 8, 8),
(799.99, 'Deering Banjo', 6, 9, 9),
(2999.99, 'Stradivarius Violin', 1, 10, 10);

-- Insert data into Discount table
INSERT INTO Discount (dis_amount, sum_to_get, name_) VALUES
(0.00, 0.00, 'Bronze Membership'),
(0.10, 1000.00, 'Silver Membership'),
(0.15, 1500.00, 'Gold Membership'),
(0.20, 3000.00, 'Platinum Membership'),
(0.25, 4500.00, 'Diamond Membership');

-- Insert data into Customer table
INSERT INTO Customer (name_, surname, phone_no, address, disc_id) VALUES
('John', 'Doe', '123-456-7890', '123 Main St, Springfield', 1),
('Jane', 'Smith', '234-567-8901', '456 Elm St, Springfield', 1),
('Michael', 'Johnson', '345-678-9012', '789 Oak St, Springfield', 1),
('Emily', 'Davis', '456-789-0123', '101 Maple St, Springfield', 1),
('David', 'Miller', '567-890-1234', '202 Pine St, Springfield', 1),
('Emma', 'Wilson', '678-901-2345', '303 Birch St, Springfield', 1),
('Daniel', 'Taylor', '789-012-3456', '404 Cedar St, Springfield', 1),
('Olivia', 'Anderson', '890-123-4567', '505 Walnut St, Springfield', 1),
('Matthew', 'Thomas', '901-234-5678', '606 Chestnut St, Springfield', 1),
('Sophia', 'Moore', '012-345-6789', '707 Ash St, Springfield', 1);

-- Insert data into SaleInstr table without specifying total_price
-- Insert data into SaleInstr table
-- Insert data into SaleInstr table
INSERT INTO SaleInstr (tran_id, amount, Inst_id) VALUES
(1, 2, 1),
(1, 1, 3),
(2, 1, 2),
(2, 1, 4),
(3, 1, 5),
(3, 2, 6),
(4, 1, 7),
(4, 2, 8),
(5, 1, 9),
(5, 1, 1),
(6, 2, 1),
(6, 1, 2),
(7, 1, 4),
(7, 1, 5);

INSERT INTO SaleOrder (tran_id, date_s, time_s, payment_id, cus_id) VALUES
(1, '2024-05-29', '10:00:00', 1, 1),
(2, '2024-05-29', '10:15:00', 2, 2),
(3, '2024-05-29', '10:30:00', 3, 3),
(4, '2024-05-29', '10:45:00', 1, 4),
(5, '2024-05-29', '11:00:00', 2, 5),
(6, '2024-05-29', '11:15:00', 3, 6),
(7, '2024-05-29', '11:30:00', 1, 7);


INSERT INTO delivery_company (name_, surname, phone_no) VALUES 
('John', 'Smith', '+1122334455'),
('Emily', 'Johnson', '+1987654321'),
('Michael', 'Williams', '+1357924680'),
('Sarah', 'Anderson', '+155509988'),
('David', 'Brown', '+1777888999'),
('Emma', 'Garcia', '+1666777888');

INSERT INTO delivery_method (aditional_price, name_, time_for_del)
VALUES 
    (5.00, 'Standard', '3-5 days'),
    (10.00, 'Express', '1-2 days'),
    (15.00, 'Inpost', '3 days');

INSERT INTO Delivery (delivery_adres, delivery_status, sale_id, del_method_id, emp_no) VALUES 
    ('123 Main St, Anytown, USA', 'In Transit', 1, 1, 1),
    ('456 Elm St, Othertown, USA', 'Pending', 2, 2, 2),
    ('789 Oak St, Anothertown, USA', 'Delivered', 3, 1, 3),
	 ('101 Pine St, Somewhereville, USA', 'Delivered', 4, 1, 4),
    ('202 Maple St, Anywhere City, USA', 'Pending', 5, 2, 5),
    ('303 Cedar St, Nowhere Town, USA', 'In Transit', 6, 1, 6);
