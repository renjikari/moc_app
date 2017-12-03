# coding:utf-8
import os, base64, hashlib
from flask import Flask, request, render_template, redirect, url_for, abort, make_response, send_from_directory
import MySQLdb.cursors
app = Flask(__name__)


def db_connect():
    """
    DB接続して、MySQLコネクションオブジェクトを返す
    :return: MySQLConnection
    """
    host = os.getenv('MYSQL_DATABASE_HOST', 'database')
    port = os.getenv('MYSQL_DATABASE_PORT', 3306)
    user = os.getenv('MYSQL_DATABASE_USER', 'root')
    passwd = os.getenv('MYSQL_DATABASE_PASSWORD', '')
    db = os.getenv('MYSQL_DATABASE_DB', 'management_ipaddress')

    request.db = MySQLdb.connect(**{
        'host': host,
        'port': port,
        'user': user,
        'passwd': passwd,
        'db': db,
        'charset': 'utf8mb4',
        'cursorclass': MySQLdb.cursors.DictCursor,
    })
    return request.db


@app.route('/')
def redirect_login():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')

# セッション機能は作ってない
@app.route('/login', methods=['POST'] )
def login_post():
    db = db_connect()
    cur = db.cursor() 
    
    # loginする人
    if request.form.getlist('login-submit'):
        username = request.form['username']
        encode_password = request.form['password'].encode('utf-8')
        hash_password = hashlib.sha256(encode_password).hexdigest()

        sql = 'SELECT * FROM users WHERE username = %s'
        cur.execute(sql, (username,))
        user = cur.fetchall()

        if user and user[0]["password"] == hash_password: 
            return redirect(url_for('home'))

    # registerする人
    elif request.form.getlist('register-submit'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm-password']

        if password != confirm:
            return render_template('login.html')

        encode_password = password.encode('utf-8')
        hash_password = hashlib.sha256(encode_password).hexdigest()

        sql = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)'
        
        cur.execute(sql, (username, hash_password, email))
        db.commit()
        cur.close()
        db.close()

        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        db = db_connect()
        cur = db.cursor()
        ipaddress = request.form['ipaddress']
        subnet = request.form['subnet']
        hostname = request.form['hostname']
        fqdn = request.form['fqdn']
        description = request.form['description']
        sql = 'INSERT INTO ipaddress_list (ipaddress, subnet, hostname, fqdn, description, created_by) ' \
              'VALUES (INET_ATON(%s), %s, %s, %s, %s, %s)'
        
        cur.execute(sql, (ipaddress, subnet, hostname, fqdn, description, "fujiwara"))
        db.commit()
        cur.close()
        db.close()
        return redirect(url_for('home'))

    cur = db_connect().cursor()
    cur.execute("SELECT id, INET_NTOA(ipaddress), subnet, hostname, fqdn, description, created_by FROM ipaddress_list")
    ipaddress_list = cur.fetchall()
    return render_template('home.html', ipaddress_list=ipaddress_list)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
