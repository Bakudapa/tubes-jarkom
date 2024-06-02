import socket
import sys
import threading
import time

def send_request(server_host, server_port, path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        request = f"GET {path} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode())
        response = b""
        while True:
            part = client_socket.recv(1024)
            if not part:
                break
            response += part
        print(response.decode())
    finally:
        client_socket.close()

def threaded_requests(server_host, server_port, path, num_requests):
    threads = []
    start_time = time.time()
    for _ in range(num_requests):
        thread = threading.Thread(target=send_request, args=(server_host, server_port, path))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"All requests processed in {end_time - start_time:.5f} seconds.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python client.py <server_host> <server_port> <path> <num_requests>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    path = sys.argv[3]
    num_requests = int(sys.argv[4])

    threaded_requests(server_host, server_port, path, num_requests)
