from flask import Flask, render_template, redirect, url_for, request, session
import mysql.connector

# check user login
def valid_input(user, pw):
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor()
    first_part = "select username, password from user where username = %s and password = %s"
    second_part = (user, pw)
    cursor.execute(first_part,second_part)
    cursor.fetchall()
    if cursor.rowcount == 0:
        result = False
    else: result = True
    cursor.close()
    connection.close()
    return result

# check user signup new account: username and password is not empty, username must be unquie
def signUp(user, pw):
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor()
    cursor.execute("select * from user where username = %s", (user,))
    if len(cursor.fetchall()) == 0 and user and pw:
        first_part = "insert into user (username, password) values (%s, %s)"
        second_part = (user, pw)
        cursor.execute(first_part,second_part)
        connection.commit()
        cursor.close()
        connection.close()
    else:
        cursor.close()
        connection.close()
        return True


# visual product from database of an user
# username ==> user_id
def user_id(username):
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor()
    cursor.execute('select user_id from user where username=%s', (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0]

# user_id ==> product_id
def product_id(user):
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor()
    cursor.execute("select user_id from user where username = %s", (user,))
    user_id = cursor.fetchone()
    cursor.execute("select product_id from user_cart where user_id = %s", user_id)
    products_list = cursor.fetchall()
    cursor.close()
    connection.close()
    return products_list

# product_id ==> product infomation
def product_info(product_id):
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from product where product_id = %s", product_id)
    products = cursor.fetchone()
    cursor.close()
    connection.close()
    return products

# user ==> product
def user_product(user):
    products_list = product_id(user)
    result = list()
    for product in products_list:
        result.append(product_info(product))
    return result

# add product to shopping cart of an user
def add_product(user, product_id):# input: list of str(product_Id)
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor()
    cursor.executemany("insert into user_cart values (%s, %s)", [(user, x) for x in product_id])
    connection.commit()
    cursor.close()
    connection.close()

# remove product from shopping cart of an user
def remove_product(product_id):# input: list of str(product_Id)
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor()
    cursor.executemany("delete from user_cart where product_id=%s", [(x,) for x in product_id]) #execute must handle on interable obj and element of that obj that be list, tuple or dictionaty
    connection.commit()
    cursor.close()
    connection.close()

app = Flask(__name__)
app.secret_key = b'Vumanhquang1' #for using session

# root page
@app.route('/')
def index():
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from product")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', product_tests = products)

# login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user-login.html')
    else:
        if valid_input(request.form['username'], request.form['password']):
            session['username'] = request.form.get('username')
            return redirect(url_for('Home'))
        else:
            return render_template('user-login.html', error = True)

# signup
@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('user-signup.html')
    else:
        error = signUp(request.form['username'], request.form['password'])
        if error:
            return render_template('user-signup.html', error = error)
        else:         
            return render_template('user-signup.html', signup = True)
    

#user home 
@app.route('/home/')
def Home():
    if session.get('username'):
        connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from product")
        products = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('user.html', user = session.get('username'), product_tests = products)
    else:
        return redirect(url_for('index'))

# method for add product of an user
@app.post('/home/')
def add_pro():
    add_product(user_id(session.get('username')), request.form.getlist('product'))
    return redirect(url_for('Home'))

# user cart
@app.route('/user-cart/')
def cart():
    if session.get('username'):
        products = user_product(session.get('username'))
        return render_template('user-cart.html', user = session.get('username'), product_tests = products)
    else:
        return redirect(url_for('index'))

# method for remove product of an user
@app.post('/user-cart/')
def remove_pro():
    remove_product(request.form.getlist('product'))
    return redirect(url_for('cart'))

# logout
@app.route('/logout/')
def logout():
    session.pop('username')
    return redirect(url_for('index'))



# test làm đường link chi tiết cho sản phẩm
@app.route('/<product>')
def product_view(product):
    product_inf = product_info((product,))
    return render_template('product_detail.html', product = product_inf)



if __name__ == '__main__':
    app.run(debug=True)
    
    
    #test