from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
import channels
from main.models import *





@receiver(post_save, sender=message)
def message_notification(sender, instance, created, **kwargs):
    '''
    Sends job status to the browser when a Job is modified
    '''
    if created:
        current_chat = instance.chat
        for i in current_chat.user.all():
            if instance.user.id != i.id:
                group_name = f'notificate{i.id}'
                text = instance.text
                if len(text) > 57:
                    text = text[:57] + '...'
                context = {'message': text, 'from_user': instance.user}
                rendered_msg_notif = render_to_string('patterns/message_notification.html', context)
                msgg = {
                    'html': rendered_msg_notif,
                }
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        'type':'send_notif',
                        'text': msgg
                    }
                )



