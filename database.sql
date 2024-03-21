CREATE TABLE products(
	product_id SERIAL PRIMARY KEY,
	type text NOT NULL,
	price int NOT NULL
);

CREATE TABLE orders(
	order_id SERIAL PRIMARY KEY,
	product_id int REFERENCES products(product_id),
	phone_number varchar(20) NOT NULL,
	type text NOT NULL,
	price int NOt NULL
);