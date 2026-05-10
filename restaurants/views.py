from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Avg, Count, Q
from .models import Restaurant, Category, Review, MenuItem
from .forms import UserRegisterForm, RestaurantForm, ReviewForm, ReviewReplyForm, MenuItemForm


def home(request):
    featured_restaurants = (
        Restaurant.objects
        .filter(status=Restaurant.STATUS_APPROVED)
        .select_related('category')
        .order_by('-created_at')[:6]
    )
    top_rated_restaurants = (
        Restaurant.objects
        .filter(status=Restaurant.STATUS_APPROVED)
        .select_related('category')
        .annotate(
            avg_rating=Avg('reviews__stars', filter=Q(reviews__parent__isnull=True)),
            review_count=Count('reviews', filter=Q(reviews__parent__isnull=True)),
        )
        .filter(review_count__gt=0)
        .order_by('-avg_rating', '-review_count', 'name')[:6]
    )
    categories = Category.objects.all()
    context = {
        'featured_restaurants': featured_restaurants,
        'top_rated_restaurants': top_rated_restaurants,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def restaurant_list(request):
    restaurants = (
        Restaurant.objects
        .filter(status=Restaurant.STATUS_APPROVED)
        .select_related('category')
        .order_by('name')
    )
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
    restaurants = Restaurant.objects.prefetch_related('menu_items', 'reviews__user', 'opening_hours')
    if request.user.is_authenticated:
        restaurants = restaurants.filter(Q(status=Restaurant.STATUS_APPROVED) | Q(creator=request.user))
    else:
        restaurants = restaurants.filter(status=Restaurant.STATUS_APPROVED)

    restaurant = get_object_or_404(
        restaurants,
        pk=pk,
    )
    reviews = (
        restaurant.reviews
        .filter(parent__isnull=True)
        .select_related('user')
        .prefetch_related('replies__user')
    )

    user_has_reviewed = False
    if request.user.is_authenticated and restaurant.status == Restaurant.STATUS_APPROVED:
        user_has_reviewed = restaurant.reviews.filter(user=request.user, parent__isnull=True).exists()

    if (
        request.method == 'POST'
        and request.user.is_authenticated
        and restaurant.status == Restaurant.STATUS_APPROVED
        and not user_has_reviewed
    ):
        form = ReviewForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                review = form.save(commit=False)
                review.restaurant = restaurant
                review.user = request.user
                review.save()
            return redirect('restaurants:restaurant_detail', pk=restaurant.pk)
    else:
        form = ReviewForm()

    is_favorite = (
        request.user.is_authenticated
        and restaurant.favorited_by.filter(pk=request.user.pk).exists()
    )

    context = {
        'restaurant': restaurant,
        'menu_items': restaurant.menu_items.all(),
        'opening_hours': restaurant.opening_hours.all(),
        'reviews': reviews,
        'form': form,
        'reply_form': ReviewReplyForm(),
        'user_has_reviewed': user_has_reviewed,
        'is_favorite': is_favorite,
    }
    return render(request, 'restaurants/restaurant_detail.html', context)


@login_required
@require_POST
def toggle_favorite(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, status=Restaurant.STATUS_APPROVED)
    if restaurant.favorited_by.filter(pk=request.user.pk).exists():
        restaurant.favorited_by.remove(request.user)
    else:
        restaurant.favorited_by.add(request.user)
    return redirect('restaurants:restaurant_detail', pk=restaurant.pk)


@login_required
@require_POST
def review_reply_create(request, pk):
    parent_review = get_object_or_404(
        Review.objects.select_related('restaurant'),
        pk=pk,
        parent__isnull=True,
        restaurant__status=Restaurant.STATUS_APPROVED,
    )
    form = ReviewReplyForm(request.POST)
    if form.is_valid():
        with transaction.atomic():
            reply = form.save(commit=False)
            reply.restaurant = parent_review.restaurant
            reply.parent = parent_review
            reply.user = request.user
            reply.save()
    return redirect('restaurants:restaurant_detail', pk=parent_review.restaurant.pk)


@login_required
def menu_item_create(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
    if restaurant.creator != request.user:
        return HttpResponseForbidden("Bu restoranın menüsünü düzenleme yetkiniz yok.")
    if restaurant.status != Restaurant.STATUS_APPROVED:
        return HttpResponseForbidden("Menü eklemek için restoran başvurusu onaylanmış olmalı.")

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            return redirect('restaurants:restaurant_detail', pk=restaurant.pk)
    else:
        form = MenuItemForm()

    return render(
        request,
        'restaurants/menu_item_form.html',
        {'form': form, 'restaurant': restaurant},
    )


@login_required
def menu_item_update(request, pk):
    menu_item = get_object_or_404(MenuItem.objects.select_related('restaurant'), pk=pk)
    if menu_item.restaurant.creator != request.user:
        return HttpResponseForbidden("Bu menü öğesini düzenleme yetkiniz yok.")
    if menu_item.restaurant.status != Restaurant.STATUS_APPROVED:
        return HttpResponseForbidden("Menü düzenlemek için restoran başvurusu onaylanmış olmalı.")

    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('restaurants:restaurant_detail', pk=menu_item.restaurant.pk)
    else:
        form = MenuItemForm(instance=menu_item)

    return render(
        request,
        'restaurants/menu_item_form.html',
        {'form': form, 'restaurant': menu_item.restaurant, 'menu_item': menu_item, 'is_update': True},
    )


@login_required
def menu_item_delete(request, pk):
    menu_item = get_object_or_404(MenuItem.objects.select_related('restaurant'), pk=pk)
    if menu_item.restaurant.creator != request.user:
        return HttpResponseForbidden("Bu menü öğesini silme yetkiniz yok.")
    if menu_item.restaurant.status != Restaurant.STATUS_APPROVED:
        return HttpResponseForbidden("Menü silmek için restoran başvurusu onaylanmış olmalı.")

    restaurant = menu_item.restaurant
    if request.method == 'POST':
        menu_item.delete()
        return redirect('restaurants:restaurant_detail', pk=restaurant.pk)

    return render(
        request,
        'restaurants/menu_item_confirm_delete.html',
        {'menu_item': menu_item, 'restaurant': restaurant},
    )


@login_required
def profile(request):
    user_reviews = (
        request.user.reviews
        .select_related('restaurant')
        .order_by('-date')
    )
    favorite_restaurants = (
        request.user.favorite_restaurants
        .filter(status=Restaurant.STATUS_APPROVED)
        .select_related('category')
        .order_by('name')
    )
    created_restaurants = request.user.created_restaurants.select_related('category').order_by('-created_at')
    context = {
        'profile_user': request.user,
        'user_reviews': user_reviews,
        'favorite_restaurants': favorite_restaurants,
        'created_restaurants': created_restaurants,
    }
    return render(request, 'registration/profile.html', context)


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
            restaurant.status = Restaurant.STATUS_PENDING
            restaurant.save()
            messages.success(request, "Restoran başvurunuz alındı. Admin onayından sonra yayına alınacaktır.")
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
        photo = restaurant.photo
        with transaction.atomic():
            restaurant.delete()
            if photo:
                transaction.on_commit(lambda: photo.delete(save=False))
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

    form_class = ReviewReplyForm if review.parent_id else ReviewForm
    if request.method == 'POST':
        form = form_class(request.POST, instance=review)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect('restaurants:restaurant_detail', pk=review.restaurant.pk)
    else:
        form = form_class(instance=review)
        
    return render(request, 'restaurants/review_form.html', {'form': form, 'review': review})
