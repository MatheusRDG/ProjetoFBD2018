from infraestrutura.banco import BancoDados
from pymysql import MySQLError

class PessoaJuridicaServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")

    def inserirPessoaJuridica(self, pessoaJuridica):
        try:
            self.connection.insert("INSERT INTO pessoa_juridica VALUES (%s, %s, %s)" %(pessoaJuridica.getCodigoCliente(), "'" + pessoaJuridica.getCnpj() + "'", "'" + pessoaJuridica.getRazaoSocial() + "'"))
        except MySQLError as e:
            return e

    def atualizarPessoaJuridica(self, codigo, pessoaJuridica):
        try:
            self.connection.update("UPDATE pessoa_juridica SET razao_social = %s, cnpj = %s WHERE codigo_cliente = %s"
                                   %("'"+ pessoaJuridica.getRazaoSocial()+"'","'" + pessoaJuridica.getCnpj() + "'",codigo))
        except MySQLError as e:
            return e

    def listarPessoas(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e