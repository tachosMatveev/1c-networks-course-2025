# DNS-server

# Сервер, на любом языке, который по протоколу DNS умеет обслуживать A записи
# Так, чтобы можно было его указать вместо системного, и мы бы смогли выполнить 
# то же упражнение с заменой, только на свой DNS
# Мы должны мочь через конфигурационный файл подавать список доменных имен и ip-адресов

# Чем больше типов запросов поддержится, тем лучше

# Результат (код) нужно выложить на github/или другой доступный git- репозиторий

from dnslib import DNSRecord, QTYPE, RR, A, DNSHeader
import sys
import socket
import socketserver

class DNSHandlerTCP(socketserver.BaseRequestHandler):
    def handle(self):

        # FOR TCP ONLY

        print("❤️ Catch DNS request")

        raw_len = self.request.recv(2)

        print("raw_len: ", int.from_bytes(raw_len, 'big'))

        if len(raw_len) < 2:
                print("👺 Failed to read length prefix")
                return
            
        msg_len = int.from_bytes(raw_len, 'big')

        data = self.request.recv(msg_len)
        
        if len(data) < msg_len:
                print("👺 Truncated DNS message")
                return

        print("🦾 TCP request:", self.request, "\n 🙄 Client: ", self.client_address)
        try:
            request = DNSRecord.parse(data)
            print(f"2🙏 Received request for: {request}")
            print(f"🙏 Received request for: {str(request.q.qname)}")

            # Create a DNS response with the same ID and the appropriate flags
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]

            print("🙂 qname: ", qname)

            if qname in DNS_DICT:
                if TTL_VALUE:
                    reply.add_answer(RR(qname, QTYPE.A, rdata=A(DNS_DICT[qname]), ttl=TTL_VALUE))
                else:
                    reply.add_answer(RR(qname, QTYPE.A, rdata=A(DNS_DICT[qname])))
                print(f"✅ Resolved {qname} to {DNS_DICT[qname]}")
            else:
                print(f"👺 No record found for {qname}")

            response_data = reply.pack()

            length_prefix = len(response_data).to_bytes(2, 'big')

            self.request.sendall(length_prefix + response_data)
        except Exception as e:
            print(f"Error handling request: {e}")

class DNSHandlerUDP(socketserver.BaseRequestHandler):
    def handle(self):

        # FOR UDP ONLY

        print("❤️ Catch DNS request")

        data, socket = self.request

        print("🛠️ data:", data.strip(), "\n")

        print("🦾 UDP request:", self.request, "\n 🙄 Client: ", self.client_address)

        try:
            request = DNSRecord.parse(data)
            print(f"2🙏 Received request for: {request}")
            print(f"🙏 Received request for: {str(request.q.qname)}")

            # Create a DNS response with the same ID and the appropriate flags
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]

            print("🙂 qname: ", qname)

            if qname in DNS_DICT:
                if TTL_VALUE:
                    reply.add_answer(RR(qname, QTYPE.A, rdata=A(DNS_DICT[qname]), ttl=TTL_VALUE))
                else:
                    reply.add_answer(RR(qname, QTYPE.A, rdata=A(DNS_DICT[qname])))
                print(f"✅ Resolved {qname} to {DNS_DICT[qname]}")
            else:
                print(f"👺 No record found for {qname}")

            # self.request.sendall(reply.pack())
            response_data = reply.pack()
            socket.sendto(response_data, self.client_address)
        except Exception as e:
            print(f"Error handling request: {e}")

TTL_VALUE = None
DNS_DICT = {}
MODE = "TCP" # TCP or UDP

if len(sys.argv) > 1:
    file_name = sys.argv[1]

if len(sys.argv) > 2:
    if sys.argv[2] == "TCP" or sys.argv[2] == "UDP":
        MODE = sys.argv[2]
    else:
        TTL_VALUE = int(sys.argv[2])

if len(sys.argv) > 3:
    if sys.argv[3] == "TCP" or sys.argv[3] == "UDP":
        MODE = sys.argv[3]

try:
    with open(file_name, 'r') as f:
        for line in f:
            l, r = line.split()
            DNS_DICT[l] = r
except FileNotFoundError:
    print("Error: The file" ,file_name, " was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

print("😎 Configuration: ", DNS_DICT, "\n")

listen_ip = "127.0.0.1"
listen_port = 8087

if MODE == "TCP":
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((listen_ip, listen_port), DNSHandlerTCP)
    print(f"DNS Server is running listen {MODE}...", listen_ip, listen_port, "\n\n")
    server.serve_forever()

if MODE == "UDP":
    server = socketserver.UDPServer((listen_ip, listen_port), DNSHandlerUDP)
    print(f"DNS Server is running listen {MODE}...", listen_ip, listen_port, "\n\n")
    server.serve_forever()

