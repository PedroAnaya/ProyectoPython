from flask import Flask, render_template, url_for, redirect
from flask import request
from flask_mysqldb import MySQL
from flask import make_response
from raven.contrib.flask import Sentry
from flask import Flask, flash, redirect, request, session, abort
import os
import form
import RegistroVendedor
import RegistroCliente
import frmProductos
import compra
from io import BytesIO
from flask import make_response
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename

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

UPLOAD_FOLDER = 'C:'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'PNG'])

app.config['UPLOAD_FOLDER'] = 'static/img/'

@app.route('/')
def index():
    valor = "0"
    session['logged_inC'] = False
    session['logged_in'] = False
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Productos")
    rv = cur.fetchall()
    cur.close()
    response = make_response(render_template('home.html', Productos=rv))
    response.set_cookie('idClienteReg',valor)
    response.set_cookie('idSec',valor)
    response.set_cookie('idProduct',valor)
    response.set_cookie('idVendedorReg',valor)
    response.set_cookie('NomProduct',valor)
    response.set_cookie('idVen',valor)
    return response

@app.route('/error', methods = ['GET', 'POST'])
def error():    
    return render_template('error.html')

@app.route('/errorCliente', methods = ['GET', 'POST'])
def errorCliente():    
    return render_template('errorCliente.html')

@app.route('/errorInesperado', methods = ['GET', 'POST'])
def errorInesperado():    
    return render_template('ErrorInesperado.html')  

@app.route('/Inicio', methods = ['GET', 'POST'])
def Inicio():
    valor = "0"
    session['logged_inC'] = False
    session['logged_in'] = False
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Productos")
    rv = cur.fetchall()
    cur.close()
    response = make_response(render_template('home.html', Productos=rv))
    response.set_cookie('idClienteReg',valor)
    response.set_cookie('idSec',valor)
    response.set_cookie('idProduct',valor)
    response.set_cookie('idVendedorReg',valor)
    response.set_cookie('idVen',valor)
    response.set_cookie('NomProduct',valor)
    return response

@app.route('/InicioVendedor', methods = ['GET', 'POST'])
def InicioVendedor():
    try:       
        idVendedor = request.cookies.get('idVendedorReg')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Vendedor WHERE id=%s", (idVendedor,))
        rv = cur.fetchall()
        cur.close()
        return render_template('InicioVendedor.html', Vendedor=rv)
    except Exception as e:
         return redirect(url_for('error'))

@app.route('/decision', methods = ['GET', 'POST'])
def decision():
    return render_template('prelogin.html')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    try:
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
            session['logged_in'] = True
            response = make_response(redirect(url_for('InicioVendedor')))
            response.set_cookie('idVendedorReg',valor)
            return response

        title = "APP Python"     
        return render_template('RegistroVen.html',title = title, RegistroVendedor = comment_form)
    except Exception as e:
         return redirect(url_for('errorInesperado'))

@app.route('/log', methods = ['GET', 'POST'])
def log():
    return render_template('loginDes.html')
 
@app.route('/InicioSecion', methods = ['GET', 'POST'])
def InicioSecion():
    try:
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            cur = mysql.connection.cursor()
            idVendedor = request.cookies.get('idVendedorReg')
            cur.execute("SELECT * FROM Vendedor WHERE id=%s", (idVendedor,))
            rv = cur.fetchall()
            cur.close()
            return render_template('InicioVendedor.html', Vendedor=rv)
    except Exception as e:
         return redirect(url_for('error'))

@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
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
    except Exception as e:
         return redirect(url_for('error'))

@app.route("/logout")
def logout():
    try:       
        session['logged_in'] = False
        valor = '0'
        response = make_response(redirect(url_for('index')))
        response.set_cookie('idVendedorReg',valor)
        return response
    except Exception as e:
         return redirect(url_for('error'))

