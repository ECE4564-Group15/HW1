import socket
import wolframalpha
import pickle
import hashlib

app_id = 'H4A6AU-YTP8RQA247'
hostname = ''
port = 50000
backlog = 5
packsize = 1024

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((hostname, port))
serverSocket.listen(backlog)
client_socket, (remote_host, remote_port) = serverSocket.accept()
wa_client = wolframalpha.Client(app_id)
print("Client connected: %s:%s" % (remote_host, remote_port))

while True:
    try:
        ans = ''
        data = client_socket.recv(packsize)
        data = pickle.loads(data)
        if data[0] != hashlib.md5(data[1].encode()).hexdigest():
            print("Question MD5 mismatch!")
            print("Calculated: ", hashlib.md5(data[1].encode()).hexdigest())
            print("Received: ", data[0])
        res = wa_client.query(data[1][1:-1])
        print(data[1])
        # print(res)
        if int(res.numpods) > 0 and res.success == "true":
            m = res.pods
            for pod in res.results:
                if pod:
                    ans = pod.text
            if ans is '':
                if res.numpods == 1:
                    ans = next(m).text
                else:
                    next(m)
                    ans = next(m).text
        else:
            ans = "Wolfram|Alpha is unable to resolve your question"
            # print(ans)
            # print("Question received: ", data[1])

        ans = ans.split('\n')[0]
        print("Question received: ", data[1])
        print("Answer is: ", ans)
        t = (hashlib.md5(ans.encode()).hexdigest(), ans)
        client_socket.send(pickle.dumps(t))
    except:
        # print("connection lost")
        client_socket, (remote_host, remote_port) = serverSocket.accept()
