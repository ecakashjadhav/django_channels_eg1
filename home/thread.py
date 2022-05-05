import threading
import time
import random
from .models import *
from channels.layers import get_channel_layer
from faker import Faker
fake = Faker()
from asgiref.sync import async_to_sync

class CreateStudentThread(threading.Thread):
    
    def __init__(self , total):
        self.total = total
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            print("Thread execution startted")
            channel_layer = get_channel_layer()
            current_total = 0
            for i in range(self.total):
                current_total +=1
                student_obj = Students.objects.create(student_name = fake.name(),
                                                        student_email = fake.email(),
                                                        address = fake.address(),
                                                        age = random.randint(10,50))
                # print(f'We are inside first thread {i}')
                # time.sleep(1)
                data = {'current_total': current_total,'total':self.total,'student_name':student_obj.student_name, 'student_email':student_obj.student_email,'address':student_obj.address,'student_age': str(student_obj.age)}
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'new_consumer_group', {
                        'type':'send_notification',
                        'value':json.dumps(data)
                    }
                ) 
        except Exception as e:
            print(e)