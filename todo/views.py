from http.client import HTTPResponse
from django.shortcuts import render,redirect
from todo.models import value
from django.http import HttpResponseRedirect
from .forms import TitleForm
from django.urls import reverse






#The Home page which conntains posting of task too
def home(request):
    
    if request.user.is_authenticated:
        values=value.objects.filter(owner=request.user)    
        form=TitleForm()
        if request.method=='POST':
            form=TitleForm(request.POST)
            if form.is_valid():
                ok=form.save(commit=False)
                ok.owner=request.user
                ok.save()
            return HttpResponseRedirect('/')
    else:
        return redirect('login1')
    context={'form':form,'values':values}
    return render(request,'home.html',context)

#Updating the task

def update(request,id):
    
    ggwp=value.objects.get(id=id)
    form=TitleForm(instance=ggwp)
    if request.method == 'POST':
        form=TitleForm(request.POST,instance=ggwp)
        if form.is_valid:
            ok=form.save(commit=False)
            ok.owner=request.user
            ok.save()
            return redirect('home')
        return HTTPResponse("op")
    context={'form':form,}
    return render(request,'update.html',context)




#Deletion of the Task

def delete_data(request, id ):
    
    if request.method=="POST":
        ggwp=value.objects.get(id=id)
        ggwp.delete()
        return HttpResponseRedirect(reverse('deldata', kwargs={'id':id}))
    return redirect("/")
    

