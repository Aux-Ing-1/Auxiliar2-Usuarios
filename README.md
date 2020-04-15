# Auxiliar 3: Django Users

>Leer antes de empezar!
>
>Hoy crearemos un sistema de usuarios y para esto tendremos que comenzar la base de datos desde 0. 
>Si vas a usar el proyecto de la aux anterior tutorial tendrás que borrar los archivos que están dentro de la carpeta todolist/migrations y solo dejar el archivo `__init__.py` y el archivo `db.sqlite3`. 
>Si vas a user este repositorio (que trae el proyecto de la aux anterior), no hagas `python manage.py makemigrations` hasta que el tutorial lo indique! 

> También recuerda que si vas a user este repositorio tienes que seguir las instrucciones de la auxiliar 1 para hacer Fork y luego clonar el repositorio, y sigue las instrucciones de como correr tu app de Django. 
## Librería Auth
Django posee su propio sistema de usuarios, el cual esta incluido en la [librería Auth](https://docs.djangoproject.com/en/2.2/topics/auth/). 
Un usuario está representado por un objeto de la clase User y sus atributos principales son:
* username
* password
* email
* first_name
* last_name

[Aquí](https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User)  encuentras todos los atributos de la clase User.

Hoy vamos a agegarle usuarios a nuestra app de Todo List para que cada uno tenga su propia lista de tareas.
Para esto tendremos que __crear usuarios__, __loguearlos__ y __asignarle un usuario a cada tarea__!

![Pantallazo del resultado final de la app](vista_final.png)

## Actividad
### [Parte 1: Crear usuarios]
Para nuestra aplicación querremos que los usuarios tengan Nombre, Apodo, Mail y Contraseña. Un User de Django ya trae algunos de estos atributos, pero no todos. 
Es por esto que vamos a crear nuestra propia clase User que heredará de AbstractUser y así podremos guardar todos los atributos que querramos. 

AbstractUser es una clase que trae toda la funcionalidad de los usuarios de Django y está diseñada para cuando queremos agregar mas información a los usuarios. 


1. __Crear modelo User__: en todolist/models.py agregaremos el modelo User que heredará de AbstractUser y le pondremos el atributo apodo, para tener mas información sobre el usuario. 

    ```python
   from django.contrib.auth.models import AbstractUser

    class User(AbstractUser):
        apodo=models.CharField(max_length=30)
    
        
    ```
    Antes de hacer las migraciones tenemos que hacer un paso más. Vamos a ir a todoapp/settings.py y agregaremos esta línea: 
    
    `AUTH_USER_MODEL = 'todolist.User'`
    
    Con esta linea le diremos al proyecto que el sistema de usuarios ahora será en base al modelo User que acabamos de crear. 
    
    > Importante! Luego de agregar este modelo hay que hacer 
    >```python
    >$ python manage.py makemigrations
    >$ python manage.py migrate
    >```
    >para que los cambios en el modelo se reflejen en la base de datos. 

2. __Formulario de registro de usuarios__:
 Para crear un  nuevo usuario crearemos una nueva url que será /register. Al entrar a esta url habrá un formulario que luego de llenarlo correctamente nos llevará a la página de inicio de la app. 
    
    2.1 __Urls__
     
     Primero crearemos la url en urls.py agregando la siguiente línea: 
     
     ```python
       path('register', views.register_user, name='register_user'), 
    ``` 
   
   2.2 __Views__

    Luego tenemos que hacer la view register_user para mostrar el formulario con el siguiente código en todolist/views.py:
  
    ```python
     def register_user(request):
       return render(request,"todolist/register_user.html")
    ```
   >Fíjate que en views creamos el método register_user porque en urls dijimos que /register estaría asociado a este método. 
   
   2.3 __Templates__
   
   Finalmente tenemos que crear el formulario para registrar al usuario. Este lo guardaremos en templates/todolist/register_user.html y llevará lo siguiente: 
   ```
        <!DOCTYPE html>
        <html lang="en">
        <head>
           <meta charset="UTF-8">
           <title>Registro</title>
        </head>
        <body>
           <h1> Registro </h1>
           <form method="post">
               {% csrf_token %}
               <div class="form-group">
                   <label for="nombre_usuario">Nombre</label>
                   <input type="text" class="form-control" id=nombre_usuario name="nombre" required>
               </div>
       
               <div class="form-group">
                   <label for="contraseña">Contraseña</label>
                   <input type="password" class="form-control" id="contraseña" name="contraseña" required>
               </div>
       
                <div class="form-group">
                   <label for="apodo">Apodo</label>
                   <input type="text" class="form-control" id="apodo" name="apodo" required>
                </div>
                 
                <div class="form-group">
                    <label for="mail">Mail</label>
                    <input type="email" class="form-control" id="mail" name="email" required>
                </div>
                <button type="submit">Crear usuario</button>
           </form>
        </body>
        </html>
    ```

    ### __¿Qué hay en este código html?__ 
    Lo mas importante por ahora es el formulario que se crea con la etiqueta ```<form>```. 
    Todo lo que está dentro de form serán los campos que tendremos que llenar para crear un usuario. 
    Cada "campo" está formado por un ```<label>``` y un ```<input>``` (este último es donde ingresamos los datos). 
    
   > Ahora si hacemos ```python manage.py runserver``` e ingresamos a 127.0.0.1/register deberíamos ver el formulario de registro. 
   
   ![Vista registro](vista-registro.png)
   
   > ¿Qué pasa si intentamos crear un usuario? Nada, porque no le hemos dado instrucciones a la app para registrar el usuario. 
   
3. __Guardar datos del formulario__:
   
   Cuando creamos el método _register_user_ solo le indicamos que hiciera render del formulario. 
   Ahora queremos diferenciar entre una llamada GET (cuando cargamos la página) y una llamada POST (cuando eviamos el formulario).
   
   Para esto vamos a editar todolist/views.py y diferenciar estos dos casos: 
   ```python
    def register_user(request):
        if request.method == 'GET':
            return render(request,"todolist/register_user.html")
    
        elif request.method == 'POST':
            nombre = request.POST['nombre']
            contraseña = request.POST['contraseña']
            apodo = request.POST['apodo']
            mail = request.POST['mail']
            user = User.objects.create_user(username=nombre, password=contraseña,email=mail,apodo=apodo)
            messages.success(request, 'Se creó el usuario para ' + user.apodo + '!')
            return HttpResponseRedirect('/')
     
   ```
    
   ```python
       #Estos son los imports que van al inicio de views.py
       from todolist.models import User       
    ```
   
   En el código anterior, cuando el método es POST estamos haciendo lo siguiente: 
   * recuperamos los datos que vienen del formulario
   * creamos un User con estos datos
   * redirigimos a la página de inicio. 
   
   > Atención: En el formulario de registro le pusimos un _name_ a cada ```<input>``` y con ese name podemos acceder a los datos en ```request.POST```.
   
   Prueba que el formulario esté funcionando y agrega cuentas. 
   Para comprobar que se crearon puedes hacer lo siguiente: 
   * Editar todolist/admin.py y agegar ```admin.site.register(models.User)``` .
   
   * Crea un superusuario haciendo ```python manage.py createsuperuser```. 
   
   * Luego ingresa a 127.0.0.1/admin y deberías poder ver todos los Users que has creado! 
   ![vista admin con my_user](vista_myuser_admin.png)

 4. __[Bonus track]__ Agregar un mensaje al crear el usuario. 
 
    Existe una librería en Django que nos permite crear mensajes o alertas ([mas info](https://docs.djangoproject.com/en/3.0/ref/contrib/messages/)) cuando terminamos de procesar alguna información. 
    
    Gracias a esto cuando procesamos un formulario podemos enviar un mensaje a la siguiente página que mostramos. 
    
    Queremos ver un mensaje así luego de crear un usuario: 
     ![Usuario creado](vista_mensaje_inicio.png)
    
     __¿Cómo hacemos esto?__
     * Importar messages de django.contrib 
     * Agregar el mensaje después de crear el usuario. 
     * Mostrar el mensaje en el template 
     
     El final del método register_user de views.py debería quedar así: 
     ```
        from django.contrib import messages
        ....
        elif request.method == 'POST':
            ...
            ...
            user = User.objects.create_user(username=nombre, password=contraseña,email=mail)
            messages.success(request, 'Se creó el usuario para ' + user.apodo)
            return HttpResponseRedirect('/')
     ```
    Aquí estamos agregando un nuevo mensaje de tipo success que dirá "Se creó el usuario para _apodo_".  
    Y en index.html agregamos el siguiente código para mostrar el mensaje al inicio de la página (fíjense que se agrega solo el if): 
    ```html
        <div class="content">
            {% if messages %}
                <ul class="messages">
                    {% for message in messages %}
                         <div class="alert">
                          {{message}}
                        </div>
                    {% endfor %}
                </ul>
            {% endif %}
            <h1>TodoApp</h1>
    ``` 
    Esto revisará si hay mensajes y por cada mensaje que haya lo mostrará en el template. 

### [Parte 2: Login y logout]
Un login es un formulario donde los usuarios inician sesión.
Mientras que logout es un botón o link por el cual los usuarios cierran sesión.
Es importante que el login solo sea visible cuando los usuarios no han iniciado sesión, en caso de que ya han iniciado sesión deber ver un link para cerrar sesión (logout).

Como el usuario que implementamos hereda de AbstractUser, la autenticación será muy fácil de implementar en nuestro proyecto. 
De hecho, antes de implementar cualquier cosa, podremos ver en nuestro código si un usuario ya inició sesión o no. 

> ¿Cómo saber si una sesión está aciva? 
> 
>En la views : _if request.user.is_authenticated():_
>
>En los templates:  _{% if user.is_authenticated %}_

    
Lo que haremos ahora es mostrar la opción de hacer login o registrarse, si no hay un usuario logueado. En caso contrario mostraremos un botón de logout. 

![Login-register](login-register.png)                    

1. __Crear botones de login - logout__: 
    En index.html vamos a crear botones para hacer login o logout según lo que se necesite. En un principio los botones no harán nada,
    y les iremos dando funcionalidad a medida que avanzamos. 
    
    index.html: 
    ```html
    <h1>TodoApp</h1>
    <p class="tagline">a Django todo app</p>
    <hr>
    {% if user.is_authenticated %}
       <a href="">Cerrar sesión</a>
    {% else %}
       <a href="{% url 'register_user' %}">Registrarse</a>
       <a href="">Iniciar Sesión</a>
    {% endif %}
    <hr>
    <form action="" method="post">
   ...
   ...
    ```  
   
    > Fíjate que hay elementos del código anterior que ya estaban en tu archivo.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    
     En el código anterior estamos revisando si el usuario que está viendo la página ya hizo login y 
     si lo hizo entonces le mostramos la opción de logout. En cambio si no ha hecho login, le daremos la opción de hacer login o registrarse. 

2. __Login__:
    Para hacer login tendremos una url especial para esto (/login). El formulario de login será igual que los que creamos antes, pero solo pediremos nombre y contraseña. 
    
    Para esto crearemos un formulario donde se inicia sesión, la url de login, y la view que nos permitirá hacer el login:
    
    2.1 __Urls__: crear la url _/login_ que cargará el método login_user en las views.  
    ```python
       path('login',views.login_user, name='login'),
    ```     
   
   2.2 __Views__: Creamos el método login_user que hará render del formulario de login. 
   ```python
   def login_user(request):
       if request.method == 'GET':
           return render("todolist/login.html")    
   ```
   
   2.3 __Templates__: Creamos el html del formulario, que tendrá nombre y contraseña. Para esto creamos un archivo login.html en la carpeta todolist/templates/todolist. 
   
   Hay que poner atención a lo que hay dentro de ```<form>``` porque ahí están los campos donde se piden los datos. 
   ```html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Login</title>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h1> Iniciar Sesión </h1>
                    <form method="post" >
                        {% csrf_token %}
                        <div class="form-group">
                            <label for="nombre_usuario">Nombre</label>
                            <input type="text" class="form-control" id=nombre_usuario name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="contraseña">Contraseña</label>
                            <input type="password" class="form-control" id="contraseña" name="contraseña" required>
                        </div>
                        <button type="submit">Entrar</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
    ```
   
   Igual que antes, si ingresamos a _127.0.0.1/login_ veremos el formulario de login donde se pide el nombre y la contraseña.
   Si enviamos el formulario (apretamos el botón) debería aparecer un error porque aun no le indicamos a la app qué hacer cuando enviamos el formulario. 
   
   Para arreglar esto tenemos que editar views.py para que inicie sesión cuando el método sea POST como muestra el paso siguiente. 
   
   2.4 __Autenticar y loguear el usuario__: A continuación está el código que nos permitirá autenticar y loguear al usuario. Este código hace lo siguiente: 
   * Cuando se reciba el formulario se guardará en variables el nombre y la contraseña que ingresó el usuario.
   * Luego usaremos el método ```authenticate(user, password)``` que nos permitirá buscar el usuario con esas credenciales. 
   * Si authenticate no entrega None, significa que el usuario si existe y podemos hacer ```login()```. 
   * Si el usuario fuera None, significa que no existe un usuario con esas credenciales y se redirige a la vista de registro. 
   
   views.py 
   ```python
   def login_user(request):
       if request.method == 'GET':
           return render(request,"todolist/login.html")
       if request.method == 'POST':
           username = request.POST['username']
           contraseña = request.POST['contraseña']
           usuario = authenticate(username=username,password=contraseña)
           if usuario is not None:
               login(request,usuario)
               return HttpResponseRedirect('/')
           else:
               return HttpResponseRedirect('/register')
   ```
   
   2.5 Antes de terminar con el login nos falta darle funcionalidad al botón de login que creamos en index.html. 
   Para esto hay que modificar la siguiente línea del archivo:
   ```python
     <a href="{% url 'login' %}">Iniciar Sesión</a>
   ``` 
   Con eso hacemos que al apretar el vínculo que dice "Iniciar Sesión", nos redirigirá a la url que tiene nombre 'login'. 
   
   2.6 __[Desafío]__ Qué pasa si ahora queremos mostrar un mensaje después de hacer login? 
   Intenta hacer que se vea esto al inicio de la página después de iniciar sesión: 
   ![Mensaje bienvenida ](mensaje_bienvenida.png) 
   
3. __Logout__: 
Para hacer logout no tendremos que llenar ningún formulario, sino que solo apretar el link y cerrar la sesión. 
Para lograr esto crearemos una url y una view que hará logout y luego redirigirá a la página de inicio. 
    
    3.1 __Urls__:
    Creamos la url /logout que cargará el método logout_user en las views y tiene como nombre 'logout'. 
     ```python
       path('logout',views.logout_user, name='logout'),
    ```
   
   3.2 __Views__:
   Como nuestros usuarios son usuarios de Django, hacer logout es igual de sencillo que el login. 
   Solo tendremos que llamar al método logout() y ya se habrá cerrado la sesión del usuario. 
   
   ```python
    from django.contrib.auth import logout
    def logout_user(request):
       logout(request)
       return HttpResponseRedirect('/')
   ```
    3.3 __Templates__: 
    Antes solo creamos el vínculo que serviría para cerrar sesión, pero no lo vinculamos con ninguna url. 
    Ahora que creamos la url para logout, podremos agregarla a nuestro template index.html modificando la siguiente línea: 
    ```python
       <a href="{% url 'logout' %}">Cerrar sesión </a>
   ```
   Al igual que con login, cuando agregamos el código `{% url 'logout' %}` a href, estamos diciendo que busque una url con el nombre 'logout'. 
   En este caso llamará a _/logout_. 
   
### [Parte 3: Cada usuario tendrá sus tasks]
Para terminar, queremos que un usuario que está logueado solo vea las tasks que fueron creadas por él. 
Para esto tendremos los siguientes requisitos: 
* Una task creada por un usuario anónimo, solo se mostrará cuando el usuario sea anónimo. 
* Una task creada por un usuario logueado, solo se mostrará cuando ese usuario esté logueado.
* Un usuario logueado solo verá las tasks creadas por él. 

Para asociar una task a un usuario tendremos que modificar nuestro modelo Task y agregarle una llave foránea.

Luego tendremos que modificar la view donde se crean las Tasks para asociarla a un usuario, en el caso que exista un usuario logueado. 

Finalmente vamos a modificar la view donde se cargan las Tasks para mostrar solamente las Taks que corresponden a ese usuario. 

1. __Modificar el modelo Task__: Vamos a agregar un atributo a Task que se llamará "owner". 
    Este atributo será una llave foránea a User y podrá ser nula. 
    En la clase Task de todolist/models.py agregamos el siguiente atributo: 

     ```python
       owner = models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE)
    ```
    > Importante! Luego de modificar este modelo hay que hacer 
    >```python
    >$ python manage.py makemigrations
    >$ python manage.py migrate
    >```
    >para que los cambios en el modelo se reflejen en la base de datos. 

       
2. __Modificar la creación de Tasks en views.py__: 
    En el método index() de views.py es donde se crean las nuevas tasks, 
    por lo tanto modificaremos este método para asociar la nueva Task a un usuario que esté logueado. 

    views.py: 
    ```python
        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            title = request.POST["description"] #title
            date = str(request.POST["date"]) #date
            category = request.POST["category_select"] #category
            content = title + " -- " + date + " " + category #content
            if request.user.is_authenticated:
                Todo = Task(title=title, content=content, due_date=date, category=Category.objects.get(name=category),owner=request.user)
            else:
                Todo = Task(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save() #saving the todo
            return redirect("/") #reloading the page
   ```
   Fijarse en sólo agregar el código que sea diferente al que ya está en views.py. 
   
   En esta variación lo que estamos haciendo es verificar si el usuario está autenticado. 
   Si está autenticado entonces se agregará el atributo "owner". 
   Si no está autenticado, se dejará vacío. 

3. __Modificar la carga de Tasks en views.py__: En el método index() de views.py creamos la variable `todos` que tomará todas las Tasks que luego mostraremos en el template. 
    Ahora, no queremos mostrar todas las Tasks sino que sólo las que pertenezcan al usuario. 
    
    Para esto tendremos que cambiar la _querie_ que haremos para cargar las Tasks. En el método index de views.py: 
    
    ```python
    def index(request): #the index view
        if request.user.is_authenticated:
            todos = Task.objects.filter(owner=request.user) #quering all todos with the object manager
        else:
            todos= Task.objects.filter(owner=None)
        categories = Category.objects.all() #getting all categories with object manager
   ```
   
   Fijarse en sólo agregar el código que sea diferente al que ya está en views.py.
   
   En esta variación estamos revisando si el usuario inició sesión o no, con user.is_autenticated.
   Si el usuario inició sesión, entonces se filtrarán las Tasks tal que el owner sea ese usuario. 
   En caso contrario, se buscarán las Tasks tal que el owner sea None.  


> Gracias a esta implementación de usuarios, la autenticación es muy fácil y muy parecida en todas las apps de Django.

> Es importante usar implementaciones de autenticación que vengan pre-hechas ya que así disminuye la posibilidad de tener problemas de seguridad. 
> Si se fijaron nunca tuvimos que preocuparnos de guardar contraseñas de forma segura porque eso lo hace la librería Auth. 

> Por si les da curiosidad la usuaria que aparece en las imágenes, el nombre está inspirado en [Mileva Marić](https://es.wikipedia.org/wiki/Mileva_Mari%C4%87), 
>y la usuaria está inspirada en mi hermana Mileva.
>
>![Mili](mili.jpeg)
>
>
