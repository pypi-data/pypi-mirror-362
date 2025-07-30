import os
import threading
import time
from .context import JobContext
from .status import AppStatus


class Worker(threading.Thread):
    def __init__(self, resource, channel, agent_logger, app_logger, context:JobContext):
        super().__init__()
        self.daemon = True
        self.resource = resource
        self.channel = channel
        self.agent_logger = agent_logger
        self.app_logger = app_logger
        self.context = context

    def run(self):
        try:
            r = self.resource(logger=self.app_logger,
                              channel=self.channel,
                              context=self.context)
        except Exception as e:
            self.agent_logger.error("init fail %s [%s] (%s:%s)", ...)
            self.app_logger.error("main: jobid[%s] - resource init failed: %s", ...)
            self.channel.publish_notify(self.context, 'job suspend', 7)
            return

        # joblog start message
        tm_st = int(time.time())
        self.channel.publish_notify(self.context, 'job start', 2)
        self.agent_logger.info("start %s [%s] (%s:%s)",
                               self.context.action_app, self.context.job_id,
                               self.context.regkey, self.context.action_id)
        self.app_logger.info("main: jobid[%s]", self.context.job_id)

        files = self.context.get_fileset()
        for _f in files:
            try:
                _sz = os.path.getsize(_f)
            except FileNotFoundError:
                _sz = -1
            self.app_logger.info("main: in-file (%s, %d)", _f, _sz)

        """user main function invoke
        return value
            success = 0
            failure = 1
        """
        try:
            rt = r.app_main()
        except Exception as e:
            self.channel.publish_notify(self.context, 'job suspend', 7)
            self.agent_logger.error("suspend %s [%s] (%s:%s)",
                                   self.context.action_app, self.context.job_id,
                                   self.context.regkey, self.context.action_id)
            self.app_logger.error("main: jobid[%s], %s", self.context.job_id, e)
            return

        if rt == AppStatus.OK:
            tm_ed = int(time.time())

            files = self.context.get_fileset()
            for _f in files:
                try:
                    _sz = os.path.getsize(_f)
                except FileNotFoundError:
                    _sz = -1
                self.app_logger.info("main: out-file (%s, %d)", _f, _sz)

            self.agent_logger.info("end   %s [%s] (%s:%s)",
                                   self.context.action_app, self.context.job_id,
                                   self.context.regkey, self.context.action_id)
            self.app_logger.info("main: status is success")
            self.channel.publish_job(self.context)
            self.channel.publish_notify(self.context, 'job end, success', 4, tm_ed-tm_st)
        elif rt == AppStatus.FIN:
            self.agent_logger.warn("fin   %s [%s] (%s:%s)",
                                   self.context.action_app, self.context.job_id,
                                   self.context.regkey, self.context.action_id)
            self.app_logger.warn("main: status is finish")
            self.channel.publish_notify(self.context, 'job end, finish', 7)
        else:
            self.agent_logger.error("end   %s [%s] (%s:%s)",
                                   self.context.action_app, self.context.job_id,
                                   self.context.regkey, self.context.action_id)
            self.app_logger.error("main: status is failure")
            self.channel.publish_notify(self.context, 'job end, failed', 7)
