#coding: utf-8

import json
import time
from azure.servicebus import ServiceBusService
import os

#azure service bus
key_name = 'xxxxx' # SharedAccessKeyName from Azure portal
key_value = 'xxxxxxxxx' # SharedAccessKey from Azure portal
service_namespace = 'xxxx'

hostid = os.popen('hostid').read().strip()
sbs = ServiceBusService(service_namespace,
                        shared_access_key_name=key_name,
                        shared_access_key_value=key_value)

datetime = os.popen('date +"%F %H:%M:%S %z"').read().strip()
jsontsl2561 = os.popen('python tsl2561_lux.py').read().strip()
#jsonadxl345 = os.popen('python adxl345.py').read().strip()
#jsonhdc1000 = os.popen('python hdc1000.py').read().strip()
jsonbme280 = os.popen('python bme280.py').read().strip()

dict = {}
dict["Date"] = datetime
dict["DeviceId"] = hostid
dict.update(json.loads(jsontsl2561))
#dict.update(json.loads(jsonadxl345))
#dict.update(json.loads(jsonhdc1000))
dict.update(json.loads(jsonbme280))
enc = json.dumps(dict)
print enc
sbs.send_event('ev4raspit01', enc)

