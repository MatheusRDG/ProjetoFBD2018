from tkinter import*
from tkinter import ttk
from habilitacao.negocio.HabilitacaoServices import HabilitacaoServices
from habilitacao.dominio.Habilitacao import Habilitacao

habilitacaoServices = HabilitacaoServices()

class Application:

    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.minsize(width=360, height=450)#Fixando as dimensões do frame master
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys
        self.frame = LabelFrame(self.master, bd=10, padx=10, width=100)
        self.frame.grid(row=0, column=0, padx=10)

        Label(self.frame, text = 'Código do serviço:').grid(row=3, column=0)
        self.codigoServico = Entry(self.frame, width=22, bd=2)
        self.codigoServico.grid(row=3, column=1, padx=40)

        #Label de exibição das mensagens de erros referentes ao campo "Código do serviço"
        self.erroCodigoServico = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCodigoServico.grid(row=4, column=1)

        Label(self.frame, text='Matrícula do empregado:').grid(row=5, column=0)
        self.matriculaEmpregado = Entry(self.frame, width=22, bd=2)
        self.matriculaEmpregado.grid(row=5, column=1)

        #Label de exibição das mensagens de erros referentes ao campo "Matrícula do empregado"
        self.erroMatriculaEmpregado = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroMatriculaEmpregado.grid(row=6, column=1)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=9, column=1)

        self.btnCadastrar = ttk.Button(self.frame, text='CADASTRAR', command=self.inserirHabilitacao).grid(row=7, column=1)

        #Populando árvore
        self.popular_arvore()

        #Cria scrollbar_vertical de rolagem
        self.scrollbar_vertical = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        #Adiciona scrollbar_vertical de rolagem
        self.scrollbar_vertical.place(x=355, y=202, height=217 + 10)

        self.tree.configure(yscroll=self.scrollbar_vertical.set)

        #Botões de interação
        self.btnApagar = ttk.Button(text='DELETAR', command=self.removerHabilitacao)
        self.btnApagar.grid(row=4, column=3, padx=10)
        self.btnAtualizar = ttk.Button(self.frame, text='ATUALIZAR')
        self.btnAtualizar.grid(row=8, column=1, pady=10)

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        codigo_servico, matricula_empregado = self.codigoServico.get().strip(), self.matriculaEmpregado.get().strip()
        verificador = True
        if codigo_servico == "":
            self.erroCodigoServico.grid()
            self.erroCodigoServico["text"] = "*Campo código não pode ficar vazio"
            verificador = False
        elif not codigo_servico.isdigit():
            self.erroCodigoServico.grid()
            self.erroCodigoServico["text"] = "*Campo código só deve conter números"
            verificador = False
        if matricula_empregado == "":
            self.erroMatriculaEmpregado.grid()
            self.erroMatriculaEmpregado["text"] = "*Campo matrícula não pode ficar vazio"
            verificador = False
        elif not matricula_empregado.isdigit():
            self.erroMatriculaEmpregado.grid()
            self.erroMatriculaEmpregado["text"] = "*Campo matrícula só deve conter números"
            verificador = False

        return verificador

    #Método de validação do cadastro (regras de negócio)
    def validarCadastro(self, verificador):
        self.limparLabels()
        booleano = True
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "*Habilitação já registrada no sistema"
                booleano = False
            elif verificador.args[0] == 1406:
                if "matricula_empregado" in verificador.args[1]:
                    self.erroMatriculaEmpregado.grid()
                    self.erroMatriculaEmpregado["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
                    booleano = False
                if "codigo_servico" in verificador.args[1]:
                    self.erroCodigoServico.grid()
                    self.erroCodigoServico["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
                    booleano = False
            elif verificador.args[0] == 1452:
                if "matricula_empregado" in verificador.args[1]:
                    self.erroMatriculaEmpregado.grid()
                    self.erroMatriculaEmpregado["text"] = "*Matrícula não cadastrada no sistema"
                    booleano = False
                if "codigo_servico" in verificador.args[1]:
                    self.erroCodigoServico.grid()
                    self.erroCodigoServico["text"] = "*Código não cadastrado no sistema"
                    booleano = False
        return booleano

    #Método de inserção do habilitação no banco de dados
    def inserirHabilitacao(self):
        if self.validarCampos():
            verificador = habilitacaoServices.inserirHabilitacao(Habilitacao(self.codigoServico.get().strip(), self.matriculaEmpregado.get().strip()))
            if self.validarCadastro(verificador):
                self.texto.grid()
                self.texto["text"] = "Habilitação cadastrada com sucesso"
                self.limparEntry()
                self.listarHabilitacacoes()

    #Método que remove habilitação do banco de dados
    def removerHabilitacao(self):
        self.limparLabels()
        habilitacao = self.selecionarHabilitacao()
        if habilitacao != None:
            verificador = habilitacaoServices.removerHabilitacao(habilitacao)
            if verificador == None:
                self.texto["text"] = "Habilitação excluído com sucesso"
                self.listarHabilitacacoes()
            else:
                self.texto["text"] = verificador

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
        self.tree = ttk.Treeview(self.master,height=10, columns=2, selectmode='browse')
        self.tree.grid(row=4, column=0, columnspan=2, pady=10)
        self.tree["columns"] = ("codigo_servico", "matricula_empregado")
        self.tree.heading("#0", text="first", anchor="w")
        self.tree.column("#0", stretch=NO, width=0, anchor="w")
        self.tree.heading("codigo_servico", text="Código serviço")
        self.tree.column("codigo_servico", anchor="center", width=120)
        self.tree.heading("matricula_empregado", text="Matrícula empregado")
        self.tree.column("matricula_empregado", anchor="center", width=200)
        self.listarHabilitacacoes()

    #Recuperando elemento selecionado na árvore
    def selecionarHabilitacao(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
            codigo_servico, matricula_empregado = str(self.tree.item(itemSelecionado)['values'][0]), self.tree.item(itemSelecionado)['values'][1]
            return Habilitacao(codigo_servico, matricula_empregado)

    #Selecionando todos os dados da tabela habilitação e inserindo no TreeView
    def listarHabilitacacoes(self):
        self.tree.delete(*self.tree.get_children())#Removendo todos os nodos da árvore
        self.habilitacoes = habilitacaoServices.listarHabilitacao("SELECT * FROM habilitacao")
        if self.habilitacoes != None:
            for i in self.habilitacoes:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto['text'] = self.habilitacoes

    #Limpando as labels para evitar mensagens de erros inconsistentes
    def limparLabels(self):
        self.erroCodigoServico["text"] = ""
        self.erroMatriculaEmpregado["text"] = ""
        self.texto["text"] = ""

    #Limapando Entrys após modificações no banco
    def limparEntry(self):
        self.codigoServico.delete(0, 'end')
        self.matriculaEmpregado.delete(0, 'end')

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
def intentHabilitacao():
    root = Tk()
    root.title("Habilitação")
    application = Application(root)
    root.mainloop()