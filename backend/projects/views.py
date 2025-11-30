from django.shortcuts import redirect, render
from .form import projectInformForm
from .models import project

def project_list_view(request):
    projects = project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})    

def project_detail_view(request, project_id):
    project_instance = project.objects.get(id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project_instance})

def create_project_view(request):
    if request.method == 'POST':
        form = projectInformForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')  # Redirect to project list view after saving
    else:
        form = projectInformForm()
    
    return render(request, 'projects/create_project.html', {'form': form})

def edit_project_view(request, project_id):
    project_instance = project.objects.get(id=project_id)
    if request.method == 'POST':
        form = projectInformForm(request.POST, instance=project_instance)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project_id)  # Redirect to project detail view after saving
    else:
        form = projectInformForm(instance=project_instance)
    
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project_instance})

def delete_project_view(request, project_id):
    project_instance = project.objects.get(id=project_id)
    if request.method == 'POST':
        project_instance.delete()
        return redirect('project_list')  # Redirect to project list view after deletion
    return render(request, 'projects/delete_project.html', {'project': project_instance})

def dashboard_view(request):
    projects = project.objects.all()
    return render(request, 'projects/dashboard.html', {'projects': projects})

def search_projects_view(request):
    query = request.GET.get('q', '')
    projects = project.objects.filter(name__icontains=query)
    return render(request, 'projects/search_results.html', {'projects': projects, 'query': query})

def filter_projects_view(request):
    status = request.GET.get('status', '')
    if status:
        projects = project.objects.filter(status=status)
    else:
        projects = project.objects.all()
    return render(request, 'projects/filter_results.html', {'projects': projects, 'status': status})

# Create your views here.
