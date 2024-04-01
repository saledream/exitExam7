from django.contrib import admin 

class SuperuserAwareModelAdmin(admin.ModelAdmin):
    superuser_fields = None
    superuser_fieldsets = None

    def get_fieldsets(self, request, obj = None):
        if request.user.is_superuser and self.superuser_fieldsets:
            return (self.fieldsets or tuple()) + self.superuser_fieldsets
        return super(SuperuserAwareModelAdmin, self).get_fieldsets(request, obj)

    def get_fields(self, request, obj = None):
        if request.user.is_superuser and self.superuser_fields:
            return (self.fields or tuple()) + self.superuser_fields
        return super(SuperuserAwareModelAdmin, self).get_fields(request, obj)