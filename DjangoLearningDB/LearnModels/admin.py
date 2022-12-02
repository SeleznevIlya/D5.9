from django.contrib import admin
from .models import Post, Category, Author, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('header', 'author', )
    list_filter = ('category', 'post_rating', 'type_of_post')
    search_fields = ('header', 'category')

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)




