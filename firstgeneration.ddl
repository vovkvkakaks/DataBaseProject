-- Generated by Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   at:        2024-05-28 20:54:14 CEST
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE brand (
    brand_id      INTEGER NOT NULL,
    name_of_brand VARCHAR2(20) NOT NULL,
    rating        NUMBER NOT NULL
);

ALTER TABLE brand ADD CONSTRAINT brand_pk PRIMARY KEY ( brand_id );

CREATE TABLE category (
    category_id INTEGER NOT NULL,
    categ_name  VARCHAR2(20) NOT NULL
);

ALTER TABLE category ADD CONSTRAINT category_pk PRIMARY KEY ( category_id );

CREATE TABLE customer (
    cus_id           INTEGER NOT NULL,
    name             VARCHAR2(100) NOT NULL,
    surname          VARCHAR2(100) NOT NULL,
    phone_no         VARCHAR2(100) NOT NULL,
    adress           VARCHAR2(100) NOT NULL,
    buying_no        NVARCHAR2(10) NOT NULL,
    discount_disc_id INTEGER NOT NULL,
    disc_id          INTEGER NOT NULL
);

ALTER TABLE customer ADD CONSTRAINT customer_pk PRIMARY KEY ( cus_id );

CREATE TABLE delivary_method (
    del_method_id   NUMBER NOT NULL,
    aditional_price CHAR(1) NOT NULL,
    name_of_method  VARCHAR2(10) NOT NULL,
    time_for_del    VARCHAR2(10) NOT NULL
);

ALTER TABLE delivary_method ADD CONSTRAINT delivary_method_pk PRIMARY KEY ( del_method_id );

CREATE TABLE delivery (
    delivary_id                   INTEGER NOT NULL,
    delivery_adress               VARCHAR2(40) NOT NULL,
    delivary_status               VARCHAR2(10) NOT NULL,
    saleorder_sale_id             INTEGER NOT NULL,
    delivary_method_del_method_id NUMBER NOT NULL,
    delivery_company_emp_no       INTEGER NOT NULL,
    emp_no                        INTEGER NOT NULL
);

ALTER TABLE delivery ADD CONSTRAINT delivery_pk PRIMARY KEY ( delivary_id );

CREATE TABLE delivery_company (
    emp_no   INTEGER NOT NULL,
    name     VARCHAR2(20) NOT NULL,
    surname  VARCHAR2(20) NOT NULL,
    phone_no VARCHAR2(16) NOT NULL
);

ALTER TABLE delivery_company ADD CONSTRAINT delivery_company_pk PRIMARY KEY ( emp_no );

CREATE TABLE discount (
    disc_id    INTEGER NOT NULL,
    dis_amount NUMBER NOT NULL,
    sum_to_get NUMBER(10, 2) NOT NULL,
    name       VARCHAR2(100) NOT NULL
);

ALTER TABLE discount ADD CONSTRAINT discount_pkv1 PRIMARY KEY ( disc_id );

CREATE TABLE instrument (
    inst_id         INTEGER NOT NULL,
    price           NUMBER(10, 2) NOT NULL,
    ins_name        VARCHAR2(255) NOT NULL,
    amount_on_store NUMBER NOT NULL,
    brand_brand_id  INTEGER NOT NULL,
    type_type_id    INTEGER NOT NULL
);

ALTER TABLE instrument ADD CONSTRAINT instrument_pk PRIMARY KEY ( inst_id );

CREATE TABLE payment (
    payment_id INTEGER NOT NULL,
    pay_method VARCHAR2(100) NOT NULL
);

ALTER TABLE payment ADD CONSTRAINT payment_pk PRIMARY KEY ( payment_id );

CREATE TABLE saleinstr (
    transaction_id     INTEGER NOT NULL,
    amount             INTEGER NOT NULL,
    saleorder_sale_id  INTEGER NOT NULL,
    instrument_inst_id INTEGER NOT NULL,
    total_price        CHAR(1) NOT NULL
);

ALTER TABLE saleinstr ADD CONSTRAINT saleinstr_pk PRIMARY KEY ( transaction_id );

CREATE TABLE saleorder (
    sale_id            INTEGER NOT NULL,
    sale_date          DATE NOT NULL,
    instrument_inst_id INTEGER NOT NULL,
    date_s             DATE NOT NULL,
    time_s             DATE NOT NULL,
    total_price        CHAR(1) NOT NULL,
    payment_payment_id INTEGER NOT NULL,
    customer_cus_id    INTEGER NOT NULL
);

ALTER TABLE saleorder ADD CONSTRAINT sale_pk PRIMARY KEY ( sale_id );

CREATE TABLE type (
    type_id              INTEGER NOT NULL,
    type_name            VARCHAR2(100) NOT NULL,
    category_category_id INTEGER NOT NULL
);

ALTER TABLE type ADD CONSTRAINT type_pk PRIMARY KEY ( type_id );

ALTER TABLE delivery
    ADD CONSTRAINT delivery_delivary_method_fk FOREIGN KEY ( delivary_method_del_method_id )
        REFERENCES delivary_method ( del_method_id );

ALTER TABLE delivery
    ADD CONSTRAINT delivery_delivery_company_fk FOREIGN KEY ( delivery_company_emp_no )
        REFERENCES delivery_company ( emp_no );

ALTER TABLE delivery
    ADD CONSTRAINT delivery_saleorder_fk FOREIGN KEY ( saleorder_sale_id )
        REFERENCES saleorder ( sale_id );

ALTER TABLE instrument
    ADD CONSTRAINT instrument_brand_fk FOREIGN KEY ( brand_brand_id )
        REFERENCES brand ( brand_id );

ALTER TABLE instrument
    ADD CONSTRAINT instrument_type_fk FOREIGN KEY ( type_type_id )
        REFERENCES type ( type_id );

ALTER TABLE saleorder
    ADD CONSTRAINT sale_instrument_fk FOREIGN KEY ( instrument_inst_id )
        REFERENCES instrument ( inst_id );

ALTER TABLE saleinstr
    ADD CONSTRAINT saleinstr_instrument_fk FOREIGN KEY ( instrument_inst_id )
        REFERENCES instrument ( inst_id );

ALTER TABLE saleinstr
    ADD CONSTRAINT saleinstr_saleorder_fk FOREIGN KEY ( saleorder_sale_id )
        REFERENCES saleorder ( sale_id );

ALTER TABLE saleorder
    ADD CONSTRAINT saleorder_customer_fk FOREIGN KEY ( customer_cus_id )
        REFERENCES customer ( cus_id );

ALTER TABLE saleorder
    ADD CONSTRAINT saleorder_payment_fk FOREIGN KEY ( payment_payment_id )
        REFERENCES payment ( payment_id );

ALTER TABLE type
    ADD CONSTRAINT type_category_fk FOREIGN KEY ( category_category_id )
        REFERENCES category ( category_id );



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                            12
-- CREATE INDEX                             0
-- ALTER TABLE                             23
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
