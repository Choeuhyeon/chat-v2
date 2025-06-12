from FreeSimpleGUI import *

def login():
    layout = [[T('IP', size=(5, 1)), I(key="ip", size=(15, 1))],
              [T('Port', size=(5, 1)), I(key="port", size=(15, 1))],
              [OK()]]
    
    window = Window('채팅 서버 연결', layout)

    event, values = window.read()
    if event in ("exit", WIN_CLOSED):
        return
    window.close()
    host = values['ip']
    port = int(values['port'])
    print(host, port)

def ui():
    users_board = Col([
        [T('연결된 유저')],
        [Listbox([], size=(25, 16), enable_events=True)]
    ])
    message_board = Col([
        [T('채팅 보드')],
        [ML(size=(45, 15), disabled=True)],
        [I(size=(15, 1)),
         B('▲ 보내기'),
         B('▲ 귓속말')]
    ])
    private_message = Col([
        [T('귓속말')],
        [ML(size=(25, 16), disabled=True)]
    ])

    layout = [[T('이름'),
               I('익명1', disabled=True, use_readonly_for_disable=True, size=(30, 1)),
               B('이름 바꾸기')],
               [users_board, message_board, private_message]]
    
    window = Window('채팅', layout)

    event, values = window.read()
    if event in ("exit", WIN_CLOSED):
        return
    window.close()
    host = values['ip']
    port = int(values['port'])
    print(host, port)

    return layout
ui()