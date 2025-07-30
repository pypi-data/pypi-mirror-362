import socket
import h5py
import io

HOST = 'localhost'
PORT = 3512  # Port

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
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
