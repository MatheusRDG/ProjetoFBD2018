class ValidarCpfCnpj:

    def __init__(self, cpf_cnpj):
        self.cpf_cnpj = cpf_cnpj

    def isCpf(self):
        lista= []
        var1, var2 = 10, 11
        for i in (self.cpf_cnpj[0:9]):  # primeiro dígito
            lista.append(int(i) * var1)
            var1 -= 1
        div = sum(lista) % 11
        digito1 = 11 - div
        if digito1 > 9:
            valido = self.cpf_cnpj[0:9] + '0'
        else:
            valido = self.cpf_cnpj[0:9] + str(digito1)
        for i in (valido[0:10]):
            lista.append(int(i) * var2)
            var2 -= 1
        div = sum(lista[10:]) % 11
        digito2 = 11 - div
        if digito2 > 9:
            valido = self.cpf_cnpj[0:10] + '0'
        else:
            valido = self.cpf_cnpj[0:10] + str(digito2)

        return (valido == self.cpf_cnpj)

    def isCnpj(self):#By: PythonBrasil -> https://wiki.python.org.br/VerificadorDeCpfCnpjSimples#CA-e0eee570d5fdfde7d52515349a1238c516293297_7
        # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
        inteiros = map(int, self.cpf_cnpj)
        inteiros = list(inteiros)
        novo = inteiros[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(novo) < 14:
            r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)
            prod.insert(0, 6)

        # Se o número gerado coincidir com o número original, é válido
        if novo == inteiros:
            return self.cpf_cnpj
        return False

'''private static int calcularDigito(String str, int[] peso) {
        int soma = 0;
        for (int indice=str.length()-1, digito; indice >= 0; indice-- ) {
            digito = Integer.parseInt(str.substring(indice,indice+1));
            soma += digito*peso[peso.length-str.length()+indice];
        }
        soma = 11 - soma % 11;

        return soma > 9 ? 0 : soma;
}
'''