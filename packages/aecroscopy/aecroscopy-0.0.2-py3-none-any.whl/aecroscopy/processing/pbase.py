
import socket
import h5py
import io

#Write a process server class
import sidpy as sid
import numpy as np
import time
from pyNSID.io.hdf_utils import read_h5py_dataset, get_all_main
from pyNSID.io.hdf_io import write_nsid_dataset
import h5py

class ProcessServer():
    def __init__(self, host_details = ['localhost', 9000], server_loc = 'local') -> None:
        
        """
        Process Server class, used for processing data acquired through the Acquisition class
        If the processing is local, initializing this will spawn a python instance with a server 
        Processing is done by a predefined choice of functions.
        In future we may want to enable customized scripts.
    
        Parameters
        ----------
        host_details : List, [HOST, PORT]
            HOST and PORT of the server to connect to. By default this is a localhost on port 3447
        server_loc: str, Default = 'local'
            One of ['local', 'remote'], where if local, a server is started locally, and if remote, 
            the user is reminded to ensure the server is running before running any processing routines
       
        Returns
        -------
        An instance of ProcessServer() class
        """
        
        self.host_name = host_details[0]
        self.host_port = host_details[1]
        self.available_processes = self._get_processes()
        self.server_loc = server_loc
        assert server_loc.lower() in ['remote', 'local']
        self.initialize_server() #initialize the server
        

    def _get_processes(self):
        '''
        Returns list of process functions available
        '''
        #Let's get a list of available processes. Maybe we should have a file which lists the name
        #and maps the name to a function contained in a specific file.
        #For now I am just hardcoding this
        available_processes = ['linear fit', 'quadratic fit', 'SHO Fit', 'Loop Fit', 'biharmonic_inpainting']
        return available_processes
        
    def initialize_server(self):
        import subprocess
        # Run the other script
        if self.server_loc=='local':
            # Get the current script's directory
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Get the parent directory
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
            print(current_dir, parent_dir)
            path_to_server = os.path.join(parent_dir, 'communication/server.py')
            print(path_to_server)
            subprocess.Popen(["python",path_to_server], )
        else:
            print('Please start the server at the remote location if it is not already running.')
        return
    
    def run_process(self, sidpy_dset, process_name, **args):
        '''
        This function will run the process on the server
        We will need to send the process name and the arguments
        The server will then run the process and return the results
        Parameters
        ----------
        sidpy_dset : sidpy.Dataset object
            Data to send for processing
        process_name: str
            Which process shoudl be performed on the sidpy dataset. Must be one of
            ['linear fit', 'quadratic fit', 'SHO Fit', 'Loop Fit']
        args: Any arguments for the chosen process. Default is None
        Returns
        -------
        An instance of ProcessServer() class
        '''
        import os
        file_name = r'temp_h5file.h5'
        try:
            os.remove(file_name)
        except:
            pass
     
        assert process_name in self.available_processes, "ERROR: Process must be one of {}".format(self.available_processes)
        process_details = {'name':process_name, 'arguments': args}
        my_dset = sidpy_dset.copy()
        my_dset.metadata['sid_process'] = process_details

        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = self.host_name
        PORT = self.host_port
        sc.connect((HOST, PORT)) # Connect to the port and host
        with h5py.File(file_name, 'a') as f:
            data_group = f.create_group('MyDataGroup')
            write_nsid_dataset(my_dset,data_group, main_data_name = 'sid_data')
            f.flush()
            img = f.id.get_file_image()
            print('sending now')
            sc.sendall(img) # Send file image in chunks
        sc.close()
        
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect((HOST, PORT)) # Connect to the port and host
        
        #Receive a hdf5 file
        chunks = []
        while True:
            chunk = sc.recv(1024)
            if not chunk:
                break
            chunks.append(chunk)

        # Load the HDF5 file from the received chunks
        with h5py.File(io.BytesIO(b''.join(chunks)), 'r') as f:
            sid.hdf_utils.print_tree(f)
            #processed_dsets = get_all_main(f['MyDataGroup'])
            processed_data = read_h5py_dataset(f['MyDataGroup/processed_data_0/processed_data_0'])
            sc.close()
            return processed_data


