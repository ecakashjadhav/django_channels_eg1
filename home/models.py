from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class Notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    notifications = models.TextField(max_length=200)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        notification_objs = Notifications.objects.filter(is_seen=False).count()
        data = {'count':notification_objs, 'current_notification':self.notifications}
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group', {
                'type':'send_notification',
                'value':json.dumps(data)
            }
        )
        super(Notifications,self).save(*args, **kwargs)

class Students(models.Model):
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    age = models.IntegerField()
    
    def __str__(self):
        return self.student_name


class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
