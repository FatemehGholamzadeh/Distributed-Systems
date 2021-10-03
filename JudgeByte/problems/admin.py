from django.contrib import admin
from problems.models import Problem

# class ProblemAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         obj.setter = request.user
#         super().save_model(request, obj, form, change)

admin.site.register(Problem)


# setter is only wdragon... fix this
