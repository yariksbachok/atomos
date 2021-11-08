from django.contrib import admin

from .models import *



admin.site.register(all_posts)
admin.site.register(likes)
admin.site.register(hidden_posts)
admin.site.register(user_profile)
admin.site.register(PostImage)
admin.site.register(complain)
admin.site.register(chat)
admin.site.register(message)