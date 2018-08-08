from tkinter import*
from tkinter import ttk
from empregado.negocio.EmpregadoServices import EmpregadoServices
from empregado.dominio.Empregado import Empregado

empragadoServices = EmpregadoServices()

class Application:

    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.minsize(width=360, height=450)#Fixando as dimensões do frame master
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys dos campos "Matrícula" e "Nome"
        self.frame = LabelFrame(self.master, text='Cadastrar novo empregado', bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text = 'Matrícula:').grid(row=3, column=0)
        self.matricula = Entry(self.frame, width=32, bd=2)
        self.matricula.grid(row=3, column=2)

        #Label de exibição das mensagens de erros referentes ao campo Matrícula
        self.erroMatricula = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroMatricula.grid(row=4, column=2)

        Label(self.frame, text='Nome:').grid(row=5, column=0)
        self.nome = Entry(self.frame, width=32, bd=2)
        self.nome.grid(row=5, column=2)

        #Label de exibição das mensagens de erros referentes ao campo Nome
        self.erroNome = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroNome.grid(row=6, column=2)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text="", font=self.fontErro, fg="red")
        self.texto.grid(row=8, column=2)

        self.btnAdd = ttk.Button(self.frame, text='CADASTRAR', command=self.validarCampos).grid(row=7, column=2)

        #Populando árvore
        self.popular_arvore()

        #Cria barra de rolagem
        self.barra = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        #Adiciona barra de rolagem
        self.barra.place(x=330, y=174, height=217 + 10)

        self.tree.configure(yscroll=self.barra.set)

        #Botões de interação
        self.btnApagar = ttk.Button(text='Deletar empregado', command=self.selecionarItem)
        self.btnApagar.grid(row=4, column=3, sticky=N)
        self.btnAtualizar = ttk.Button(text='Atualizar empregado')
        self.btnAtualizar.grid(row=4, column=3, sticky=S, padx=10)

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        matricula, nome = self.matricula.get().strip(), self.nome.get().strip()
        verificador = True
        if matricula == "":
            self.erroMatricula.grid()
            self.erroMatricula["text"] = "*Campo matrícula não pode ficar vazio"
            verificador = False
        elif not str(matricula).isdigit():
            self.erroMatricula.grid()
            self.erroMatricula["text"] = "*Campo matrícula só deve conter números"
            verificador = False
        if nome == "":
            self.erroNome.grid()
            self.erroNome["text"] = "*Campo nome não pode ficar vazio"
            verificador = False

        if verificador:
            self.inserirEmpregado(Empregado(matricula, nome))

    #Método de validação do cadastro (regras de negócio)
    def validarCadastro(self, verificador):
        self.limparLabels()
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "Empregado já cadastrado no sistema"
            elif verificador.args[0] == 1406:
                if "nome" in verificador.args[1]:
                    self.erroNome.grid()
                    self.erroNome["text"] = "Nome: máximo de 100 caracteres"
                else:
                    self.erroMatricula.grid()
                    self.erroMatricula["text"] = "Matrícula: máximo de 11 caracteres"
        else:
            self.texto.grid()
            self.texto["text"] = "Empregado cadstrado com sucesso!"
            self.listarEmpregados()

    #Método de inserção do empregado no banco de dados
    def inserirEmpregado(self, empregado):
        verificador = empragadoServices.inserirEmpregado(empregado)
        self.validarCadastro(verificador)

    #Método que remove empregado do banco de dados
    def removerEmpregado(self, empregado):
        self.limparLabels()
        verificador = empragadoServices.deletarEmpregado(empregado)
        if verificador == None:
            self.texto["text"] = "Empregado excluído com sucesso"
            self.listarEmpregados()
        else:
            self.texto["text"] = verificador

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
        self.tree = ttk.Treeview(self.master,height=10, columns=2, selectmode='browse')
        #self.tree.bind('<ButtonRelease-1>', self.selecionarItem)
        self.tree.grid(row=4, column=0, columnspan=2, pady=20, padx=20)
        self.tree["columns"] = ("matricula", "nome")
        self.tree.heading("#0", text="first", anchor="w")
        self.tree.column("#0", stretch=NO, width=0, anchor="w")
        self.tree.heading("matricula", text="Matrícula")
        self.tree.column("matricula", anchor="center", width=120)
        self.tree.heading("nome", text="Nome")
        self.tree.column("nome", anchor="center", width=190)
        self.listarEmpregados()

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        matricula, nome = str(self.tree.item(itemSelecionado)['values'][0]), self.tree.item(itemSelecionado)['values'][1]
        self.removerEmpregado(Empregado(matricula, nome))

    #Selecionando todos os dados da tabela empregado e inserindo no TreeView
    def listarEmpregados(self):
        self.tree.delete(*self.tree.get_children())#Removendo todos os nodos da árvore
        self.empregados = empragadoServices.listarEmpregados("SELECT * FROM empregado")
        if self.empregados != None:
            for i in self.empregados:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto['text'] = self.empregados

    #Limpando as labels para evitar mensagens de erros inconsistentes
    def limparLabels(self):
        self.erroMatricula["text"] = ""
        self.erroNome["text"] = ""
        self.texto["text"] = ""

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == '__main__':
    root = Tk()
    root.title("Empregados")
    application = Application(root)
    root.mainloop()