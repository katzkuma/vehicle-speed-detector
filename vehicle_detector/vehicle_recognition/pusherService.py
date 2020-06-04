
import pusher
from threading import Thread

class pusherService:
    def __init__(self):
        self.pusher_client = pusher.Pusher(
            app_id='982998',
            key='b65f086d00319eef857b',
            secret='0fffa578aabacabc1f2b',
            cluster='us2',
            ssl=True
        )

    # start the thread to read frames from the video stream     
    # def start(self):
    #     t = Thread(target=self.start_push, args=())
    #     t.daemon = True
    #     t.start()
    #     return self

    # start Pusher method
    def push(self, context):
        self.pusher_client.trigger('my-channel', 'my-event', {'message': context})




