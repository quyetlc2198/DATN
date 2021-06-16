from django.contrib import admin

# Register your models here.
from customer.models import Comments, Signup



class SignUpAdmin(admin.ModelAdmin):
    list_display = ['id','user','contact']


admin.site.register(Signup,SignUpAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'create_date', 'evaluation']
    list_filter = ['category']


admin.site.register(Comments,CommentAdmin)



