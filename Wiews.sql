CREATE VIEW CustomerTotalSpending AS
SELECT c.name_ AS customer_name,
       c.surname AS customer_surname,
       c.cus_id AS customer_id,
       SUM(so.total_price) AS total_spent
FROM Customer c
JOIN SaleOrder so ON c.cus_id = so.cus_id
GROUP BY c.cus_id;

CREATE OR REPLACE VIEW InstrumentSalesRanking AS
SELECT
    i.Inst_id,
    i.ins_name,
    COALESCE(SUM(s.amount), 0) AS total_amount_sold,
    RANK() OVER (ORDER BY COALESCE(SUM(s.amount), 0) DESC) AS sales_rank
FROM
    Instrument i
LEFT JOIN
    SaleInstr s ON i.Inst_id = s.Inst_id
GROUP BY
    i.Inst_id,
    i.ins_name;

