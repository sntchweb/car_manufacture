from django.contrib import admin

from cars.models import Car, CarBody, CarComponents, Components


class CarComponentsInline(admin.TabularInline):
    model = CarComponents
    min_value = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'vin', 'employee', 'car_body', 'creation_date')
    search_fields = ('vin', 'employee__first_name', 'employee__last_name')
    list_filter = ('car_body', 'employee__first_name', 'employee__last_name')
    inlines = [CarComponentsInline]

    def vin(self, obj):
        return ''.join(str(obj.vin_code).split('-')).upper()
    vin.short_description = 'VIN-код'


@admin.register(Components)
class Components(admin.ModelAdmin):
    list_display = ('name', 'manufacturer_country')
    search_fields = ('name', 'manufacturer_country')
    list_filter = ('name', 'manufacturer_country', )


@admin.register(CarBody)
class CarBodyAdmin(admin.ModelAdmin):
    list_display = ('type', 'color', 'slug')
    search_fields = ('type', 'color')
    prepopulated_fields = {'slug': ('type',)}
