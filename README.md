# Título del proyecto

Creación de una api simple, para mostrar conocimiento en un Challenge


## Instalación

Necesario tener Python 3.5 o mayor

$ git clone https://github.com/Rumper/ChallengerAPIRest.git

Creamos maquina virtual

(En caso de no tenerlo installarlo)

$ sudo pip install virtualenv

Una vez obtenido virtualenv

$ cd ChallengerAPIRest
$ virtualenv Challenger
$ source bin/activate

Instalamos dependencias

(Challenger)$ pip install -r config/requeriments.txt

Creamos Base de datos

(Challenger)$ python manage.py makemigrations
(Challenger)$ python manage.py migrate


Si quiere crear super usuario

(Challenger)$ python manage.py createsuperuser

Ya esta listo para su funcionamiento
(Challenger)$ python manage.py runserver

## Test

Aplicar el siguiente comando para ejecutar los test:

(Challenger)$ python manage.py -test

Si se quiere ejecutar con más detalles:

python manage.py -test -v 2


## URLS ACTIVA

### /api/1.0/budgets/

METHOD POST
Crea una nueva solicitud en el sistema, si el email no esta registrado se crea nuevo usuario,
se actualiza sus teléfono o dirección
Ejemplo

{
  'title': 'Título de la solicitud del presupuesto' (opcional),
  'descripción': 'Descripción de la solicitud del presupuesto',
  'category: 'Categoría de la solicitud del presupuesto' (opcional),
  'email': 'Email del ususario',
  'phone': 'Teléfono del usuario',
  'address': 'Dirección del usuario'
}

METHOD GET
Solicita todo los email del sistema

### /api/1.0/budgets/<email>/

METHOD GET
Solicita todo los email que hay en el sistema con ese usuario


### /api/1.0/budget/

METHOD POST
Actualiza el título, descripción o categoría de la solicitud de presupuesto identificada por el uuid

{
   'uuid': 'identifacador de la solicitud de presupuesto',
   'title': 'Título de la solicitud del presupuesto' (opcional),
   'descripción': 'Descripción de la solicitud del presupuesto' (opcional),
   'category: 'Categoría de la solicitud del presupuesto' (opcional),
}


### /api/1.0/budget/<uuid>/

METHOD PUT
Publica la solicitud de presupuesto identificado por uuid si es validado, en caso contrario informa de error.

METHOD DELETE
Descarta la solicitud de presupuesto identificado por uuid si es validado, en caso contrario informa de error.


### /api/1.0/suggest_budget/<uuid>/

Sugiere una categoria o varias para la solicitud de presupuesto por el identificador uuid

## License

Este proyecto esta sujeto a la lincencia GPLv3 ver más en LINCENSE

