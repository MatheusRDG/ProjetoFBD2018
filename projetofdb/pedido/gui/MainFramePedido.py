from tkinter import*
from tkinter import ttk
from pedido.negocio.PedidoServices import PedidoServices
from pedido.dominio.Pedido import Pedido

pedidoServices = PedidoServices()

class Application:
    def __init__(self, master):
        self.master = master
        self.estilo_botao = ttk.Style().configure("TButton", relief="flat", background="#ccc")#Estilo para os botões
        self.master.resizable(width=0, height=0)#Retirando o opção de maximização do frame master
        self.fontErro = ("Arial", "8", "italic")#Estilo de fonte para as mensagens de erro

        #LabelFrame que comporta as Labels e Entrys presentes no frame
        self.frame = LabelFrame(self.master, text='Cadastrar novo pedido', bd=10, padx=10)
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
        self.texto.grid(row=14, column=2)

        #Populando árvore
        self.popular_arvore()

        #Cria barra de rolagem
        self.barra = Scrollbar(self.master, orient='vertical', command=self.tree.yview)

        #Adiciona barra de rolagem
        self.barra.place(x=620, y=286, height=218 + 10)

        self.tree.configure(yscroll=self.barra.set)

        #Botões de interação
        self.btnApagar = ttk.Button(text='Deletar cliente')
        self.btnApagar.grid(row=4, column=5, sticky=N)
        self.btnAtualizar = ttk.Button(text='Atualizar cliente')
        self.btnAtualizar.grid(row=4, column=5, sticky=S, padx=10, pady=10)

    # Método para validação dos campos
    def validarCampos(self):
            self.limparLabels()
            numero, codigo_cliente, data_abertura, local, dataRealizacao = self.numero.get().strip(), self.codigoCliente.get().strip(), self.dataAbertura.get().strip(), self.local.get().strip(),self.dataRealizacao.get().strip()
            verificador = True
            if numero == "":
                self.erroNumero.grid()
                self.erroNumero["text"] = "*Campo número não pode ficar vazio"
                verificador = False
            elif not str(numero).isdigit():
                self.erroNumero.grid()
                self.erroNumero["text"] = "*Campo número só deve conter números"
                verificador = False
            if codigo_cliente == "":
                self.erroCodigoCliente.grid()
                self.erroCodigoCliente["text"] = "*Campo código do cliente não pode ficar vazio"
                verificador = False
            elif not str(codigo_cliente).isdigit():
                self.erroCodigoCliente.grid()
                self.erroCodigoCliente["text"] = "*Campo código do cliente só deve conter números"
                verificador = False
            if data_abertura == "":
                self.erroDataAbertura.grid()
                self.erroDataAbertura["text"] = "*Campo data de abertura não deve ficar vazio"
                verificador = False
            if local == "":
                self.erroLocal.grid()
                self.erroLocal["text"] = "*Campo local não deve ficar vazio"
                verificador = False
            if dataRealizacao == "":
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
                #self.listarPedido()

    def validarCadastro(self, verificador):
        booleano = True
        print(verificador)
        self.limparLabels()
        if verificador != None:
            if verificador.args[0] == 1062:
                self.texto.grid()
                self.texto["text"] = "Pedido já cadastrado no sistema"
                booleano = False
            elif verificador.args[0] == 1406:
                if "numero" in verificador.args[1]:
                    self.erroNumero.grid()
                    self.erroNumero["text"] = "Número: máximo de 11 caracteres"
                    booleano = False
                elif "local" in verificador.args[1]:
                    self.erroLocal.grid()
                    self.erroLocal["text"] = "Local: máximo de 45 caracteres"
                    booleano = False
                else:
                    self.erroCodigoCliente.grid()
                    self.erroCodigoCliente["text"] = "Código do cliente: máximo de 11 caracteres"
                    booleano = False
        return booleano

    def limparLabels(self):
        self.erroNumero["text"] = ""
        self.erroCodigoCliente["text"] = ""
        self.erroDataAbertura["text"] = ""
        self.erroLocal["text"] = ""
        self.erroDataRealizacao["text"] = ""

    #Montando o tree view e preenchendo com os dados cadastrados no banco
    def popular_arvore(self):
            self.tree = ttk.Treeview(self.master, height=10, columns=2, selectmode='browse')
            self.tree.grid(row=4, column=0, columnspan=5, pady=10, padx=10)
            self.tree["columns"] = ("numero", "codigo_cliente", "data_abertura", "local", "data_realizacao")
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

#Executando a classe main, que nesse caso é o Application, mas caso ela seja importado como módulo em outro arquivo a sua execução será controlada
if __name__ == '__main__':
    root = Tk()
    root.title("Pedidos")
    application = Application(root)
    root.mainloop()