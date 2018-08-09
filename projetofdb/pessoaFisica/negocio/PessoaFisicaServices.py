from infraestrutura.banco import BancoDados

class PessoaFisicaServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")

    def inserirPessoaFisica(self, pessoaFisica):
        try:
            atributos = "('" + pessoaFisica.getCodigoCliente() + "'" + "," + "'" + pessoaFisica.getCpf() + "'" + "," + "'" + pessoaFisica.getNome() + "'" + ")"
            self.connection.insert("INSERT INTO pessoa_fisica VALUES " + atributos)
        except Exception as e:
            return e

    def removerPessoaFisica(self, pessoaFisica):
        try:
            self.connection.delete("DELETE FROM pessoa_fisica WHERE codigo_cliente = " + pessoaFisica.getCodigo())
        except Exception as e:
            return e

    def listarPessoasFisicas(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except Exception as e:
            return e