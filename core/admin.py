from django.contrib.admin import ModelAdmin, site
from core.models import MessageModel
from core.models import MessageModel, Group


class MessageModelAdmin(ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'
class GroupAdmin(ModelAdmin):
    readonly_fields = ('members','messages',)
    search_fields = ('id', 'name',)
    list_display = ('id', 'name',)
    list_display_links = ('id','name',)
    list_filter = ('name',)


site.register(MessageModel, MessageModelAdmin)

site.register(Group, GroupAdmin)