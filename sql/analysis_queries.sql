
USE ecommerce_db;


-- =====================================================
-- 1. DATABASE STRUCTURE
-- =====================================================

SHOW CREATE TABLE orders;


-- =====================================================
-- 2. ORDER STATUS ANALYSIS
-- =====================================================

-- Task 1: Total orders by order status

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- Task 2: Total orders by payment status

SELECT
    payment_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY payment_status
ORDER BY total_orders DESC;


-- Task 3: Order counts by payment and order status

SELECT
    payment_status,
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY payment_status, order_status
ORDER BY payment_status, total_orders DESC;


-- =====================================================
-- 3. REVENUE ANALYSIS
-- =====================================================

-- Task 4: Total order value for paid, completed orders

SELECT
    ROUND(
        SUM(quantity * unit_price * (1 - discount_pct)),
        2
    ) AS total_order_value
FROM orders
WHERE payment_status = 'Paid'
  AND order_status = 'Completed';


-- Task 5: Revenue by region

SELECT
    region,
    ROUND(
        SUM(quantity * unit_price * (1 - discount_pct)),
        2
    ) AS total_order_value
FROM orders
WHERE payment_status = 'Paid'
  AND order_status = 'Completed'
GROUP BY region
ORDER BY total_order_value DESC;


-- Task 6: Revenue and order counts by sales channel

SELECT
    channel,
    COUNT(*) AS total_orders,
    ROUND(
        SUM(quantity * unit_price * (1 - discount_pct)),
        2
    ) AS total_order_value
FROM orders
WHERE payment_status = 'Paid'
  AND order_status = 'Completed'
GROUP BY channel
ORDER BY total_order_value DESC;


-- Task 7: Average order value by sales channel

SELECT
    channel,
    COUNT(*) AS total_orders,
    ROUND(
        SUM(quantity * unit_price * (1 - discount_pct))
        / COUNT(*),
        2
    ) AS average_order_value
FROM orders
WHERE payment_status = 'Paid'
  AND order_status = 'Completed'
GROUP BY channel
ORDER BY average_order_value DESC;


-- Task 8: Order value by order status

SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(
        SUM(quantity * unit_price * (1 - discount_pct)),
        2
    ) AS total_order_value
FROM orders
GROUP BY order_status
ORDER BY total_order_value DESC;


-- =====================================================
-- 4. PRODUCT ANALYSIS
-- =====================================================

-- Task 9: Top 10 products by order value

SELECT
    product_id,
    SUM(quantity) AS total_quantity_sold,
    ROUND(
        SUM(quantity * unit_price * (1 - discount_pct)),
        2
    ) AS total_order_value
FROM orders
WHERE payment_status = 'Paid'
  AND order_status = 'Completed'
GROUP BY product_id
ORDER BY total_order_value DESC
LIMIT 10;


-- =====================================================
-- 5. CUSTOMER ANALYSIS
-- =====================================================

-- Task 10: Top 10 customers by total order value

SELECT
    customer_id,
    COUNT(*) AS total_orders,
    ROUND(
        SUM(quantity * unit_price * (1 - discount_pct)),
        2
    ) AS total_order_value
FROM orders
WHERE payment_status = 'Paid'
  AND order_status = 'Completed'
GROUP BY customer_id
ORDER BY total_order_value DESC
LIMIT 10;


-- Task 11: Number of unique customers

SELECT
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;


-- Task 12: Customers with at least two paid, completed orders

SELECT
    customer_id,
    COUNT(*) AS total_orders,
    ROUND(
        AVG(quantity * unit_price * (1 - discount_pct)),
        2
    ) AS average_order_value
FROM orders
WHERE payment_status = 'Paid'
  AND order_status = 'Completed'
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY average_order_value DESC
LIMIT 10;


-- =====================================================
-- 6. BUSINESS PERFORMANCE METRICS
-- =====================================================

-- Task 13: Order completion rate

SELECT
    COUNT(*) AS total_orders,
    SUM(
        CASE
            WHEN order_status = 'Completed' THEN 1
            ELSE 0
        END
    ) AS completed_orders,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN order_status = 'Completed' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS completion_rate_pct
FROM orders;


-- Task 14: Order return rate

SELECT
    COUNT(*) AS total_orders,
    SUM(
        CASE
            WHEN order_status = 'Returned' THEN 1
            ELSE 0
        END
    ) AS returned_orders,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN order_status = 'Returned' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS return_rate_pct
FROM orders;


-- Task 15: Percentage of orders by payment status

SELECT
    payment_status,
    COUNT(*) AS total_orders,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS percentage
FROM orders
GROUP BY payment_status
ORDER BY percentage DESC;


-- =====================================================
-- 7. DATA QUALITY VALIDATION
-- =====================================================

-- Task 16: Check for duplicate order IDs
-- Expected result: no rows

SELECT
    order_id,
    COUNT(*) AS occurrences
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;


-- Task 17: Check for invalid quantities or prices
-- Expected result: invalid_orders = 0

SELECT
    COUNT(*) AS invalid_orders
FROM orders
WHERE quantity <= 0
   OR unit_price <= 0
   OR quantity IS NULL
   OR unit_price IS NULL;


-- Task 18: Check for invalid discounts
-- Expected result: invalid_discounts = 0

SELECT
    COUNT(*) AS invalid_discounts
FROM orders
WHERE discount_pct < 0
   OR discount_pct > 1
   OR discount_pct IS NULL;


-- Task 19: Check for missing required values

SELECT
    SUM(order_id IS NULL) AS missing_order_ids,
    SUM(order_date IS NULL) AS missing_order_dates,
    SUM(customer_id IS NULL) AS missing_customer_ids,
    SUM(product_id IS NULL) AS missing_product_ids
FROM orders;


-- =====================================================
-- 8. FINAL DATABASE VERIFICATION
-- =====================================================

-- Expected result: 10020 total rows and 10020 unique IDs

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_order_ids
FROM orders;
