DELIMITER //

CREATE TRIGGER before_insert_saleinstr
BEFORE INSERT ON SaleInstr
FOR EACH ROW
BEGIN
    DECLARE instrument_price DECIMAL(10,2);
    
    -- Get the price of the instrument
    SELECT price INTO instrument_price FROM Instrument WHERE Inst_id = NEW.Inst_id;
    
    -- Calculate the total price
    SET NEW.total_price = NEW.amount * instrument_price;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_insert_saleinstr_update_inventory
BEFORE INSERT ON SaleInstr
FOR EACH ROW
BEGIN
    DECLARE available_amount INTEGER;

    -- Get the current amount on store for the instrument
    SELECT amount_on_store INTO available_amount FROM Instrument WHERE Inst_id = NEW.Inst_id;
    
    -- Check if there is enough stock
    IF available_amount < NEW.amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough stock for this instrument';
    ELSE
        -- Subtract the amount being purchased from the stock
        UPDATE Instrument
        SET amount_on_store = amount_on_store - NEW.amount
        WHERE Inst_id = NEW.Inst_id;
        
        -- Calculate the total price
        SET NEW.total_price = NEW.amount * (SELECT price FROM Instrument WHERE Inst_id = NEW.Inst_id);
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_insert_update_total_price
BEFORE INSERT ON SaleOrder
FOR EACH ROW
BEGIN
    DECLARE total DOUBLE(10,2);
    DECLARE discountr DOUBLE(3,3);
    DECLARE customer_disc_id INTEGER; -- Declare variable here
    
    -- Calculate total price from SaleInstr table for the given tran_id
    SELECT SUM(total_price) INTO total FROM SaleInstr WHERE tran_id = NEW.tran_id;
    
    -- Get disc_id from Customer table for the given cus_id
    SELECT disc_id INTO customer_disc_id FROM Customer WHERE cus_id = NEW.cus_id;
    
    -- Get discount amount from Discount table based on the disc_id obtained from the Customer table
    SELECT dis_amount INTO discountr FROM Discount WHERE disc_id = customer_disc_id;
    
    -- Calculate final total price after discount
    IF discountr IS NOT NULL THEN
        SET NEW.total_price = total - (total * discountr);
    ELSE
        SET NEW.total_price = total;
    END IF;
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER update_customer_discount
AFTER INSERT ON SaleOrder
FOR EACH ROW
BEGIN
    DECLARE total_spent DECIMAL(10, 2);
    DECLARE new_disc_id INTEGER;
    
    -- Calculate the total spending of the customer
    SELECT SUM(total_price) INTO total_spent
    FROM SaleOrder
    WHERE cus_id = NEW.cus_id;
    
    -- Determine the appropriate discount level
    IF total_spent >= (
        SELECT MAX(sum_to_get)
        FROM Discount
    ) THEN
        SET new_disc_id = (
            SELECT disc_id
            FROM Discount
            WHERE sum_to_get = (
                SELECT MAX(sum_to_get)
                FROM Discount
            )
        );
    ELSE
        SET new_disc_id = (
            SELECT disc_id
            FROM Discount
            WHERE sum_to_get <= total_spent
            ORDER BY sum_to_get DESC
            LIMIT 1
        );
    END IF;
    
    -- Update the Customer table with the new discount level
    UPDATE Customer
    SET disc_id = new_disc_id
    WHERE cus_id = NEW.cus_id;
END //

DELIMITER ;