@app.route('/productos', methods = ['GET', 'POST'])
def productos():
    try:     
        idVendedor = request.cookies.get('idVendedorReg')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Productos WHERE idVendedor=%s", (idVendedor,))
        rv = cur.fetchall()
        cur.close()
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM CatCategoria")
        rv1 = cur1.fetchall()
        cur1.close()    
        return render_template('productos.html', Productos=rv, CatCategoria = rv1)
    except Exception as e:
         return redirect(url_for('error'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/createProducto', methods = ['GET', 'POST'])
def createProducto():
    try:      
        comment_form = frmProductos.CommentForm(request.form)       
        if request.method == 'POST' and comment_form.validate():
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.filename.strip('.')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))    
                idVendedor = request.cookies.get('idVendedorReg')
            strRutaImagen = app.config['UPLOAD_FOLDER']+file.filename    
            strNombre = request.form['strNombre']
            curPrecio = request.form['curPrecio']
            decStock = request.form['decStock']
            strDescripcion =request.form['strDescripcion']
            strContendo =request.form['strMarca']
            strMarca =request.form['strMarca']
            strModelo =request.form['strModelo']
            idCatCategoria =request.form['idCatCategoria']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Productos (idVendedor,strNombre,curPrecio,decStock,strDescripcion,strContendo,idCatCategoria,strRutaImagen,strMarca,strModelo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
             (idVendedor,strNombre,curPrecio,decStock,strDescripcion,strContendo,idCatCategoria,strRutaImagen,strMarca,strModelo))
            mysql.connection.commit() 
            return redirect(url_for('productos'))

        title = "APP Python"   
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM CatCategoria")
        rv1 = cur1.fetchall()
        cur1.close()      
        return render_template('ReguistroProducto.html',title = title, frmProductos = comment_form, CatCategoria = rv1)
    except Exception as e:
         return redirect(url_for('error'))

@app.route('/updateProducto/<string:id_data>', methods = ['GET', 'POST'])
def updateProducto(id_data):
    try:     
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Productos WHERE id=%s", (id_data,))
        rv = cur.fetchall()
        cur.close()
        comment_form = frmProductos.CommentForm(request.form)
        if request.method == 'POST' and comment_form.validate():   
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.filename.strip('.')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))    
                idVendedor = request.cookies.get('idVendedorReg')
            strRutaImagen = app.config['UPLOAD_FOLDER']+file.filename    
            strNombre = request.form['strNombre']
            curPrecio = request.form['curPrecio']
            decStock = request.form['decStock']
            strDescripcion =request.form['strDescripcion']
            strContendo =request.form['strContendo']
            idCatCategoria =request.form['idCatCategoria']
            strMarca =request.form['strMarca']
            strModelo =request.form['strModelo']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Productos SET strNombre=%s, curPrecio=%s, decStock=%s, strDescripcion=%s, strContendo=%s, idCatCategoria=%s, strRutaImagen=%s, strMarca=%s, strModelo=%s WHERE id=%s",  
                (strNombre,curPrecio,decStock,strDescripcion,strContendo,idCatCategoria,strRutaImagen,strMarca,strModelo,id_data,))
            mysql.connection.commit()
            return redirect(url_for('productos'))
        title = "APP Python"
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM CatCategoria")
        rv1 = cur1.fetchall()
        cur1.close()    
        return render_template('ReguistroProducto.html',title = title, frmProductos = comment_form, Productos=rv, CatCategoria = rv1) 
  
    except Exception as e:
         print(e)
         return redirect(url_for('error'))
 
