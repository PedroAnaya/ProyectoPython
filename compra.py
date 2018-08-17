from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class CommentForm(Form):
	strCantidad = StringField('Cantidad',
		[
		validators.length(max=10, message='El numero de caracteres es incorrecto el maximo de caracteres es 10'),
		validators.required(message='Falta ingresar la cantidad')
		]
		)
	strDireccion = StringField('Direccion',
		[
		validators.length(max=240, message='El numero de caracteres es incorrecto el maximo de caracteres es 250'),
		validators.required(message='Falta ingresar la direccion')
		]
		)
	strReferencias = StringField('Referencias de direccion',
		[
		validators.length(max=240, message='El numero de caracteres es incorrecto el maximo de caracteres es 250'),
		validators.required(message='Falta ingresar las referencias de la direccon')
		]
		)
	strObservaciones = StringField('Observaciones',
		[
		validators.length(max=40, message='El numero de caracteres es incorrecto el maximo de caracteres es 250')		
		]
		)
	strTelefono = StringField('Telefono',
		[
		validators.length(max=240, message='El numero de caracteres es incorrecto el maximo de caracteres es 10'),
		validators.required(message='Falta ingresar el telefono')
		]
		)
	