from django.shortcuts import render,redirect
#from django.http import  HttpResponse\
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login #within this method it will help us to automatically login the user once they have created the account 
from .models import Task
from .models import Task

class CustomLoginView(LoginView):
    template_name='todo/login.html'
    fields= '__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('tasks') 
        
class RegisterForm(FormView):
    template_name='todo/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True  
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user) # if the user is sucessfully created then automatically redirect the user to the task page 
        return super(RegisterForm,self ).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks') 
        return super(RegisterForm, self).get(*args, **kwargs)       

class TaskList(LoginRequiredMixin, ListView): #this view is going to be restricted and requires that the user should be logged in
    model= Task
    context_object_name='tasks'

    def get_context_data(self, **kwargs): # this function will help that each user get their own data
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        return context
        
class TaskDetail(LoginRequiredMixin, DetailView): 
    model=Task 
    context_object_name='task'
    template_name='todo/task.html'  #to ovveride the default template name

class TaskCreate(LoginRequiredMixin, CreateView):
        model=Task
        fields= ['title','description','complete'] #you can specify fields you want in the form or bring all the fields
        success_url=reverse_lazy('tasks')

        def form_valid(self, form): #built_in
            form.instance.user=self.request.user
            return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=Task
    fields= ['title','description','complete']
    success_url=reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')



#def tasklist(request):
    #return HttpResponse('To Do List')

