from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired
from wtforms import validators

class CommentForm(Form):
	strNombre = StringField('Nombre',
		[
		validators.length(max=100, message='El numero de caracteres es incorrecto el maximo de caracteres es 100'),
		validators.required(message='Falta ingresar el Nombre del producto')
		]
		)
	curPrecio = StringField('Precio $',
		[
		validators.length(max=21, message='El numero de caracteres es incorrecto el maximo de caracteres es 18 enteros y dos decimales'),
		validators.required(message='Falta ingresar el Precio')
		]
		)
	decStock = StringField('Stock en Existencia',
		[
		validators.length(max=18, message='El numero de caracteres es incorrecto el maximo de caracteres es 18'),
		validators.required(message='Falta ingresar el Stock')
		]
		)
	strDescripcion = StringField('Descripcion Producto',
		[		
		validators.required(message='Falta ingresar la descripcion del producto')
		]
		)
	strContendo = StringField('Contenido producto',
		[
		validators.required(message='Falta ingresar el contenido')
		]
		)
	strMarca = StringField('Marca',
		[
		validators.length(max=100, message='El numero de caracteres es incorrecto el maximo de caracteres es 50'),
		validators.required(message='Falta ingresar el Marca')
		]
		)
	strModelo = StringField('Modelo',
		[
		validators.length(max=100, message='El numero de caracteres es incorrecto el maximo de caracteres es 50'),
		validators.required(message='Falta ingresar el Modelo')
		]
		)
	file = FileField('Imagen producto'
		)

