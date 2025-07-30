import socket
import h5py
import io
import sys

#The following enables us to close the server with ctrl+c in windows
#Credit to https://stackoverflow.com/a/52941752/8448563

def handler(a,b=None):
    sys.exit(1)
def install_handler():
    if sys.platform == "win32":
        import win32api
        win32api.SetConsoleCtrlHandler(handler, True)

HOST = 'localhost'
PORT = 3512  # Port

if __name__ == '__main__':
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        install_handler()
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
        s.close()
        conn.close()

        #Read the hdf5 file 
        with h5py.File(io.BytesIO(b''.join(chunks)), 'r') as f:
            print(f.keys())
            img = f.id.get_file_image()
        
        #Now send it back
        #First, open the connection again
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()
        conn, address = s.accept()
        conn.sendall(img)

        #Close off the connections
        conn.close()    
        s.close()

"""

**EDIT: Solved. Thank you user207421 for the explanation.** The server is reading to the end of stream but because the connection was never closed it never gets there. The following code changes enable us to send multiple files by running the client script as many times as necessary.

Server:

```
import socket
import h5py
import io

HOST = 'localhost'
PORT = 3512  # Port
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

    #Read the hdf5 file 
    with h5py.File(io.BytesIO(b''.join(chunks)), 'r') as f:
        print(f.keys())
        img = f.id.get_file_image()
    
    #Now send it back
    s.listen()
    conn, address = s.accept()
    conn.send(img)
    conn.close()    

```

Client side:
```
import socket
import h5py
import io

HOST = 'localhost'
PORT = 3512

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect((HOST, PORT)) # Connect to the port and host

file_name = r'test_file.h5'

#create hdf5 file with some dummy content
h5_f = h5py.File(file_name, 'a')
grp = h5_f.create_group("Something")
grp.create_dataset("test", shape = (50,50))
h5_f.flush()

#Send the file
img = h5_f.id.get_file_image()
sc.send(img) # Send file image in chunks
sc.close()

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect((HOST,PORT))

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
```
"""
