import os
import threading
import time
import socket
import json
from queue import Queue
from typing import Any, Dict
from .adapter import Adapter
from .context import JobContext


class Channel(threading.Thread):
    def __init__(self, agent_logger: Any, namespace: str, alias: str, devel: bool = False):
        super().__init__()
        self.daemon: bool = True
        self.que: Queue = Queue()
        self.hostname: str = socket.gethostname()
        self.logger: Any = agent_logger
        self.namespace: str = namespace
        self.alias: str = alias
        self.runnable: bool = True
        self.devel: bool = devel

    def stop(self) -> None:
        self.runnable = False

    def run(self) -> None:
        adapter = Adapter(self.logger)
        if not adapter.open():
            self.logger.warning("main, channel: can not open adapter")
            return

        self.logger.debug("main, channel manager start")
        while self.runnable:
            if self.que.qsize() > 0:
                d: Dict[str, Any] = self._dequeue()
                adapter.publish(d['exchange'], d['routing_key'], d['body'])
            else:
                time.sleep(5 / 1000)
        self.logger.debug("main, channel manager stop")
        adapter.close()

    def _dequeue(self) -> Dict[str, Any]:
        return self.que.get()

    def _enqueue(self, exchange: str, routing_key: str, json_msg: str) -> None:
        data: Dict[str, str] = {
            'exchange': exchange,
            'routing_key': routing_key,
            'body': json_msg
        }
        self.que.put(data)

    def publish_heartbeat(self, worker_name: str) -> None:
        if self.devel:
            return

        data: Dict[str, Any] = {
            'metric-type': 4,
            'metric-status': 0,
            'metric-name': self.alias,
            'namespace': self.namespace,
            'process': worker_name,
            'psn': 0,
            'hostname': self.hostname,
            'timestamp': time.time()
        }
        routing_key = f'sys.{self.namespace}.heartbeat.agent'
        self._enqueue(Adapter.EXCHANGE_METRIC, routing_key, json.dumps(data))

    def publish_job(self, context: JobContext) -> None:
        if self.devel:
            return

        # 메시지가 없은 경우
        if not context.messages:
            context.msgbox = None
            data: Dict[str, Any] = {
                'regkey': context.regkey,
                'topic': context.topic,
                'action-id': context.action_id,
                'action-ns': context.action_ns,
                'action-app': context.action_app,
                'action-params': context.action_params,
                'job-id': context.job_id,
                'job-hostname': context.job_hostname,
                'job-seq': context.job_seq,
                'timestamp': context.timestamp,
                'filenames': context.filenames,
                'msgbox': context.msgbox
            }

            self._nextjob(context, data)
            return

        # messages가 하나 이상 있는 경우 반복 전송
        while context.messages:
            message = context.messages.pop(0)
            context.msgbox = {
                'type': 'ascii',
                'size': len(message),
                'data': message
            }

            data: Dict[str, Any] = {
                'regkey': context.regkey,
                'topic': context.topic,
                'action-id': context.action_id,
                'action-ns': context.action_ns,
                'action-app': context.action_app,
                'action-params': context.action_params,
                'job-id': context.job_id,
                'job-hostname': context.job_hostname,
                'job-seq': context.job_seq,
                'timestamp': context.timestamp,
                'filenames': context.filenames,
                'msgbox': context.msgbox
            }

            self._nextjob(context, data)

    def _nextjob(self, context: JobContext, data: Dict):
        if context.timestamp == 0:
            routing_key = f'job.des.msm.early.{context.topic}'
        else:
            routing_key = f'job.des.msm.now.{context.topic}'

        json_str: str = json.dumps(data)
        self.logger.debug("sent message, %s", json_str)
        self._enqueue(Adapter.EXCHANGE_ACTION, routing_key, json_str)

    def publish_notify(self, context: JobContext, text: str = '', status: int = 3, elapsed: int = 0) -> None:
        """status code
        STATUS_JOB_CREATED    1  /* 작업생성 */
        STATUS_JOB_STARTED    2  /* 작업시작 */
        STATUS_JOB_RUNNING    3  /* 작업수행중 */
        STATUS_JOB_ENDED      4  /* 작업종료(정상) */
        STATUS_JOB_FINISHED   5  /* 액션트리 종료 */
        STATUS_JOB_ARBORTED   6  /* 작업강제중단 */
        STATUS_JOB_FAILED     7  /* 작업오류 */
        STATUS_JOB_RETRY      8  /* 작업오류 재처리 */
        """

        if self.devel:
            return

        data: Dict[str, Any] = {
            'job-id': context.job_id,
            'job-status': status,
            'job-elapsed': elapsed,
            'reg-subject': context.regkey.split('@')[0],
            'reg-version': context.regkey.split('@')[1],
            'reg-topic': context.topic,
            'action-id': context.action_id,
            'action-app': context.action_app,
            'action-ns': context.action_ns,
            'hostname': self.hostname,
            'timestamp': int(time.time())
        }

        filesize: int = 0
        for file in context.filenames:
            try:
                filesize += os.stat(file).st_size
            except Exception:
                continue

        data['filesize'] = filesize
        data['filenames'] = context.filenames
        data['err-code'] = 0
        data['err-mesg'] = text

        routing_key = f'log.{context.action_ns}'
        self._enqueue(Adapter.EXCHANGE_LOGS, routing_key, json.dumps(data))