from tkinter import*
from tkinter import ttk
from pessoaJuridica.negocio.PessoaJuridicaServices import PessoaJuridicaServices
from infraestrutura.utils.ValidarCpfCnpj import ValidarCpfCnpj
from pessoaJuridica.dominio.PessoaJuridica import PessoaJuridica

pessoaJuridicaServices = PessoaJuridicaServices()

class Application:
    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys presentes no frame
        self.frame = LabelFrame(self.master, bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text='Razão social:').grid(row=3, column=0)
        self.razaoSocial = Entry(self.frame, width=32, bd=2)
        self.razaoSocial.grid(row=3, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Razão social"
        self.erroRazaoSocial = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroRazaoSocial.grid(row=4, column=2)

        Label(self.frame, text='CNPJ:').grid(row=5, column=0)
        self.cnpj = Entry(self.frame, width=32, bd=2)
        self.cnpj.grid(row=5, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "CNPJ"
        self.erroCnpj = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCnpj.grid(row=6, column=2)

        self.btnAdd = ttk.Button(self.frame, text='ATUALIZAR', command=self.atualizarPessoaJuridica).grid(row=7, column=2)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=8, column=2)

        #Populando árvore
        self.popular_arvore()

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
            self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
            self.tree.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
            self.tree["columns"] = ("codigo_cliente", "cnpj", "razao_social")
            self.tree.bind('<Double-1>', self.preencheCampoClick)
            self.tree.heading("#0", text="first", anchor="w")
            self.tree.column("#0", stretch=NO, width=0, anchor="w")
            self.tree.heading("codigo_cliente", text="Código cliente")
            self.tree.column("codigo_cliente", anchor="center", width=100)
            self.tree.heading("cnpj", text="CNPJ")
            self.tree.column("cnpj", anchor="center", width=100)
            self.tree.heading("razao_social", text="Razão social")
            self.tree.column("razao_social", anchor="center", width=200)
            self.listarPessoas()

    #Selecionando todos os dados da tabela pessoa_fisica e inserindo no TreeView
    def listarPessoas(self):
        self.tree.delete(*self.tree.get_children())#Removendo todos os nodos da árvore
        self.pessoas = pessoaJuridicaServices.listarPessoas("SELECT * FROM pessoa_juridica")
        if self.pessoas != None:
            for i in self.pessoas:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto["text"] = self.pessoas

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        razao_social, cnpj = self.razaoSocial.get().strip(), self.cnpj.get().strip()
        verificador = True
        if razao_social == "":
            self.erroRazaoSocial.grid()
            self.erroRazaoSocial["text"] = "*Campo razão social não pode ficar vazio"
            verificador = False
        if cnpj == "":
            self.erroCnpj.grid()
            self.erroCnpj["text"] = "*Campo CNPJ não pode ficar vazio"
            verificador = False
        elif not cnpj.isdigit():
            self.erroCnpj.grid()
            self.erroCnpj["text"] = "*Campo CNPJ só deve conter números"
            verificador = False
        elif len(cnpj) != 14:
            self.erroCnpj.grid()
            self.erroCnpj["text"] = "*Campo CNPJ possui informações inválidas"
            verificador = False
        elif len(cnpj) == 14:
            if not(ValidarCpfCnpj(cnpj).isCnpj()):
                self.erroCnpj.grid()
                self.erroCnpj["text"] = "*Campo CNPJ possui informações inválidas"
                verificador = False
        return verificador

    #Método de validação do cadastro (regras de negócio)
    def validarAtualizacao(self, verificador):
        self.limparLabels()
        booleano = True
        if verificador != None:
            if verificador.args[0] == 1406:
                self.erroRazaoSocial.grid()
                self.erroRazaoSocial["text"] = "*Razão social: máximo de 100 caracteres"
                booleano = False
        return booleano

    #Método que atualiza pessoa jurídica
    def atualizarPessoaJuridica(self):
        pessoaJuridicaAntiga = self.selecionarItem()
        if pessoaJuridicaAntiga != None:
            if self.validarCampos():
                pessoaJuridicaAtual = PessoaJuridica(None, self.cnpj.get().strip(), self.razaoSocial.get().strip())
                verificador = pessoaJuridicaServices.atualizarPessoaJuridica(pessoaJuridicaAntiga.getCodigoCliente(), pessoaJuridicaAtual)
                if self.validarAtualizacao(verificador):
                    self.texto.grid()
                    self.texto["text"] = "Pesso jurídica atualizada com sucesso"
                    self.limparEntry()
                    self.listarPessoas()

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
            codigo_cliente, cnpj, razao_social = self.tree.item(itemSelecionado)['values'][0], \
                                                 self.tree.item(itemSelecionado)['values'][1], \
                                                 self.tree.item(itemSelecionado)['values'][2]
            return PessoaJuridica(codigo_cliente, cnpj, razao_social)

    #Preenchendo campos quando for detectado o evento de double click em algum elemento da árvore
    def preencheCampoClick(self, event):
        if self.tree.focus() != "":
            self.limparEntry()
            pessoaJuridica = self.selecionarItem()
            self.razaoSocial.insert (0, pessoaJuridica.getRazaoSocial())
            self.cnpj.insert(0, pessoaJuridica.getCnpj())

    #Limpando as labels para evitar mensagens de erros inconsistentes
    def limparLabels(self):
        self.erroRazaoSocial["text"] = ""
        self.erroCnpj["text"] = ""
        self.texto["text"] = ""

    #Limapando Entrys após modificações no banco
    def limparEntry(self):
        self.razaoSocial.delete(0, 'end')
        self.cnpj.delete(0, 'end')

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
def intentPessoaJuridica():
    root = Tk()
    root.title("Pessoa jurídica")
    application = Application(root)
    root.mainloop()