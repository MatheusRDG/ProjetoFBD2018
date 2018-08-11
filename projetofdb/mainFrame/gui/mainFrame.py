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
        self.label.pack()

        self.bt1 = Button(self.master, width=20, text="Alocação", command=lambda:intentAlocacao(self.master))
        self.bt1.pack()

        self.bt2 = Button(self.master, width=20, text="Cliente", command=lambda:intentCliente(self.master))
        self.bt2.pack()

        self.bt3 = Button(self.master, width=20, text="Empregado", command=lambda:intentEmpregado(self.master))
        self.bt3.pack()

        self.bt4 = Button(self.master, width=20, text="Habilitação", command=lambda:intentHabilitacao(self.master))
        self.bt4.pack()

        self.bt9 = Button(self.master, width=20, text="Pedido", command=lambda:intentPedido(self.master))
        self.bt4.pack()

        self.bt5 = Button(self.master, width=20, text="Item Pedido", command=lambda:intentItemPedido(self.master))
        self.bt5.pack()

        self.bt6 = Button(self.master, width=20, text="Pessoa Física", command=self.abrePessoaFisica)
        self.bt6.pack()

        self.bt7 = Button(self.master, width=20, text="Pessoa Jurídica", command=self.abrePessoaJuridica)
        self.bt7.pack()

        self.bt8 = Button(self.master, width=20, text="Tipo Serviço", command=lambda:intentTipoServico(self.master))
        self.bt8.pack()

        self.root.mainloop()

    def abrePessoaJuridica(self):
        MainFramePessoaJuridica()

    def abrePessoaFisica(self):
        MainFramePessoaFisica()

if __name__ == '__main__':
    TelaMain()