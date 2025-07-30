
"""
import socket
import os
import time
import numpy as np
import sidpy as sid
import h5py
import pyNSID as nsid

HOST = 'localhost'  # The server's hostname or IP address
PORT = 9000        # The port used by the server
file_name = 'data1234.h5'
# Send data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # Connect to the port and host
    t0 = time.time()

    my_data = np.random.uniform(size=(100,100))
    my_data_sid = sid.Dataset.from_array(my_data, title = 'my_data')
    my_data_sid.set_dimension(0, sid.Dimension(np.arange(100),
                                            name='x',
                                            units='m', quantity='x',
                                            dimension_type='spatial'))
    my_data_sid.set_dimension(1, sid.Dimension(np.arange(100),
                                            name='y',
                                            units='m', quantity='y',
                                            dimension_type='spatial'))
    my_data_sid.data_type = 'IMAGE'
    with h5py.File(file_name, 'a') as f:
        data_group = f.create_group('DataGroup')
        nsid.hdf_io.write_nsid_dataset(my_data_sid,data_group, main_data_name = 'my_data')
        f.flush()
        img = f.id.get_file_image()
        s.send(img) # Send file image in chunks

    t2 = time.time()
    s.close()

time_for_all = t2-t0
os.remove(file_name)
print('Total time taken for all iterations: {}'.format(time_for_all))
"""


