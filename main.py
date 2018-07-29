from flask import Flask, render_template, url_for, redirect
from flask import request
from flask_mysqldb import MySQL
from flask import make_response
from raven.contrib.flask import Sentry
from flask import Flask, flash, redirect, request, session, abort
import os
import form
import RegistroVendedor
from io import BytesIO
from flask import make_response
from reportlab.pdfgen import canvas

app = Flask(__name__)

sentry = Sentry(app, dsn='https://34b4dd07263949959a499ac3a98ea9d2:bba044ffa89544af98017e588e66e975@sentry.io/1210257')

ADMINS = ['exceptionappweb@gmail.com']
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'exceptionappweb@gmail.com',
                               ADMINS, 'Error en la aplicaion')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pedro0319'
app.config['MYSQL_DB'] = 'CopiaAmazon'
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Vendedor")
    rv = cur.fetchall()
    cur.close()
    return render_template('home.html', Vendedor=rv)

@app.route('/Inicio', methods = ['GET', 'POST'])
def Inicio():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Vendedor")
    rv = cur.fetchall()
    cur.close()
    return render_template('home.html', Vendedor=rv)

@app.route('/InicioVendedor', methods = ['GET', 'POST'])
def InicioVendedor():  
    idVendedor = request.cookies.get('idVendedorReg')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Vendedor WHERE id=%s", (idVendedor,))
    rv = cur.fetchall()
    cur.close()
    return render_template('InicioVendedor.html', Vendedor=rv)  

@app.route('/decision', methods = ['GET', 'POST'])
def decision():
    return render_template('prelogin.html')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    comment_form = RegistroVendedor.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():  
        strRazonSocial = request.form['strRazonSocial']
        strRFC = request.form['strRFC']
        strTelefono = request.form['strTelefono']
        strCorreo = request.form['strCorreo']
        strDireccion =request.form['strDireccion']
        strSitioWeb =request.form['strSitioWeb']
        strContraseña =request.form['strContraseña']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Vendedor (strRazonSocial,strRFC,strTelefono,strCorreo,strDireccion,strSitioWeb) VALUES (%s,%s,%s,%s,%s,%s) ",
            (strRazonSocial,strRFC,strTelefono,strCorreo,strDireccion,strSitioWeb))
        mysql.connection.commit() 

        cur.close()
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM Vendedor WHERE strRFC=%s", (strRFC,))
        rv = cur1.fetchall()
        cur1.close()
        idVendedor = rv[0]
        idven = idVendedor[0]
        valor = ''
        valor +=str(idven)
                    

        cur2 = mysql.connection.cursor()
        cur2.execute("INSERT INTO Usuario (strCorreo,strContraseña,idVendedor) VALUES (%s,%s,%s) ",
            (strCorreo,strContraseña,idven))
        mysql.connection.commit() 
        cur2.close()
        response = make_response(redirect(url_for('InicioVendedor')))
        response.set_cookie('idVendedorReg',valor)
        return response

    title = "APP Python"     
    return render_template('RegistroVen.html',title = title, RegistroVendedor = comment_form)

@app.route('/log', methods = ['GET', 'POST'])
def log():
    return render_template('loginDes.html')
 
@app.route('/InicioSecion', methods = ['GET', 'POST'])
def InicioSecion():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        cur = mysql.connection.cursor()
        idVendedor = request.cookies.get('idVendedorReg')
        cur.execute("SELECT * FROM Vendedor WHERE id=%s", (idVendedor,))
        rv = cur.fetchall()
        cur.close()
        return render_template('InicioVendedor.html', Vendedor=rv)

@app.route('/login', methods=['POST'])
def do_admin_login():
    usuario = request.form['username']
    contrasena = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuario WHERE strCorreo=%s and strContraseña=%s ", (usuario,contrasena,))
    rv = cur.fetchall()
    cur.close()
    if rv:  
        session['logged_in'] = True
        idVendedor = rv[0]
        idven = idVendedor[3]
        valor = ''
        valor +=str(idven)
    else:       
        valor = '0'
        session['logged_in'] = False

    response = make_response(redirect(url_for('InicioSecion')))
    response.set_cookie('idVendedorReg',valor)    
    return response

@app.route("/logout")
def logout():
    session['logged_in'] = False
    valor = '0'
    response = make_response(redirect(url_for('index')))
    response.set_cookie('idVendedorReg',valor)
    return response


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
