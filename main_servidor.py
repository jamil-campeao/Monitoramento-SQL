import socket
import pyodbc
from datetime import datetime
import logging

logging.basicConfig(filename='server.log', level=logging.INFO)

conexao = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.112;DATABASE=MONITORAMENTO;UID=DBA2;PWD=123')
cursor = conexao.cursor()

host = '192.168.1.112'
porta = 1433

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((host, porta))
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)

while True:
    data, endereco_cliente = servidor.recvfrom(8192)
    decoded_data = data.decode()

    parts = decoded_data.split(",")  # Divide os dados nos segmentos conhecidos

    ip = parts[0]
    mem = parts[1]
    cpu = parts[2]
    disco = parts[3]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_query = "INSERT INTO informacoes (ip_origem, mem, cpu, disco, tempo) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(insert_query, (ip, mem, cpu, disco, timestamp))
    cursor.commit()
    logging.info("Dados inseridos com sucesso.")