@app.route('/deleteProducto/<string:id_data>', methods=["GET"])
def deleteProducto(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Productos WHERE id=%s", (id_data,))
        mysql.connection.commit()
        return redirect(url_for('productos'))
    except Exception as e:
         return redirect(url_for('error'))

@app.route('/infoProducto/<string:id_data>', methods = ['GET', 'POST'])
def infoProducto(id_data):
    try:     
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Productos WHERE id=%s", (id_data,))
        rv = cur.fetchall()
        cur.close()
        cat = rv[0]
        idcat = cat[7]
        idcven = cat[1]
        title = "APP Python"
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM CatCategoria WHERE id=%s", (idcat,))
        rv1 = cur1.fetchall()
        cur1.close()
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM Vendedor WHERE id=%s", (idcven,))
        rv2 = cur2.fetchall()
        cur2.close()   
        return render_template('infoProducto.html',title = title, Productos=rv, CatCategoria = rv1, Vendedor=rv2 ) 
    except Exception as e:
         return redirect(url_for('error'))

@app.route('/busqueda', methods=['POST'])
def busquedaProduct():
    try:        
        if not session.get('logged_inC'):
            busqueda = request.form['busqueda']
            cur = mysql.connection.cursor()      
            con = "%"+ busqueda +"%"    
            cur.execute("SELECT * FROM Productos WHERE strNombre like %s", (con,))
            rv = cur.fetchall()
            cur.close()
            return render_template('busquedaProducto.html', Productos=rv )
        else:
            busqueda = request.form['busqueda']
            cur = mysql.connection.cursor()      
            con = "%"+ busqueda +"%"    
            cur.execute("SELECT * FROM Productos WHERE strNombre like %s", (con,))
            rv = cur.fetchall()
            cur.close()
            return render_template('busquedaProductoC.html', Productos=rv )

    except Exception as e:
         return redirect(url_for('error'))

@app.route('/createCliente', methods = ['GET', 'POST'])
def createCliente():
    try:
        comment_form = RegistroCliente.CommentForm(request.form)
        if request.method == 'POST' and comment_form.validate():  
            strNombre = request.form['strNombre']
            strTelefono = request.form['strTelefono']
            strCorreo = request.form['strCorreo']
            strDireccion =request.form['strDireccion']
            strContraseña =request.form['strContraseña']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Cliente (strNombre,strTelefono,strCorreo,strDireccion,strContraseña) VALUES (%s,%s,%s,%s,%s) ",
                (strNombre,strTelefono,strCorreo,strDireccion,strContraseña))
            mysql.connection.commit() 

            cur.close()
            cur1 = mysql.connection.cursor()
            con = 1
            cur1.execute("SELECT * FROM Cliente order by id desc limit %s", (con,))
            rv = cur1.fetchall()
            cur1.close()
            idVendedor = rv[0]
            idven = idVendedor[0]
            valor = ''
            valor +=str(idven)   

            session['logged_inC'] = True
            response = make_response(redirect(url_for('InicioCliente')))
            response.set_cookie('idClienteReg',valor)
            return response

        title = "APP Python"     
        return render_template('RegistroCliente.html',title = title, RegistroCliente = comment_form)
    except Exception as e:
         return redirect(url_for('errorInesperado'))

@app.route('/InicioCliente', methods = ['GET', 'POST'])
def InicioCliente():
    try:       
        idCliente = request.cookies.get('idClienteReg')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Cliente WHERE id=%s", (idCliente,))
        rv = cur.fetchall()
        cur.close()
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM Productos")
        rvd = cur1.fetchall()
        cur1.close()  
        return render_template('InicioCliente.html', Cliente=rv, Productos=rvd)
    except Exception as e:
         return redirect(url_for('errorCliente'))
 
@app.route('/InicioSecionC', methods = ['GET', 'POST'])
def InicioSecionC():
    try:
        if not session.get('logged_inC'):
            return render_template('loginCliente.html')
        else:
            idsec = request.cookies.get('idSec')
            if idsec == "1":
                return redirect(url_for('compras'))
            else:
                cur = mysql.connection.cursor()
                idVendedor = request.cookies.get('idClienteReg')
                cur.execute("SELECT * FROM Cliente WHERE id=%s", (idVendedor,))
                rv = cur.fetchall()
                cur.close()
                cur1 = mysql.connection.cursor()
                cur1.execute("SELECT * FROM Productos")
                rvd = cur1.fetchall()
                cur1.close()  
                return render_template('InicioCliente.html', Cliente=rv, Productos=rvd)
    except Exception as e:
         return redirect(url_for('error'))

@app.route('/loginC', methods=['POST'])
def do_admin_loginC():
    try:
        usuario = request.form['username']
        contrasena = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Cliente WHERE strCorreo=%s and strContraseña=%s ", (usuario,contrasena,))
        rv = cur.fetchall()
        cur.close()
        if rv:  
            session['logged_inC'] = True
            idVendedor = rv[0]
            idven = idVendedor[0]
            valor = ''
            valor +=str(idven)
        else:       
            valor = '0'
            session['logged_inC'] = False

        response = make_response(redirect(url_for('InicioSecionC')))
        response.set_cookie('idClienteReg',valor)    
        return response
    except Exception as e:
         return redirect(url_for('error'))

@app.route("/logoutC")
def logoutC():
    try:       
        session['logged_inC'] = False
        valor = '0'
        response = make_response(redirect(url_for('index')))
        response.set_cookie('idClienteReg',valor)
        response.set_cookie('idSec',valor)
        response.set_cookie('idProduct',valor)
        return response
    except Exception as e:
         return redirect(url_for('error'))

