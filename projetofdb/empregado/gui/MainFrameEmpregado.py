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
        self.frame = LabelFrame(self.master, bd=10, padx=10)
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
        self.texto.grid(row=9, column=2)

        self.btnCadastrar = ttk.Button(self.frame, text='CADASTRAR', command=self.inserirEmpregado).grid(row=7, column=2)

        #Populando árvore
        self.popular_arvore()

        #Cria scrollbar_vertical de rolagem
        self.scrollbar_vertical = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        #Adiciona scrollbar_vertical de rolagem
        self.scrollbar_vertical.place(x=330, y=212, height=217 + 10)

        self.tree.configure(yscroll=self.scrollbar_vertical.set)

        #Botões de interação
        self.btnApagar = ttk.Button(text='DELETAR', command=self.removerEmpregado)
        self.btnApagar.grid(row=4, column=3)
        self.btnAtualizar = ttk.Button(self.frame, text='ATUALIZAR', command=self.atualizarEmpregado)
        self.btnAtualizar.grid(row=8, column=2, pady=10)

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        matricula, nome = self.matricula.get().strip(), self.nome.get().strip()
        verificador = True
        if matricula == "":
            self.erroMatricula.grid()
            self.erroMatricula["text"] = "*Campo matrícula não pode ficar vazio"
            verificador = False
        elif not matricula.isdigit():
            self.erroMatricula.grid()
            self.erroMatricula["text"] = "*Campo matrícula só deve conter números"
            verificador = False
        if nome == "":
            self.erroNome.grid()
            self.erroNome["text"] = "*Campo nome não pode ficar vazio"
            verificador = False
        return verificador

    #Método atualização
    def validarAtualizacao(self):
        self.limparLabels()
        nome = self.nome.get().strip()
        verificador = True
        if nome == "":
            self.erroNome.grid()
            self.erroNome["text"] = "*Campo nome não pode ficar vazio"
            verificador = False
        return verificador

    #Método de validação do cadastro (regras de negócio)
    def validarCadastro(self, verificador):
        self.limparLabels()
        booleano = True
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "*Empregado já cadastrado no sistema"
                booleano = False
            elif verificador.args[0] == 1406:
                if "nome" in verificador.args[1]:
                    self.erroNome.grid()
                    self.erroNome["text"] = "*Nome: máximo de 100 caracteres"
                    booleano = False
                if "matricula" in verificador.args[1]:
                    self.erroMatricula.grid()
                    self.erroMatricula["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
                    booleano = False
        return booleano

    #Método de inserção do empregado no banco de dados
    def inserirEmpregado(self):
        if self.validarCampos():
            verificador = empragadoServices.inserirEmpregado(Empregado(self.matricula.get().strip(), self.nome.get().strip()))
            if self.validarCadastro(verificador):
                self.texto.grid()
                self.texto["text"] = "Empregado cadastrado com sucesso"
                self.limparEntry()
                self.listarEmpregados()

    #Método que remove empregado do banco de dados
    def removerEmpregado(self):
        self.limparLabels()
        empregado = self.selecionarItem()
        if empregado != None:
            verificador = empragadoServices.deletarEmpregado(empregado)
            if verificador == None:
                self.texto["text"] = "Empregado excluído com sucesso"
                self.listarEmpregados()
            else:
                self.texto["text"] = verificador

    #Método que atualiza empregado
    def atualizarEmpregado(self):
        self.limparLabels()
        empragadoAntigo = self.selecionarItem()
        if empragadoAntigo != None:
            if self.validarAtualizacao():
                verificador = empragadoServices.atualizarEmpregado(empragadoAntigo.getMatricula(), Empregado(self.matricula.get().strip(), self.nome.get().strip()))
                if self.validarCadastro(verificador):
                    self.texto.grid()
                    self.texto["text"] = "*Empregado atualizado com sucesso"
                    self.limparEntry()
                    self.listarEmpregados()

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
        self.tree = ttk.Treeview(self.master,height=10, columns=2, selectmode='browse')
        self.tree.grid(row=4, column=0, columnspan=2, pady=20, padx=20)
        self.tree["columns"] = ("matricula", "codigo")
        self.tree.bind('<Double-1>', self.preencheCampoClick)
        self.tree.heading("#0", text="first", anchor="w")
        self.tree.column("#0", stretch=NO, width=0, anchor="w")
        self.tree.heading("matricula", text="Matrícula")
        self.tree.column("matricula", anchor="center", width=120)
        self.tree.heading("codigo", text="Nome")
        self.tree.column("codigo", anchor="center", width=190)
        self.listarEmpregados()

    #Preenchendo campos para atualização
    def preencheCampoClick(self, event):
        if self.tree.focus() != "":
            self.limparEntry()
            self.limparLabels()
            self.texto["text"] = "*Só é permitido atualizar o campo nome"
            empregado = self.selecionarItem()
            self.matricula.insert(0, empregado.getMatricula())
            self.nome.insert(0, empregado.getNome())

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
            matricula, nome = str(self.tree.item(itemSelecionado)['values'][0]), self.tree.item(itemSelecionado)['values'][1]
            return Empregado(matricula, nome)

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

    #Limapando Entrys após modificações no banco
    def limparEntry(self):
        self.matricula.delete(0, 'end')
        self.nome.delete(0, 'end')

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == '__main__':
    root = Tk()
    root.title("Empregados")
    application = Application(root)
    root.mainloop()