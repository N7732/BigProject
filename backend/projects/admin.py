from django.contrib import admin
from .models import project , task , comment , attachment , project_member , milestone , time_log


# Register your models here.
admin.site.register(project)
admin.site.register(task)      
admin.site.register(comment)
admin.site.register(attachment)
admin.site.register(project_member)
admin.site.register(milestone)
admin.site.register(time_log)

