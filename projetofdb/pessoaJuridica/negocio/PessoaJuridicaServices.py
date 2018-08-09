from infraestrutura.banco import BancoDados
from pymysql import MySQLError

class PessoaJuridicaServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")

    def inserirPessoaJuridica(self, pessoaJuridica):
        try:
            self.connection.insert("INSERT INTO pessoa_juridica VALUES (%s, %s, %s)" %(pessoaJuridica.getCodigoCliente(), pessoaJuridica.getCnpj(), pessoaJuridica.getRazaoSocial()))
        except MySQLError as e:
            return e

    def removerPessoaJuridica(self, pessoaJuridica):
        try:
            self.connection.delete("DELETE FROM pessoa_juridica WHERE codigo_cliente = " + pessoaJuridica.getCodigo())
        except MySQLError as e:
            return e

    def listarPessoas(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e