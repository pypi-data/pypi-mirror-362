#Aecroscopy microscope device for bluesky (AEMD) base class
import asyncio
import time
import numpy as np
from typing import AsyncIterator
from ophyd_async.core import Device, AsyncStatus, soft_signal_rw
from ophyd.sim import det, flyer1, flyer2
from bluesky.plans import count
from bluesky.protocols import Movable, Readable, Flyable
from bluesky import RunEngine
from bluesky.preprocessors import fly_during_wrapper
from bluesky.plans import grid_scan, scan
from bluesky.callbacks.core import CallbackBase
from bluesky.callbacks.tiled_writer import TiledWriter
from tiled.client import from_uri
from tiled.structures.array import ArrayStructure
from tiled.structures.core import Spec

class AsyncAEMotor(Device, Movable, Readable):
    
    def __init__(self, name: str):
        super().__init__(name=name)
        self.pos = soft_signal_rw(float, initial_value=0.0, name=f"{name}_pos")

    def set(self, value):
        async def move():
            print(f"[{self.name}] Moving to {value}")
            ## execute afm_motor_sdk move
            # await asyncio.sleep(0.1) 
            await self.pos.set(value)            
        return AsyncStatus(move())
    
    async def read(self):
        return {self.name: {"value": await self.pos.get_value(), "timestamp": time.time()}}

    def describe(self):
        return {self.name: {"dtype": "number", "shape": [], "source": "afm_motor_sdk"}}
    
class AsyncAEDetector(Device, Flyable, Readable):
    def __init__(self, name: str, motor_x, shape=(1,)):
        super().__init__(name=name)
        self.signal = soft_signal_rw(np.ndarray, name=f"{name}_signal")
        self.shape = shape
        self.buffer = []
        self.acquiring = False
        self.acquisition_tasks = [] 
        object.__setattr__(self, "motor_x", motor_x)

    @AsyncStatus.wrap
    async def kickoff(self):
        print(f"[{self.name}] Kickoff starting...")
        self.buffer.clear()
        self.acquisition_tasks.clear()         
        self.acquiring = True        
        last_pos = None
    
        async def monitor_motor():
            nonlocal last_pos
            while self.acquiring:
                current_pos = await self.motor_x.pos.get_value()
                if current_pos != last_pos:
                    last_pos = current_pos
    
                    async def single_acquire(pos):
                        ## execute afm_detector_sdk acquisition
                        valf = np.random.randn(*self.shape).flatten()
                        valf[-1] = pos
                        val = valf.reshape(self.shape)
                        self.buffer.append((valf[-1], val, time.time()))
                        await asyncio.sleep(2)  ## simulate detector delay processing
                        await self.signal.set(val)                        
                        print(f"[{self.name}] Acquisition done at (delayed): {pos}: {val}")
    
                    task = asyncio.create_task(single_acquire(current_pos))
                    self.acquisition_tasks.append(task)
                # await asyncio.sleep(0.01) 

        asyncio.create_task(monitor_motor())

    def complete(self):
        async def _wait_until_done():
            if self.acquisition_tasks:
                await asyncio.gather(*self.acquisition_tasks)  ## ensure all acquisition finishes
            self.acquiring = False  ## no more monitoring required
        return AsyncStatus(_wait_until_done())

    async def collect(self) -> AsyncIterator[dict]:
        for i, (val_last, val, ts) in enumerate(self.buffer, 1):
            yield {
                "data": {self.name: val},
                "timestamps": {self.name: ts},
                "time": ts,
                "seq_num": i,
                "filled": {},
                "data_keys": {
                    self.name: {
                        "dtype": "array",
                        "shape": list(self.shape),
                        "source": "afm_det_sdk"
                    }
                },
                "structure_family": "array",
                "structure": ArrayStructure.from_array(val),
                "descriptor": "flyer",
                "type": "event"
            }

    def describe_collect(self):
        return {"flyer": {self.name: {"dtype": "array", "shape": list(self.shape), "source": "afm_det_sdk"}}}
    
    async def read(self):
        return {self.name: {"value": await self.signal.get_value(), "timestamp": time.time()}}

    def describe(self):
        return {self.name: {"dtype": "array", "shape": list(self.shape), "source": "afm_det_sdk"}}
    
class AEMD_base(Device):
    def __init__(self, name="afm", shape=(1,)):
        super().__init__(name=name)
        self.motor_x = AsyncAEMotor(name="motor_x")
        self.motor_y = AsyncAEMotor(name="motor_y")
        self.det_x = AsyncAEDetector(name="det_x", motor_x=self.motor_x, shape=shape)