@app.route('/detalleProducto/<string:id_data>', methods = ['GET', 'POST'])
def detalleProducto(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Productos WHERE id=%s", (id_data,))
        rv = cur.fetchall()
        cur.close()
        cat = rv[0]
        idcat = cat[7]
        idven = cat[1]
        nombreProduct = cat[2]
        title = "APP Python"
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM CatCategoria WHERE id=%s", (idcat,))
        rv1 = cur1.fetchall()
        cur1.close()
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM Vendedor WHERE id=%s", (idven,))
        rv2 = cur2.fetchall()
        cur2.close()
        response = make_response(render_template('detalleProducto.html',title = title, Productos=rv, CatCategoria = rv1, Vendedor=rv2 ))
        response.set_cookie('idProduct',id_data)
        response.set_cookie('NomProduct',nombreProduct)
        return response
    except Exception as e:
         return redirect(url_for('errorInesperado'))

@app.route('/detalleProductoC/<string:id_data>', methods = ['GET', 'POST'])
def detalleProductoC(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Productos WHERE id=%s", (id_data,))
        rv = cur.fetchall()
        cur.close()
        cat = rv[0]
        idcat = cat[7]
        idven = cat[1]
        nombreProduct = cat[2]
        title = "APP Python"
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM CatCategoria WHERE id=%s", (idcat,))
        rv1 = cur1.fetchall()
        cur1.close()
        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT * FROM Vendedor WHERE id=%s", (idven,))
        rv2 = cur2.fetchall()
        cur2.close()
        response = make_response(render_template('detalleProductoC.html',title = title, Productos=rv, CatCategoria = rv1, Vendedor=rv2 ))
        response.set_cookie('idProduct',id_data)
        response.set_cookie('NomProduct',nombreProduct)
        return response
    except Exception as e:
         return redirect(url_for('errorCliente'))

@app.route("/compras", methods = ['GET', 'POST'])
def compras():
    try:
        comment_form = compra.CommentForm(request.form)
        if not session.get('logged_inC'):
            idsec = "1"
            response = make_response(redirect(url_for('InicioSecionC')))
            response.set_cookie('idSec',idsec)
            return response
        else:
            idProducto = request.cookies.get('idProduct')
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Productos WHERE id=%s", (idProducto,))
            rv = cur.fetchall()
            cur.close()
            if request.method == 'POST' and comment_form.validate():
                nombreProduct = request.cookies.get('NomProduct')
                idCliente = request.cookies.get('idClienteReg')
                idProducto = request.cookies.get('idProduct')
                strCantidad = request.form['strCantidad']
                strTelefono = request.form['strTelefono']
                strReferencias = request.form['strReferencias']
                strDireccion =request.form['strDireccion']
                strObservaciones =request.form['strObservaciones']
                idEstadoCompraCliente = 1
                cur1 = mysql.connection.cursor()
                cur1.execute("INSERT INTO CompraCliente (idProducto,idCliente,idEstadoCompraCliente,strCantidad,strTelefono,strReferencias,strDireccion,strObservaciones,strNombreProducto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                    (idProducto,idCliente,idEstadoCompraCliente,strCantidad,strTelefono,strReferencias,strDireccion,strObservaciones,nombreProduct))
                mysql.connection.commit()
                cur1.close()
                return redirect(url_for('RegistrosCompras'))
            return render_template('compraCliente.html', compra = comment_form, Producto=rv)    
    except Exception as e:
        return redirect(url_for('errorCliente'))

@app.route("/RegistrosCompras")
def RegistrosCompras():
    try:
        idCliente = request.cookies.get('idClienteReg')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM CompraCliente WHERE idCliente=%s",(idCliente,))
        rv = cur.fetchall()
        cur.close()
        return  render_template('RegistroCompras.html', Compras=rv)        
    except Exception as e:
         return redirect(url_for('errorCliente'))

@app.route("/Ventas")
def Ventas():
    try:
        idVen = request.cookies.get('idVen')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM CompraCliente WHERE idVendedor=%s",(idVen,))
        rv = cur.fetchall()
        cur.close()
        return  render_template('CompraVendedor.html', Compras=rv)        
    except Exception as e:
         return redirect(url_for('errorCliente'))


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
