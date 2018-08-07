from tkinter import*
from tkinter import ttk
from cliente.negocio.ClienteServices import ClienteServices
from cliente.dominio.Cliente import Cliente

clienteServices = ClienteServices()

class Application:
    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.minsize(width=360, height=450)#Fixando as dimensões do frame master
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

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

        Label(self.frame, text='Rua:').grid(row=7, column=0)
        self.rua = Entry(self.frame, width=32, bd=2)
        self.rua.grid(row=7, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Rua"
        self.erroRua = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroRua.grid(row=8, column=2)

        Label(self.frame, text='Complemento:').grid(row=9, column=0)
        self.complemento = Entry(self.frame, width=32, bd=2)
        self.complemento.grid(row=9, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Complemento"
        self.erroComplemento = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroComplemento.grid(row=10, column=2)

        Label(self.frame, text='Cidade:').grid(row=11, column=0)
        self.cidade = Entry(self.frame, width=32, bd=2)
        self.cidade.grid(row=11, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Cidade"
        self.erroCidade = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCidade.grid(row=12, column=2)

        #ComboBox com os estados do Brasil
        Label(self.frame, text='Estado:').grid(row=13, column=0)
        self.estado = ttk.Combobox(self.frame, width=29, state="readonly")
        self.estado['values'] = ("","AC - Acre", "AL - Alagoas", "AP - Amapá", "AM - Amazonas", "BA - Bahia", "CE - Ceará", "DF - Distrito Federal",
                                 "ES - Espírito Santo","GO - Goiás", "MA - Maranhão", "MT - Mato Grosso", "MS - Mato Grosso do Sul",
                                 "MG - Minas Gerais", "PA - Pará", "PB - Paraíba", "PR - Paraná", "PE - Pernambuco", "PI - Piauí",
                                 "RJ - Rio de Janeiro", "RN - Rio Grande do Norte", "RS - Rio Grande do Sul", "RO - Rondônia", "RR - Roraima",
                                 "SC - Santa Catarina", "SP - São Paulo", "SE - Sergipe", "TO - Tocatins")
        self.estado.grid(row=13, column=2)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=16, column=2)

        #Label necessário para manter o espaçamento do botão cadastrar do comboBox
        self.ajuste = Label(self.frame)
        self.ajuste.grid(row=14, column=2)

        self.btnAdd = ttk.Button(self.frame, text='CADASTRAR', command=self.validarCampos).grid(row=15, column=2)

        #Populando árvore
        self.popular_arvore()

        #Cria barra de rolagem
        self.barra = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        #Adiciona barra de rolagem
        self.barra.place(x=390, y=318, height=218 + 10)

        self.tree.configure(yscroll=self.barra.set)

        #Botões de interação
        self.btnApagar = ttk.Button(text='Deletar cliente', command=self.selecionarItem)
        self.btnApagar.grid(row=4, column=3, sticky=N)
        self.btnAtualizar = ttk.Button(text='Atualizar cliente')
        self.btnAtualizar.grid(row=4, column=3, sticky=S, padx=10)

    def montarEndereco(self):
        return self.rua.get().strip() + ", " + self.complemento.get().strip() + ". " + self.cidade.get().strip() + ", " + self.estado.get() + "."

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        codigo, telefone, endereco = self.codigo.get().strip(), self.telefone.get().strip(), self.montarEndereco()
        verificador = True
        if codigo == "":
            self.erroCodigo.grid()
            self.erroCodigo["text"] = "*Campo telefone não pode ficar vazio"
            verificador = False
        elif not str(codigo).isdigit():
            self.erroCodigo.grid()
            self.erroCodigo["text"] = "*Campo matrícula só deve conter números"
            verificador = False
        if telefone == "":
            self.erroTelefone.grid()
            self.erroTelefone["text"] = "*Campo telefone não pode ficar vazio"
            verificador = False
        if verificador:
            self.inserirCliente(Cliente(codigo, telefone, endereco))

    #Método de validação do cadastro (regras de negócio)
    def validarCadastro(self, verificador):
        self.limparLabels()
        if verificador == 1062:
            self.texto.grid()
            self.texto["text"] = "Cliente já cadastrado no sistema"
        elif verificador == 1406:
            self.erroTelefone.grid()
            self.erroCodigo.grid()
            self.erroTelefone["text"] = "Telefone: máximo de 20 caracteres"
            self.erroCodigo["text"] = "Código: máximo de 11 caracteres"
        else:
            self.texto.grid()
            self.texto["text"] = "Cliente cadstrado com sucesso!"
            self.listarClientes()

    #Método de inserção do cliente no banco de dados
    def inserirCliente(self, cliente):
        verificador = clienteServices.inserirCliente(cliente)
        self.validarCadastro(verificador)

    #Método que remove cliente do banco de dados
    def removerCliente(self, cliente):
        self.limparLabels()
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
        self.tree.grid(row=4, column=0, columnspan=2)
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
        self.removerCliente(Cliente(codigo, telefone, endereco))

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