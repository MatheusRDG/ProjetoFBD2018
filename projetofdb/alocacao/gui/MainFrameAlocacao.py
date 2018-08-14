from tkinter import*
from tkinter import ttk
from alocacao.negocio.AlocacaoServices import AlocacaoServices
from alocacao.dominio.Alocacao import Alocacao

alocacaoServices = AlocacaoServices()

class MainFrameAlocacao:
    def __init__(self):
        self.root = Toplevel()
        self.root.grab_set()
        self.root.title("Alocação")
        self.master = self.root
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys presentes no frame
        self.frame = LabelFrame(self.master, bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text='Matrícula do empregado:').grid(row=3, column=0)
        self.matriculaEmpregado = Entry(self.frame, width=22, bd=2)
        self.matriculaEmpregado.grid(row=3, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Matrícula do empregado"
        self.erroMatriculaEmpregado = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroMatriculaEmpregado.grid(row=4, column=2)

        Label(self.frame, text='Código do serviço:').grid(row=5, column=0)
        self.codigoServico = Entry(self.frame, width=22, bd=2)
        self.codigoServico.grid(row=5, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Código do serviço"
        self.erroCodigoServico = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCodigoServico.grid(row=6, column=2)

        Label(self.frame, text='Número do pedido:').grid(row=7, column=0)
        self.numeroPedido = Entry(self.frame, width=22, bd=2)
        self.numeroPedido.grid(row=7, column=2)

        # Label de exibição das mensagens de erros referentes ao campo "Número pedido"
        self.erroNumeroPedido = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroNumeroPedido.grid(row=8, column=2)

        self.btnCadastrar = ttk.Button(self.frame, text='CADASTRAR', command=self.inserirAlocacao).grid(row=9, column=2)

        # Botões de interação
        self.btnApagar = ttk.Button(self.master,text='DELETAR', command=self.removerAlocacao)
        self.btnApagar.grid(row=4, column=3, padx=10)
        self.btnAtualizar = ttk.Button(self.frame, text='ATUALIZAR')
        self.btnAtualizar.grid(row=10, column=2, pady=10)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=11, column=2)

        #Populando árvore
        self.popular_arvore()

        # Cria scrollbar_vertical de rolagem
        self.scrollbar_vertical = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        # Adiciona scrollbar_vertical de rolagem
        self.scrollbar_vertical.place(x=450, y=243, height=217 + 10)

        self.tree.configure(yscroll=self.scrollbar_vertical.set)

        self.root.mainloop()

    def retornarDadosEntry(self):
        return self.matriculaEmpregado.get().strip(), self.codigoServico.get().strip(), self.numeroPedido.get().strip()

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        dados = self.retornarDadosEntry()
        matricula_empregado, codigo_servico,numero_pedido = dados[0], dados[1], dados[2]
        verificador = True
        if matricula_empregado == "":
            self.erroMatriculaEmpregado.grid()
            self.erroMatriculaEmpregado["text"] = "*Campo matrícula empregado não pode ficar vazio"
            verificador = False
        elif not matricula_empregado.isdigit():
            self.erroMatriculaEmpregado.grid()
            self.erroMatriculaEmpregado["text"] = "*Campo matrícula empregado só deve conter números"
            verificador = False
        if codigo_servico == "":
            self.erroCodigoServico.grid()
            self.erroCodigoServico["text"] = "*Campo código serviço não pode ficar vazio"
            verificador = False
        elif not numero_pedido.isdigit():
            self.erroCodigoServico.grid()
            self.erroCodigoServico["text"] = "*Campo código serviço só deve conter números"
            verificador = False
        if numero_pedido == "":
            self.erroNumeroPedido.grid()
            self.erroNumeroPedido["text"] = "*Campo número pedido não pode ficar vazio"
            verificador = False
        elif not numero_pedido.isdigit():
            self.erroNumeroPedido.grid()
            self.erroNumeroPedido["text"] = "*Campo número pedido só deve conter números"
            verificador = False
        return verificador

    #Método de validação do cadastro (regras de negócio)
    def validarCadastroAlocacao(self, verificador):
        self.limparLabels()
        booleano = True
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "*Alocação já cadastrada no sistema"
                booleano = False
            elif verificador.args[0] == 1264:
                if "matricula_empregado" in verificador.args[1]:
                    self.erroMatriculaEmpregado.grid()
                    self.erroMatriculaEmpregado["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
                    booleano = False
                if "codigo_servico" in verificador.args[1]:
                    self.erroCodigoServico.grid()
                    self.erroCodigoServico["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
                    booleano = False
                if "numero_pedido" in verificador.args[1]:
                    self.erroNumeroPedido.grid()
                    self.erroNumeroPedido["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
            elif verificador.args[0] == 1452:
                print("codigo_servico" in verificador.args[1])
                if "matricula_empregado" in verificador.args[1]:
                    self.erroMatriculaEmpregado.grid()
                    self.erroMatriculaEmpregado["text"] = "*Matrícula de empregado não cadastrado no sistema"
                    booleano = False
                elif "codigo_servico" in verificador.args[1]:
                    self.erroCodigoServico.grid()
                    self.erroCodigoServico["text"] = "*Código de serviço não cadastrado no sistema"
                    booleano = False
                elif "numero_pedido" in verificador.args[1]:
                    self.erroNumeroPedido.grid()
                    self.erroNumeroPedido["text"] = "*Número de pedido não cadastrado no sistema"
                    booleano = False
        return booleano

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
            self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
            self.tree.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
            self.tree["columns"] = ("matricula_empregado", "codigo_servico", "numero_pedido")
            self.tree.heading("#0", text="first", anchor="w")
            self.tree.column("#0", stretch=NO, width=0, anchor="w")
            self.tree.heading("matricula_empregado", text="Matrícula empregado")
            self.tree.column("matricula_empregado", anchor="center", width=150)
            self.tree.heading("codigo_servico", text="Código serviço")
            self.tree.column("codigo_servico", anchor="center", width=150)
            self.tree.heading("numero_pedido", text="Número pedido")
            self.tree.column("numero_pedido", anchor="center", width=150)
            self.listarAlocacoes()

    #Método de inserção do alocação no banco de dados
    def inserirAlocacao(self):
        if self.validarCampos():
            dados = self.retornarDadosEntry()
            verificador = alocacaoServices.inserirAlocacao(Alocacao(dados[0], dados[1], dados[2]))
            if self.validarCadastroAlocacao(verificador):
                self.texto.grid()
                self.texto["text"] = "Alocação cadastrada com sucesso"
                self.limparEntry()
                self.listarAlocacoes()

    #Método que remove alocação do banco de dados
    def removerAlocacao(self):
        self.limparLabels()
        alocacao = self.selecionarAlocacao()
        if alocacao != None:
            verificador = alocacaoServices.removerAlocacao(alocacao)
            if verificador == None:
                self.texto["text"] = "Alocação excluída com sucesso"
                self.listarAlocacoes()
            else:
                self.texto["text"] = verificador

    #Recuperando elemento selecionado na árvore
    def selecionarAlocacao(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
            matricula_empregado, codigo_servico, numero_pedido = str(self.tree.item(itemSelecionado)['values'][0]), \
                                                      self.tree.item(itemSelecionado)['values'][1], \
                                                      self.tree.item(itemSelecionado)['values'][2]

            return Alocacao(matricula_empregado, codigo_servico, numero_pedido)

    #Selecionando todos os dados da tabela pessoa_fisica e inserindo no TreeView
    def listarAlocacoes(self):
        self.tree.delete(*self.tree.get_children())#Removendo todos os nodos da árvore
        self.alocacoes = alocacaoServices.listarAlocacao("SELECT * FROM alocacao")
        if self.alocacoes != None:
            for i in self.alocacoes:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto["text"] = self.alocacoes

    #Limpando as labels para evitar mensagens de erros inconsistentes
    def limparLabels(self):
        self.erroMatriculaEmpregado["text"] = ""
        self.erroMatriculaEmpregado["text"] = ""
        self.erroNumeroPedido["text"] = ""
        self.texto["text"] = ""

    #Limapando Entrys após modificações no banco
    def limparEntry(self):
        self.codigoServico.delete(0, 'end')
        self.matriculaEmpregado.delete(0, 'end')
        self.numeroPedido.delete(0, 'end')

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == "__main__":
    MainFrameAlocacao()