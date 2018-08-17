from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class CommentForm(Form):
	strNombre = StringField('Nombre',
		[
		validators.length(max=100, message='El numero de caracteres es incorrecto el maximo de caracteres es 100'),
		validators.required(message='Falta ingresar el Nombre')
		]
		)
	strTelefono = StringField('Telefono',
		[
		validators.length(max=15, message='El numero de caracteres es incorrecto el maximo de caracteres es 15'),
		]
		)
	strCorreo = StringField('Correo Electonico',
		[
		validators.length(max=50, message='El numero de caracteres es incorrecto el maximo de caracteres es 55'),
		validators.required(message='Falta ingresar el Correo Electronico')
		]
		)
	strDireccion = StringField('Direccion',
		[
		validators.length(max=250, message='El numero de caracteres es incorrecto el maximo de caracteres es 250'),
		]
		)
	strContraseña = StringField('Contraseña',
		[
		validators.length(max=10, message='El numero de caracteres es incorrecto el maximo de caracteres es 10'),
		validators.required(message='Falta ingresar la Contraseña')
		]
		)
