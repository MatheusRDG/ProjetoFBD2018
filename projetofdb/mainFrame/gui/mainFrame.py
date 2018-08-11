from alocacao.gui.MainFrameAlocacao import *
from cliente.gui.MainFrameCliente import *
from empregado.gui.MainFrameEmpregado import *
from habilitacao.gui.MainFrameHabilitacao import *
from itemPedido.gui.MainFrameItemPedido import *
from pedido.gui.MainFramePedido import *
from pessoaFisica.gui.MainFramePessoaFisica import *
from pessoaJuridica.gui.MainFramePessoaJuridica import *
from tipoServico.gui.MainFrameTipoServico import *

class TelaMain:
    def __init__(self):
        self.root = Tk()
        self.master = self.root
        self.root.geometry('300x250+150+150')
        self.root.title("Serviços de limpeza")
        self.master.resizable(width=0, height=0)

        self.label = Label(self.master,text="Bem vindo ao gerenciador Serviço de Limpeza.\n Selecione uma entidade:")
        self.label.grid(row=0, column=1)

        self.bt1 = Button(self.master, width=20, text="Alocação", command=self.abreAlocacao)
        self.bt1.grid(row=2, column=1)

        self.bt2 = Button(self.master, width=20, text="Cliente", command=self.abreCliente)
        self.bt2.grid(row=3, column=1)

        self.bt3 = Button(self.master, width=20, text="Empregado", command=self.abreEmpregado)
        self.bt3.grid(row=4, column=1)

        self.bt4 = Button(self.master, width=20, text="Habilitação", command=self.abreHabilitacao)
        self.bt4.grid(row=5, column=1)

        self.bt9 = Button(self.master, width=20, text="Pedido", command=self.abreItemPedido)
        self.bt4.grid(row=6, column=1)

        self.bt5 = Button(self.master, width=20, text="Item Pedido", command=self.abreItemPedido)
        self.bt5.grid(row=7, column=1)

        self.bt6 = Button(self.master, width=20, text="Pessoa Física", command=self.abrePessoaFisica)
        self.bt6.grid(row=8, column=1)

        self.bt7 = Button(self.master, width=20, text="Pessoa Jurídica", command=self.abrePessoaJuridica)
        self.bt7.grid(row=9, column=1)

        self.bt8 = Button(self.master, width=20, text="Tipo Serviço", command=self.abreTipoServico)
        self.bt8.grid(row=10, column=1)

        self.root.mainloop()

    def abreAlocacao(self):
        MainFrameAlocacao()

    def abreHabilitacao(self):
        MainFrameHabilitacao()

    def abrePedido(self):
        MainFramePedido()

    def abreItemPedido(self):
        MainFrameItemPedido()

    def abrePessoaJuridica(self):
        MainFramePessoaJuridica()

    def abrePessoaFisica(self):
        MainFramePessoaFisica()

    def abreCliente(self):
        MainFrameCliente()

    def abreEmpregado(self):
        MainFrameEmpregado()

    def abreTipoServico(self):
        MainFrameTipoServico()

if __name__ == '__main__':
    TelaMain()