from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Resource
from .forms import ResourceForm

@login_required
def resource_list(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    return render(request, 'resources/resource_list.html', {'resources': resources})

@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/resource_detail.html', {'resource': resource})

@login_required
def resource_upload(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            return redirect('resource_detail', pk=resource.pk)
    else:
        form = ResourceForm()
    return render(request, 'resources/resource_upload.html', {'form': form})

@login_required
@user_passes_test(lambda u: u == get_object_or_404(Resource, pk=u.kwargs['pk']).uploaded_by)
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
