import socket

addr = '192.168.12.218'
port = 50000
size = 1024

def check_quit(text):
    text = text.lower()
    if text == "quit":
        print(">> Exit the program.")
        print(">> bye.")
        exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((addr, port))
    data = s.recv(size)
    print(data.decode())

    while True:    
        data = s.recv(size)
        print(data.decode())

        ################################################
        # この枠内を改造
        # 変数 sentence にウェアラブルデバイスからの
        # 入力が入るように

        sentence = input()
        
        # ちなみにこのままならキーボード入力で
        # 使用可能
        ################################################

        check_quit(sentence)
        s.sendall(sentence.encode())

        data = s.recv(size)
        print(data.decode())

    