# Create your views here.
from django.shortcuts import render, redirect

# Create your views here.
from todolist.models import Task, Category


def index(request): #the index view
   todos = Task.objects.all()  # quering all todos with the object manager
   categories = Category.objects.all()  # getting all categories with object manager

   if request.method == "GET":
       return render(request, "todolist/index.html", {"todos": todos, "categories": categories})

   if request.method == "POST":  # checking if the request method is a POST
       if "taskAdd" in request.POST:  # checking if there is a request to add a todo
           title = request.POST["description"]  # title
           date = str(request.POST["date"])  # date
           category = request.POST["category_select"]  # category
           content = title + " -- " + date + " " + category  # content
           Todo = Task(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
           Todo.save()
           return redirect("/")  # reloading the page

       if "taskDelete" in request.POST: #checking if there is a request to delete a todo
           checkedlist = request.POST["checkedbox"]  # checked todos to be deleted
           for todo_id in checkedlist:
               todo = Task.objects.get(id=int(todo_id))  # getting todo id
               todo.delete()  # deleting todo
           return render(request, "todolist/index.html", {"todos": todos, "categories": categories})

