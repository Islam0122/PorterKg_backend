from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, GuestProfile, DriverProfile, Car, CarImage


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_verified', 'auth_type', 'is_active']
    list_filter = ['role', 'is_verified', 'auth_type', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-id']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {
            'fields': ('role', 'is_verified', 'auth_type', 'is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'auth_type'),
        }),
    )


@admin.register(GuestProfile)
class GuestProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone_number']
    list_filter = ['created']
    readonly_fields = ['created']


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    readonly_fields = ['created']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['driver', 'marka', 'model', 'color', 'year', 'number_plate']
    search_fields = ['driver__user__email', 'marka', 'model', 'number_plate']
    list_filter = ['fuel_type', 'year', 'created']
    readonly_fields = ['created', 'modified']
    inlines = [CarImageInline]


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'rating', 'experience_years', 'verified_driver', 'created']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone_number', 'driver_license_number']
    list_filter = ['verified_driver', 'experience_years', 'created']
    readonly_fields = ['created', 'rating']

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'phone_number', 'bio')
        }),
        ('Водительские данные', {
            'fields': ('driver_license_number', 'driver_license_category', 'experience_years')
        }),
        ('Статистика', {
            'fields': ('rating', 'verified_driver', 'created')
        }),
    )


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'created']
    list_filter = ['created']
    readonly_fields = ['created']