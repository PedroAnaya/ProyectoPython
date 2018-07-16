from flask import Flask, render_template, url_for, redirect
from flask import request
from flask_mysqldb import MySQL
from flask import make_response
from raven.contrib.flask import Sentry
import form
from io import StringIO
from io import BytesIO
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
app.config['MYSQL_DB'] = 'Prueba'
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Persona")
    rv = cur.fetchall()
    cur.close()
    cur1 = mysql.connection.cursor()
    cur1.execute("SELECT * FROM Sexo")
    rv2 = cur1.fetchall()
    cur1.close()
    return render_template('home.html', Persona=rv, Sexo=rv2)


@app.route('/create', methods = ['GET', 'POST'])
def create():
    cur1 = mysql.connection.cursor()
    cur1.execute("SELECT * FROM Sexo")
    rv2 = cur1.fetchall()
    cur1.close()
    comment_form = form.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():       
        strNombre = request.form['strNombre']
        strApaterno = request.form['strApaterno']
        strAmaterno = request.form['strAmaterno']
        idSexo = request.form['idSexo']
        dtefechaNacimiento =request.form['dtefechaNacimiento']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Persona (strNombre,strApaterno,strAmaterno,dtefechaNacimiento,idSexo) VALUES (%s,%s,%s,%s,%s) ",(strNombre,strApaterno,strAmaterno,dtefechaNacimiento,idSexo))
        mysql.connection.commit()       
        return redirect(url_for('index'))

    title = "APP Python"   
    return render_template('index.html',title = title, form = comment_form, Sexo=rv2)

@app.route('/update/<string:id_data>', methods = ['GET', 'POST'])
def update(id_data):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Persona WHERE id=%s", (id_data,))
    rv = cur.fetchall()
    cur.close()
    comment_form = form.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():   
        id_data1 = id_data
        strNombre = request.form['strNombre']
        strApaterno = request.form['strApaterno']
        strAmaterno = request.form['strAmaterno']
        dtefechaNacimiento = request.form['dtefechaNacimiento']
        idSexo = request.form['idSexo']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Persona SET strNombre=%s, strApaterno=%s, strAmaterno=%s, dtefechaNacimiento=%s, idSexo=%s WHERE id=%s", (strNombre,strApaterno,strAmaterno,dtefechaNacimiento,idSexo,id_data1,))
        mysql.connection.commit()
        return redirect(url_for('index'))
    title = "APP Python"   
    return render_template('index.html',title = title, form = comment_form, Persona=rv)   

@app.route('/hapus/<string:id_data>', methods=["GET"])
def hapus(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Persona WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/cookie')
def cookie():
    reponse = make_response( render_template('cookie.html') )
    reponse.set_cookie('custome_cookie', 'Pedro')
    return reponse

@app.route('/pdf/<string:id_data>/<string:strNombre>/<string:strApaterno>/<string:strAmaterno>/<string:dtefechaNacimiento>/<string:idSexo>', methods=["GET"])
def pdf(id_data,strNombre,strApaterno,strAmaterno,dtefechaNacimiento,idSexo):
    output = BytesIO()

    p = canvas.Canvas(output)
    p.drawString(100, 800, 'Nombre: '+strNombre)
    p.drawString(100, 750, 'Apellido Paterno: '+strApaterno)
    p.drawString(100, 700, 'Apellido Materno: '+strAmaterno)
    p.drawString(100, 650, 'Fecha de Nacimiento: '+dtefechaNacimiento)

    if idSexo == '1':
        p.drawString(100, 600, 'Sexo: HOMBRE')
    else:  
        p.drawString(100, 600, 'Sexo: MUJER')
    p.showPage()
    p.save()
    
    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename='archivo.pdf"
    response.mimetype = 'application/pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
