from flask import render_template, Flask, request, redirect, url_for
import psycopg2

test = Flask(__name__)

def connect_to_db():
    con = psycopg2.connect(
        dbname = 'тут должно быть написано ваше название',
        user = 'postgres',
        password = 'тут должен быть написан ваш пароль',
        host = 'localhost',
        port = '5432',
    )
    return con

# Функция для получения данных о продуктах из базы данных PostgreSQL
def get_products_from_db():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()
            cur.close()
            conn.close()
            return products
        except psycopg2.Error as e:
            print("Error fetching data from PostgreSQL:", e)
            return []
    else:
        return []

@test.route('/')
def index():
    return render_template('main4.html')

@test.route('/products')
def products():
    products = get_products_from_db()
    return render_template('products.html', products=products)

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
                product_id = request.form['productId']
                phone_number = request.form['phoneNumber']

                # Получаем информацию о товаре из базы данных
                conn = connect_to_db()
                if conn:
                    cur = conn.cursor()
                    cur.execute("SELECT type, price FROM products WHERE product_id = %s", (product_id,))
                    product_info = cur.fetchone()
                    
                    if product_info:
                        price = product_info[0]  # Поскольку в кортеже только один элемент
                        type = ''  # Здесь вы можете указать тип продукта, если у вас есть такая информация
                    else:
                        return "Error: Product information not found."

                # Вставляем данные заказа в таблицу "orders"
                cur.execute("INSERT INTO orders (product_id, phone_number, type, price) VALUES (%s, %s, %s, %s) RETURNING order_id",
                            (product_id, phone_number, product_info[0], product_info[1]))
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