from tkinter import*
from tkinter import ttk
from pessoaFisica.negocio.PessoaFisicaServices import PessoaFisicaServices

pessoaFisicaServices = PessoaFisicaServices()

class Application:
    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys presentes no frame
        self.frame = LabelFrame(self.master, bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text='Nome:').grid(row=3, column=0)
        self.nome = Entry(self.frame, width=32, bd=2)
        self.nome.grid(row=3, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Nome"
        self.erroNome = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroNome.grid(row=4, column=2)

        Label(self.frame, text='CPF:').grid(row=5, column=0)
        self.cpf = Entry(self.frame, width=32, bd=2)
        self.cpf.grid(row=5, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Cpf"
        self.erroCpf = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCpf.grid(row=6, column=2)

        self.btnAdd = ttk.Button(self.frame, text='ATUALIZAR').grid(row=7, column=2)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=8, column=2)

        #Populando árvore
        self.popular_arvore()

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
            self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
            self.tree.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
            self.tree["columns"] = ("codigo_cliente", "descricao", "codigo")
            self.tree.heading("#0", text="first", anchor="w")
            self.tree.column("#0", stretch=NO, width=0, anchor="w")
            self.tree.heading("codigo_cliente", text="Código cliente")
            self.tree.column("codigo_cliente", anchor="center", width=100)
            self.tree.heading("descricao", text="CPF")
            self.tree.column("descricao", anchor="center", width=100)
            self.tree.heading("codigo", text="Nome")
            self.tree.column("codigo", anchor="center", width=200)
            self.listarPessoas()

    #Selecionando todos os dados da tabela pessoa_fisica e inserindo no TreeView
    def listarPessoas(self):
        self.tree.delete(*self.tree.get_children())#Removendo todos os nodos da árvore
        self.pessoas = pessoaFisicaServices.listarPessoasFisicas("SELECT * FROM pessoa_fisica")
        if self.pessoas != None:
            for i in self.pessoas:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto["text"] = self.pessoas

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == '__main__':
    root = Tk()
    root.title("Pessoa física")
    application = Application(root)
    root.mainloop()