from django.forms import ModelForm
from models import todo
    
class ToDoForm(ModelForm):
    class Meta:
        model = todo
        fields = ('name', 'description')