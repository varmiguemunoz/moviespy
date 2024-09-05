# ¿De qué tratará nuestra API?
El proyecto que estaremos construyendo a lo largo del curso será una API que nos brindará información relacionada con películas, por lo que tendremos lo siguiente:

### Consulta de todas las películas
Para lograrlo utilizaremos el método GET y solicitaremos todos los datos de nuestras películas.

### Filtrado de películas
También solicitaremos información de películas por su id y por la categoría a la que pertenecen, para ello utilizaremos el método GET y nos ayudaremos de los parámetros de ruta y los parámetros query.

### Registro de peliculas
Usaremos el método POST para registrar los datos de nuestras películas y también nos ayudaremos de los esquemas de la librería pydantic para el manejo de los datos.

### Modificación y eliminación
Finalmente para completar nuestro CRUD realizaremos la modificación y eliminación de datos en nuestra aplicación, para lo cual usaremos los métodos PUT y DELETE respectivamente.

```npm
uvicorn main:app --reload
```