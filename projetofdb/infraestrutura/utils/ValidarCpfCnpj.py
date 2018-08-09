import re

class ValidarCpfCnpj:

    def __init__(self, cpf_cnpj):
        self.cpf_cnpj = cpf_cnpj

    def isCpf(self):#By: hdiogenes -> https://pt.stackoverflow.com/questions/64608/como-validar-e-calcular-o-d%C3%ADgito-de-controle-de-um-cpf
        cpf = ''.join(re.findall(r'\d', str(self.cpf_cnpj)))

        antigo = [int(d) for d in cpf]
        #Gera CPF com novos dígitos verificadores e compara com CPF informado
        novo = antigo[:9]
        while len(novo) < 11:
            resto = sum([v * (len(novo) + 1 - i) for i, v in enumerate(novo)]) % 11
            digito_verificador = 0 if resto <= 1 else 11 - resto
            novo.append(digito_verificador)
        if novo == antigo:
            return True
        return False

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