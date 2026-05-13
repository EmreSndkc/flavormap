from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db import transaction, IntegrityError
from django.db.models import Avg, Count, Q
from .models import Restaurant, Category, Review, MenuItem, ContactMessage, OpeningHours
from .forms import UserRegisterForm, RestaurantForm, ReviewForm, ReviewReplyForm, MenuItemForm, OpeningHoursFormSet


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
        .annotate(
            avg_rating=Avg('reviews__stars', filter=Q(reviews__parent__isnull=True)),
            review_count=Count('reviews', filter=Q(reviews__parent__isnull=True)),
        )
    )
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    price_range = request.GET.get('price')
    search_query = request.GET.get('q')
    location_query = request.GET.get('location')
    sort = request.GET.get('sort', 'name')
    min_rating_raw = request.GET.get('min_rating')
    has_photo = request.GET.get('has_photo')

    # Min puanı sayısala dönüştür (geçersiz değerleri yoksay)
    min_rating = None
    if min_rating_raw:
        try:
            value = float(min_rating_raw)
            if 1 <= value <= 5:
                min_rating = value
        except (TypeError, ValueError):
            min_rating = None

    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    if price_range:
        restaurants = restaurants.filter(price_range=price_range)
    if search_query:
        restaurants = restaurants.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    if location_query:
        restaurants = restaurants.filter(address__icontains=location_query)
    if min_rating is not None:
        restaurants = restaurants.filter(avg_rating__gte=min_rating)
    if has_photo:
        restaurants = restaurants.exclude(photo='').exclude(photo__isnull=True)

    if sort == 'rating':
        restaurants = restaurants.order_by('-avg_rating', '-review_count', 'name')
    elif sort == 'newest':
        restaurants = restaurants.order_by('-created_at')
    else:
        restaurants = restaurants.order_by('name')

    # Filtre query string'ini koru (page parametresi hariç)
    qs_params = request.GET.copy()
    qs_params.pop('page', None)
    querystring = qs_params.urlencode()

    paginator = Paginator(restaurants, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'restaurants': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'querystring': querystring,
        'total_count': paginator.count,
        'categories': categories,
        'selected_category': category_id,
        'selected_price': price_range,
        'selected_sort': sort,
        'search_query': search_query,
        'location_query': location_query,
        'selected_min_rating': min_rating_raw or '',
        'selected_has_photo': has_photo or '',
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
            try:
                with transaction.atomic():
                    review = form.save(commit=False)
                    review.restaurant = restaurant
                    review.user = request.user
                    review.save()
                messages.success(request, "Yorumunuz eklendi.")
                return redirect('restaurants:restaurant_detail', pk=restaurant.pk)
            except IntegrityError:
                messages.error(request, "Bu restorana zaten yorum yapmışsınız.")
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
    # Aynı kullanıcı aynı yoruma çok kez cevap yazmasın (spam koruması)
    already_replied = Review.objects.filter(
        parent=parent_review,
        user=request.user,
    ).exists()
    if already_replied:
        messages.error(request, "Bu yoruma zaten cevap yazmışsınız.")
        return redirect('restaurants:restaurant_detail', pk=parent_review.restaurant.pk)

    form = ReviewReplyForm(request.POST)
    if form.is_valid():
        try:
            with transaction.atomic():
                reply = form.save(commit=False)
                reply.restaurant = parent_review.restaurant
                reply.parent = parent_review
                reply.user = request.user
                reply.save()
            messages.success(request, "Cevabınız eklendi.")
        except IntegrityError:
            messages.error(request, "Cevap eklenirken bir hata oluştu, lütfen tekrar deneyin.")
    else:
        messages.error(request, "Cevap boş olamaz.")
    return redirect('restaurants:restaurant_detail', pk=parent_review.restaurant.pk)


@login_required
def opening_hours_manage(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
    if restaurant.creator != request.user:
        return HttpResponseForbidden("Bu restoranın saatlerini düzenleme yetkiniz yok.")
    if restaurant.status != Restaurant.STATUS_APPROVED:
        return HttpResponseForbidden("Çalışma saatleri eklemek için restoran onaylanmış olmalı.")

    if request.method == 'POST':
        formset = OpeningHoursFormSet(request.POST, instance=restaurant)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Çalışma saatleri güncellendi.")
            return redirect('restaurants:restaurant_detail', pk=restaurant.pk)
    else:
        formset = OpeningHoursFormSet(instance=restaurant)
    return render(
        request,
        'restaurants/opening_hours_form.html',
        {'formset': formset, 'restaurant': restaurant},
    )


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


def _build_profile_context(request, profile_user):
    """Profil sayfası için ortak bağlamı üretir.

    Kendi profilini görüntüleyen kullanıcı her şeyi görür; başka bir
    kullanıcının profili görüntüleniyorsa sadece onaylı restoranlar ve
    ana yorumlar (cevaplar değil) listelenir.
    """
    is_own_profile = request.user.is_authenticated and request.user.pk == profile_user.pk

    user_reviews = (
        profile_user.reviews
        .select_related('restaurant')
        .order_by('-date')
    )
    if not is_own_profile:
        user_reviews = user_reviews.filter(
            parent__isnull=True,
            restaurant__status=Restaurant.STATUS_APPROVED,
        )

    created_restaurants = (
        profile_user.created_restaurants
        .select_related('category')
        .order_by('-created_at')
    )
    if not is_own_profile:
        created_restaurants = created_restaurants.filter(status=Restaurant.STATUS_APPROVED)

    return {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
        'user_reviews': user_reviews,
        'created_restaurants': created_restaurants,
    }


@login_required
def profile(request):
    context = _build_profile_context(request, request.user)
    return render(request, 'registration/profile.html', context)


@login_required
def favorites_list(request):
    restaurants = (
        request.user.favorite_restaurants
        .filter(status=Restaurant.STATUS_APPROVED)
        .select_related('category')
        .annotate(
            avg_rating=Avg('reviews__stars', filter=Q(reviews__parent__isnull=True)),
            review_count=Count('reviews', filter=Q(reviews__parent__isnull=True)),
        )
        .order_by('name')
    )
    return render(request, 'restaurants/favorites_list.html', {'restaurants': restaurants})


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    context = _build_profile_context(request, profile_user)
    return render(request, 'registration/profile.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        message = (request.POST.get('message') or '').strip()
        if not name or not email or not message:
            messages.error(request, "Lütfen tüm alanları doldurun.")
        else:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, "Mesajınız alındı, en kısa sürede dönüş yapacağız.")
            return redirect('restaurants:contact')
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
        try:
            with transaction.atomic():
                restaurant.delete()
                if photo:
                    transaction.on_commit(lambda: photo.delete(save=False))
            messages.success(request, "Restoran başarıyla silindi.")
            return redirect('restaurants:restaurant_list')
        except IntegrityError:
            messages.error(request, "Restoran silinirken bir hata oluştu, lütfen tekrar deneyin.")
            return redirect('restaurants:restaurant_detail', pk=restaurant.pk)
        
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
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, "Yorumunuz güncellendi.")
                return redirect('restaurants:restaurant_detail', pk=review.restaurant.pk)
            except IntegrityError:
                messages.error(request, "Yorum güncellenirken bir hata oluştu.")
                return redirect('restaurants:restaurant_detail', pk=review.restaurant.pk)
    else:
        form = form_class(instance=review)
        
    return render(request, 'restaurants/review_form.html', {'form': form, 'review': review})
