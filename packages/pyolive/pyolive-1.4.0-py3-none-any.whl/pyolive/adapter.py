import os
import pika
from .config import Config


class Adapter:
    EXCHANGE_ACTION = "action"
    EXCHANGE_CONTROL = "control"
    EXCHANGE_METRIC = "metric"
    EXCHANGE_LOGS = "logs"

    def __init__(self, agent_logger):
        self.connection = None
        self.channel = None
        self.logger = agent_logger

    def _get_connection(self):
        ip, port, username, password = self.load_broker_config()
        if ip is None:
            return None
        credentials = pika.PlainCredentials(username, password)

        for i in range(len(ip)):
            parameters = pika.ConnectionParameters(ip[i], port, '/', credentials)
            try:
                return pika.BlockingConnection(parameters)
            except:
                continue
        return None

    def open(self):
        self.connection = self._get_connection()
        if self.connection is None:
            self.logger.error("main, adapter connection failed")
            return False
        self.channel = self.connection.channel()
        return True

    def close(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except:
                pass
            self.connection = None

    def publish(self, exchange, routing_key, body):
        try:
            self.channel.basic_publish(
                exchange=exchange, routing_key=routing_key, body=body)
            self.logger.debug("adapter, publish: (%s : %s) %s", exchange, routing_key, body)
        except Exception as e:
            self.logger.warning("main, adapter: (%s : %s), %s", exchange, routing_key, e)

    def start_consume(self, namespace, callback):
        queue_name = self.get_queue_name(namespace)
        if queue_name is None:
            self.logger.warning("main, adapter: cannot get queue name")
            return
        try:
            self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        except Exception as e:
            self.logger.error("main, adapter: basic_consume, %s", e)
            return
        try:
            self.channel.start_consuming()
        except Exception as e:
            self.logger.error("main, adapter: start_consuming, %s", e)
            self.close()

    def stop_consume(self):
        self.channel.stop_consuming()

    def load_broker_config(self):
        config = Config('athena-env.yaml')
        hosts = config.get_value('broker/hosts')
        port = config.get_value('broker/amqp-port')
        username = config.get_value('broker/username')
        password = config.get_value('broker/password')
        return hosts, port, username, password

    def get_queue_name(self, namespace):
        subsystem = namespace.split('.')[0]
        module = namespace.split('.')[1]
        config = Config('athena-mq.yaml')
        str = config.get_value(subsystem)
        for s in str:
            if module == s.split(':')[1]:
                return 'ovq.' + subsystem + '-' + s.split(':')[0]
        return None
