import socket
import sympy
import random

# Function to find a primitive root for a prime number
def primitive_root(p):
    if not sympy.isprime(p):
        raise ValueError("Input must be a prime number")

    # Calculate factors of p-1
    factors = sympy.factorint(p - 1)
    
    # Check for the smallest generator
    for g in range(2, p):
        if all(pow(g, (p - 1) // factor, p) != 1 for factor in factors):
            return g

    raise ValueError("No primitive root found")

# Create a socket
user1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 12345

# Connect to the server
user1_socket.connect((HOST, PORT))

# Select a prime number and find its primitive root
p = random.randint(100,999)
while not sympy.isprime(p):
    p = random.randint(100, 999)

g = primitive_root(p)

#Private key generation
private_key = random.randint(100,999)

#R1 calulation
def R1_calculation(private_key,p,g):
    R1 = pow(g,private_key,p)
    return R1

def key_generation(R2,private_key,p):
    key = pow(R2,private_key,p)
    return key

try:
    # Send the prime number and primitive root to the server
    user1_socket.send(str(p).encode())
    user1_socket.send(str(g).encode())

    # Receive and print the response from the server
    response = user1_socket.recv(1024).decode()
    print("Server Response:", response)

    R1 = R1_calculation(private_key,p,g)
    user1_socket.send(str(R1).encode())
    print(f"R1 of alice is {R1}")
    R2 = user1_socket.recv(1024).decode()
    R2 = int(R2)
    print("Received R2=", R2)
    
    key = key_generation(R2,private_key,p)
    print(f"The key generated is {key}")

except KeyboardInterrupt:
    print("Interrupted by user")
    
except Exception as e:
    print("Interrpted", e)

finally:
    # Close the socket
    user1_socket.close()
