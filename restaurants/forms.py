from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurant, Review, MenuItem, OpeningHours

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='E-posta')

    class Meta:
        model = User
        fields = ['username', 'email']

class RestaurantForm(forms.ModelForm):
    MAX_PHOTO_SIZE_MB = 5

    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'address', 'phone', 'price_range', 'category', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'price_range': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and hasattr(photo, 'size'):
            if photo.size > self.MAX_PHOTO_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(
                    f"Fotoğraf {self.MAX_PHOTO_SIZE_MB}MB'dan büyük olamaz."
                )
        if photo and hasattr(photo, 'content_type') and photo.content_type:
            if not photo.content_type.startswith('image/'):
                raise forms.ValidationError("Lütfen geçerli bir görsel dosyası yükleyin.")
        return photo

class ReviewForm(forms.ModelForm):
    stars = forms.IntegerField(
        label='Yıldız',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5,
            'id': 'id_stars',
        }),
    )

    class Meta:
        model = Review
        fields = ['stars', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ReviewReplyForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Cevabınızı yazın...'}),
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Ana Yemek, Tatlı, İçecek'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


OpeningHoursFormSet = inlineformset_factory(
    Restaurant,
    OpeningHours,
    fields=['day_of_week', 'open_time', 'close_time', 'is_closed'],
    extra=7,
    max_num=7,
    can_delete=True,
    widgets={
        'day_of_week': forms.Select(attrs={'class': 'form-select'}),
        'open_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        'close_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        'is_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    },
)
