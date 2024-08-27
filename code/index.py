from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from num2words import num2words
from docxtpl import DocxTemplate
from datetime import datetime
import unicodedata
import decimal
import copy
import keyboard
import re
import sys
import os
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def enter_press(event):
    if event.keysym == 'Return':
        keyboard.send('tab')
        
window = Tk()
window.bind('<Key>', enter_press)


class Formater: #TODO Formaters
    def cpf_formater(text, var, index, mode):
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 11:
           valor = valor[:3] + "." + valor[3:6] + "." + valor[6:9] + "-" + valor[9:]
        else:
            valor = valor.replace('.','').replace('-','')
        text.set(valor)

    def cnpj_formater(text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 14:
           valor = valor[:2] + "." + valor[2:5] + "." + valor[5:8] + "/" + valor[8:12] + "-" + valor[12:]
        else:
            valor = valor.replace('.','').replace('-','').replace('/','')
        text.set(valor)
    

    def cep_formater(text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 8 and '-' not in valor:
           valor = valor[:5] + "-" + valor[5:]
        else:
            valor = valor.replace('-','')
        text.set(valor)

    def rg_formater(text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 10:
           valor = valor[:2] + "-" + valor[2:4] + "." + valor[4:7] + "." + valor[7:]
        else:
            valor = valor.replace('.','').replace('-','').replace(' ','')
        text.set(valor)
    
    def date_formater(text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 8:
           valor = valor[:2] + "/" + valor[2:4] + "/" + valor[4:]
        else:
            valor = valor.replace('/','')
        text.set(valor)

    def comp_formater(text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 6 and '/' not in valor:
           valor = valor[:2] + "/" + valor[2:]
        else:
            valor = valor.replace('/','')
        text.set(valor)

    def valor_formater(text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if ',' not in valor:
            valor = valor + ',00'
        
        text.set(valor)      

class Validator:    #TODO Validators
    def str_validator(text):
        return not text.isdecimal()
    
    def num_validator(text):
        return text.isdecimal()
    
    def valor_validator(text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) == 0:
            return True
        return re.match(padrao, text) is not None

    
    def cpf_validator(text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 15:
            if len(text) >= 12:
                return re.match(padrao, text) is not None
            elif len(text) == 0 or text.isdecimal():
                return True
        return False
        
    def cnpj_validator(text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 19:
            if len(text) >= 15:
                return re.match(padrao, text) is not None
            elif len(text) == 0 or text.isdecimal():
                return True
        return False
    
    def cep_validator(text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 10:
            if len(text) >= 9:
                return re.match(padrao, text) is not None
            elif len(text) in [0,8] or text.isdecimal():
                return True
        return False
    
    def rg_validator(text):
        if len(text) < 14:
            return True
        return False
    
    def date_validator(text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 11:
            if len(text) >= 9:
                return re.match(padrao, text) is not None
            elif len(text) == 0 or text.isdecimal():
                return True
        return False
    
    def comp_validator(text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 8:
            if len(text) >= 7:
                return re.match(padrao, text) is not None
            elif len(text) in [0,6] or text.isdecimal():
                return True
        return False
#sdas
#Arquivo

class File:
    def __init__(self, nome):
        self.arquivo = DocxTemplate(f'Z:\\18 - PROGRAMAS DELTA\\code\\CPS\'s\\CPS {unicodedata.normalize('NFKD', nome.upper()).encode('ascii', 'ignore').decode('ascii')}.docx')    

    def alterar(self, conteudo):  
        self.arquivo.render(conteudo)

    def abrir(self):
        file = asksaveasfilename(title='Defina o nome e o local onde o arquivo será salvo', filetypes=((".docx","*.docx"),))

        ultima_barra = file.rfind('/')
         
        if file[ultima_barra+1:] == '':
            raise Exception('Operação Cancelada')

        self.arquivo.save(file+'.docx')

        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')

        os.startfile(file+'.docx')

#Socios
class Socios:
    def __init__(self, qnt = 1, *, frame, ref):
        self.frame = frame
        self.qnt = qnt
        self.referencias = ref
    
    def set_qnt(self, valor):
        if valor < 5 and valor > 0:
            self.qnt = valor
        else:
            raise Exception('Valor indisponível')

    def exibir_input(self):
        if self.qnt == 1:
            self.input1()

    def input1(self):
        #TODO Socio
        Label(self.frame, text='Sócio',\
            background='lightblue', font=('Times New Roman',15,'bold italic'))\
                .place(relx=0.05,rely=0.42)
                
        self.canvas = Canvas(self.frame, width=655, height=10,border=-5)
        self.canvas.place(relx=0.13,rely=0.455)
                
        self.canvas.create_line(-5,0,655,0, fill="darkblue", width=10)
        
        # x,angulo x , y, angulo y

        ###########nome

        Label(self.frame, text='Nome',\
            background='lightblue', font=(10))\
                .place(relx=0.05,rely=0.48)

        Entry(self.frame,\
            textvariable=self.referencias['nomeContra'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.05,rely=0.53,relwidth=0.25,relheight=0.05)
        
         ###########RG
        
        self.valRG = StringVar()

        self.valRG.trace_add('write', lambda *args, passed = self.valRG:\
            Formater.rg_formater(passed, *args) )

        Label(self.frame, text='RG',\
            background='lightblue', font=(10))\
                .place(relx=0.33,rely=0.48)
        

        Entry(self.frame, textvariable = self.valRG, \
            validate ='key', validatecommand =(self.frame.register(Validator.rg_validator), '%P'))\
                .place(relx=0.33,rely=0.53,relwidth=0.1,relheight=0.05)

        self.referencias['rgContra'] = self.valRG
        
        ###########Org. Emissor

        Label(self.frame, text='Org.',\
            background='lightblue', font=(10))\
                .place(relx=0.45,rely=0.48)

        Entry(self.frame,\
            textvariable=self.referencias['emissorContra'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.45,rely=0.53,relwidth=0.05,relheight=0.05)

        ###########CPF
        
        self.valCPF = StringVar()

        self.valCPF.trace_add('write', lambda *args, passed = self.valCPF:\
            Formater.cpf_formater(passed, *args) )

        Label(self.frame, text='CPF',\
            background='lightblue', font=(10))\
                .place(relx=0.53,rely=0.48)
        

        Entry(self.frame, textvariable = self.valCPF, \
            validate ='key', validatecommand =(self.frame.register(Validator.cpf_validator), '%P'))\
                .place(relx=0.52,rely=0.53,relwidth=0.105,relheight=0.05)

        self.referencias['cpfContra'] = self.valCPF
        
        ###########TODO Nacionalidade
        nacio_var = BooleanVar()
        ttk.Checkbutton(self.frame, text='Não é brasileiro?', variable= nacio_var, \
            command= lambda: \
                self.input_janela('Nacionalidade') if nacio_var.get()\
                    else self.referencias['valNacionalidade']\
                        .set('brasileiro(a)'))\
                .place(relx=0.6425,rely=0.53,relwidth=0.142,relheight=0.05)

        ###########Emprego
        empreg_var = BooleanVar()
        ttk.Checkbutton(self.frame, text='Não é empresário?', variable= empreg_var, \
            command= lambda: \
                self.input_janela('Emprego') if empreg_var.get() \
                    else self.referencias['valEmprego']\
                        .set('empresário(a)'))\
                .place(relx=0.8,rely=0.53,relwidth=0.155,relheight=0.05)

        ###########rua

        Label(self.frame, text='Rua',\
            background='lightblue', font=(10))\
                .place(relx=0.05,rely=0.61)

        Entry(self.frame,\
            textvariable=self.referencias['ruaContra'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.05,rely=0.66,relwidth=0.25,relheight=0.05)

        ###########Num

        Label(self.frame, text='Num.',\
            background='lightblue', font=(10))\
                .place(relx=0.33,rely=0.61)

        Entry(self.frame,\
            textvariable=self.referencias['numContra'],\
                validate='key', validatecommand=(self.frame.register(lambda text: text.isdecimal()), '%S'))\
                .place(relx=0.33,rely=0.66,relwidth=0.05,relheight=0.05)

        ###########bairro

        Label(self.frame, text='Bairro',\
            background='lightblue', font=(10))\
                .place(relx=0.4,rely=0.61)

        Entry(self.frame,\
            textvariable=self.referencias['bairroContra'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.4,rely=0.66,relwidth=0.2,relheight=0.05)
        
        ###########CEP 
        
        self.valCEP_Contra = StringVar()

        self.valCEP_Contra.trace_add('write', lambda *args, passed = self.valCEP_Contra:\
            Formater.cep_formater(passed, *args) )

        Label(self.frame, text='CEP',\
            background='lightblue', font=(10))\
                .place(relx=0.65,rely=0.61)
        

        Entry(self.frame, textvariable = self.valCEP_Contra, \
            validate ='key', validatecommand =(self.frame.register(Validator.cep_validator), '%P'))\
                .place(relx=0.65,rely=0.66,relwidth=0.075,relheight=0.05)

        self.referencias['cepContra'] = self.valCEP_Contra

        ###########Estado Civil
        
        Label(self.frame, text='Estado Civil',\
            background='lightblue', font=(10))\
                .place(relx=0.75,rely=0.61)

        self.estadoEntry = StringVar(self.frame)

        self.estadoEntryOpt = ('solteiro(a)','divorciado(a)','viuvo(a)')

        self.popup = ttk.OptionMenu(self.frame, self.estadoEntry,'', *self.estadoEntryOpt)

        self.menuCasado = self.popup['menu']

        #Casado
        self.subLista = Menu(self.menuCasado, tearoff=False)
        self.menuCasado.add_cascade(label = 'casado(a)',menu= self.subLista)
        self.subLista.add_command(label='Comunhão Parcial de Bens', \
            command= lambda: self.estadoEntry.set('casado(a) em CPB'))
        
        self.subLista.add_command(label='Comunhão Total de Bens',\
            command= lambda: self.estadoEntry.set('casado(a) em CTB'))
        
        self.subLista.add_command(label='Separação Total de Bens',\
            command= lambda: self.estadoEntry.set('casado(a) em STB'))


        self.popup.place(relx=0.75,rely=0.66,relwidth=0.2,relheight=0.06)

        self.referencias['estadoCivilContra'] = self.estadoEntry
        
        ###########Cidade

        Label(self.frame, text='Cidade',\
            background='lightblue', font=(10))\
                .place(relx=0.05,rely=0.72)

        Entry(self.frame,\
            textvariable=self.referencias['cidadeContra'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.05,rely=0.77,relwidth=0.25,relheight=0.05)
        
        ###########Estado

        Label(self.frame, text='Estado',\
            background='lightblue', font=(10))\
                .place(relx=0.33,rely=0.72)

        Entry(self.frame,\
            textvariable=self.referencias['estadoContra'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.33,rely=0.77,relwidth=0.25,relheight=0.05)

        ###########Complemento

        Label(self.frame, text='Complemento (opcional)',\
            background='lightblue', font=(10))\
                .place(relx=0.6,rely=0.72)

        Entry(self.frame,\
            textvariable=self.referencias['compleContra'])\
                .place(relx=0.61,rely=0.77,relwidth=0.34,relheight=0.05)

#Conteudo
class Content:
    def __init__(self, referencias):
        self.dictonary = {chave: copy.deepcopy(valor.get()) for chave, valor in referencias.items()}
        
        self.SAL_MINIMO = 1412.00
        self.CUSTO_CORREIO = 0.02

    def update_dict(self):

        for chave, valor in self.dictonary.items():
            if chave == 'estadoCivilContra':
                self.dictonary[chave] = self.__set_estadoCivil(valor)
            elif chave == 'valPag':
                valorDbl = valor[2:].replace(',','.')
                self.dictonary[chave] = self.__set_valor(valorDbl)
            elif chave in ['numEmpre','dtVenc']:
                self.dictonary[chave] = self.__set_num(valor)
            elif chave == 'dataComple':
                self.dictonary[chave] = self.dictonary['dtInic'].get()[2:]
            elif chave in ['dtAss', 'dtInic']:
                self.dictonary[chave] = self.__set_data(valor)
            elif chave in ['nomeContra','nomeEmp','rgContra','emissorContra']:
                self.dictonary[chave] = valor.upper()
            else:
                self.dictonary[chave] = valor.capitalize()

        self.dictonary['valPorc'] = self.__calc_porc(valorDbl)

        return self.dictonary

    def __set_estadoCivil(self, estadoCiv):
        if 'STB' in estadoCiv:
            estadoCiv = 'Casado em Separação Total de Bens'
        elif 'CPB' in estadoCiv:
            estadoCiv = 'Casado em Comunhão Parcial de Bens'
        elif 'CTB' in estadoCiv:
            estadoCiv = 'Casado em Comunhão Total de Bens'
        return estadoCiv

    def __set_valor(self, valor):
        valorExtenso = num2words(valor,lang='pt_BR', to='currency')\
            .replace('reais e','reais,')
        return f'R$ {float(valor):,.2f} ({valorExtenso})'.replace('.',',')
    
    def __set_num(self, num):
        valorExtenso = num2words(num,lang='pt_BR')
        return f'{num} ({valorExtenso})'
    
    def __set_data(self, data):
        data_format = datetime.strptime(data, '%d/%m/%Y')
        return data_format.strftime("%d de %B de %Y")

    def __calc_porc(self, honorarios):
        custo_envio = self.SAL_MINIMO * self.CUSTO_CORREIO
        return f'{((custo_envio / float(honorarios)) * 100):,.2f}%'

#Páginas

class Pages:
    def __init__(self, titulo):
        self.frame = Frame(window, bd=4, bg='lightblue')
        self.frame.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)
        window.bind('<KeyRelease>', self.alter_estado)

        #TODO Referencias
        self.referencias = {
            'nomeContra' : StringVar(),
            'rgContra' : StringVar(),  
            'emissorContra' : StringVar(), 
            'cpfContra' : StringVar(), 
            'estadoCivilContra' : StringVar(),
            'valNacionalidade': StringVar(), 
            'valEmprego': StringVar(),
            'ruaContra' : StringVar(), 
            'numContra' : StringVar(), 
            'bairroContra' : StringVar(),  
            'cepContra' : StringVar(),  
            'cidadeContra' : StringVar(), 
            'estadoContra' : StringVar(), 
            "compleContra" : StringVar(),
            "valPag" : StringVar(),
            "dtInic" : StringVar(),
            "dtAss" : StringVar(),
            "dtVenc" : StringVar(),
            "numEmpre" : StringVar()
        }            

        self.referencias['valNacionalidade'].set('brasileiro(a)')
        self.referencias['valEmprego'].set('empresário(a)')

        self.socio = Socios(frame = self.frame, ref=self.referencias)

        self.titulo = titulo
        self.file = File(titulo)

    def alter_estado(self, event):
        if event.keysym == 'Down' or event.keysym == 'Up':
            self.popup.focus()
            keyboard.send('space')

    def cabecalho(self, y = 0):
        #Titulo
        Label(self.frame, text= self.titulo, background='lightblue',\
            font=('Times',30,'bold'))\
                .place(relx=0.325,rely= y + 0.05)
        #Logo
        self.logo = PhotoImage(file='Z:\\18 - PROGRAMAS DELTA\\code\\imgs\\deltaprice_logo-slim.png')
        
        self.logo = self.logo.subsample(5,5)
        
        Label(self.frame, image=self.logo, background='lightblue')\
            .place(relx=0.75,rely= y + 0.01,relwidth=0.12,relheight=0.15)

        #Botão voltar
        Button(self.frame, text='Voltar ao menu',\
            command= lambda: self.frame.destroy())\
                .place(relx=0,rely= 0,relwidth=0.25,relheight=0.06)

    def contrato(self):
        #Contrato
        Label(self.frame, text='Contrato',\
            background='lightblue', font=('Times New Roman',15,'bold italic'))\
                .place(relx=0.05,rely=0.82)
                
        self.canvas = Canvas(self.frame, width=625, height=10,border=-5)
        self.canvas.place(relx=0.17,rely=0.845)
                
        self.canvas.create_line(-5,0,625,0, fill="darkblue", width=10)
        
        # x,angulo x , y, angulo y

        ###########Valor pagamento
        
        self.valPag = StringVar()

        self.valPag.trace_add('write', lambda *args, passed = self.valPag:\
            Formater.valor_formater(passed, *args) )

        Label(self.frame, text='Val. Contrato.',\
            background='lightblue', font=(10))\
                .place(relx=0.05,rely=0.88)
        
        Entry(self.frame, textvariable = self.valPag, \
            validate ='key', validatecommand =(self.frame.register(Validator.valor_validator), '%P'))\
                .place(relx=0.06,rely=0.93,relwidth=0.1,relheight=0.05)
                
        self.referencias['valPag'] = self.valPag

        ###########Data inicio
        
        self.valDT_inic = StringVar()

        self.valDT_inic.trace_add('write', lambda *args, passed = self.valDT_inic:\
            Formater.date_formater(passed, *args) )

        Label(self.frame, text='Data início',\
            background='lightblue', font=(10))\
                .place(relx=0.182,rely=0.88)
        

        Entry(self.frame, textvariable = self.valDT_inic, \
            validate ='key', validatecommand =(self.frame.register(Validator.date_validator), '%P')).place(relx=0.185,rely=0.93,relwidth=0.08,relheight=0.05)

        self.referencias['dtInic'] = self.valDT_inic

        ###########Data Assinatura
        
        self.valDT_ass = StringVar()

        self.valDT_ass.trace_add('write', lambda *args, passed = self.valDT_ass:\
            Formater.date_formater(passed, *args) )

        Label(self.frame, text='Data Ass.',\
            background='lightblue', font=(10))\
                .place(relx=0.3,rely=0.88)
        

        Entry(self.frame, textvariable = self.valDT_ass, \
            validate ='key', validatecommand =(self.frame.register(Validator.date_validator), '%P')).place(relx=0.3,rely=0.93,relwidth=0.08,relheight=0.05)

        self.referencias['dtAss'] = self.valDT_ass

        ###########Dia vencimento
        
        Label(self.frame, text='Dia Venc.',\
            background='lightblue', font=(10))\
                .place(relx=0.4,rely=0.88)
        

        Entry(self.frame,textvariable=self.referencias['dtVenc'], validate='key', validatecommand=(self.frame.register(lambda text: text.isdecimal() if len(text) < 3 else False), '%P')).place(relx=0.435,rely=0.93,relwidth=0.02,relheight=0.05)


        ###########Num. Empregados

        Label(self.frame, text='Num.Empre.',\
            background='lightblue', font=(10))\
                .place(relx=0.5,rely=0.88)

        Entry(self.frame,\
            textvariable=self.referencias['numEmpre'],\
                validate='key', validatecommand=(self.frame.register(lambda text: text.isdecimal()), '%S'))\
                .place(relx=0.535,rely=0.93,relwidth=0.05,relheight=0.05)

        #Botão enviar
        self.btnEnviar = Button(self.frame, text='Gerar CPS',\
            command= lambda: self.executar())
        self.btnEnviar.place(relx=0.7,rely=0.86,relwidth=0.25,relheight=0.12)

    def executar(self):
        try:
            # if self.__input_vazio():
            #     raise Exception ('Existem entradas vazias, favor preencher todas')
            
            conteudoUpdt = Content(self.referencias).update_dict()

            self.file.alterar(conteudoUpdt)
            self.file.abrir()

        except decimal.InvalidOperation:
            messagebox.showwarning(title='Aviso', message= 'Insira um número válido')
        except ValueError:
            messagebox.showwarning(title='Aviso', message= 'Insira datas válidas')
        except Exception as e:
            messagebox.showwarning(title='Aviso', message= e)

    def __input_vazio(self):
        for chave, valor in self.referencias.items():
            if valor.get() == ''\
                and chave != 'compleContra' \
                    and chave != 'compleEmp':
                return True
        return False
    
    def input_janela(self, tipo):
        self.janela = Toplevel(self.frame, bd=4, bg='darkblue' )
        self.janela.resizable(False,False)
        self.janela.geometry('300x70')
        self.janela.iconbitmap('Z:\\18 - PROGRAMAS DELTA\\code\\imgs\\delta-icon.ico')
        self.janela.title(tipo)
        self.janela.transient(window)
        self.janela.focus_force()
        self.janela.grab_set()

        self.janela_frame = Frame(self.janela, bd=4, bg='lightblue')
        self.janela_frame.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        #Titulo
        Label(self.janela_frame, text= tipo,\
            background='lightblue', font=('Times New Roman',15,'bold italic'))\
                .place(relx=0,rely=0)
                
        self.canvas = Canvas(self.janela_frame, width=625, height=10, background='darkblue',border=-5)
        self.canvas.place(relx=0.55,rely=0.05)
                
        self.canvas.create_line(-5,0,625,0, fill="darkblue", width=10)

        ###########Valor Competência
        valComp = StringVar()

        self.entryVal = Entry(
            self.janela_frame, 
            textvariable = valComp,
            validate='key', 
            validatecommand=(
                self.frame.register(lambda text: not text.isdecimal()), '%S'
                )
            ).place(relx=0,rely=0.65,relwidth=0.7,relheight=0.3)
                
        self.referencias[f'val{tipo}'] = valComp

        Button(self.janela_frame, text='OK',\
            command= lambda: self.janela.destroy())\
                .place(relx=0.75,rely=0.6,relwidth=0.15,relheight=0.4)
                

class Enterprise(Pages):
    def __init__(self, titulo):
        super().__init__(titulo)
        
        self.referencias = {
            'nomeEmp' : StringVar(),
            'ruaEmp' : StringVar(), 
            'numEmp' : StringVar(), 
            'bairroEmp' : StringVar(),
            'cepEmp' : StringVar(), 
            'cnpjEmp' : StringVar(),  
            "compleEmp" : StringVar(), 
            'nomeContra' : StringVar(),
            'rgContra' : StringVar(),  
            'emissorContra' : StringVar(), 
            'cpfContra' : StringVar(), 
            'estadoCivilContra' : StringVar(), 
            'ruaContra' : StringVar(), 
            'numContra' : StringVar(), 
            'bairroContra' : StringVar(),  
            'cepContra' : StringVar(),  
            'cidadeContra' : StringVar(), 
            'estadoContra' : StringVar(), 
            "compleContra" : StringVar(),
            "valPag" : StringVar(),
            "dtInic" : StringVar(),
            "dtAss" : StringVar(),
            "dtVenc" : StringVar(),
            "numEmpre" : StringVar()
        }            

    def index(self):
        self.cabecalho()

        #Empresa
        Label(self.frame, text='Empresa',\
            background='lightblue', font=('Times New Roman',15,'bold italic'))\
                .place(relx=0.05,rely=0.115)
                
        self.canvas = Canvas(self.frame, width=625, height=10, background='darkblue',border=-5)
        self.canvas.place(relx=0.17,rely=0.15)
                
        self.canvas.create_line(-5,0,625,0, fill="darkblue", width=10)
        
        # x,angulo x , y, angulo y
                
        ###########nome empresa

        Label(self.frame, text='Nome',\
            background='lightblue', font=(10))\
                .place(relx=0.05,rely=0.18)

        self.nomeEmpEntry = Entry(self.frame,\
            textvariable=self.referencias['nomeEmp'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.05,rely=0.23,relwidth=0.25,relheight=0.05)

        ###########rua

        Label(self.frame, text='Rua',\
            background='lightblue', font=(10))\
                .place(relx=0.35,rely=0.18)

        self.ruaEmpEntry = Entry(self.frame,\
            textvariable=self.referencias['ruaEmp'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.35,rely=0.23,relwidth=0.20,relheight=0.05)

        ###########Num

        Label(self.frame, text='Num.',\
            background='lightblue', font=(10))\
                .place(relx=0.6,rely=0.18)

        self.numEmpEntry = Entry(self.frame,\
            textvariable=self.referencias['numEmp'],\
                validate='key', validatecommand=(self.frame.register(lambda text: text.isdecimal()), '%S'))\
                    .place(relx=0.61,rely=0.23,relwidth=0.05,relheight=0.05)

        ###########bairro

        Label(self.frame, text='Bairro',\
            background='lightblue', font=(10))\
                .place(relx=0.7,rely=0.18)

        self.bairroEmpEntry = Entry(self.frame,\
            textvariable=self.referencias['bairroEmp'],\
                validate='key', validatecommand=(self.frame.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.7,rely=0.23,relwidth=0.25,relheight=0.05)

        ########### CEP Empre

        self.valCEP_Empre = StringVar()

        self.valCEP_Empre.trace_add('write', lambda *args, passed = self.valCEP_Empre:\
            Formater.cep_formater(passed, *args) )

        Label(self.frame, text='CEP',\
            background='lightblue', font=(10))\
                .place(relx=0.05,rely=0.31)
        

        self.CEPEntry = Entry(self.frame, textvariable = self.valCEP_Empre, \
            validate ='key', validatecommand =(self.frame.register(Validator.cep_validator), '%P'))\
                .place(relx=0.05,rely=0.36,relwidth=0.075,relheight=0.05)

        self.referencias['cepEmp'] = self.valCEP_Empre

        ########### CNPJ
        
        self.valCNPJ = StringVar()

        self.valCNPJ.trace_add('write', lambda *args, passed = self.valCNPJ:\
            Formater.cnpj_formater(passed, *args) )

        Label(self.frame, text='CNPJ',\
            background='lightblue', font=(10))\
                .place(relx=0.35,rely=0.31)
        

        Entry(self.frame, textvariable = self.valCNPJ, \
            validate ='key', validatecommand =(self.frame.register(Validator.cnpj_validator), '%P'))\
                .place(relx=0.35,rely=0.36,relwidth=0.135,relheight=0.05)

        self.referencias['cnpjEmp'] = self.valCNPJ
                
        ###########Complemento

        Label(self.frame, text='Complemento (opcional)',\
            background='lightblue', font=(10))\
                .place(relx=0.6,rely=0.31)

        self.complementoEntry = Entry(self.frame,\
            textvariable=self.referencias['compleEmp'])\
                .place(relx=0.61,rely=0.36,relwidth=0.35,relheight=0.05)
        
        #TODO Inp-Soc
        self.socio.exibir_input()

        self.contrato()


class LucroPresumido(Enterprise):
    def __init__(self, titulo):
        super().__init__(titulo)
        self.referencias['valCompe'] = StringVar(value='R$ ')
        self.referencias['dtCompe'] = StringVar()

        self.index()
        self.add_competencia()

    def add_competencia(self):
        ###########Valor EFD
        
        self.valCompe = StringVar()

        self.valCompe.trace_add('write', lambda *args, passed = self.valCompe:\
            Formater.valor_formater(passed, *args) )

        Label(self.frame, text='Val. EFD-Compe.',\
            background='lightblue', font=(10))\
                .place(relx=0.62,rely=0.88)
        
        Entry(self.frame, textvariable = self.valCompe, \
            validate ='key', validatecommand =(self.frame.register(Validator.valor_validator), '%P'))\
                .place(relx=0.65,rely=0.93,relwidth=0.1,relheight=0.05)
                
        self.referencias['valCompe'] = self.valCompe

        #btn Enviar
        self.btnEnviar.place(relx=0.8,rely=0.86,relwidth=0.15,relheight=0.12)

class Person(Pages):
    def __init__(self, titulo):
        super().__init__(titulo)
    
    def index(self):
        self.cabecalho(0.08)
        self.socio.exibir_input()
        self.contrato()

#Aplicação

class App:
    def __init__(self):
        self.window = window
        self.tela()
        self.menu()
        window.mainloop()

    def tela(self):
        self.window.configure(background='darkblue')
        self.window.resizable(False,False)
        self.window.geometry('880x500')
        self.window.iconbitmap('Z:\\18 - PROGRAMAS DELTA\\code\\imgs\\delta-icon.ico')
        self.window.title('Gerador de CPS')

    def menu(self):
        self.menu = Frame(self.window, bd=4, bg='lightblue')
        self.menu.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        self.textOrientacao = Label(self.menu, text='Selecione o tipo de CPS que deseja fazer:', background='lightblue', font=('arial',20,'bold'))\
        .place(relx=0.15,rely=0.23,relheight=0.15)
        
        #Logo
        self.logo = PhotoImage(file='Z:\\18 - PROGRAMAS DELTA\\code\\imgs\\deltaprice-hori.png').subsample(4,4)
        
        Label(self.menu, image=self.logo, background='lightblue')\
            .place(relx=0.175,rely=0.05,relwidth=0.7,relheight=0.2)

        #Pessoa física
        Button(self.menu, text='CPS Pessoa Física',\
            command= lambda: Person('Pessoa Física').index())\
                .place(relx=0.15,rely=0.7,relwidth=0.25,relheight=0.15)

        #Inatividade
        Button(self.menu, text='CPS Inatividade',\
            command= lambda: Enterprise('Inatividade').index())\
                .place(relx=0.60,rely=0.4,relwidth=0.25,relheight=0.15)

        #Lucro Presumido
        Button(self.menu, text='CPS Lucro Presumido / Real',\
            command= lambda: LucroPresumido('Lucros'))\
                .place(relx=0.15,rely=0.4,relwidth=0.25,relheight=0.15)

        #Simples Nacional
        Button(self.menu, text='CPS Simples Nacional',\
            command= lambda: Enterprise('Simples Nacional').index())\
                .place(relx=0.60,rely=0.7,relwidth=0.25,relheight=0.15)

App()