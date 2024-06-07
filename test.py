from flask import Flask, render_template, request, redirect, url_for
import psycopg2

test = Flask(__name__)

def connect_to_db():
    con = psycopg2.connect(
        dbname='database123',
        user='postgres',
        password='123srmax',
        host='localhost',
        port='5432',
    )
    return con

@test.route('/product')
def product():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('product.html', rows=rows)

@test.route('/')
def index():
    return render_template('main1.html')

@test.route('/purschaces/<int:product_id>')
def purschaces(product_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if product:
        return render_template('purschaces.html', product=product)
    else:
        return "Product not found", 404

@test.route('/success_order')
def success_order():
    return render_template('success_order.html')

@test.route('/contacts')
def contacts():
    return render_template('contacts.html')

@test.route('/submit_order', methods=['POST'])
def submit_order():
    if request.method == 'POST':
        try:
            conn = connect_to_db()
            if conn:
                cur = conn.cursor()
                product_id = request.form['product_id']
                address = request.form['address']
                phone_number = request.form['phone_number']
                card_number = request.form['card_number']
                expiry_date = request.form['expiry_date']
                cvv = request.form['cvv']

                # Get product information from the database
                cur.execute("SELECT model, price FROM products WHERE product_id = %s", (product_id,))
                product_info = cur.fetchone()
                
                if product_info:
                    product_type = product_info[0]
                    price = product_info[1]
                else:
                    return "Error: Product information not found."

                # Insert order data into the "orders" table, including post_date
                cur.execute(
                    "INSERT INTO orders (product_id, address, phone_number, card_number, expiry_date, cvv, name_of_product, price, post_date) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW()) RETURNING order_id",
                    (product_id, address, phone_number, card_number, expiry_date, cvv, product_type, price)
                )
                conn.commit()
                cur.close()
                conn.close()
                
                return redirect(url_for('success_order'))
            else:
                return "Error connecting to the database."
        except Exception as e:
            print("Error submitting order:", e)
            return "Error submitting order: " + str(e)
    else:
        return "Method not supported."

if __name__ == '__main__':
    test.run(debug=True)
