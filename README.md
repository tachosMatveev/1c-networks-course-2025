Запускать командой ```python3 dns_server.py ./my_conf.txt {тут TTL (например 300) необязательный параметр} {тут либо UDP либо TCP}```

Вот пример запуска ```$ python3 dns_server.py ./my_conf.txt 450 UDP```

/// Логи dig

 /tmp/ dig @127.0.0.1 -p 8087 +tcp

; <<>> DiG 9.20.13 <<>> @127.0.0.1 -p 8087 +tcp
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 38726
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;.				IN	NS

;; ANSWER SECTION:
.			450	IN	A	127.0.0.1

;; Query time: 1 msec
;; SERVER: 127.0.0.1#8087(127.0.0.1) (TCP)
;; WHEN: Sat Oct 18 21:59:16 MSK 2025
;; MSG SIZE  rcvd: 32

 /tmp/ dig @127.0.0.1 -p 8087     

; <<>> DiG 9.20.13 <<>> @127.0.0.1 -p 8087
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54645
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;.				IN	NS

;; ANSWER SECTION:
.			450	IN	A	127.0.0.1

;; Query time: 2 msec
;; SERVER: 127.0.0.1#8087(127.0.0.1) (UDP)
;; WHEN: Sat Oct 18 21:59:26 MSK 2025
;; MSG SIZE  rcvd: 32
