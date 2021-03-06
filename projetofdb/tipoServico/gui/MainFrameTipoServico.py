from tkinter import*
from tkinter import ttk
from tipoServico.negocio.TipoServicoServices import TipoServicoServices
from tipoServico.dominio.TipoServico import TipoServico

tipoServicoServices = TipoServicoServices()

class MainFrameTipoServico:
    def __init__(self):
        self.root = Toplevel()
        self.root.grab_set()
        self.root.title("Tipo serviço")
        self.master = self.root
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

        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=13, column=2)

        #Populando árvore
        self.popular_arvore()

        #Cria scrollbar_vertical de rolagem
        self.scrollbar_vertical = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        #Adiciona scrollbar_vertical de rolagem
        self.scrollbar_vertical.place(x=430, y=283, height=218 + 10)

        self.tree.configure(yscroll=self.scrollbar_vertical.set)

        #Botões de interação
        self.btnApagar = ttk.Button(self.master, text='DELETAR', command=self.removerTipoServico)
        self.btnApagar.grid(row=4, column=3)
        self.btnAtualizar = ttk.Button(self.frame, text='ATUALIZAR', command=self.atualizarTipoServico)
        self.btnAtualizar.grid(row=12, column=2, sticky=S, padx=10, pady=10)

        self.root.mainloop()

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
        self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
        self.tree.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
        self.tree["columns"] = ("codigo", "descricao", "duracao_m2", "valor_m2")
        self.tree.bind('<Double-1>', self.preencheCampoClick)
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

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        verificador = True
        try:
            tipoServico = self.criarTipoServico()
            if tipoServico.getCodigo() == "":
                self.erroCodigo.grid()
                self.erroCodigo["text"] = "*Campo código não pode ficar vazio"
                verificador = False
            elif not tipoServico.getCodigo().isdigit():
                self.erroCodigo.grid()
                self.erroCodigo["text"] = "*Campo código só deve conter números"
                verificador = False
            if tipoServico.getDescricao() == "":
                self.erroDescricao.grid()
                self.erroDescricao["text"] = "*Campo descrição não pode ficar vazio"
                verificador = False
            if tipoServico.getDuracaoM2() == "":
                self.erroDuracaoM2.grid()
                self.erroDuracaoM2["text"] = "*Campo duração(m2) não deve ficar vazio"
                verificador = False
            elif float(tipoServico.getDuracaoM2()):
                pass
            if tipoServico.getValorM2() == "":
                self.erroValorM2.grid()
                self.erroValorM2["text"] = "*Campo valor por m2 não deve ficar vazio"
                verificador = False
            elif float(tipoServico.getValorM2()):
                pass
        except ValueError:
            self.texto.grid()
            self.texto["text"] = "*Campo duração e valor só devem números"
            verificador = False
        return verificador

    #Método de inserção do tipo de serviço no banco de dados
    def inserirTipoServico(self):
        if self.validarCampos():
            tipoServico = self.criarTipoServico()
            verificador = tipoServicoServices.inserirTipoServico(tipoServico)
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

    #Método que atualiza tipo de serviço
    def atualizarTipoServico(self):
        self.limparLabels()
        tipoServicoAntigo = self.selecionarItem()
        if tipoServicoAntigo != None:
            if self.validarCampos():
                tipoServicoAtual = self.criarTipoServico()
                verificador = tipoServicoServices.atualizarTipoServico(tipoServicoAntigo.getCodigo(), tipoServicoAtual)
                if self.validarCadastroTipoServico(verificador):
                    self.texto.grid()
                    self.texto["text"] = "Tipo de serviço atualizado com sucesso"
                    self.limparEntry()
                    self.listarTiposServicos()

    #Preenchendo campos para atualização
    def preencheCampoClick(self, event):
        if self.tree.focus() != "":
            self.limparEntry()
            self.limparLabels()
            self.texto["text"] = "*Atualize apenas os campos nome, descrição, duração e valor"
            tipoServico = self.selecionarItem()
            self.codigo.insert(0,tipoServico.getCodigo())
            self.descricao.insert(0,tipoServico.getDescricao())
            self.duracao_m2.insert(0, tipoServico.getDuracaoM2())
            self.valor_m2.insert(0, tipoServico.getValorM2())

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
                    booleano = False
            elif verificador.args[0] == 1406:
                self.erroDescricao.grid()
                self.erroDescricao["text"] = "Descrição: máximo de 100 caracteres"
                booleano = False
        return booleano

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
            codigo, descricao, duracao_m2, valor_m2 = str(self.tree.item(itemSelecionado)['values'][0]), \
                                         self.tree.item(itemSelecionado)['values'][1], \
                                         self.tree.item(itemSelecionado)['values'][2], \
                                         self.tree.item(itemSelecionado)['values'][3]
            return TipoServico(codigo, descricao, duracao_m2, valor_m2)

    #Retornando valores digitados nos campos
    def criarTipoServico(self):
        codigo, descricao, duracao_m2, valor_m2 = self.codigo.get().strip(), self.descricao.get().strip(), \
                                                  self.duracao_m2.get().strip().replace(",", "."), self.valor_m2.get().strip().replace(",", ".")
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

    #Limpando as labels para evitar mensagens de erros inconsistentes
    def limparLabels(self):
        self.erroCodigo["text"] = ""
        self.erroDescricao["text"] = ""
        self.erroDuracaoM2["text"] = ""
        self.erroValorM2["text"] = ""

    #Limapando Entrys após modificações no banco
    def limparEntry(self):
        self.codigo.delete(0, 'end')
        self.descricao.delete(0, 'end')
        self.duracao_m2.delete(0, 'end')
        self.valor_m2.delete(0, 'end')

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__=='__main__':
    MainFrameTipoServico()