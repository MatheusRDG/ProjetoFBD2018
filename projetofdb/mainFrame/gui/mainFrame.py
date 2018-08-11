#Classe main de execução

from tkinter import*
from tkinter import ttk

from alocacao.gui.MainFrameAlocacao import *
from cliente.gui.MainFrameCliente import *
from empregado.gui.MainFrameEmpregado import *
from habilitacao.gui.MainFrameHabilitacao import *
from itemPedido.gui.MainFrameItemPedido import *
from pedido.gui.MainFramePedido import *
from pessoaFisica.gui.MainFramePessoaFisica import *
from pessoaJuridica.gui.MainFramePessoaJuridica import *
from tipoServico.gui.MainFrameTipoServico import *

def telaMain():
    root = Tk()

    label = Label(root,text="Bem vindo ao gerenciador Serviço de Limpeza.\n Selecione uma entidade:")
    label.grid(row=0,column=0)

    bt1 = Button(root, width=20, text="Alocação", command=intentAlocacao)
    bt1.grid(row = 1,column= 0)

    bt2 = Button(root, width=20, text="Cliente", command=intentCliente)
    bt2.grid(row=2, column=0)

    bt3 = Button(root, width=20, text="Empregado", command=intentEmpregado)
    bt3.grid(row=3, column=0)

    bt4 = Button(root, width=20, text="Habilitação", command=intentHabilitacao)
    bt4.grid(row=4, column=0)

    bt5 = Button(root, width=20, text="Item Pedido", command=intentItemPedido)
    bt5.grid(row=5, column=0)

    bt6 = Button(root, width=20, text="Pessoa Física", command=intentPessoaFisica)
    bt6.grid(row=6, column=0)

    bt7 = Button(root, width=20, text="Pessoa Jurídica", command=intentPessoaJuridica)
    bt7.grid(row=7, column=0)

    bt8 = Button(root, width=20, text="Tipo Serviço", command=intentTipoServico)
    bt8.grid(row=8, column=0)

    root.geometry('300x300+200+200')
    root.mainloop()
def intentBt1():
    root.de
telaMain()

