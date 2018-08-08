from infraestrutura.banco import BancoDados


class PessoaJuridicaServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")

    def inserirPessoaJuridica(self, pessoaJuridica):
        try:
            atributos = "('" + pessoaJuridica.getCodigoCliente() + "'" + "," + "'" + pessoaJuridica.getCnpj() + "'" + "," + "'" + pessoaJuridica.getRazaoSocial() + "'" + ")"
            self.connection.insert("INSERT INTO pessoa_juridica VALUES " + atributos)
        except Exception as e:
            return e

    def removerPessoaJuridica(self, pessoaJuridica):
        try:
            self.connection.delete("DELETE FROM pessoa_juridica WHERE codigo = " + pessoaJuridica.getCodigo())
        except Exception as e:
            return e