import threading


class Heartbeat:
    def __init__(self, channel, namespace, worker_name):
        self.channel = channel
        self.namespace = namespace
        self.worker_name = worker_name
        self.timer = None

    def start(self):
        self.channel.publish_heartbeat(self.worker_name)
        self.timer = threading.Timer(1, self.start)
        self.timer.start()

    def stop(self):
        self.timer.cancel()