CREATE VIEW CustomerTotalSpending AS
SELECT c.name_ AS customer_name,
       c.surname AS customer_surname,
       c.cus_id AS customer_id,
       SUM(so.total_price) AS total_spent
FROM Customer c
JOIN SaleOrder so ON c.cus_id = so.cus_id
GROUP BY c.cus_id;
