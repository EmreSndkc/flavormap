from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Category
from .forms import UserRegisterForm, RestaurantForm


def home(request):
    featured_restaurants = Restaurant.objects.select_related('category').order_by('-created_at')[:6]
    categories = Category.objects.all()
    context = {
        'featured_restaurants': featured_restaurants,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def restaurant_list(request):
    restaurants = Restaurant.objects.select_related('category').order_by('name')
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    price_range = request.GET.get('price')
    search_query = request.GET.get('q')

    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    if price_range:
        restaurants = restaurants.filter(price_range=price_range)
    if search_query:
        restaurants = restaurants.filter(name__icontains=search_query)

    context = {
        'restaurants': restaurants,
        'categories': categories,
        'selected_category': category_id,
        'selected_price': price_range,
        'search_query': search_query,
    }
    return render(request, 'restaurants/restaurant_list.html', context)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(
        Restaurant.objects.prefetch_related('menu_items', 'reviews'),
        pk=pk,
    )
    context = {
        'restaurant': restaurant,
        'menu_items': restaurant.menu_items.all(),
        'reviews': restaurant.reviews.all(),
    }
    return render(request, 'restaurants/restaurant_detail.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('restaurants:home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.creator = request.user
            restaurant.save()
            return redirect('restaurants:restaurant_detail', pk=restaurant.pk)
    else:
        form = RestaurantForm()
    return render(request, 'restaurants/restaurant_form.html', {'form': form})

@login_required
def restaurant_update(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if restaurant.creator != request.user:
        return HttpResponseForbidden("Bu restoranı düzenleme yetkiniz yok.")
    
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurants:restaurant_detail', pk=restaurant.pk)
    else:
        form = RestaurantForm(instance=restaurant)
    
    return render(request, 'restaurants/restaurant_form.html', {'form': form, 'is_update': True})

@login_required
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if restaurant.creator != request.user:
        return HttpResponseForbidden("Bu restoranı silme yetkiniz yok.")
        
    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurants:restaurant_list')
        
    return render(request, 'restaurants/restaurant_confirm_delete.html', {'restaurant': restaurant})
