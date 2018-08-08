from infraestrutura.banco import BancoDados

class ClienteServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")

    def inserirCliente(self, cliente):
        try:
            if cliente.getEndereco() == ", . , .":
                atributos = "('" + cliente.getCodigo() + "'" + "," + "'" + cliente.getTelefone() + "'" + "," + " null)"
            else:
                atributos = "('" + cliente.getCodigo() + "'" + "," + "'" + cliente.getTelefone() + "'" + "," + "'" + cliente.getEndereco() + "'" + ")"
            self.connection.insert("INSERT INTO cliente VALUES " + atributos)
        except Exception as e:
            return e

    def removerCliente(self, cliente):
        try:
            self.connection.delete("DELETE FROM cliente WHERE codigo = " + cliente.getCodigo())
        except Exception as e:
            return e

    def listarClientes(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except Exception as e:
            return e