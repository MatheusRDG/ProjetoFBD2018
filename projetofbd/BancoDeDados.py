#Arquivo que cria conexão com o banco de dados
import pymysql

def conectarAoBanco():
    Connection = pymysql.connect(host='localhost',user='root',password='',database = 'servicos_limpeza')