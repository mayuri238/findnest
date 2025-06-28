from django.shortcuts import render, get_object_or_404
from .models import Property
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
from django.shortcuts import render, get_object_or_404
from .models import Property
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from listings.views import property_detail

from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                f"New Inquiry from {form.cleaned_data['name']}",
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return render(request, 'listings/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'listings/contact.html', {'form': form})



def property_search(request):
    location = request.GET.get('location')
    max_price = request.GET.get('max_price')
    properties = Property.objects.all()
    
    if location:
        properties = properties.filter(location__icontains=location)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    
    return render(request, 'listings/search_results.html', {'properties': properties})

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


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'listings/detail.html', {'property': property})