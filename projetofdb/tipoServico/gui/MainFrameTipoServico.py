from tkinter import*
from tkinter import ttk
from tipoServico.negocio.TipoServicoServices import TipoServicoServices
from tipoServico.dominio.TipoServico import TipoServico

tipoServicoServices = TipoServicoServices()

class Application:
    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys presentes no frame
        self.frame = LabelFrame(self.master, bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text='Código:').grid(row=3, column=0)
        self.codigo = Entry(self.frame, width=32, bd=2)
        self.codigo.grid(row=3, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Código"
        self.erroCodigo = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCodigo.grid(row=4, column=2)

        Label(self.frame, text='Descrição:').grid(row=5, column=0)
        self.descricao = Entry(self.frame, width=32, bd=2)
        self.descricao.grid(row=5, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Descrição"
        self.erroDescricao = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroDescricao.grid(row=6, column=2)

        Label(self.frame, text='Duração (m2):').grid(row=7, column=0)
        self.duracao_m2 = Entry(self.frame, width=32, bd=2)
        self.duracao_m2.grid(row=7, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Descrição(m2)"
        self.erroDuracaoM2 = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroDuracaoM2.grid(row=8, column=2)

        Label(self.frame, text='Valor por m2:').grid(row=9, column=0)
        self.valor_m2 = Entry(self.frame, width=32, bd=2)
        self.valor_m2.grid(row=9, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Valor por m2"
        self.erroValorM2 = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroValorM2.grid(row=10, column=2)

        self.btnAdd = ttk.Button(self.frame, text='CADASTRAR', command=self.inserirTipoServico).grid(row=11, column=2)

        self.texto = Label(self.frame, text='asd', font=self.fontErro, fg="red")
        self.texto.grid(row=13, column=2)

        #Populando árvore
        self.popular_arvore()

        # Cria scrollbar_vertical de rolagem
        self.scrollbar_vertical = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        # Adiciona scrollbar_vertical de rolagem
        self.scrollbar_vertical.place(x=430, y=283, height=218 + 10)

        self.tree.configure(yscroll=self.scrollbar_vertical.set)

        # Botões de interação
        self.btnApagar = ttk.Button(text='DELETAR', command=self.removerTipoServico)
        self.btnApagar.grid(row=4, column=3)
        self.btnAtualizar = ttk.Button(self.frame, text='ATUALIZAR')
        self.btnAtualizar.grid(row=12, column=2, sticky=S, padx=10, pady=10)

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
        self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
        self.tree.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
        self.tree["columns"] = ("codigo", "descricao", "duracao_m2", "valor_m2")
        self.tree.heading("#0", text="first", anchor="w")
        self.tree.column("#0", stretch=NO, width=0, anchor="w")
        self.tree.heading("codigo", text="Código")
        self.tree.column("codigo", anchor="center", width=100)
        self.tree.heading("descricao", text="Descrição")
        self.tree.column("descricao", anchor="center", width=150)
        self.tree.heading("duracao_m2", text="Duração(m2)")
        self.tree.column("duracao_m2", anchor="center", width=100)
        self.tree.heading("valor_m2", text="Valor(m2)")
        self.tree.column("valor_m2", anchor="center", width=80)
        self.listarTiposServicos()

    def retonarDadosCampo(self):
        return (self.codigo.get().strip(), self.descricao.get().strip(), self.duracao_m2.get().strip().replace(",", "."), self.valor_m2.get().strip().replace(",", "."))

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        verificador = True
        try:
            dados = self.retonarDadosCampo()
            codigo, descricao, duracao_m2, valor_m2 = dados[0], dados[1], dados[2], dados[3]
            if codigo == "":
                self.erroCodigo.grid()
                self.erroCodigo["text"] = "*Campo código não pode ficar vazio"
                verificador = False
            elif not codigo.isdigit():
                self.erroCodigo.grid()
                self.erroCodigo["text"] = "*Campo código só deve conter números"
                verificador = False
            if descricao == "":
                self.erroDescricao.grid()
                self.erroDescricao["text"] = "*Campo descrição não pode ficar vazio"
                verificador = False
            if duracao_m2 == "":
                self.erroDuracaoM2.grid()
                self.erroDuracaoM2["text"] = "*Campo duração(m2) não deve ficar vazio"
                verificador = False
            elif float(duracao_m2):
                pass
            if valor_m2 == "":
                self.erroValorM2.grid()
                self.erroValorM2["text"] = "*Campo valor por m2 não deve ficar vazio"
                verificador = False
            elif float(valor_m2):
                pass
        except ValueError:
            self.texto.grid()
            self.texto["text"] = "*Campo duração e valor só devem números"
            verificador = False
        return verificador

    #Método de inserção do tipo de serviço no banco de dados
    def inserirTipoServico(self):
        if self.validarCampos():
            dados = self.retonarDadosCampo()
            codigo, descricao, duracao_m2, valor_m2 = dados[0], dados[1], dados[2], dados[3]
            verificador = tipoServicoServices.inserirTipoServico(TipoServico(codigo, descricao, duracao_m2, valor_m2))
            if self.validarCadastroTipoServico(verificador):
                self.texto.grid()
                self.texto["text"] = "Tipo de serviço cadastrado com sucesso"
                self.listarTiposServicos()

    def removerTipoServico(self):
        self.limparLabels()
        tipoServico = self.selecionarItem()
        if tipoServico != None:
            verificador = tipoServicoServices.removerTipoServico(tipoServico)
            if verificador == None:
                self.texto["text"] = "Tipo serviço excluído com sucesso"
                self.listarTiposServicos()
            else:
                self.texto["text"] = verificador

    #Método de validação do cadastro (regras de negócio)
    def validarCadastroTipoServico(self, verificador):
        booleano = True
        self.limparLabels()
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "Tipo serviço já cadastrado no sistema"
                booleano = False
            elif verificador.args[0] == 1264:
                if "codigo" in verificador.args[1]:
                    self.erroCodigo.grid()
                    self.erroCodigo["text"] = "Código: máximo de 11 caracteres"
                    booleano = False
                elif "duracao_m2" in verificador.args[1]:
                    self.erroDuracaoM2.grid()
                    self.erroDuracaoM2["text"] = "*Duração máxima excedida"
                    booleano = False
                elif "valor_m2" in verificador.args[1]:
                    self.erroValorM2.grid()
                    self.erroValorM2["text"] = "*Valor máximo excedido"
            elif verificador.args[0] == 1406:
                self.erroDescricao.grid()
                self.erroDescricao["text"] = "Descrição: máximo de 100 caracteres"
                booleano = False
        return booleano

    #Limpando as labels para evitar mensagens de erros inconsistentes
    def limparLabels(self):
        self.erroCodigo["text"] = ""
        self.erroDescricao["text"] = ""
        self.erroDuracaoM2["text"] = ""
        self.erroValorM2["text"] = ""

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
            codigo, descricao, duracao_m2, valor_m2 = str(self.tree.item(itemSelecionado)['values'][0]), \
                                         self.tree.item(itemSelecionado)['values'][1], \
                                         self.tree.item(itemSelecionado)['values'][2], \
                                         self.tree.item(itemSelecionado)['values'][3]
            return TipoServico(codigo, descricao, duracao_m2, valor_m2)

    #Selecionando todos os dados da tabela pessoa_fisica e inserindo no TreeView
    def listarTiposServicos(self):
        self.tree.delete(*self.tree.get_children())  # Removendo todos os nodos da árvore
        self.tipos = tipoServicoServices.listarTipos("SELECT * FROM tipo_servico")
        if self.tipos != None:
            for i in self.tipos:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto["text"] = self.tipos

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == '__main__':
    root = Tk()
    root.title("Tipo serviço")
    application = Application(root)
    root.mainloop()