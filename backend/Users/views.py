from django.shortcuts import render
from .form import UserInformForm
from .models import userinform


# Create your views here.

def profile_view(request):
    if request.method == 'POST':
        form = UserInformForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserInformForm(instance=request.user)
    
    return render(request, 'Users/profile.html', {'form': form})

def user_list_view(request):
    users = userinform.objects.all()
    return render(request, 'Users/user_list.html', {'users': users}) 

def user_detail_view(request, user_id):
    user = userinform.objects.get(id=user_id)
    return render(request, 'Users/user_detail.html', {'user': user})    

from django.shortcuts import render, redirect
from .form import UserInformForm    

def edit_profile_view(request):
    if request.method == 'POST':
        form = UserInformForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile view after saving
    else:
        form = UserInformForm(instance=request.user)
    
    return render(request, 'Users/edit_profile.html', {'form': form})

