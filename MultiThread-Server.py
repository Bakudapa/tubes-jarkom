from socket import *
import threading
import time

def handle_client(connectionSocket, addr):
    try:
        start_time = time.time() 

        message = connectionSocket.recv(1024).decode()
        print(f"Received message: {message}")  
        filename = message.split()[1]
        print(f"Requested file: {filename}") 

        f = open(filename[1:])
        outputdata = f.read()
        
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

        end_time = time.time()  
        print(f"Request from {addr} processed in {end_time - start_time:.5f} seconds.")

    except IOError:

        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        
        connectionSocket.close()

        end_time = time.time()  
        print(f"Request from {addr} failed: File not found. Processed in {end_time - start_time:.5f} seconds.")


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverPort = 6789
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen(5)
    print('The server is ready to receive')

    while True:
 
        connectionSocket, addr = serverSocket.accept()
        print('Connection received from:', addr)


        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()

    serverSocket.close()

if __name__ == "__main__":
    main()
