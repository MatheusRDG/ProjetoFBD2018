import BancoDeDados

clientes = BancoDeDados.select("SELECT * FROM cliente")

for i in clientes:
    print(i)
