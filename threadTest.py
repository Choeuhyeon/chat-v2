import threading
import time
import FreeSimpleGUI as sg
def long_operation_thread(window):
    print('3초 걸리는 작업을 서브 스레드에서 시작합니다.')
    time.sleep(3)
    window.write_event_value('-THREAD-', '** 작업 끝 **')

def main_thread():
    layout = [[sg.Text('오래 걸리는 작업을 시작해야 하는 상황!')],
              [sg.Output()],
              [sg.Button('서브 스레드 시작', key='start'), sg.Button('Exit')],]
    
    window = sg.Window('Multithreaded Window', layout, finalize=True)
    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'start':
            threading.Thread(target=long_operation_thread, args=(window), daemon=True).start()
        elif event == '-THREAD-':
            print('서브 스레드에서 메시지를 받았습니다:', values[event])
    
    window.close()
main_thread()