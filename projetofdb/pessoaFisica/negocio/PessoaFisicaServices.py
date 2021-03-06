from infraestrutura.banco import BancoDados
from pymysql import MySQLError

class PessoaFisicaServices:

    def __init__(self):
        self.connection = BancoDados.Banco()

    def inserirPessoaFisica(self, pessoaFisica):
        try:
            self.connection.insert("INSERT INTO pessoa_fisica VALUES (%s, %s, %s)" %(pessoaFisica.getCodigoCliente(), "'" + pessoaFisica.getCpf() + "'", "'" + pessoaFisica.getNome() + "'"))
        except MySQLError as e:
            return e

    def removerPessoaFisica(self, pessoaFisica):
        try:
            self.connection.delete("DELETE FROM pessoa_fisica WHERE codigo_cliente = " + pessoaFisica.getCodigo())
        except MySQLError as e:
            return e

    def atualizaPessoaFisica(self, codigo_cliente, pessoaFisica):
        try:
            self.connection.update("UPDATE pessoa_fisica SET cpf = %s, nome = %s WHERE codigo_cliente = %s"
                                   % ("'" + pessoaFisica.getCpf() + "'", "'" + pessoaFisica.getNome() + "'", codigo_cliente))
        except MySQLError as e:
            return e

    def listarPessoasFisicas(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e