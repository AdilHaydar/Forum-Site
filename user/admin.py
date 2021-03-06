from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserPermission

User = get_user_model()
class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm
	list_display = ('username', 'email', 'admin', 'is_banned')
	list_filter = ('admin', 'active', 'is_banned')
	fieldsets = (
			('User info', {'fields' : ('username','email','birthday','password','avatar')}),
			('Permissions', {'fields' : ('admin','staff','active','is_banned')})
		)

	add_fieldsets = (
		(None, {
			'classes' : ('wide',),
			'fields' : ('username', 'email','birthday','avatar','password1','password2','active','staff','admin','is_banned')}
			),
		)

	search_fields = ('email','username')
	ordering = ('-last_login',)
	filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class UserPermissionAdmin(admin.ModelAdmin):
	list_display = ('user','permission')
	list_filter = ('permission',)


admin.site.register(UserPermission, UserPermissionAdmin)