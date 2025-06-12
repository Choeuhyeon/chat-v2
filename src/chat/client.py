import socket
import json
from threading import Thread
from FreeSimpleGUI import *

class ChatClient:
    def __init__(self):
        self.host = ''
        self.port = 0
        self.name = ''
        self.window = None
        self.users = []
        self.s = socket.socket()

        theme('Reddit')

    def _ui(self):
        users_board = Col([
            [T('연결된 유저')],
            [Listbox([], size=(25, 16), enable_events=True, key='users')]
        ])
        message_board = Col([
            [T('채팅 보드')],
            [ML(size=(45, 15), disabled=True, key='public_messages_board')],
            [I(key='message', size=(15, 1)),
             B('▲ 보내기', key='send_public_message'),
             B('▲ 귓속말', key='send_private_message')]
        ])
        private_message = Col([
            [T('귓속말')],
            [ML(size=(25, 16), disabled=True, key='private_messages_board')]
        ])

        layout = [[T('이름'),
                   I(self.name, disabled=True, use_readonly_for_disable=True, size=(30, 1), key='my_name'),
                   B('이름 바꾸기', key='change_name')],
                   [users_board, message_board, private_message]]
        return layout
    
    def login(self):
        layout = [
            [T('IP', size=(5, 1)), I(key="ip", size=(15, 1), default_text="localhost")],
            [T('Port', size=(5, 1)), I(key="port", size=(15, 1), default_text="6000")],            
            [OK()]
        ] 

        window = Window('채팅 서버 연결', layout)

        event, values = window.read()
        if event in ("exit", WIN_CLOSED):
            return
        window.close()
        self.host = values['ip']
        self.port = int(values['port'])

    def communication_with_server(self):
        while True:
            message = self.s.recv(1024).decode()
            message = json.loads(message)
            if message['type'] == 'new_user':
                self.window.write_event_value('new_user', message)
            elif message['type'] == 'send_public_message':
                self.window.write_event_value('get_public_message', message)
            elif message['type'] == 'send_private_message':
                self.window.write_event_value('get_private_message', message)
            elif message['type'] == 'change_name':
                self.window.write_event_value('get_change_name', message)

    def _send_public_message(self, text):
        message ={
            'type' : 'send_public_message',
            'from' : self.name,
            'text' : text,
        }
        self.window['public_messages_board'].print(f'{self.name}: {text}')
        self.window['message'].update('')
        self.s.send(json.dumps(message).encode())
    
    def _send_private_message(self, to, text):
        message = {
            'type' : 'send_private_message',
            'to' : to,
            'from' : self.name,
            'text' : text,
        }
        self.window['private_messages_board'].print(f'To {to}: {text}')
        self.window['message'].update('')
        self.s.send(json.dumps(message).encode())

    def _get_change_name(self, name, new_name):
        for i, user in enumerate(self.users):
            if user == name:
                self.users[i] = new_name
                break
        self.window['users'].update(values=self.users)

    def _change_name(self):
        new_name = popup_get_text("새로운 이름")
        message = {
            'type' : 'change_name',
            'name' : self.name,
            'new_name' : new_name,
        }
        self.name = new_name
        self.window['my_name'].update(new_name)
        self.s.send(json.dumps(message).encode())

    def _init_connection(self):
        print(f"[*] {self.host}:{self.port} 로 연결시도")
        self.s.connect((self.host, self.port))
        print("[*]연결 완료")

        self.window = Window('채팅', self._ui(), finalize=True)

        data = json.loads(self.s.recv(1024).decode())
        self.name = data['name']
        self.users = data['user_list']
        self.window['my_name'].update(self.name)
        self.window['users'].update(values=self.users)

    def connect(self):
        self._init_connection()
        t = Thread(target=self.communication_with_server, daemon = True)
        t.start()

        while True:
            event, values = self.window.read()

            if event in ("exit", WIN_CLOSED):
                break
            elif event == 'new_user':
                self.users.append(values[event]['name'])
                self.window['users'].update(values=self.users)
            elif event == 'send_public_message':
                self._send_public_message(values['message'])
            elif event == 'get_public_message':
                message = f"{values[event]['from']}: {values[event]['text']}"
                self.window['public_messages_board'].print(message)
            elif event == 'send_private_message':
                if (not values['users']) or len(values['users']) < 0:
                    popup('귓속말을 보낼 대상을 선태해주세요')
                    continue
                self._send_private_message(values['users'][0], values['message'])                                                                                             
            elif event == 'get_private_message':
                message = f"From {values[event]['from']}: {values[event]['text']}"
                self.window['private_messages_board'].print(message)
            elif event == 'change_name':
                self._change_name()
            elif event == 'get_change_name':
                self._get_change_name(values[event]['name'], values[event]['new_name'])


        self.window.close()
        self.s.close()

    def run(self):
        self.login()
        self.connect()
        
if __name__ == '__main__':
    client = ChatClient()
    client.run()