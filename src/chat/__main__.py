"""채팅 프로그램

Usage:
    chatserver <port>

Options:
    -h --help       도움말
    -V --version    버전 출력
"""
from docopt import docopt
from .server import ChatServer

def main():
    arguments = docopt(__doc__, version="채팅 프로그램 0.0.3")
    server = ChatServer(int(arguments['<port>']))
    server.serve()

if __name__ == '__main__':
    main()
#1. 클라이언트가 다른 클라이언트와 중복된 닉네임으로 이름 변경을 요청했을 때, 에러 팝업을 띄우고 요청을 기각시키기. ex) "중복된 닉네임 입니다!" 라는 팝업을 띄우기 (힌트: https://pysimplegui.readthedocs.io/en/latest/#popup-output)

#2. 클라이언트가 로그인 창에서 잘못된 서버 IP 와 PORT 를 입력했을 때 "서버에 연결할 수 없습니다" 라는 팝업을 띄우기. (힌트: https://docs.python.org/ko/3/library/socket.html#socket.socket.connect, https://stackoverflow.com/a/25448603/15266921)

#3. 클라이언트들이 메시지를 보낼 때 유저들마다 채팅 색깔을 다르게 출력하기.(https://pysimplegui.readthedocs.io/en/latest/call%20reference/#multiline-element 에서 print 메소드의