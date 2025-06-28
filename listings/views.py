from django.shortcuts import render, get_object_or_404
from .models import Property
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm

def home(request):
    properties = Property.objects.all()
    query = request.GET.get('q')
    min_rent = request.GET.get('min_rent')
    max_rent = request.GET.get('max_rent')

    if query:
        properties = properties.filter(address__icontains=query)
    if min_rent:
        properties = properties.filter(rent__gte=min_rent)
    if max_rent:
        properties = properties.filter(rent__lte=max_rent)

    return render(request, 'listings/home.html', {'properties': properties})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log them in after signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'listings/signup.html', {'form': form})


@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('home')
    else:
        form = PropertyForm()
    return render(request, 'listings/add_property.html', {'form': form})