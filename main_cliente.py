import pyodbc
import psutil
import socket
from datetime import datetime
import time
import logging

logging.basicConfig(filename='client.log', level=logging.INFO)

def coletar_informacoes():
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disco = psutil.disk_usage('/').percent
    ip = '192.168.1.103' #ip maquina cliente

    return (ip, mem, cpu, disco)

conexao = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.112;DATABASE=MONITORAMENTO;UID=DBA2;PWD=123') # Conexao do banco
cursor = conexao.cursor()

ip_servidor = '192.168.1.112'
intervalo = 5

while True:
    dados = coletar_informacoes()
    try:
        pacote = ','.join(map(str, dados))
        cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cliente.sendto(pacote.encode(), (ip_servidor, 1433))
        logging.info("Dados enviados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar dados: {e}")
    time.sleep(intervalo)
