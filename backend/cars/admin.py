from django.contrib import admin

from cars.models import Car, CarBody, CarComponents, Components


class CarComponentsInline(admin.TabularInline):
    model = CarComponents
    min_value = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'car_body', 'creation_date')
    inlines = [CarComponentsInline]


@admin.register(Components)
class Components(admin.ModelAdmin):
    list_display = ('name', 'manufacturer_country')


@admin.register(CarBody)
class CarBodyAdmin(admin.ModelAdmin):
    list_display = ('type', 'color', 'slug', 'vin_code')
    prepopulated_fields = {'slug': ('type',)}
