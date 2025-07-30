

import os
import socket
#from mlsocket import MLSocket
import numpy as np
import pickle
from SciFiReaders import NSIDReader as nsreader
import h5py
import io
from pyNSID.io.hdf_utils import read_h5py_dataset
from pyNSID.io.hdf_io import write_nsid_dataset

import sidpy
from aecroscopy.processing.sho_fitting import SHO_fit_flattened, sho_guess_fn, better_sho_guess_fn

HOST = 'localhost'
PORT = 3451  # Port

os.environ['OPENBLAS_NUM_THREADS'] = '1'

file_name = r'temp_h5file.h5' #temporary file


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
        #Close the connection after receiving
        #s.close()
        #conn.close()

        #Read the hdf5 file 
        with h5py.File(io.BytesIO(b''.join(chunks)), 'r') as f:
            sidpy.hdf_utils.print_tree(f)
            f.flush()
            sid_dset = read_h5py_dataset(f['MyDataGroup/sid_data/sid_data'])
        
        print('Received dataset {}'.format(sid_dset))
        process_details = sid_dset.metadata['sid_process']
        process_name = process_details['name']
        process_args = process_details['arguments']

        if process_name == 'SHO Fit':
            print('---Performing SHO Fit----')
            #get some defaults out of the way
            chosen_parms = {'ind_dims': [0,1], 'num_workers':4, 'return_cov':False, 'return_fit': False,
                            'return_std': False, 'km_guess':False, 'num_fit_parms':None,
                            'threads':1}
            
            process_details = sid_dset.metadata['sid_process']
            process_name = process_details['name']
            process_parms = process_details['arguments']
            num_workers = process_parms['num_workers']
            return_cov = process_parms['return_cov']
            return_fit = process_parms['return_fit']

            for key in process_args.keys():
                chosen_parms[key] = process_args[key]
            
            fitter = sidpy.proc.fitter.SidFitter(sid_dset, SHO_fit_flattened,
                                num_workers=chosen_parms['num_workers'],
                                guess_fn = better_sho_guess_fn,ind_dims=chosen_parms['ind_dims'],
                            threads=chosen_parms['threads'], return_cov=chosen_parms['return_cov'], 
                            return_fit=chosen_parms['return_fit'], return_std=chosen_parms['return_std'],
                            km_guess=chosen_parms['km_guess'],num_fit_parms = chosen_parms['num_fit_parms'],
                            n_clus=5)
            #Let's see if the progressbar works
            #from dask.diagnostics import ProgressBar
            #ProgressBar().register()
            freq_vec = sid_dset._axes[2].values
            lb = [0, freq_vec.min(), 5, -2*np.pi]
            ub = [1000, freq_vec.max(), 5000, 2*np.pi]
            fitter.do_guess()
            fit_parameters = fitter.do_fit(bounds=(lb,ub), maxfev=30)
            fit_parameters= fitter.do_fit() #Fit the SHO

            print(fit_parameters)
        
            try:
                os.remove(file_name)
            except:
                pass

            with h5py.File(file_name, 'a') as f:
                data_group = f.create_group('MyDataGroup')
                for ind,dsets in enumerate(fit_parameters):
                    write_nsid_dataset(dsets,data_group, main_data_name = 'processed_data_'+str(ind))
                f.flush()
                img = f.id.get_file_image()
                print('now sending the data back to client')
            
            #Now send it back
            #First, open the connection again
            #First, open the connection again
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.bind((HOST, PORT))
            #s.listen()
            conn, address = s.accept()
            conn.sendall(img)
                
            #Close off the connections
            conn.close()    
            
