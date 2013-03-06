# Create your views here.
from models import todo  
from forms import ToDoForm  
from django.shortcuts import render, render_to_response  
from django.http import HttpResponseRedirect
import sys

def index(request):
    items = todo.objects.all() 
    form = ToDoForm()
    return render(request, 'index.html', {
        'form': form,
        'items': items
    })

def test_path(request):
	path = sys.path
	return render_to_response("testpath.html", locals())
	
def add_todo(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ToDoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method			
            new_todo = form.save(commit=False)
            new_todo.user = request.user if request.user.is_authenticated() else None
            new_todo.save()
            return HttpResponseRedirect('/') # Redirect after POST

                
    else:
        form = ToDoForm() # An unbound form

    return render(request, 'index.html', {
        'items': items,
        'form': form
    })