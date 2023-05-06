from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')     # поля на которые мы можем кликнуть и перейти на статью
    search_fields = ('title',)    # по каким полям может происходить поиск информации
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'category', 'branding', 'saleornew', 'content', 'photo', 'get_html_photo',
              'is_published', 'time_create', 'time_update')  # порядок редактируемых полей
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True  # появляется панель сверху 'удалить', 'сохранить' и т.д.

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50")
    get_html_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class PostPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_html_photo', 'product')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=30")
    get_html_photo.short_description = 'Фото'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Branding)
admin.site.register(SaleorNew)
admin.site.register(PostPhoto, PostPhotoAdmin)


