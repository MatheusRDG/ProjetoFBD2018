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
        self.frame = LabelFrame(self.master, bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text = 'Código:').grid(row=3, column=0)
        self.codigo = Entry(self.frame, width=22, bd=2)
        self.codigo.grid(row=3, column=1)

        #Label de exibição das mensagens de erros referentes ao campo código
        self.erroCodigo = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCodigo.grid(row=4, column=1)

        Label(self.frame, text='Telefone:').grid(row=5, column=0)
        self.telefone = Entry(self.frame, width=22, bd=2)
        self.telefone.grid(row=5, column=1)

        #Label de exibição das mensagens de erros referentes ao campo "Telefone"
        self.erroTelefone = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroTelefone.grid(row=6, column=1)

        Label(self.frame, text='CPF/CNPJ:').grid(row=9, column=2)
        self.cpfCnpj = Entry(self.frame, width=22, bd=2)
        self.cpfCnpj.grid(row=9, column=3)

        # Label de exibição das mensagens de erros referentes ao campo "Cpf/Cnpj"
        self.erroCpfCnpj = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCpfCnpj.grid(row=10, column=3)

        Label(self.frame, text='Nome/Razão Social:').grid(row=9, column=0)
        self.nomeRazaoSocial = Entry(self.frame, width=22, bd=2)
        self.nomeRazaoSocial.grid(row=9, column=1)

        # Label de exibição das mensagens de erros referentes ao campo "Nome/Razão Social"
        self.erroNomeRazaoSocial = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroNomeRazaoSocial.grid(row=10, column=1)

        Label(self.frame, text='Rua:').grid(row=11, column=0)
        self.rua = Entry(self.frame, width=22, bd=2)
        self.rua.grid(row=11, column=1)

        #Label de exibição das mensagens de erros referentes ao campo "Rua"
        self.erroRua = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroRua.grid(row=12, column=1)

        Label(self.frame, text='Complemento:').grid(row=11, column=2)
        self.complemento = Entry(self.frame, width=22, bd=2)
        self.complemento.grid(row=11, column=3)

        #Label de exibição das mensagens de erros referentes ao campo "Complemento"
        self.erroComplemento = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroComplemento.grid(row=12, column=3)

        Label(self.frame, text='Cidade:').grid(row=15, column=0)
        self.cidade = Entry(self.frame, width=22, bd=2)
        self.cidade.grid(row=15, column=1)

        #Label de exibição das mensagens de erros referentes ao campo "Cidade"
        self.erroCidade = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCidade.grid(row=16, column=1)

        #ComboBox com os estados do Brasil
        Label(self.frame, text='Estado:').grid(row=17, column=0)
        self.estado = ttk.Combobox(self.frame, width=29, state="readonly")
        self.estado['values'] = (self.estados)
        self.estado.grid(row=17, column=1)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=21, column=1)

        #Label necessário para manter o espaçamento do botão cadastrar do comboBox
        self.ajuste = Label(self.frame)
        self.ajuste.grid(row=18, column=2)

        self.btnAdd = ttk.Button(self.frame, text='CADASTRAR', command=self.verificarTipoPessoa).grid(row=19, column=1)

        #Populando árvore
        self.popular_arvore()

        #Cria scrollbar_vertical de rolagem
        self.scrollbar_vertical = Scrollbar(self.master, orient='vertical', command=self.tree.yview)
        self.scrollbar_horizontal = Scrollbar(self.master, orient='horizontal', command=self.tree.xview)

        #Adiciona scrollbar_vertical de rolagem
        self.scrollbar_vertical.place(x=698, y=377, height=218 + 10)
        self.scrollbar_horizontal.place(x=0, y=600, width=698)

        self.tree.configure(yscroll=self.scrollbar_vertical.set)
        self.tree.configure(xscroll=self.scrollbar_horizontal.set)

        #Botões de interação
        self.btnApagar = ttk.Button(text='DELETAR', command=self.removerCliente)
        self.btnApagar.grid(row=4, column=4, padx=20)
        self.btnAtualizar = ttk.Button(self.frame, text='ATUALIZAR', command=self.atualizarCliente)
        self.btnAtualizar.grid(row=20, column=1, padx=10, pady=10)

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        dados = self.retornarDadosEntrys()
        codigo, telefone, endereco, cpfCnpj, nomeRazaoSocial = dados[0], dados[1], dados[2], dados[3], dados[4]
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
        elif not cpfCnpj.isdigit():
            self.erroCpfCnpj.grid()
            self.erroCpfCnpj["text"] = "*Campo CPF/CNPJ só deve conter números"
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
        self.limparLabels()
        booleano = True
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "*Cliente já cadastrado no sistema"
                booleano = False
            elif verificador.args[0] == 1406:
                if "telefone" in verificador.args[1]:
                    self.erroTelefone.grid()
                    self.erroTelefone["text"] = "*Telefone: máximo de 20 caracteres"
                    booleano = False
                if "endereco" in verificador.args[1]:
                    self.texto.grid()
                    self.texto['text'] = "*Reduza as informações do endereço (Máximo: 100 caracteres)"
                    booleano = False
            elif verificador.args[0] == 1264:
                self.erroCodigo.grid()
                self.erroCodigo["text"] = "*Valor máximo excedido do código do cliente (máximo: 11 caracteres)"
                booleano = False
        return booleano

    #Validando cadastro da pessoa física
    def validarCadastroPessoa(self, verificador):
        booleano = True
        self.limparLabels()
        if verificador != None:
            if verificador.args[0] == 1406:
                self.erroNomeRazaoSocial.grid()
                self.erroNomeRazaoSocial["text"] = "Nome/Razão Social: máximo 100 caracteres"
                booleano = False
        return booleano

    def verificarTipoPessoa(self):
        if self.validarCampos():
            dados = self.retornarDadosEntrys()
            cliente, cpfCnpj = Cliente(dados[0], str(dados[1]), dados[2]), dados[3]
            if cliente.getEndereco() == ", . , .":
                cliente.setEndereco("null")
            if self.inserirCliente(cliente):
                if len(self.cpfCnpj.get().strip()) == 11:#isPessoaFísica
                    self.inserirPessoaFisica(PessoaFisica(cliente.getCodigo(), cpfCnpj, self.nomeRazaoSocial.get().strip()), cliente)
                else:
                    self.inserirPessoaJuridica(PessoaJuridica(cliente.getCodigo(), cpfCnpj, self.nomeRazaoSocial.get().strip()), cliente)

    #Método de inserção do cliente no banco de dados
    def inserirCliente(self, cliente):
        verificador = clienteServices.inserirCliente(cliente)
        if self.validarCadastroCliente(verificador):
            return True

    #Inserindo pessoa física no banco
    def inserirPessoaFisica(self, pessoaFisica, cliente):
        verificador = pessoaFisicaServices.inserirPessoaFisica(pessoaFisica)
        if self.validarCadastroPessoa(verificador):
            self.texto.grid()
            self.texto["text"] = "Cliente cadastrado com sucesso"
            self.limparEntry()
            self.listarClientes()
        else:
            clienteServices.removerCliente(cliente)

    #Inserindo pessoa jurídica no banco
    def inserirPessoaJuridica(self, pessoaJuridica, cliente):
        verificador = pessoaJuridicaServices.inserirPessoaJuridica(pessoaJuridica)
        if self.validarCadastroPessoa(verificador):
            self.texto.grid()
            self.texto["text"] = "Cliente cadastrado com sucesso"
            self.limparEntry()
            self.listarClientes()
        else:
            clienteServices.removerCliente(cliente)

    #Método que remove cliente do banco de dados
    def removerCliente(self):
        self.limparLabels()
        cliente = self.selecionarItem()
        if cliente != None:
            verificador = clienteServices.removerCliente(cliente)
            if verificador == None:
                self.texto["text"] = "Cliente excluído com sucesso"
                self.limparEntry()
                self.listarClientes()
            else:
                self.texto["text"] = "Error: %s" %verificador.args[1]

    def validarCamposAtualizacao(self):
        self.limparLabels()
        telefone = self.telefone.get().strip()
        verificador = True
        if telefone == "":
            self.erroTelefone.grid()
            self.erroTelefone["text"] = "*Erro ao atualizar! Esse campo não pode ficar vazio"
            verificador = False
        return verificador

    #Método que atualiza o cliente cadastrado no banco de dados
    def atualizarCliente(self):
        self.limparLabels()
        clienteAntigo = self.selecionarItem()
        if clienteAntigo != None:
            if self.validarCamposAtualizacao():
                cilenteAtual = self.retornarDadosEntrys()
                clienteAtual = Cliente(cilenteAtual[0], cilenteAtual[1], cilenteAtual[2])
                if clienteAtual.getEndereco() == ", . , .":
                    clienteAtual.setEndereco("null")
                verificador = clienteServices.atualizarCliente(clienteAntigo.getCodigo(), clienteAtual)
                if self.validarCadastroCliente(verificador):
                    self.texto.grid()
                    self.texto["text"] = "Cliente atualizado com sucesso"
                    self.limparEntry()
                    self.listarClientes()

    #Preenchendo campos quando for detectado o evento de double click em algum elemento da árvore
    def preencheCampoClick(self, event):
        if self.tree.focus() != "":
            self.limparEntry()
            self.limparLabels()
            self.texto["text"] = "*Atualize todos os campos exceto o campo código"
            cliente = self.selecionarItem()
            self.codigo.insert (0,cliente.getCodigo())
            self.telefone.insert(0,cliente.getTelefone())
            if cliente.getEndereco() != "null":
                lista = cliente.getEndereco().split(",")
                self.rua.insert(0,lista[0])
                self.complemento.insert(0,lista[1].split(".")[0])
                self.cidade.insert(0,lista[1].split(".")[1])
                #Setando o Estado
                index = list(self.estados).index(lista[2].replace(".","").strip())
                self.estado.set(self.estados[index])

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
        self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
        self.tree.bind('<Double-1>', self.preencheCampoClick)
        self.tree.grid(row=4, column=0, columnspan=3, pady=20, sticky="WE")
        self.tree["columns"] = ("codigo", "telefone", "endereco")
        self.tree.heading("#0", text="first", anchor="w")
        self.tree.column("#0", stretch=NO, width=0, anchor="w")
        self.tree.heading("codigo", text="Código")
        self.tree.column("codigo", anchor="center", width=100, minwidth=150, stretch=True)
        self.tree.heading("telefone", text="Telefone")
        self.tree.column("telefone", anchor="center", width=100, minwidth=150, stretch=True)
        self.tree.heading("endereco", text="Endereço")
        self.tree.column("endereco", anchor="center", width=500, minwidth=550, stretch=True)
        self.listarClientes()

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
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

    #Montando string de endereço
    def montarEndereco(self):
        return self.rua.get().strip() + ", " + self.complemento.get().strip() + ". " + self.cidade.get().strip() + ", " + self.estado.get() + "."

    #Retornando os dados digitados nos Entrys
    def retornarDadosEntrys(self):
        return (self.codigo.get().strip(), ''.join(re.findall('\d', self.telefone.get().strip())), self.montarEndereco(),
                                        ''.join(re.findall('\d', self.cpfCnpj.get().strip())), self.nomeRazaoSocial.get().strip())

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

    #Limapando Entrys após modificações no banco
    def limparEntry(self):
        self.codigo.delete(0, 'end')
        self.telefone.delete(0, 'end')
        self.rua.delete(0, 'end')
        self.cpfCnpj.delete(0, 'end')
        self.nomeRazaoSocial.delete(0, 'end')
        self.complemento.delete(0, 'end')
        self.cidade.delete(0, 'end')
        self.estado.set('')

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == '__main__':
    root = Tk()
    root.title("Clientes")
    application = Application(root)
    root.mainloop()