from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class CommentForm(Form):
	strRazonSocial = StringField('Razon Social',
		[
		validators.length(max=100, message='El numero de caracteres es incorrecto el maximo de caracteres es 100'),
		validators.required(message='Falta ingresar la Razon Social')
		]
		)
	strRFC = StringField('RFC',
		[
		validators.length(max=13, message='El numero de caracteres es incorrecto el maximo de caracteres es 13'),
		validators.required(message='Falta ingresar el RFC')
		]
		)
	strTelefono = StringField('Telefono',
		[
		validators.length(max=15, message='El numero de caracteres es incorrecto el maximo de caracteres es 15'),
		validators.required(message='Falta ingresar el Telefono')
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
		validators.length(max=50, message='El numero de caracteres es incorrecto el maximo de caracteres es 50'),
		validators.required(message='Falta ingresar la Direccion')
		]
		)
	strSitioWeb = StringField('Direccion de sitio web',
		[
		validators.length(max=50, message='El numero de caracteres es incorrecto el maximo de caracteres es 250'),
		]
		)
	strContraseña = StringField('Contraseña',
		[
		validators.length(max=10, message='El numero de caracteres es incorrecto el maximo de caracteres es 10'),
		validators.required(message='Falta ingresar la Contraseña')
		]
		)
