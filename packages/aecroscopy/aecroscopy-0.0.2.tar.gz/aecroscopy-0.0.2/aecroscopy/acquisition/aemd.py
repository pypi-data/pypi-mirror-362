#Aecroscopy microscope device for bluesky (AEMD) base class
"""
This class should have the following sub-devices
- MotorX (piezo)
- MotorY (piezo)
- Detectors (photodector, lockins, etc.)
- Outputs (Waveforms to go to tip and/or sample, etc.)
"""
"""
from typing import Any, Callable


class AEMD_base(object):
    
    #Aecroscopy Microscope Device Base class for Bluesky
    #Class representing an AFM that can be used with bluesky
    
    def __init__(self):
        self.name = 'AEMD_Base_Class'
        self.parent = None
        self.conn = "None"

        ## the following properties are required for bluesky -> RE -> count
        self.position = 0.0 
        self.dial_position = 0.0        
        self.offset = 0.0  
        self.step_size = 1.0  
        self.sign = 1  
        

    def get(self, prop_name:str):
        return "100.0" 

    def set(self, prop_name:str, value:Any, wait_for_error:float=0):
        return self.conn.set("motor/{}/{}".format(self.name, prop_name), value, wait_for_error=wait_for_error)

    def _prop_getter_setter(self, name, readonly=False):
        def getter():
            return self.get(name)
        def setter(val):
            if readonly:
                raise Exception("Property is read-only")
            self.set(name, val)
        return property(getter, setter)


    def move(self, value:float, blocking:bool=True, callback:Callable=None):
        pass
     
    def subscribe(self, prop:str, callback:Callable, nowait:bool=False, timeout:float=1.0) -> bool:
        return "whatever"

    def unsubscribe(self, prop:str, callback:Callable) -> bool:
        return self.conn.unsubscribe("motor/{}/{}".format(self.name, prop), callback)

    def read(self):
       pass
    
    def describe(self):
        pass
    
    def trigger(self):
        status = 'No status for now'
        return status
    
    def set(self, position):
        self.status = "No Status"
        return self.status

"""
#RKV to do: create objects for motors, detectors, outputs, and add them to the base class. 