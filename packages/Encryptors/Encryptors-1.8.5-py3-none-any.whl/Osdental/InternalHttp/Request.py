import re
import asyncio
from json import dumps
from datetime import datetime
from fastapi import Request
from tzlocal import get_localzone
from Osdental.ServicesBus.TaskQueue import task_queue
from Osdental.Handlers.Instances import environment, microservice_name, microservice_version, aes
from Osdental.Handlers.DBSecurityQuery import DBSecurityQuery
from Osdental.Shared.Enums.Constant import Constant

class CustomRequest:

    def __init__(self, request: Request):
        self.request = request
        self.local_tz = get_localzone()

    async def send_to_service_bus(self) -> None:
        legacy = await DBSecurityQuery.get_legacy_data()
        message_in = await self.request.json()  
        request_data = Constant.DEFAULT_EMPTY_VALUE  
        match = re.search(r'data:\s*"([^"]+)"', message_in.get('query', ''))
        if match:
            encrypted_data = match.group(1)
            request_data = aes.decrypt(legacy.aes_key_user, encrypted_data)

        message_json = {
            'idMessageLog': self.request.headers.get('Idmessagelog'),
            'type': Constant.RESPONSE_TYPE_REQUEST,
            'environment': environment,
            'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
            'header': dumps(dict(self.request.headers)),
            'microServiceUrl': str(self.request.url),
            'microServiceName': microservice_name,
            'microServiceVersion': microservice_version,
            'serviceName': message_in.get('operationName'),
            'machineNameUser': self.request.headers.get('Machinenameuser'),
            'ipUser': self.request.headers.get('Ipuser'),
            'userName': self.request.headers.get('Username'),
            'localitation': self.request.headers.get('Localitation'),
            'httpMethod': self.request.method,
            'httpResponseCode': Constant.DEFAULT_EMPTY_VALUE,
            'messageIn': request_data,
            'messageOut': Constant.DEFAULT_EMPTY_VALUE,
            'errorProducer': Constant.DEFAULT_EMPTY_VALUE,
            'auditLog': Constant.MESSAGE_LOG_INTERNAL,
            'batch': Constant.DEFAULT_EMPTY_VALUE
        }
        await task_queue.enqueue(message_json)