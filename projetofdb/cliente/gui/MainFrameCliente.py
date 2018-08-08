from tkinter import*
from tkinter import ttk
from cliente.negocio.ClienteServices import ClienteServices
from pessoaFisica.negocio.PessoaFisicaServices import PessoaFisicaServices
from pessoaJuridica.negocio.PessoaJuridicaServices import PessoaJuridicaServices
from infraestrutura.utils.ValidarCpfCnpj import ValidarCpfCnpj
from cliente.dominio.Cliente import Cliente
from pessoaFisica.dominio.PessoaFisica import PessoaFisica
from pessoaJuridica.dominio.PessoaJuridica import PessoaJuridica

import re

clienteServices = ClienteServices()
pessoaFisicaServices = PessoaFisicaServices()
pessoaJuridicaServices = PessoaJuridicaServices()

class Application:
    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro
        self.estados = ("","AC - Acre", "AL - Alagoas", "AP - Amapá", "AM - Amazonas", "BA - Bahia", "CE - Ceará", "DF - Distrito Federal",
                                 "ES - Espírito Santo","GO - Goiás", "MA - Maranhão", "MT - Mato Grosso", "MS - Mato Grosso do Sul",
                                 "MG - Minas Gerais", "PA - Pará", "PB - Paraíba", "PR - Paraná", "PE - Pernambuco", "PI - Piauí",
                                 "RJ - Rio de Janeiro", "RN - Rio Grande do Norte", "RS - Rio Grande do Sul", "RO - Rondônia", "RR - Roraima",
                                 "SC - Santa Catarina", "SP - São Paulo", "SE - Sergipe", "TO - Tocatins")

        #LabelFrame que comporta as Labels e Entrys presentes no frame
        self.frame = LabelFrame(self.master, text='Cadastrar novo cliente', bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text = 'Código:').grid(row=3, column=0)
        self.codigo = Entry(self.frame, width=32, bd=2)
        self.codigo.grid(row=3, column=2)

        #Label de exibição das mensagens de erros referentes ao campo código
        self.erroCodigo = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCodigo.grid(row=4, column=2)

        Label(self.frame, text='Telefone:').grid(row=5, column=0)
        self.telefone = Entry(self.frame, width=32, bd=2)
        self.telefone.grid(row=5, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Telefone"
        self.erroTelefone = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroTelefone.grid(row=6, column=2)

        Label(self.frame, text='CPF/CNPJ:').grid(row=7, column=0)
        self.cpfCnpj = Entry(self.frame, width=32, bd=2)
        self.cpfCnpj.grid(row=7, column=2)

        # Label de exibição das mensagens de erros referentes ao campo "Cpf/Cnpj"
        self.erroCpfCnpj = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCpfCnpj.grid(row=8, column=2)

        Label(self.frame, text='Nome/Razão Social:').grid(row=9, column=0)
        self.nomeRazaoSocial = Entry(self.frame, width=32, bd=2)
        self.nomeRazaoSocial.grid(row=9, column=2)

        # Label de exibição das mensagens de erros referentes ao campo "Nome/Razão Social"
        self.erroNomeRazaoSocial = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroNomeRazaoSocial.grid(row=10, column=2)

        Label(self.frame, text='Rua:').grid(row=11, column=0)
        self.rua = Entry(self.frame, width=32, bd=2)
        self.rua.grid(row=11, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Rua"
        self.erroRua = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroRua.grid(row=12, column=2)

        Label(self.frame, text='Complemento:').grid(row=13, column=0)
        self.complemento = Entry(self.frame, width=32, bd=2)
        self.complemento.grid(row=13, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Complemento"
        self.erroComplemento = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroComplemento.grid(row=14, column=2)

        Label(self.frame, text='Cidade:').grid(row=15, column=0)
        self.cidade = Entry(self.frame, width=32, bd=2)
        self.cidade.grid(row=15, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Cidade"
        self.erroCidade = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCidade.grid(row=16, column=2)

        #ComboBox com os estados do Brasil
        Label(self.frame, text='Estado:').grid(row=17, column=0)
        self.estado = ttk.Combobox(self.frame, width=29, state="readonly")
        self.estado['values'] = (self.estados)
        self.estado.grid(row=17, column=2)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=20, column=2)

        #Label necessário para manter o espaçamento do botão cadastrar do comboBox
        self.ajuste = Label(self.frame)
        self.ajuste.grid(row=18, column=2)

        self.btnAdd = ttk.Button(self.frame, text='CADASTRAR', command=self.verificarTipoPessoa).grid(row=19, column=2)

        #Populando árvore
        self.popular_arvore()

        #Cria barra de rolagem
        self.barra = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        #Adiciona barra de rolagem
        self.barra.place(x=390, y=400, height=218 + 10)

        self.tree.configure(yscroll=self.barra.set)

        #Botões de interação
        self.btnApagar = ttk.Button(text='Deletar cliente', command=self.removerCliente)
        self.btnApagar.grid(row=4, column=3, sticky=N)
        self.btnAtualizar = ttk.Button(text='Atualizar cliente', command=self.frameAtualizar)
        self.btnAtualizar.grid(row=4, column=3, sticky=S, padx=10, pady=10)

    def frameAtualizar(self):
        if self.tree.focus() != "":
            #Falta continuar
            clienteSelecionado = self.selecionarItem()
            topLevel = Toplevel()
            topLevel.title("Atualizar cliente")
            topLevel.geometry("300x300+100+100")
            topLevel.resizable(width=0, height=0)  # Retirando o opção de maximização do frame master
            topLevel.grab_set()#Direcinando o foco para a nova label
            self.inserirWidgets(topLevel)

    def inserirWidgets(self, topLevel):
        labelCodigo = Label(topLevel, text="Código", height=0, width=100)
        labelCodigo.pack()
        entryCodigo = Entry(topLevel, width=32, bd=2)
        entryCodigo.pack()
        labelTelefone = Label(topLevel, text="Telefone", height=0, width=100)
        labelTelefone.pack()
        entryTelefone = Entry(topLevel, width=32, bd=2)
        entryTelefone.pack()
        labelRua = Label(topLevel, text="Rua", height=0, width=100)
        labelRua.pack()
        entryRua = Entry(topLevel, width=32, bd=2)
        entryRua.pack()
        labelComplemento = Label(topLevel, text="Complemento", height=0, width=100)
        labelComplemento.pack()
        entryComplemento = Entry(topLevel, width=32, bd=2)
        entryComplemento.pack()
        labelCidade = Label(topLevel, text="Cidade", height=0, width=100)
        labelCidade.pack()
        entryCidade = Entry(topLevel, width=32, bd=2)
        entryCidade.pack()
        labelEstado = Label(topLevel, text='Estado:', height=0, width=100)
        labelEstado.pack()
        boxEstados = ttk.Combobox(topLevel, width=29, state="readonly")
        boxEstados['values'] = (self.estados)
        boxEstados.pack()
        buttonAlterar = ttk.Button(topLevel, text='ALTERAR')
        buttonAlterar.pack(pady=10)

    def montarEndereco(self):
        return self.rua.get().strip() + ", " + self.complemento.get().strip() + ". " + self.cidade.get().strip() + ", " + self.estado.get() + "."

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        codigo, telefone, endereco, cpfCnpj, nomeRazaoSocial = self.codigo.get().strip(), self.telefone.get().strip(), self.montarEndereco(), \
                                                               ''.join(re.findall('\d', str(self.cpfCnpj.get().strip()))), self.nomeRazaoSocial.get().strip()
        verificador = True
        if codigo == "":
            self.erroCodigo.grid()
            self.erroCodigo["text"] = "*Campo código não pode ficar vazio"
            verificador = False
        elif not str(codigo).isdigit():
            self.erroCodigo.grid()
            self.erroCodigo["text"] = "*Campo código só deve conter números"
            verificador = False
        if telefone == "":
            self.erroTelefone.grid()
            self.erroTelefone["text"] = "*Campo telefone não pode ficar vazio"
            verificador = False
        if cpfCnpj == "":
            self.erroCpfCnpj.grid()
            self.erroCpfCnpj["text"] = "*Campo CPF/CNPJ não deve ficar vazio"
            verificador = False
        elif len(cpfCnpj) != 11 and len(cpfCnpj) != 14:
            self.erroCpfCnpj.grid()
            self.erroCpfCnpj["text"] = "*Campo CPF/CNPJ possui informações inválidas"
            verificador = False
        elif len(cpfCnpj) == 11:
            if not(ValidarCpfCnpj(cpfCnpj).isCpf()):
                self.erroCpfCnpj.grid()
                self.erroCpfCnpj["text"] = "*Campo CPF/CNPJ possui informações inválidas"
                verificador = False
        elif len(cpfCnpj) == 14:
            if not(ValidarCpfCnpj(cpfCnpj).isCnpj()):
                self.erroCpfCnpj.grid()
                self.erroCpfCnpj["text"] = "*Campo CPF/CNPJ possui informações inválidas"
                verificador = False
        if nomeRazaoSocial == "":
            self.erroNomeRazaoSocial.grid()
            self.erroNomeRazaoSocial["text"] = "*Campo Nome/Razão Social não deve ficar vazio"
            verificador = False

        return verificador

    #Método de validação do cadastro (regras de negócio)
    def validarCadastroCliente(self, verificador):
        booleano = True
        self.limparLabels()
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "Cliente já cadastrado no sistema"
                booleano = False
            elif verificador.args[0] == 1406:
                if "telefone" in verificador.args[1]:
                    self.erroTelefone.grid()
                    self.erroTelefone["text"] = "Telefone: máximo de 20 caracteres"
                    booleano = False
                else:
                    self.erroCodigo.grid()
                    self.erroCodigo["text"] = "Código: máximo de 11 caracteres"
                    booleano = False
        return booleano

    def validarCadastroPessoa(self, verificador):
        booleano = True
        self.limparLabels()
        if verificador != None:
            if verificador.args[0] == 1046:
                self.erroNomeRazaoSocial.grid()
                self.erroNomeRazaoSocial["text"] = "Nome/Razão Social: máximo 100 caracteres"
                booleano = False
        return booleano

    def verificarTipoPessoa(self):
        if self.validarCampos():
            cliente = Cliente(self.codigo.get().strip(), self.telefone.get().strip(), self.montarEndereco())
            cpfCnpj = ''.join(re.findall('\d', str(self.cpfCnpj.get().strip())))
            if self.inserirCliente(cliente):
                if len(self.cpfCnpj.get().strip()) == 11:#isPessoaFísica
                    self.inserirPessoaFisica(PessoaFisica(cliente.getCodigo(), cpfCnpj, self.nomeRazaoSocial.get().strip()))
                else:
                    self.inserirPessoaJuridica(PessoaJuridica(cliente.getCodigo(), cpfCnpj, self.nomeRazaoSocial.get().strip()))

    #Método de inserção do cliente no banco de dados
    def inserirCliente(self, cliente):
        verificador = clienteServices.inserirCliente(cliente)
        if self.validarCadastroCliente(verificador):
            return True

    #Inserindo pessoa física no banco
    def inserirPessoaFisica(self, pessoaFisica):
        verificador = pessoaFisicaServices.inserirPessoaFisica(pessoaFisica)
        if self.validarCadastroPessoa(verificador):
            self.texto.grid()
            self.texto["text"] = "Cliente cadastrado com sucesso"
            self.listarClientes()

    #Inserindo pessoa jurídica no banco
    def inserirPessoaJuridica(self, pessoaJuridica):
        verificador = pessoaJuridicaServices.inserirPessoaJuridica(pessoaJuridica)
        if self.validarCadastroPessoa(verificador):
            self.texto.grid()
            self.texto["text"] = "Cliente cadastrado com sucesso"
            self.listarClientes()

    #Método que remove cliente do banco de dados
    def removerCliente(self):
        self.limparLabels()
        cliente = self.selecionarItem()
        verificador = clienteServices.removerCliente(cliente)
        if verificador == None:
            self.texto["text"] = "Cliente excluído com sucesso"
            self.listarClientes()
        else:
            self.texto["text"] = verificador

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
        self.tree = ttk.Treeview(self.master,height=10, columns=2, selectmode='browse')
        #self.tree.bind('<ButtonRelease-1>', self.selecionarItem)
        self.tree.grid(row=4, column=0, columnspan=3)
        self.tree["columns"] = ("codigo", "telefone", "endereco")
        self.tree.heading("#0", text="first", anchor="w")
        self.tree.column("#0", stretch=NO, width=0, anchor="w")
        self.tree.heading("codigo", text="Código")
        self.tree.column("codigo", anchor="center", width=100)
        self.tree.heading("telefone", text="Telefone")
        self.tree.column("telefone", anchor="center", width=100)
        self.tree.heading("endereco", text="Endereço")
        self.tree.column("endereco", anchor="center", width=200)
        self.listarClientes()

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        codigo, telefone, endereco = str(self.tree.item(itemSelecionado)['values'][0]), self.tree.item(itemSelecionado)['values'][1], self.tree.item(itemSelecionado)['values'][2]

        return Cliente(codigo, telefone, endereco)

    #Selecionando todos os dados da tabela cliente e inserindo no TreeView
    def listarClientes(self):
        self.tree.delete(*self.tree.get_children())#Removendo todos os nodos da árvore
        self.clientes = clienteServices.listarClientes("SELECT * FROM cliente")
        if self.clientes != None:
            for i in self.clientes:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto["text"] = self.clientes

    #Limpando as labels para evitar mensagens de erros inconsistentes
    def limparLabels(self):
        self.erroCodigo["text"] = ""
        self.erroTelefone["text"] = ""
        self.erroCpfCnpj["text"] = ""
        self.erroNomeRazaoSocial["text"] = ""
        self.erroRua["text"] = ""
        self.erroComplemento["text"] = ""
        self.erroCidade["text"] = ""
        self.texto["text"] = ""

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == '__main__':
    root = Tk()
    root.title("Clientes")
    application = Application(root)
    root.mainloop()