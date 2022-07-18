import mysql.connector

# creat database
connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1')
cursor = connection.cursor()
cursor.execute('create database if not exists shopee')
cursor.execute('use shopee')

# creat table
def creat_table(table, content):
    connection = mysql.connector.connect(host='localhost', user='Quang', password='Vumanhquang1', database='shopee')
    cursor = connection.cursor()
    cursor.execute(content)
    cursor.close()
    connection.close()
    print('creat table %s successfully' %table)

# user table
creat_table('user', '''create table if not exists user (
                user_Id int unsigned auto_increment, 
                username char(255) not null, 
                password char(255) not null, 
                PRIMARY KEY (user_Id)
                )''')

# Product table
creat_table('product', '''create table if not exists product (
                product_Id int unsigned auto_increment, 
                prod_name char(255) not null, 
                old_price int unsigned not null, 
                new_price int unsigned not null, 
                sold_quantity int unsigned not null, 
                vendor char(255) not null, 
                country char(255) not null, 
                image char(255) not null, 
                PRIMARY KEY (product_Id)
                )''')

# user product table
creat_table('user_cart', '''create table if not exists user_cart (
                user_Id int unsigned not null, 
                product_Id int unsigned not null, 
                FOREIGN KEY (user_Id) REFERENCES user(user_Id)
                )''')
                
# add some product info to test
for i in range(10):
    print(i)
    cursor.execute('''insert into product (prod_name, old_price, new_price, sold_quantity, vendor, country, image) values (
                'Set dưỡng trắng Whoo  đông y hoàng cung  Gong Jinh Yang Seol Radiant',
                1200000, 
                999000,
                123, 
                'Apple', 
                'Vietnam', 
                'https://cf.shopee.vn/file/c3369cf5d98244b025b5a837bf274447'
                )''')
    connection.commit()

cursor.close()               
connection.close()