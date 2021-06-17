from django.contrib import admin

from project_api.models import Article, Comment, Category, ArticleImages

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(ArticleImages)