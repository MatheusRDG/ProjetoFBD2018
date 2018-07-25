from tkinter import *
from BancoDeDados import *

janelaMain = Tk()
janelaMain.title('Serviço de limpeza')

janelaMain.geometry('300x300+200+200')

banco = Banco('localhost', 'root', '', 'servicos_limpeza')

#Lista de entidades para o Option Menu
listaEntidades = ["empregado"]
selecaoInicial = StringVar()
selecaoInicial.set(listaEntidades[0])

#Option Menu

menuEntidades = OptionMenu(janelaMain,selecaoInicial,*listaEntidades)
menuEntidades.pack(side=BOTTOM)

labelReturn = Label(janelaMain,bg="white",height=3,width=10)

#FRAME EMPREGADO
def btnInserirClick():
    try:
        int(edMatricula.get())
    except:
        labelReturn['text']="Matrícula inválida. Por favor digite um número inteiro."
    labelReturn['text']=banco.insert("INSERT INTO servicos_limpeza.empregado(matricula,nome) values (%d,'%s');" % (int(edMatricula.get()), edNome.get()))



labelMatricula= Label(janelaMain, text="Matrícula")

edMatricula = Entry(janelaMain)

labelNome = Label(janelaMain, text="Nome")

edNome = Entry(janelaMain)

btnInserir = Button(janelaMain, width=20, text="Inserir", command=btnInserirClick)


labelMatricula.pack(side=TOP)
edMatricula.pack(side=TOP)
labelNome.pack(side=TOP)
edNome.pack(side=TOP)
btnInserir.pack(side=TOP)
labelReturn.pack(side=TOP,fill=X)

janelaMain.mainloop()


