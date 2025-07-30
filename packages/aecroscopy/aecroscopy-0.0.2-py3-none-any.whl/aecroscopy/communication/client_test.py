import socket
import h5py
import io
import os


HOST = 'localhost'
PORT = 3512

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect((HOST, PORT)) # Connect to the port and host

#create hdf5 file with some dummy content
h5_f = h5py.File("test_file.h5", 'a')
grp = h5_f.create_group("Something")
grp.create_dataset("test", shape = (50,50))
h5_f.flush()

#Send the file
img = h5_f.id.get_file_image()
sc.sendall(img) # Send file image in chunks
#Close tehe connection
sc.close()

#Now time to receive, open connection
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
    print(f.keys())

sc.close()