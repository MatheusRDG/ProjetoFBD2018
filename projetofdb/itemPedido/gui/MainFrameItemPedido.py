from tkinter import*
from tkinter import ttk
from itemPedido.negocio.ItemPedidoServices import ItemPedidoServices
from itemPedido.dominio.ItemPedido import ItemPedido

itemPedidoServices = ItemPedidoServices()

class Application:
    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys presentes no frame
        self.frame = LabelFrame(self.master, bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text='Código do serviço:').grid(row=3, column=0)
        self.codigoServico = Entry(self.frame, width=22, bd=2)
        self.codigoServico.grid(row=3, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Código do serviço"
        self.erroCodigoServico = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCodigoServico.grid(row=4, column=2)

        Label(self.frame, text='Número do pedido:').grid(row=5, column=0)
        self.numeroPedido = Entry(self.frame, width=22, bd=2)
        self.numeroPedido.grid(row=5, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Número do pedido"
        self.erroNumeroPedido = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroNumeroPedido.grid(row=6, column=2)

        Label(self.frame, text='Metragem:').grid(row=7, column=0)
        self.metragem = Entry(self.frame, width=22, bd=2)
        self.metragem.grid(row=7, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Número do pedido"
        self.erroMetragem = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroMetragem.grid(row=8, column=2)

        self.btnAdd = ttk.Button(self.frame, text='CADASTRAR', command=self.inserirItemPedido).grid(row=9, column=2)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=11, column=2)

        # Botões de interação
        self.btnApagar = ttk.Button(text='DELETAR', command=self.removerItemPedido)
        self.btnApagar.grid(row=4, column=3, padx=10)
        self.btnAtualizar = ttk.Button(self.frame, text='ATUALIZAR', command=self.atualizarItemPedido)
        self.btnAtualizar.grid(row=10, column=2, pady=10)

        #Populando árvore
        self.popular_arvore()

        # Cria scrollbar_vertical de rolagem
        self.scrollbar_vertical = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        # Adiciona scrollbar_vertical de rolagem
        self.scrollbar_vertical.place(x=398, y=243, height=217 + 10)

        self.tree.configure(yscroll=self.scrollbar_vertical.set)

    #Método para validação dos campos
    def validarCampos(self):
        self.limparLabels()
        itemPedido = self.criarItemPedido()
        verificador = True
        try:
            if itemPedido.getCodigoServico() == "":
                self.erroCodigoServico.grid()
                self.erroCodigoServico["text"] = "*Campo código do serviço não pode ficar vazio"
                verificador = False
            elif not itemPedido.getCodigoServico().isdigit():
                self.erroCodigoServico.grid()
                self.erroCodigoServico["text"] = "*Campo código só deve conter números"
                verificador = False
            if itemPedido.getNumeroPedido() == "":
                self.erroNumeroPedido.grid()
                self.erroNumeroPedido["text"] = "*Campo número do pedido não pode ficar vazio"
                verificador = False
            elif not itemPedido.getNumeroPedido().isdigit():
                self.erroNumeroPedido.grid()
                self.erroNumeroPedido["text"] = "*Campo número só deve conter números"
                verificador = False
            if itemPedido.getMetragem() == "":
                self.erroMetragem.grid()
                self.erroMetragem["text"] = "*Campo metragem não pode ficar vazio"
                verificador = False
            if float(itemPedido.getMetragem()):
                pass
            elif not itemPedido.getMetragem().isdigit():
                self.erroMetragem.grid()
                self.erroMetragem["text"] = "*Campo metragem só deve conter números"
                verificador = False
        except ValueError:
            self.texto.grid()
            self.texto["text"] = "*Todos os campos só devem conter números"
            verificador = False
        return verificador

    #Método de validação do cadastro (regras de negócio)
    def validarCadastroItemPedido(self, verificador):
        self.limparLabels()
        booleano = True
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "*Item de pedido já cadastrado no sistema"
                booleano = False
            elif verificador.args[0] == 1264:
                if "codigo_servico" in verificador.args[1]:
                    self.erroCodigoServico.grid()
                    self.erroCodigoServico["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
                    booleano = False
                if "metragem" in verificador.args[1]:
                    self.erroMetragem.grid()
                    self.erroMetragem["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
                    booleano = False
                if "numero_pedido" in verificador.args[1]:
                    self.erroNumeroPedido.grid()
                    self.erroNumeroPedido["text"] = "*Valor máximo excedido (máximo: 11 caracteres)"
                    booleano = False
            elif verificador.args[0] == 1452:
                if "codigo_servico" in verificador.args[1]:
                    self.erroCodigoServico.grid()
                    self.erroCodigoServico["text"] = "*Tipo de serviço não cadastrado no sistema"
                    booleano = False
                if "numero_pedido" in verificador.args[1]:
                    self.erroNumeroPedido.grid()
                    self.erroNumeroPedido["text"] = "*Número de pedido não cadastrado no sistema"
                    booleano = False
        return booleano

    #Método de inserção do cliente no banco de dados
    def inserirItemPedido(self):
        if self.validarCampos():
            dados = self.criarItemPedido()
            verificador = itemPedidoServices.inserirItemPedido(ItemPedido(dados[0], dados[1], dados[2]))
            if self.validarCadastroItemPedido(verificador):
                self.texto.grid()
                self.texto["text"] = "Item de pedido cadastrado com sucesso"
                self.limparEntry()
                self.listarItens()

    #Método que remove cliente do banco de dados
    def removerItemPedido(self):
        self.limparLabels()
        itemPedido = self.selecionarItem()
        if itemPedido != None:
            verificador = itemPedidoServices.removerItemPedido(itemPedido)
            if verificador == None:
                self.texto["text"] = "Item excluído com sucesso"
                self.listarItens()
            else:
                self.texto["text"] = verificador

    #Método que atualiza o cliente cadastrado no banco de dados
    def atualizarItemPedido(self):
        self.limparLabels()
        itemPedidoAntigo = self.selecionarItem()
        if itemPedidoAntigo != None:
            if self.validarCampos():
                verificador = itemPedidoServices.atualizarItemPedido(itemPedidoAntigo, self.criarItemPedido())
                if self.validarCadastroItemPedido(verificador):
                    self.texto.grid()
                    self.texto["text"] = "Item pedido atualizado com sucesso"
                    self.limparEntry()
                    self.listarItens()

    #Método que retorna um objeto item de pedido
    def criarItemPedido(self):
        codigo_servico, numero_pedido, metragem = self.codigoServico.get().strip(), self.numeroPedido.get().strip(), \
                                                  self.metragem.get().strip().replace(",", ".")
        return ItemPedido(codigo_servico, numero_pedido, metragem)

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
            self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
            self.tree.grid(row=4, column=0, columnspan=3, pady=10, padx=10)
            self.tree["columns"] = ("codigo_servico", "numero_pedido", "metragem")
            self.tree.bind("<Double-1>", self.preencheCampoClick)
            self.tree.heading("#0", text="first", anchor="w")
            self.tree.column("#0", stretch=NO, width=0, anchor="w")
            self.tree.heading("codigo_servico", text="Código serviço")
            self.tree.column("codigo_servico", anchor="center", width=120)
            self.tree.heading("numero_pedido", text="Número pedido")
            self.tree.column("numero_pedido", anchor="center", width=150)
            self.tree.heading("metragem", text="Metragem")
            self.tree.column("metragem", anchor="center", width=120)
            self.listarItens()

    #Preenchendo campos para atualização
    def preencheCampoClick(self, event):
        if self.tree.focus() != "":
            self.limparEntry()
            self.limparLabels()
            self.texto["text"] = "*Só é permitido atualizar o campo metragem"
            itemPedido = self.selecionarItem()
            self.codigoServico.insert(0, itemPedido.getCodigoServico())
            self.numeroPedido.insert(0, itemPedido.getNumeroPedido())
            self.metragem.insert(0, itemPedido.getMetragem())

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
            codigo_servico, numero_pedido, metragem = str(self.tree.item(itemSelecionado)['values'][0]), \
                                         self.tree.item(itemSelecionado)['values'][1], \
                                         self.tree.item(itemSelecionado)['values'][2]
            return ItemPedido(codigo_servico, numero_pedido, metragem)

    #Selecionando todos os dados da tabela item_pedido e inserindo no TreeView
    def listarItens(self):
        self.tree.delete(*self.tree.get_children())  # Removendo todos os nodos da árvore
        self.itensPedido = itemPedidoServices.listarItensPedido("SELECT * FROM item_pedido")
        if self.itensPedido != None:
            for i in self.itensPedido:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto["text"] = self.itensPedido

    #Limpando as labels para evitar mensagens de erros inconsistentes
    def limparLabels(self):
        self.erroCodigoServico["text"] = ""
        self.erroNumeroPedido["text"] = ""
        self.erroMetragem["text"] = ""
        self.texto["text"] = ""

    #Limapando Entrys após modificações no banco
    def limparEntry(self):
        self.codigoServico.delete(0, 'end')
        self.numeroPedido.delete(0, 'end')
        self.metragem.delete(0, 'end')

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == '__main__':
    root = Tk()
    root.title("Item pedido")
    application = Application(root)
    root.mainloop()