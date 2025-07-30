import base64
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union


@dataclass
class JobContext:
    regkey: str = ''
    topic: str = ''
    action_id: int = 0
    action_ns: str = ''
    action_app: str = 'ovm_hello_py'
    action_params: str = ''
    job_id: str = ''
    job_hostname: str = ''
    job_seq: int = 0
    timestamp: int = 0
    filenames: List[str] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)
    msgbox: Dict[str, Union[str, int]] = field(default_factory=dict)

    def __init__(self, message: Optional[Dict[str, Union[str, int, list, dict]]] = None, devel: bool = False):
        if not devel and message is not None:
            self.regkey = message['regkey']
            self.topic = message['topic']
            self.action_id = int(message['action-id'])
            self.action_ns = message['action-ns']
            self.action_app = message['action-app']
            self.action_params = message['action-params']
            self.job_id = message['job-id']
            self.job_hostname = message['job-hostname']
            self.job_seq = int(message['job-seq'])
            self.timestamp = int(message['timestamp'])
            self.filenames = message['filenames'][:]
            self.msgbox = message['msgbox']
        else:
            self.regkey = ''
            self.topic = ''
            self.action_id = 0
            self.action_ns = ''
            self.action_app = 'ovm_pytest'
            self.action_params = ''
            self.job_id = ''
            self.job_hostname = ''
            self.job_seq = 0
            self.timestamp = 0
            self.filenames = []
            self.msgbox = {}

    def get_param(self, key: str) -> str:
        pattern = re.compile(rf"{re.escape(key)}='(.*?)'")
        match = pattern.search(self.action_params)
        return match.group(1) if match else ''

    def get_fileset(self) -> List[str]:
        return self.filenames

    def get_msgbox(self) -> str:
        if self.msgbox == {}:
            return ''
        if self.msgbox.get('type') == 'binary':
            bstr = base64.b64decode(self.msgbox['data'])
            return bstr.decode('UTF-8')
        else:
            return self.msgbox.get('data', '')

    def set_param(self, param: Dict[str, Union[str, int]], devel: bool = False) -> None:
        if devel:
            self.action_params = '&'.join(f'{k}={v}' for k, v in param.items())

    def set_fileset(self, filename: str = "", devel: bool = False) -> None:
        if not filename.strip():
            self.filenames = []
            return

        if not devel:
            self.filenames.append(filename)
        else:
            self.filenames = filename.split(',')

    def set_msgbox(self, data: str) -> None:
        self.messages.append(data)
