from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class CommentForm(Form):
	strNombre = StringField('Nombre',
		[
		validators.length(max=40, message='El numero de caracteres es incorrecto el maximo de caracteres es 40'),
		validators.required(message='Falta ingresar el Nombre')
		]
		)
	strApaterno = StringField('Apellido Paterno',
		[
		validators.length(max=40, message='El numero de caracteres es incorrecto el maximo de caracteres es 40'),
		validators.required(message='Falta ingresar el Apellido Paterno')
		]
		)
	strAmaterno = StringField('Apellido Materno',
		[
		validators.length(max=40, message='El numero de caracteres es incorrecto el maximo de caracteres es 40'),
		validators.required(message='Falta ingresar el Apellido Materno')
		]
		)
	dtefechaNacimiento = StringField('Fecha Nacimiento',
		[
		validators.length(max=40, message='El numero de caracteres es incorrecto el maximo de caracteres es 40'),
		validators.required(message='Falta ingresar la Fecha de Nacimiento')
		]
		)
	