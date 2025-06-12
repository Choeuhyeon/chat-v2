import socket
import json 
from threading import Thread

class ChatServer():
    def __init__(self, port):
        self.host = '0.0.0.0'
        self.port = port
        self.anonymous_number = 1

        self.clients = []

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen()
        print(f"[*] {self.host}:{self.port} 주소에서 통신 대기중")

    def broadcast(self, data, exclusion=[]):
        for client in self.clients:
            if client['socket'] not in exclusion:
                client['socket'].send(data.encode())

    def init_connection(self, cs, user_info):
        users = [client['name'] for client in self.clients]
        cs.send(json.dumps({'type' : 'init',
                            'name' : user_info['name'],
                            'user_list' : users}).encode())
        
        self.clients.append(user_info)

        message = json.dumps({'type' : 'new_user', 'name' : user_info['name']})
        self.broadcast(message, exclusion=[cs])

    def send_private_message(self, message):
        for client in self.clients:
            if client['name'] == message['to']:
                client['socket'].send(json.dumps(message).encode())
                break

    def change_name(self, message, cs):
        for client in self.clients:
            if client['name'] == message['name']:
                client['name'] = message['new_name']
                break
        self.broadcast(json.dumps(message), exclusion=[cs])

    def communication_with_client(self, cs):
        name = f'익명{self.anonymous_number}'   
        self.anonymous_number += 1
        user_info  = {
            'socket' : cs,
            'name' : name
        }
        self.init_connection(cs, user_info)

        while True:
            try:
                message = cs.recv(1024).decode()
                message = json.loads(message)
            except Exception as e:
                print(f"[!] 에러 발생 : {e}")
                self.clients.remove(user_info)
                break
            else:
                if message['type'] == 'send_public_message':
                    self.broadcast(data=json.dumps(message), exclusion=[cs])
                elif message['type'] == 'send_private_message':
                    self.send_private_message(message)
                elif message['type'] == 'change_name':
                    self.change_name(message, cs)
        
    def serve(self):
        while True:
            client_socket, client_address = self.s.accept()
            print(f"[+] 연결완료 : {client_address}")
            t = Thread(target=self.communication_with_client, args=(client_socket,), daemon=True)
            t.start()

        for cs in self.client_sockets:
            cs.close()
        self.s.close()

if __name__ == '__main__':
    import sys
    server = ChatServer(int(sys.argv[1]))
    server.serve()