import FreeSimpleGUI as sg

def demo_column():
    col = [[sg.Text('col Row 1')],
           [sg.Text('col Row 2'), sg.Input('col input 1')],
           [sg.Text('col Row 3'), sg.Input('col input 2')],
           [sg.Text('col Row 4'), sg.Input('col input 3')],
           [sg.Text('col Row 5'), sg.Input('col input 4')],
           [sg.Text('col Row 6'), sg.Input('col input 5')],
           [sg.Text('col Row 7'), sg.Input('col input 6')]]

    layout = [[sg.Slider(range=(1,100), default_value=10, orientation='v', size=(8,20)), sg.Column(col)],
              [sg.In('Last input')],
              [sg.OK()]]

    window = sg.Window('Compact 1-line window with column', layout)
    event, values = window.read()
    window.close()

    sg.Popup(event, values, line_width=200)

def demo_frame():
    frame_layout = [[sg.T('Text inside of a frame')],
                    [sg.CB('Check 1'), sg.CB('Check 2 ')]]
    layout = [[sg.Frame('My Frame Title', frame_layout, font='Any 12', title_color='blue')],
              [sg.Submit(), sg.Cancel()]]
    
    window = sg.Window('Frame with buttons', layout, font=("Helvetica", 12))
    event, values = window.read()
    window.close()

    sg.Popup(event, values, line_width=200)

def demo_listbox():
    layout = [
        [sg.Listbox(values=['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(30, 6), key='listbox')],
        [sg.Ok(), sg.Cancel()]
    ]
    
    window = sg.Window('Listbox', layout, font=("Helvetica", 12))
    event, values = window.read()
    window.close()

    print("선택한 값:", values['listbox'])

def demo_multiline():
    text = '''Multiline 엘리먼트입니다.
    아래에서 텍스트를 입력하고 OK 버튼을 눌러보세요.'''
    layout = [
        [sg.Multiline(text, size=(45, 5), key="ml")],
        [sg.I(key="input"), sg.Ok(), sg.Cancel()]
    ]

    window = sg.Window('Multiline', layout, font=("Helvetica", 12))
    while True:
        event, values = window.read()
        if event in ("Cancel", sg.WIN_CLOSED):
            break
        elif event == 'Ok':
            window['ml'].print(values['input'])
            window['input'].update('')
    window.close()

def long_operation_thread(window):
    print('3초 걸리는 작업을 서브 스레드에서 시작합니다.')
    time.sleep(3)
    window.write_event_value('-THREAD-', '** 작업 끝 **')

