from django.contrib import admin

# Register your models here.
from .models import RoomMember
admin.site.register(RoomMember)

from .models import Post
admin.site.register(Post)

from .models import Notifications
admin.site.register(Notifications)

from .models import Notify
admin.site.register(Notify)