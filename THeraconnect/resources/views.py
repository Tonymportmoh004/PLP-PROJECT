from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Resource
from .forms import ResourceForm

def is_creator(user, resource):
    return user == resource.creator

@login_required
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'resources/resource_list.html', {'resources': resources})

@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/resource_detail.html', {'resource': resource})

@login_required
@user_passes_test(lambda u: is_creator(u, get_object_or_404(Resource, pk=u.kwargs['pk'])))
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_detail', pk=resource.pk)
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resources/resource_edit.html', {'form': form})

@login_required
@user_passes_test(lambda u: is_creator(u, get_object_or_404(Resource, pk=u.kwargs['pk'])))
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        return redirect('resource_list')
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})

@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.creator = request.user
            resource.save()
            return redirect('resource_detail', pk=resource.pk)
    else:
        form = ResourceForm()
    return render(request, 'resources/resource_create.html', {'form': form})
