

import os
import gc
import socket
#from mlsocket import MLSocket
import numpy as np
import pickle
import json
from SciFiReaders import NSIDReader as nsreader
import h5py
import io
from pyNSID.io.hdf_utils import read_h5py_dataset
from pyNSID.io.hdf_io import write_nsid_dataset

import sidpy
from aecroscopy.processing.sho_fitting import perform_SHO_fitting
import logging

# Configure logging
log_file_path = 'app.log'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename=log_file_path)

HOST = 'localhost'
PORT = 3451  # Port

os.environ['OPENBLAS_NUM_THREADS'] = '1'

file_name = r'temp_h5file.h5' #temporary file
error_file_name  =r'error_file.dat'

#TODO:
"""
There is still a problem with this. Sending multiple requests of the same type (error or not error) works
But sending one error type request and another request without an error, fails. 

Bad-> Good Fails #Need to figure out why this occurs...
Good-> Bad Works
Bad-> Bad Works
Good-> Good Works
"""

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    while True:
        
        s.listen()
        conn, address = s.accept()

        #Receive the HDF5 file in chunks
        chunks = []
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            chunks.append(chunk)

        #if there is already a processed output variable, delete it. 
        try:
            del processed_output
            gc.collect()
        except: 
            pass
        
        #Read the hdf5 file 
        with h5py.File(io.BytesIO(b''.join(chunks)), 'r') as f:
            sidpy.hdf_utils.print_tree(f)
            f.flush()
            sid_dset = read_h5py_dataset(f['MyDataGroup/sid_data/sid_data'])
            

        print('Received dataset {}'.format(sid_dset))
        process_details = sid_dset.metadata['sid_process']
        process_name = process_details['name']
        process_args = process_details['arguments']
        
        error_received = True
        match process_name:
            case 'SHO Fit':
                try:
                    processed_output, fitter = perform_SHO_fitting(sid_dset, process_args)
                    error_received = False
                    
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
                    print('shutting down the dask client')
                    try:
                        fitter.client.shutdown()
                    except:
                        pass
                    
            case "Biharmonic Inpainting":
                print("Biharmonic code goes here")
        
        #If we received an error message...

        if error_received==True:
            try:
                os.remove(error_file_name)
            except:
                pass

            #Read the log
            print('in error handling section')
            with open(log_file_path, 'r') as f:
                log_contents = f.read()
                log_lines = log_contents.split('\n')
                f.flush()
                
            json_data = json.dumps(log_lines, indent=4)

            with open(error_file_name, 'a') as f:
                f.write(json_data)
                f.flush()

            with open(error_file_name, 'rb') as f:
                f.flush()
                img = f.read()
                print('Failed; sending the error back to client')
                
        else:
            try:
                os.remove(file_name)
            except:
                pass
            
            with h5py.File(file_name, 'a') as h5_f:
                data_group = h5_f.create_group('MyDataGroup')
                for ind,dsets in enumerate(processed_output):
                    print(ind, dsets)
                    write_nsid_dataset(dsets,data_group, main_data_name = 'processed_data_' + str(ind))
                h5_f.flush()
                img = h5_f.id.get_file_image()
                
                print('now sending the data back to client')

        #Now send it back

        conn, address = s.accept()
        conn.sendall(img)

        try:
            del processed_output
            gc.collect()
        except: 
            pass
   
        #Close off the connections
        conn.close()    
        
""""
To test the failure:

num_workers = 2

#sequence = good, bad, good

sequence_text= ['Good', 'Bad', 'Good']

for ind, seq_val in enumerate(sequence_text):
    print('\n----------Next Trial--------\n')
    print("Currently testing {} sequence".format(sequence_text[ind]))
    if seq_val =='Good': ind_dims = [0,1,3,4] 
    else: ind_dims=[0,1]
    
    process_args = {'num_workers':num_workers, 
                'ind_dims':ind_dims, 
                'return_cov':False, 
                'return_fit':False}
    
    processed_data = pserver.run_process(beps_small,
                                     'SHO Fit',
                                     **process_args )
    print(processed_data)

It fails from bad->Good.
"""