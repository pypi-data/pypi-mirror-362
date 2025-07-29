# coding=utf-8
import time
from typing import List, Optional
from smartpi import base_driver

#��������ȡ port:����P�˿ڣ�command:1:��ȡ��
#def get_value(port:bytes,command:bytes) -> Optional[bytes]:
#    ultrasonic_str=[0xA0, 0x06, 0x00, 0xBE]
#    ultrasonic_str[0]=0XA0+port
#    ultrasonic_str[2]=command 
#    response = base_driver.single_operate_sensor(ultrasonic_str)
#    if response:
#        return 0
#    else:
#        return -1
        
        
def get_value(port:bytes) -> Optional[bytes]:
    ultrasonic_str=[0xA0, 0x06, 0x00, 0xBE]
    ultrasonic_str[0]=0XA0+port
    ultrasonic_str[2]=1 
    response = base_driver.single_operate_sensor(ultrasonic_str)
    if response:
        return 0
    else:
        return -1
        