# Create your views here.
from models import todo  
from forms import ToDoForm  
from django.shortcuts import render, render_to_response  
from django.http import HttpResponseRedirect

def index(request):
    items = todo.objects.all() 
    form = ToDoForm()
    return render(request, 'index.html', {
        'form': form,
        'items': items
    })    
    
def add_todo(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ToDoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            form.save()            
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = ToDoForm() # An unbound form

    return render(request, 'index.html', {
        'items': items,
        'form': form
    })