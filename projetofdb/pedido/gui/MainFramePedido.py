from tkinter import*
from tkinter import ttk
from pedido.negocio.PedidoServices import PedidoServices
from pedido.dominio.Pedido import Pedido

pedidoServices = PedidoServices()

class MainFramePedido:
    def __init__(self):
        self.root = Toplevel()
        self.root.grab_set()
        self.root.title("Pedidos")
        self.master = self.root
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys presentes no frame
        self.frame = LabelFrame(self.master, bd=10, padx=10)
        self.frame.grid(row=0, column=0)

        Label(self.frame, text = 'Número:').grid(row=3, column=0)
        self.numero = Entry(self.frame, width=32, bd=2)
        self.numero.grid(row=3, column=2)

        #Label de exibição das mensagens de erros referentes ao campo número
        self.erroNumero = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroNumero.grid(row=4, column=2)

        Label(self.frame, text='Código do cliente:').grid(row=5, column=0)
        self.codigoCliente = Entry(self.frame, width=32, bd=2)
        self.codigoCliente.grid(row=5, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Código do cliente"
        self.erroCodigoCliente = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroCodigoCliente.grid(row=6, column=2)

        Label(self.frame, text='Data de abertura:').grid(row=7, column=0)
        self.dataAbertura = Entry(self.frame, width=32, bd=2)
        self.dataAbertura.grid(row=7, column=2)

        # Label de exibição das mensagens de erros referentes ao campo "Data de abertura"
        self.erroDataAbertura = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroDataAbertura.grid(row=8, column=2)

        Label(self.frame, text='Local:').grid(row=9, column=0)
        self.local = Entry(self.frame, width=32, bd=2)
        self.local.grid(row=9, column=2)

        # Label de exibição das mensagens de erros referentes ao campo "Local"
        self.erroLocal = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroLocal.grid(row=10, column=2)

        Label(self.frame, text='Data de realização:').grid(row=11, column=0)
        self.dataRealizacao = Entry(self.frame, width=32, bd=2)
        self.dataRealizacao.grid(row=11, column=2)

        #Label de exibição das mensagens de erros referentes ao campo "Data de realização"
        self.erroDataRealizacao = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.erroDataRealizacao.grid(row=12, column=2)

        self.btnAdd = ttk.Button(self.frame, text='CADASTRAR', command=self.inserirPedido).grid(row=13, column=2)

        #Label de exibição das mensagens de erros relacionadas as regras de negócio
        self.texto = Label(self.frame, text='', font=self.fontErro, fg="red")
        self.texto.grid(row=15, column=2)

        #Populando árvore
        self.popular_arvore()

        #Cria scrollbar_vertical de rolagem
        self.scrollbar_vertical = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        #Adiciona scrollbar_vertical de rolagem
        self.scrollbar_vertical.place(x=620, y=315, height=218 + 10)

        self.tree.configure(yscroll=self.scrollbar_vertical.set)

        #Botões de interação
        self.btnApagar = ttk.Button(self.master,text='DELETAR', command=self.removerPedido)
        self.btnApagar.grid(row=4, column=5)
        self.btnAtualizar = ttk.Button(self.frame, text='ATUALIZAR', command=self.atualizarPedido)
        self.btnAtualizar.grid(row=14, column=2, padx=10, pady=5)

        self.root.mainloop()

    #Método que retorna os dados dos campos
    def criarPedido(self):
        numero, codigo_cliente, data_abertura, local, data_realizacao = self.numero.get().strip(), self.codigoCliente.get().strip(), self.dataAbertura.get().strip(), self.local.get().strip(),self.dataRealizacao.get().strip()
        pedido = Pedido(numero, codigo_cliente, data_abertura, local, data_realizacao)
        return pedido

    #Método para validação dos campos
    def validarCampos(self):
            self.limparLabels()
            pedido = self.criarPedido()
            verificador = True
            if pedido.getNumero() == "":
                self.erroNumero.grid()
                self.erroNumero["text"] = "*Campo número não pode ficar vazio"
                verificador = False
            elif not pedido.getNumero().isdigit():
                self.erroNumero.grid()
                self.erroNumero["text"] = "*Campo número só deve conter números"
                verificador = False
            if pedido.getCodigoCliente() == "":
                self.erroCodigoCliente.grid()
                self.erroCodigoCliente["text"] = "*Campo código do cliente não pode ficar vazio"
                verificador = False
            elif not pedido.getCodigoCliente().isdigit() and pedido.getCodigoCliente() != "None":
                self.erroCodigoCliente.grid()
                self.erroCodigoCliente["text"] = "*Campo código do cliente só deve conter números"
                verificador = False
            if pedido.getDataAbertura() == "":
                self.erroDataAbertura.grid()
                self.erroDataAbertura["text"] = "*Campo data de abertura não deve ficar vazio"
                verificador = False
            if pedido.getLocal() == "":
                self.erroLocal.grid()
                self.erroLocal["text"] = "*Campo local não deve ficar vazio"
                verificador = False
            if pedido.getDataRealizacao() == "":
                self.erroDataRealizacao.grid()
                self.erroDataRealizacao["text"] = "*Campo data realização não deve ficar vazio"
                verificador = False
            return verificador

    def inserirPedido(self):
        if self.validarCampos():
            verificador = pedidoServices.inserirPedido(Pedido(self.numero.get().strip(), self.codigoCliente.get().strip(), self.dataAbertura.get().strip(), self.local.get().strip(), self.dataRealizacao.get().strip()))
            if self.validarCadastro(verificador):
                self.texto.grid()
                self.texto["text"] = "Pedido cadastrado com sucesso"
                self.limparEntry()
                self.listarPedidos()

    #Método que remove cliente do banco de dados
    def removerPedido(self):
        self.limparLabels()
        pedido = self.selecionarItem()
        if pedido != None:
            verificador = pedidoServices.removerPedido(pedido)
            if verificador == None:
                self.texto["text"] = "Pedido excluído com sucesso"
                self.listarPedidos()
            else:
                self.texto["text"] = verificador

    #Método que atualiza o cliente cadastrado no banco de dados
    def atualizarPedido(self):
        self.limparLabels()
        pedidoAntigo = self.selecionarItem()
        if pedidoAntigo != None:
            if self.validarCampos():
                pedidoAtual = self.criarPedido()
                verificador = pedidoServices.atualizarPedido(pedidoAntigo.getNumero(), pedidoAtual)
                if self.validarCadastro(verificador):
                    self.texto.grid()
                    self.texto["text"] = "Pedido atualizado com sucesso"
                    self.limparEntry()
                    self.listarPedidos()

    #Preenchendo campos para atualização
    def preencheCampoClick(self, event):
        if self.tree.focus() != "":
            self.limparEntry()
            self.limparLabels()
            self.texto["text"] = "*Atualize todos os campos exceto o número"
            pedido = self.selecionarItem()
            self.numero.insert(0, pedido.getNumero())
            self.codigoCliente.insert(0, pedido.getCodigoCliente())
            self.dataAbertura.insert(0, pedido.getDataAbertura())
            self.local.insert(0, pedido.getLocal())
            self.dataRealizacao.insert(0, pedido.getDataRealizacao())

    #Recuperando elemento selecionado na árvore
    def selecionarItem(self):
        itemSelecionado = self.tree.focus()
        if itemSelecionado != "":
            numero, codigo_cliente, data_abertura, local, data_realizacao = (
                                            str(self.tree.item(itemSelecionado)['values'][0]),
                                            self.tree.item(itemSelecionado)['values'][1],
                                            self.tree.item(itemSelecionado)['values'][2],
                                            self.tree.item(itemSelecionado)['values'][3],
                                            self.tree.item(itemSelecionado)['values'][4])
            return Pedido(numero, codigo_cliente, data_abertura, local, data_realizacao)

    #Validação dos cadastros
    def validarCadastro(self, verificador):
        booleano = True
        self.limparLabels()
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "*Pedido já cadastrado no sistema"
                booleano = False
            elif verificador.args[0] == 1406:
                if "numero" in verificador.args[1]:
                    self.erroNumero.grid()
                    self.erroNumero["text"] = "*Valor máximo excedido do número do pedido (máximo: 11 caracteres)"
                    booleano = False
                if "local" in verificador.args[1]:
                    self.erroLocal.grid()
                    self.erroLocal["text"] = "*Local: máximo de 45 caracteres"
                    booleano = False
            elif verificador.args[0] == 1264:
                self.erroCodigoCliente.grid()
                self.erroCodigoCliente["text"] = "*Valor máximo excedido do código do servico (máximo: 11 caracteres)"
                booleano = False
            elif verificador.args[0] == 1292:
                if "data_abertura" in verificador.args[1]:
                    self.erroDataAbertura.grid()
                    self.erroDataAbertura["text"] = "*Digite a data no seguinte formato: AAAA-MM-DD"
                    booleano = False
                else:
                    self.erroDataRealizacao.grid()
                    self.erroDataRealizacao["text"] = "*Digite a data no seguinte formato: AAAA-MM-DD"
                    booleano = False
            elif verificador.args[0] == 1452:
                self.texto.grid()
                self.texto["text"] = "*Cliente não cadastrado no banco"
                booleano = False
        return booleano

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
            self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
            self.tree.grid(row=4, column=0, columnspan=5, pady=10, padx=10)
            self.tree["columns"] = ("numero", "codigo_cliente", "data_abertura", "local", "data_realizacao")
            self.tree.bind('<Double-1>', self.preencheCampoClick)
            self.tree.heading("#0", text="first", anchor="w")
            self.tree.column("#0", stretch=NO, width=0, anchor="w")
            self.tree.heading("numero", text="Número")
            self.tree.column("numero", anchor="center", width=100)
            self.tree.heading("codigo_cliente", text="Código cliente")
            self.tree.column("codigo_cliente", anchor="center", width=100)
            self.tree.heading("data_abertura", text="Data abertura")
            self.tree.column("data_abertura", anchor="center", width=100)
            self.tree.heading("local", text="Local")
            self.tree.column("local", anchor="center", width=200)
            self.tree.heading("data_realizacao", text="Data realização")
            self.tree.column("data_realizacao", anchor="center", width=120)
            self.listarPedidos()

    #Selecionando todos os dados da tabela pedido e inserindo no TreeView
    def listarPedidos(self):
        self.tree.delete(*self.tree.get_children())  # Removendo todos os nodos da árvore
        self.pedidos = pedidoServices.listarPedidos("SELECT * FROM pedido")
        if self.pedidos != None:
            for i in self.pedidos:
                self.tree.insert("", "end", text="Person", values=i)
        else:
            self.texto["text"] = self.pedidos

    #Limpando labels com os erros/sucesso
    def limparLabels(self):
        self.erroNumero["text"] = ""
        self.erroCodigoCliente["text"] = ""
        self.erroDataAbertura["text"] = ""
        self.erroLocal["text"] = ""
        self.erroDataRealizacao["text"] = ""

    #Limapando Entrys após modificações no banco
    def limparEntry(self):
        self.numero.delete(0, 'end')
        self.codigoCliente.delete(0, 'end')
        self.dataAbertura.delete(0, 'end')
        self.local.delete(0, 'end')
        self.dataRealizacao.delete(0, 'end')

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__=="__main__":
    MainFramePedido()