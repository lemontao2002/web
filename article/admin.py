#APP注册后台管理实体
from django.contrib import admin
from django.forms import ModelForm
from article.models import Author,Tag,Classification,Article,Comment
from article.widgets import Ueditor
# Register your models here.
#from django_summernote.admin import SummernoteModelAdmin
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Classification)

#class ArticleAdmin(SummernoteModelAdmin):
      #pass
admin.site.register(Comment)

#class ArticleAdmin(admin.ModelAdmin):
#      class Media:
#         js = (

#         '/static/tinymce/tinymce.min.js',
#         '/static/tinymce/config.js',
        
#         )
#      class Meta:
#        verbose_name = '文章'
#        verbose_name_plural = '文章'
#admin.site.register(Article,ArticleAdmin)



class ArticleForm(ModelForm):
      class Meta:
         model = Article
         fields = '__all__'
         widgets = {
             'content': Ueditor(),  
         }



class ArticleAdmin(admin.ModelAdmin):
     form = ArticleForm
     search_fields = ('content',)

admin.site.register(Article,ArticleAdmin)
