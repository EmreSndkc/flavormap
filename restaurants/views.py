from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Category, Review
from .forms import UserRegisterForm, RestaurantForm, ReviewForm


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
    location_query = request.GET.get('location')

    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    if price_range:
        restaurants = restaurants.filter(price_range=price_range)
    if search_query:
        restaurants = restaurants.filter(name__icontains=search_query)
    if location_query:
        restaurants = restaurants.filter(address__icontains=location_query)

    context = {
        'restaurants': restaurants,
        'categories': categories,
        'selected_category': category_id,
        'selected_price': price_range,
        'search_query': search_query,
        'location_query': location_query,
    }
    return render(request, 'restaurants/restaurant_list.html', context)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(
        Restaurant.objects.prefetch_related('menu_items', 'reviews__user'),
        pk=pk,
    )
    
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = restaurant.reviews.filter(user=request.user).exists()
        
    if request.method == 'POST' and request.user.is_authenticated and not user_has_reviewed:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.save()
            return redirect('restaurants:restaurant_detail', pk=restaurant.pk)
    else:
        form = ReviewForm()
        
    context = {
        'restaurant': restaurant,
        'menu_items': restaurant.menu_items.all(),
        'reviews': restaurant.reviews.all(),
        'form': form,
        'user_has_reviewed': user_has_reviewed,
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
        form = RestaurantForm(request.POST, request.FILES)
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
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
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

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        return HttpResponseForbidden("Bu yorumu silme yetkiniz yok.")
        
    restaurant_pk = review.restaurant.pk
    if request.method == 'POST':
        review.delete()
        return redirect('restaurants:restaurant_detail', pk=restaurant_pk)
        
    return render(request, 'restaurants/review_confirm_delete.html', {'review': review})

@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        return HttpResponseForbidden("Bu yorumu düzenleme yetkiniz yok.")
        
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('restaurants:restaurant_detail', pk=review.restaurant.pk)
    else:
        form = ReviewForm(instance=review)
        
    return render(request, 'restaurants/review_form.html', {'form': form, 'review': review})
