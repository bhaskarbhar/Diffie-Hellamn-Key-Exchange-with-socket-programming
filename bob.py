import socket
import random

# Create a socket for the server
user2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
PORT = 12345

# Bind the socket to the host and port, then start listening for connections
user2_socket.bind((HOST, PORT))
user2_socket.listen(1)
print("Server is listening on port", PORT)

# Accept a connection
conn, addr = user2_socket.accept()
print("Connection established with", addr)

#Private key generation
private_key = random.randint(100,999)

#R1 calulation
def R2_calculation(private_key,p,g):
    R2 = pow(g,private_key,p)
    return R2

def key_generation(R1,private_key,p):
    key = pow(R1,private_key,p)
    return key

try:
    # Receive the prime number and primitive root from the client
    p = conn.recv(1024).decode()
    g = conn.recv(1024).decode()
    print(f"Received prime number {p} and primitive root {g}")

    p = int(p)
    g = int(g)
    # Send a confirmation message back to the client
    conn.send("Received both prime number and primitive root.".encode())
    R2 = R2_calculation(private_key,p,g)
    print(f"R1 of alice is {R2}")
    R1 = conn.recv(1024).decode()
    R1 = int(R1)
    print("Received R1=", R1)
    
    conn.send(str(R2).encode())
    key = key_generation(R1,private_key,p)
    print(f"The key generated is {key}")

except KeyboardInterrupt:
    print("Interrupted by user")
        
except Exception as e:
    print("Interrpted", e)

finally:
    # Close the connection and server socket
    conn.close()
    user2_socket.close()
