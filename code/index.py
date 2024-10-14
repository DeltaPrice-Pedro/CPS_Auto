from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from abc import ABCMeta, abstractmethod
from num2words import num2words
from docxtpl import DocxTemplate, RichText
from datetime import datetime
from itertools import cycle
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
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def enter_press(event):
    if event.keysym == 'Return':
        keyboard.send('tab')

def alter_estado(self, event):
    if event.keysym == 'Down' or event.keysym == 'Up':
        self.popup.focus()
        keyboard.send('space')
        
window = Tk()
window.bind('<Key>', enter_press)


class IFormater: #TODO Formaters
    def cpf_formater(self, text, var, index, mode):
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 11:
           valor = valor[:3] + "." + valor[3:6] + "." + valor[6:9] + "-" + valor[9:]
        else:
            valor = valor.replace('.','').replace('-','')
        text.set(valor)

    def cnpj_formater(self, text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 14:
           valor = valor[:2] + "." + valor[2:5] + "." + valor[5:8] + "/" + valor[8:12] + "-" + valor[12:]
        else:
            valor = valor.replace('.','').replace('-','').replace('/','')
        text.set(valor)
    

    def cep_formater(self, text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 8 and '-' not in valor:
           valor = valor[:5] + "-" + valor[5:]
        else:
            valor = valor.replace('-','')
        text.set(valor)

    def rg_formater(self, text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 10:
           valor = valor[:2] + "-" + valor[2:4] + "." + valor[4:7] + "." + valor[7:]
        else:
            valor = valor.replace('.','').replace('-','').replace(' ','')
        text.set(valor)
    
    def date_formater(self, text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 8:
           valor = valor[:2] + "/" + valor[2:4] + "/" + valor[4:]
        else:
            valor = valor.replace('/','')
        text.set(valor)

    def comp_formater(self, text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if len(valor) == 6 and '/' not in valor:
           valor = valor[:2] + "/" + valor[2:]
        else:
            valor = valor.replace('/','')
        text.set(valor)

    def valor_formater(self, text, var, index, mode): 
        #Só recebe valor que passa pelo validador
        valor = text.get()
        if ',' not in valor:
            valor = valor + ',00'
        
        text.set(valor)      

class IValidator:    #TODO Validators
    def str_validator(self, text):
        return not text.isdecimal()
    
    def num_validator(self, text):
        return text.isdecimal()
    
    def valor_validator(self, text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) == 0:
            return True
        return re.match(padrao, text) is not None

    def operacao_cpf(self, text):
        numeros = [int(digito) for digito in text if digito.isdigit()]
  
        for i in range(9,11):
            soma_produtos = sum(a*b for a, b in zip (numeros[0:i], range (i + 1, 1, -1)))
            digito_esperado = (soma_produtos * 10 % 11) % 10
            if numeros[i] != digito_esperado:
                return False
        return True
        
    def cpf_validator(self, text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 15:
            if len(text) >= 12:
                if len(text) == 14 and self.operacao_cpf(text) == False:
                    messagebox.showwarning(title='Aviso', message='O CPF digitado é inválido')
                return re.match(padrao, text) is not None
            elif len(text) == 0 or text.isdecimal():
                return True
        return False
    
    def operacao_cnpj(self, text):
        cnpj = ''.join([digito for digito in text if digito.isdigit()])
        if cnpj in (c * 14 for c in "1234567890"):
            return False

        cnpj_r = cnpj[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            return False
        return True
        
    def cnpj_validator(self, text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 19:
            if len(text) >= 15:
                if len(text) == 18 and self.operacao_cnpj(text) == False:
                    messagebox.showwarning(title='Aviso', message='O CNPJ digitado é inválido')
                return re.match(padrao, text) is not None
            elif len(text) == 0 or text.isdecimal():
                return True
        return False
    
    def cep_validator(self, text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 10:
            if len(text) >= 9:
                return re.match(padrao, text) is not None
            elif len(text) in [0,8] or text.isdecimal():
                return True
        return False
    
    def rg_validator(self, text):
        if len(text) < 14:
            return True
        return False
    
    def date_validator(self, text):
        padrao = r"^[-\d.,/]+$"  # Permite dígitos, ponto, vírgula, hífen e barra
        if len(text) < 11:
            if len(text) >= 9:
                return re.match(padrao, text) is not None
            elif len(text) == 0 or text.isdecimal():
                return True
        return False
    
    def comp_validator(self, text):
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
        self.arquivo = DocxTemplate(resource_path(f'CPS\'s\\CPS {unicodedata.normalize('NFKD', nome.upper()).encode('ascii', 'ignore').decode('ascii')}.docx'))

    def alterar(self, base, updt):  
        self.arquivo.render(base)
        self.arquivo.save(self.caminho)
        self.arquivo = DocxTemplate(self.caminho)
        self.arquivo.render(updt)
        self.arquivo.save(self.caminho)

    def salvar(self):
        self.caminho = asksaveasfilename(title='Defina o nome e o local onde o arquivo será salvo', filetypes=((".docx","*.docx"),))

        if self.caminho[self.caminho.rfind('/') + 1:] == '':
            raise Exception('Operação Cancelada')
        
        self.caminho = self.caminho + '.docx'
        
    
    def abrir(self):
        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
        os.startfile(self.caminho)

class IValido:
    def __init__(self) -> None:
        pass

    def validar(self, ref):
        resp_final = self.__textos_vazios(self.__add_vazios(ref))

        if len(resp_final) != 0:
            raise Exception (f'Estão vazios as seguintes dados:\n{resp_final}\nfavor preencher todos')
        
    def __add_vazios(self, ref):
        vazios_contrato = []
        vazios_emp = []
        vazios_repre1 = []
        vazios_repre2 = []
        vazios_repre3 = []
    
        vazios_repre = {
            1: vazios_repre1,
            2: vazios_repre2,
            3: vazios_repre3
        }

        for key, valor in ref.items():
            if valor == '':
                if 'Contra' in key:
                    for index, lista in vazios_repre.items():
                        if str(index) in key:
                            lista.append(key.replace('Contra'+ str(index), ''))
                elif 'Emp' in key:
                    vazios_emp.append(key.replace('Emp',''))
                else:
                    vazios_contrato.append(key)

        return [vazios_emp, vazios_repre, vazios_contrato]

    def __textos_vazios(self, lista):
        resp_final = ''

        text_void = {
            'Empresa: ': lista[0],
            'Representante 1: ': lista[1][1],
            'Representante 2: ': lista[1][2],
            'Representante 3: ': lista[1][3],
            'Contrato: ': lista[2]
        }
         
        for titulo, vet in text_void.items():
            if len(vet) != 0:
                resp_final = f'{resp_final}\n{titulo.upper()}\n{' - '.join(str(x) for x in vet)}\n'

        return resp_final

class Content:
    def __init__(self, referencias):
        self.dictonary = {chave: copy.deepcopy(valor.get()) for chave, valor in referencias.items()}
        
        self.SAL_MINIMO = 1412.00
        self.CUSTO_CORREIO = 0.02

    def update_dict(self, qnt_repre):

        ref = {
            'valorPagamento': self.__set_valor(),
            'numeroRuaEmp': self.__set_num(self.dictonary['numeroRuaEmp']),
            'diaVenc': self.__set_num(self.dictonary['diaVencimento']),
            'dataComple': lambda: self.dictonary['dataInicio'].get()[2:],
            'dataAssinatura': self.__set_data(self.dictonary['dataAssinatura']),
            'dataInicio': self.__set_data(self.dictonary['dataInicio']),
        }

        self.dictonary['valPorc'] = self.__calc_porc()
        
        for key, func in ref.items():
            self.dictonary[key] = func

        self.__set_IJuridica()
        self.__update_repre(qnt_repre)

        return self.dictonary
    
    def __update_repre(self, qnt_repre):
        ref_estado = {
            'STB': 'Casado em Separação Total de Bens',
            'CPB': 'Casado em Comunhão Parcial de Bens',
            'CUB': 'Casado em Comunhão Universal de Bens'
        }

        for i in range(1, qnt_repre + 1):
            i = str(i)
            ref = {
                'nomeContra': RichText(self.dictonary['nomeContra' + i].upper(), bold = True),
                'ruaContra': self.dictonary['ruaContra'+ i].title(), 
                'bairroContra':self.dictonary['bairroContra'+ i].title(),
                'cpfContra' : RichText(self.dictonary['cpfContra'+ i].upper(), bold = True),
                'compleContra': self.dictonary['compleContra'+ i].title()
            }

            regime = self.dictonary['estadoCivilContra' + i]
            if regime in ref_estado:
                self.dictonary['estadoCivilContra' + i] = ref_estado[regime]

            for index, value in ref.items():
                self.dictonary[index + i] = value

    def __set_IJuridica(self):
        if 'nomeEmp' in self.dictonary:

            ref = {
                'nomeEmp': RichText(self.dictonary['nomeEmp'].upper(), bold = True),
                'ruaEmp': self.dictonary['ruaEmp'].title(), 
                'bairroEmp':self.dictonary['bairroEmp'].title(),
                'cnpjEmp' : RichText(self.dictonary['cnpjEmp'].upper(), bold = True),
                'compleEmp': self.dictonary['bairroEmp'].title()
            }

            for index, value in ref.items():
                self.dictonary[index] = value

            # if "LTDA" in self.dictonary['nomeEmp']:
            #     self.dictonary['nomeEmp'] = self.dictonary['nomeEmp'].replace('LTDA',' LTDA.')

    def __set_valor(self):
        valor = self.dictonary['valorPagamento'].replace(',','.')
        valorExtenso = num2words(valor, lang='pt_BR', to='currency')\
            .replace('reais e','reais,')
        return f'R$ {float(valor):,.2f} ({valorExtenso})'.replace('.',',')
    
    def __set_num(self, num):
        valorExtenso = num2words(num,lang='pt_BR')
        return f'{num} ({valorExtenso})'

    def __set_data(self, data):
        data_format = datetime.strptime(data, '%d/%m/%Y')
        return data_format.strftime("%d de %B de %Y")
        
    def __calc_porc(self):
        valor = self.dictonary['valorPagamento'].replace(',','.')
        custo_envio = self.SAL_MINIMO * self.CUSTO_CORREIO
        return f'{((custo_envio / float(valor)) * 100):,.2f}%'
    
class Opcionais:
    def __init__(self, frame):
        self.janela = Toplevel(frame, bd=4, bg='darkblue' )
        self.janela.resizable(False,False)
        self.janela.iconbitmap(resource_path('imgs\\cps-icon.ico'))
        self.janela.transient(window)
        self.janela.focus_force()
        self.janela.grab_set()
        self.janela.protocol("WM_DELETE_WINDOW", self.__disable_x)

        self.janela_frame = Frame(self.janela, bd=4, bg='lightblue')
        self.janela_frame.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)
        self.janela.geometry('300x70')
        self.janela.title('Complemento')
        
    def __disable_x(self):
        pass

    def exibir(self, title, ref):
        #Titulo
        Label(self.janela_frame, text= title,\
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
                self.janela.register(lambda text: not text.isdecimal()), '%S'
                )
            ).place(relx=0,rely=0.65,relwidth=0.7,relheight=0.3)
                
        ref[f'val{title}'] = valComp

        Button(self.janela_frame, text='OK',\
            command= lambda: self.janela.destroy())\
                .place(relx=0.75,rely=0.6,relwidth=0.15,relheight=0.4)
        
class Layout():
    def __init__(self) -> None:
        pass

    def  janela(self, obj, id, frame):
        self.janela = Toplevel(frame, bd=4, bg='darkblue' )
        self.janela.resizable(False,False)
        self.janela.iconbitmap(resource_path('imgs\\cps-icon.ico'))
        self.janela.transient(window)
        self.janela.focus_force()
        self.janela.grab_set()
        self.janela.geometry('880x190')
        self.janela.title(f'Entrada Sócio {id}')
        self.janela.protocol("WM_DELETE_WINDOW", self.__disable_x)

        obj.frame_ativo = Frame(self.janela, bd=4, bg='lightblue')
        obj.frame_ativo.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        obj.base(id)

        obj.compleEntry.place(relx=0.65,rely=0.85,relwidth=0.225,relheight=0.15)

        Button(obj.frame_ativo, text='OK',\
            command= lambda: self.__fechar_janela(obj))\
                .place(relx=0.9,rely=0.75,relwidth=0.1,relheight=0.25)
        
    def __fechar_janela(self, obj):
        self.janela.destroy()
        obj.exibir()

    def __disable_x(self):
        pass
        
#Representante
class Representante (IValidator, IFormater):
    def __init__(self, frame, ref):
        self.frame_mae = frame
        self.referencias = ref
        self.qnt = 1
        self.opcoes_disp = (1,2)

        self.cabecalho = '{{r nomeEmp }}, estabelecida na rua {{ ruaEmp }}, nº {{ numEmp }}, {{ compleEmp }}, bairro {{ bairroEmp }}, CEP {{ cepEmp }}, CNPJ {{r cnpjEmp }}, neste ato representada por ',

        self.conteudo = {
            1: [
                '{{r nomeContra1 }}, {{ nacionalidadeContra1 }}, {{ empregoContra1 }}, {{ estadoCivilContra1 }}, residente e domiciliado(a) na rua {{ ruaContra1 }}, nº {{ numContra1 }}, {{ compleContra1 }} bairro {{ bairroContra1 }} , CEP {{ cepContra1 }}, {{ cidadeContra1 }}, {{ estadoContra1 }}, portador(a) do documento de identidade sob o nº {{ rgContra1 }} {{ emissorContra1 }}, CPF {{r cpfContra1 }}',

                '''_______________________________                                                  ____________________________________
                    Deltaprice Serviços Contábeis Ltda.                                                        {{r nomeContra1 }}
                '''
                ],
            2: [
                '{{r nomeContra1 }}, brasileiro(a), empresário(a), {{ estadoCivilContra1 }}, residente e domiciliado(a) na rua {{ ruaContra1 }}, nº {{ numContra1 }}, {{ compleContra1 }} bairro {{ bairroContra1 }} , CEP {{ cepContra1 }}, {{ cidadeContra }}, {{ estadoContra1 }}, portador(a) do documento de identidade sob o nº {{ rgContra1 }} {{ emissorContra1 }}, CPF {{r cpfContra1 }} e {{r nomeContra2 }}, brasileiro(a), empresário(a), {{ estadoCivilContra2 }}, residente e domiciliado(a) na rua {{ ruaContra2 }}, nº {{ numContra2 }}, {{ compleContra2 }} bairro {{ bairroContra2 }} , CEP {{ cepContra2 }}, {{ cidadeContra2 }}, {{ estadoContra2 }}, portador(a) do documento de identidade sob o nº {{ rgContra2 }} {{ emissorContra }}, CPF {{r cpfContra2 }} denominados(a) daqui por diante de Contratante;',

                '''_______________________________                                                  ____________________________________
                    Deltaprice Serviços Contábeis Ltda.                                                        {{r nomeContra1 }}
                ''']
        }

    def get_qnt(self):
        return self.qnt

    def titulo_divisor(self, y = 0):
        #TODO repre
        Label(self.frame_mae, text='Representante',\
            background='lightblue', font=('Times New Roman',15,'bold italic'))\
                .place(relx=0.05,rely= y + 0.42)
                
        canvas = Canvas(self.frame_mae, width=555, height=10,border=-5)
        canvas.place(relx=0.23,rely= y + 0.455)
                
        canvas.create_line(-5,0,555,0, fill="darkblue", width=10)

        ###########TODO Inp-Soc
        
        Label(self.frame_mae, text='Quantidade:',\
            background='lightblue', font=('Arial',12,'bold italic'))\
                .place(relx=0.7,rely= y + 0.42)

        num_repres = IntVar(value=1)

        popup_repre = ttk.OptionMenu(self.frame_mae, num_repres,'', *self.opcoes_disp, command= lambda val: self.alterar_qnt(num_repres.get()))

        popup_repre.place(relx=0.85,rely= y + 0.42,relwidth=0.1,relheight=0.06)

    def alterar_qnt(self, quantidade):
        self.frame_ativo.destroy()
        self.qnt = quantidade
        self.exibir()

    def exibir(self):
        self.frame_ativo = Frame(self.frame_mae, bd=4, bg='lightblue')
        self.frame_ativo.place(relx=0.05,rely=0.48,relwidth=0.9,relheight=0.34)

        if self.qnt == 1:
            self.base('1')
        elif self.qnt == 2:
            self.__dois()

    def __dois(self):
        #Botão 1
        Button(self.frame_ativo, text= 'Representante 1', font=('Times',20,'bold'), command= lambda : Layout().janela(self, '1', self.frame_ativo)).place(relx=0,rely=0, relwidth=0.5,relheight=0.4)

        ###Nome
        Label(self.frame_ativo, text= 'Nome:', font=('Arial', 15, 'bold italic')).place(relx=0,rely=0.45)

        Label(self.frame_ativo, background='lightblue', text= self.referencias['nomeContra1'].get(), font=('Calibri', 12, 'italic')).place(relx=0.1,rely=0.45)

        ###CPF
        Label(self.frame_ativo, text= 'CPF:', font=('Arial', 15, 'bold italic')).place(relx=0,rely=0.75)

        Label(self.frame_ativo, background='lightblue', text= self.referencias['cpfContra1'].get(), font=('Calibri', 12, 'italic')).place(relx=0.08,rely=0.75)

        #Botão 2
        Button(self.frame_ativo, text= 'Representante 2', font=('Times',20,'bold'), command= lambda: Layout().janela(self, '2', self.frame_ativo)).place(relx=0.5,rely=0, relwidth=0.5,relheight=0.4)

        ###Nome
        Label(self.frame_ativo, text= 'Nome:', font=('Arial', 15, 'bold italic')).place(relx=0.5,rely=0.45)

        Label(self.frame_ativo, background='lightblue', text= self.referencias['nomeContra2'].get(), font=('Calibri', 12, 'italic')).place(relx=0.6,rely=0.45)

        ###CPF
        Label(self.frame_ativo, text= 'CPF:', font=('Arial', 15, 'bold italic')).place(relx=0.5,rely=0.75)

        Label(self.frame_ativo, background='lightblue', text= self.referencias['cpfContra2'].get(), font=('Calibri', 12, 'italic')).place(relx=0.58,rely=0.75)

    def base(self, id):
        self.frame_ativo.bind('<KeyRelease>', alter_estado)
    ###########nome
        Label(self.frame_ativo, text='Nome',\
            background='lightblue', font=(10))\
                .place(relx=0,rely=0)

        Entry(self.frame_ativo,\
            textvariable=self.referencias['nomeContra' + id],\
                validate='key', validatecommand=(self.frame_ativo.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0,rely=0.15,relwidth=0.25,relheight=0.15)
        
         ###########RG
        
        valRG = StringVar(value= self.referencias['rgContra' + id].get())

        valRG.trace_add('write', lambda *args, passed = valRG:\
            self.rg_formater(passed, *args) )

        Label(self.frame_ativo, text='RG',\
            background='lightblue', font=(10))\
                .place(relx=0.28,rely=0)
        

        Entry(self.frame_ativo, textvariable = valRG, \
            validate ='key', validatecommand =(self.frame_ativo.register(self.rg_validator), '%P'))\
                .place(relx=0.28,rely=0.15,relwidth=0.1,relheight=0.15)

        self.referencias['rgContra' + id] = valRG
        
        ###########Org. Emissor

        Label(self.frame_ativo, text='Org.',\
            background='lightblue', font=(10))\
                .place(relx=0.4,rely=0)

        Entry(self.frame_ativo,\
            textvariable=self.referencias['emissorContra' + id],\
                validate='key', validatecommand=(self.frame_ativo.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.4,rely=0.15,relwidth=0.05,relheight=0.15)

        ###########CPF
        
        valCPF = StringVar(value= self.referencias['cpfContra' + id].get())

        valCPF.trace_add('write', lambda *args, passed = valCPF:\
            self.cpf_formater(passed, *args) )

        Label(self.frame_ativo, text='CPF',\
            background='lightblue', font=(10))\
                .place(relx=0.47,rely=0)
        

        Entry(self.frame_ativo, textvariable = valCPF, \
            validate ='key', validatecommand =(self.frame_ativo.register(self.cpf_validator), '%P'))\
                .place(relx=0.47,rely=0.15,relwidth=0.13,relheight=0.15)

        self.referencias['cpfContra' + id] = valCPF
        
        ###########TODO Nacionalidade
        nacio_var = BooleanVar()
        ttk.Checkbutton(self.frame_ativo, text='Não é brasileiro?', variable= nacio_var, \
            command= lambda: \
                Opcionais(self.frame_ativo).exibir('Nacionalidade', self.referencias) if nacio_var.get() else self.referencias['nacionalidadeContra' + id].set('brasileiro(a)'))\
                    .place(relx=0.644,rely=0,relwidth=0.16,relheight=0.15)

        ###########Emprego
        empreg_var = BooleanVar()
        ttk.Checkbutton(self.frame_ativo, text='Não é empresário?', variable= empreg_var, \
            command= lambda:\
                Opcionais(self.frame_ativo).exibir('Emprego', self.referencias)if empreg_var.get() else self.referencias['empregoContra' + id].set('empresário(a)'))\
                    .place(relx=0.637,rely=0.18,relwidth=0.175,relheight=0.15)

        ###########Tipo
        
        Label(self.frame_ativo, text='Tipo',\
            background='lightblue', font=(10))\
                .place(relx=0.84,rely=0)

        tipoRepreEntry = StringVar(value= self.referencias['tipoRepre' + id].get())

        tipoRepreEntryOpt = ('Sócio', 'Administrador', 'Procurador')

        popup = ttk.OptionMenu(self.frame_ativo, tipoRepreEntry, *tipoRepreEntryOpt)

        popup.place(relx=0.84,rely=0.15,relwidth=0.16,relheight=0.16)

        self.referencias['tipoRepre' + id] = tipoRepreEntry

        ###########rua
        
        tipoRuaEntry = StringVar(value= self.referencias['tipoRua' + id].get())

        tipoRuaEntryOpt = ('Rua', 'Avenida', 'Logadouro')

        popup = OptionMenu(self.frame_ativo, tipoRuaEntry, *tipoRuaEntryOpt)
        popup.config(indicatoron = False, font=('Arial',10), justify='left')

        popup.place(relx=0,rely=0.35,relwidth=0.1,relheight=0.16)

        self.referencias['tipoRepre' + id] = tipoRuaEntry

        Entry(self.frame_ativo,\
            textvariable=self.referencias['ruaContra' + id],\
                validate='key', validatecommand=(self.frame_ativo.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0,rely=0.5,relwidth=0.25,relheight=0.15)

        ###########Num

        Label(self.frame_ativo, text='Num.',\
            background='lightblue', font=(10))\
                .place(relx=0.33,rely=0.35)

        Entry(self.frame_ativo,\
            textvariable=self.referencias['numContra' + id],\
                validate='key', validatecommand=(self.frame_ativo.register(lambda text: text.isdecimal()), '%S'))\
                .place(relx=0.33,rely=0.5,relwidth=0.05,relheight=0.15)

        ###########bairro

        Label(self.frame_ativo, text='Bairro',\
            background='lightblue', font=(10))\
                .place(relx=0.4,rely=0.35)

        Entry(self.frame_ativo,\
            textvariable=self.referencias['bairroContra' + id],\
                validate='key', validatecommand=(self.frame_ativo.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.4,rely=0.5,relwidth=0.2,relheight=0.15)
        
        ###########CEP 
        
        valCEP_Contra = StringVar(value= self.referencias['cepContra' + id].get())

        valCEP_Contra.trace_add('write', lambda *args, passed = valCEP_Contra:\
            self.cep_formater(passed, *args) )

        Label(self.frame_ativo, text='CEP',\
            background='lightblue', font=(10))\
                .place(relx=0.65,rely=0.35)
        

        Entry(self.frame_ativo, textvariable = valCEP_Contra, \
            validate ='key', validatecommand =(self.frame_ativo.register(self.cep_validator), '%P'))\
                .place(relx=0.65,rely=0.5,relwidth=0.075,relheight=0.15)

        self.referencias['cepContra' + id] = valCEP_Contra

        ###########Estado Civil
        
        Label(self.frame_ativo, text='Estado Civil',\
            background='lightblue', font=(10))\
                .place(relx=0.8,rely=0.35)

        estadoEntry = StringVar(value= self.referencias['estadoCivilContra' + id].get())

        estadoEntryOpt = ('solteiro(a)','divorciado(a)','viuvo(a)')

        popup = ttk.OptionMenu(self.frame_ativo, estadoEntry,'', *estadoEntryOpt)

        menuCasado = popup['menu']

        #Casado
        subLista = Menu(menuCasado, tearoff=False)
        menuCasado.add_cascade(label = 'casado(a)',menu= subLista)
        subLista.add_command(label='Comunhão Parcial de Bens', \
            command= lambda: estadoEntry.set('casado(a) em CPB'))
        
        subLista.add_command(label='Comunhão Universal de Bens',\
            command= lambda: estadoEntry.set('casado(a) em CUB'))
        
        subLista.add_command(label='Separação Total de Bens',\
            command= lambda: estadoEntry.set('casado(a) em STB'))


        popup.place(relx=0.8,rely=0.5,relwidth=0.2,relheight=0.16)

        self.referencias['estadoCivilContra' + id] = estadoEntry
        
        ###########Cidade

        Label(self.frame_ativo, text='Cidade',\
            background='lightblue', font=(10))\
                .place(relx=0,rely=0.7)

        Entry(self.frame_ativo,\
            textvariable=self.referencias['cidadeContra' + id],\
                validate='key', validatecommand=(self.frame_ativo.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0,rely=0.85,relwidth=0.25,relheight=0.15)
        
        ###########Estado

        Label(self.frame_ativo, text='Estado',\
            background='lightblue', font=(10))\
                .place(relx=0.33,rely=0.7)

        Entry(self.frame_ativo,\
            textvariable=self.referencias['estadoContra' + id],\
                validate='key', validatecommand=(self.frame_ativo.register(lambda text: not text.isdecimal()), '%S'))\
                .place(relx=0.33,rely=0.85,relwidth=0.25,relheight=0.15)

        ###########Complemento

        Label(self.frame_ativo, text='Complemento (opcional)',\
            background='lightblue', font=(10))\
                .place(relx=0.65,rely=0.7)

        self.compleEntry = Entry(self.frame_ativo,\
            textvariable=self.referencias['compleContra' + id])
        self.compleEntry.place(relx=0.65,rely=0.85,relwidth=0.35,relheight=0.15)

    def conteudo_base(self):
        return {
            'cabecalho_emp' : self.cabecalho[0],
            'honorarios' : self.conteudo[self.qnt][0],
            'assinatura' : self.conteudo[self.qnt][1]
        }

class IPages(metaclass=ABCMeta):
    @abstractmethod
    def index(self):
        pass

class IFisica(IPages):
    def index(self):
        self.cabecalho(0.08)
        self.repre.titulo_divisor()
        self.repre.exibir()
        self.contrato(True)

class IJuridica(IPages):
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
            self.cep_formater(passed, *args) )

        Label(self.frame, text='CEP',\
            background='lightblue', font=(10))\
                .place(relx=0.05,rely=0.31)
        

        self.CEPEntry = Entry(self.frame, textvariable = self.valCEP_Empre, \
            validate ='key', validatecommand =(self.frame.register(self.cep_validator), '%P'))\
                .place(relx=0.05,rely=0.36,relwidth=0.075,relheight=0.05)

        self.referencias['cepEmp'] = self.valCEP_Empre

        ########### CNPJ
        
        self.valCNPJ = StringVar()

        self.valCNPJ.trace_add('write', lambda *args, passed = self.valCNPJ:\
            self.cnpj_formater(passed, *args) )

        Label(self.frame, text='CNPJ',\
            background='lightblue', font=(10))\
                .place(relx=0.35,rely=0.31)
        

        Entry(self.frame, textvariable = self.valCNPJ, \
            validate ='key', validatecommand =(self.frame.register(self.cnpj_validator), '%P'))\
                .place(relx=0.35,rely=0.36,relwidth=0.135,relheight=0.05)

        self.referencias['cnpjEmp'] = self.valCNPJ
                
        ###########Complemento

        Label(self.frame, text='Complemento (opcional)',\
            background='lightblue', font=(10))\
                .place(relx=0.6,rely=0.31)

        self.complementoEntry = Entry(self.frame,\
            textvariable=self.referencias['compleEmp'])\
                .place(relx=0.61,rely=0.36,relwidth=0.35,relheight=0.05)

        self.repre.titulo_divisor()
        self.repre.exibir()

        self.contrato()

class ILucroPresumido(IPages):
    def index(self):
        IJuridica.index(self)

        ###########Valor EFD
        
        self.valCompe = StringVar()

        self.valCompe.trace_add('write', lambda *args, passed = self.valCompe:\
            self.valor_formater(passed, *args) )

        Label(self.frame, text='Val. EFD-Compe.',\
            background='lightblue', font=(10))\
                .place(relx=0.62,rely=0.88)
        
        Entry(self.frame, textvariable = self.valCompe, \
            validate ='key', validatecommand =(self.frame.register(self.valor_validator), '%P'))\
                .place(relx=0.65,rely=0.93,relwidth=0.1,relheight=0.05)
                
        self.referencias['valCompe'] = self.valCompe

        #btn Enviar
        self.btnEnviar.place(relx=0.8,rely=0.86,relwidth=0.15,relheight=0.12)


class Form (IValidator, IFormater):
    def __init__(self, titulo, tipo = IPages):
        self.frame = Frame(window, bd=4, bg='lightblue')
        self.frame.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)
        self.MIN_REPRE = 1
        self.MAX_REPRE = 3

        self.tipo = tipo

        #TODO Referencias
        self.referencias = {}

        valores_ref = [
            'valorPagamento', 'dataInicio', 'dataAssinatura', 'diaVencimento'
            ] 
        
        self.itens_juri = ['numeroRuaEmp','nomeEmp', 'ruaEmp', 'numEmp', 'bairroEmp','cepEmp', 'cnpjEmp','compleEmp','valCompe']

        self.itens_repre = [
            'nomeContra',
            'rgContra',  
            'emissorContra', 
            'cpfContra', 
            'estadoCivilContra',
            'nacionalidadeContra', 
            'empregoContra',
            'tipoRua',
            'tipoRepre',
            'ruaContra', 
            'numContra', 
            'bairroContra',  
            'cepContra',  
            'cidadeContra', 
            'estadoContra', 
            'compleContra'
            ]
        
        values_padroes = {
            'tipoRua': 'Rua',
            'tipoRepre': 'Sócio'
        }

        nacio_emp_padrao = {
            'nacionalidadeContra': 'brasileiro(a)',
            'empregoContra': 'empresário(a)'
        }
        
        for i in valores_ref + self.itens_juri:
            self.referencias[i] = StringVar() 
        
        for index in range(1, 3):
            for i in self.itens_repre:
                self.referencias[i + str(index)] = StringVar()

        for index in range(1, 3):
            for nome, valor in nacio_emp_padrao.items():
                self.referencias[nome + str(index)].set(valor)

        for index in range(1, 3):
            for key, valor in values_padroes.items():
                self.referencias[key + str(index)].set(valor)

        self.titulo = titulo
        self.file = File(titulo)
        self.repre = Representante(frame = self.frame, ref=self.referencias)

    def exibir_page(self):
        self.tipo.index(self)

    def executar(self, fisi):
            #TODO EXECUTAR
        try:
            IValido().validar(self.filtro(fisi))

            conteudo_base = self.repre.conteudo_base()

            conteudo_updt = Content(self.referencias).update_dict(self.repre.get_qnt())

            self.file.salvar()
            self.file.alterar(conteudo_base, conteudo_updt)
            self.file.abrir()

        except decimal.InvalidOperation:
            messagebox.showwarning(title='Aviso', message= 'Insira um número válido')
        except ValueError:
            messagebox.showwarning(title='Aviso', message= 'Insira datas válidas')
        except Exception as e:
            messagebox.showwarning(title='Aviso', message= e)

    def filtro(self, fisi):
        ref_temp = {chave: copy.deepcopy(valor.get()) for chave, valor in self.referencias.items()}

        ref_temp.pop('compleEmp')

        if fisi == True:
            for i in self.itens_juri:
                ref_temp.pop(i,None)

        for i in range(1, self.repre.get_qnt() +1):
            ref_temp.pop('emissorContra' + str(i))
            ref_temp.pop('compleContra' + str(i))
            if ref_temp['nacionalidadeContra' + str(i)] != 'brasileiro(a)':
                ref_temp.pop('rgContra' + str(i))

        for i in range(self.repre.get_qnt() + 1, 4):
            for j in self.itens_repre:
                ref_temp.pop(j + str(i),None)

        return ref_temp

    def cabecalho(self, y = 0):
        #Titulo
        Label(self.frame, text= self.titulo, background='lightblue',\
            font=('Times',30,'bold'))\
                .place(relx=0.325,rely= y + 0.05)
        
        #Logo
        self.logo = PhotoImage(file=resource_path('imgs\\cps_logo.png'))
        
        self.logo = self.logo.subsample(5,5)
        
        Label(self.frame, image=self.logo, background='lightblue')\
            .place(relx=0.75,rely= y + 0.01,relwidth=0.12,relheight=0.15)
        
        #Botão voltar
        Button(self.frame, text='Voltar ao menu',\
            command= lambda: self.frame.destroy())\
                .place(relx=0,rely= 0,relwidth=0.25,relheight=0.06)
        
    def contrato(self, fisi = False):
        #Contrato
        Label(self.frame, text='Contrato',\
            background='lightblue', font=('Times New Roman',15,'bold italic'))\
                .place(relx=0.05,rely=0.82)
                
        self.canvas = Canvas(self.frame, width=625, height=10,border=-5)
        self.canvas.place(relx=0.17,rely=0.845)
                
        self.canvas.create_line(-5,0,625,0, fill="darkblue", width=10)
        
        # x,angulo x , y, angulo y

        ###########Valor pagamento
        self.valorPagamento = StringVar()
        self.valorPagamento.trace_add('write', lambda *args, passed = self.valorPagamento:\
            self.valor_formater(passed, *args) )
        Label(self.frame, text='Val. Contrato.',\
            background='lightblue', font=(10))\
                .place(relx=0.05,rely=0.88)
        
        Entry(self.frame, textvariable = self.valorPagamento, \
            validate ='key', validatecommand =(self.frame.register(self.valor_validator), '%P'))\
                .place(relx=0.06,rely=0.93,relwidth=0.1,relheight=0.05)
                
        self.referencias['valorPagamento'] = self.valorPagamento

        ###########Data inicio
        self.valDT_inic = StringVar()
        self.valDT_inic.trace_add('write', lambda *args, passed = self.valDT_inic:\
            self.date_formater(passed, *args) )
        Label(self.frame, text='Data início',\
            background='lightblue', font=(10))\
                .place(relx=0.182,rely=0.88)
        
        Entry(self.frame, textvariable = self.valDT_inic, \
            validate ='key', validatecommand =(self.frame.register(self.date_validator), '%P')).place(relx=0.185,rely=0.93,relwidth=0.08,relheight=0.05)
        self.referencias['dataInicio'] = self.valDT_inic

        ###########Data Assinatura
        self.valDT_ass = StringVar()
        self.valDT_ass.trace_add('write', lambda *args, passed = self.valDT_ass:\
            self.date_formater(passed, *args) )
        Label(self.frame, text='Data Ass.',\
            background='lightblue', font=(10))\
                .place(relx=0.3,rely=0.88)
        
        Entry(self.frame, textvariable = self.valDT_ass, \
            validate ='key', validatecommand =(self.frame.register(self.date_validator), '%P')).place(relx=0.3,rely=0.93,relwidth=0.08,relheight=0.05)
        self.referencias['dataAssinatura'] = self.valDT_ass

        ###########Dia vencimento
        Label(self.frame, text='Dia Venc.',\
            background='lightblue', font=(10))\
                .place(relx=0.4,rely=0.88)
        
        Entry(self.frame,textvariable=self.referencias['diaVencimento'], validate='key', validatecommand=(self.frame.register(lambda text: text.isdecimal() if len(text) < 3 else False), '%P')).place(relx=0.435,rely=0.93,relwidth=0.02,relheight=0.05)

        ###########Num. Empregados
        Label(self.frame, text='Num.Empre.',\
            background='lightblue', font=(10))\
                .place(relx=0.5,rely=0.88)
        Entry(self.frame,\
            textvariable=self.referencias['numeroRuaEmp'],\
                validate='key', validatecommand=(self.frame.register(lambda text: text.isdecimal()), '%S'))\
                .place(relx=0.535,rely=0.93,relwidth=0.05,relheight=0.05)
        
        #Botão enviar
        self.btnEnviar = Button(self.frame, text='Gerar CPS',\
            command= lambda: self.executar(fisi))
        self.btnEnviar.place(relx=0.7,rely=0.86,relwidth=0.25,relheight=0.12)

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
        self.window.iconbitmap(resource_path('imgs\\cps-icon.ico'))
        self.window.title('Gerador de CPS')

    def menu(self):
        self.menu = Frame(self.window, bd=4, bg='lightblue')
        self.menu.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        self.textOrientacao = Label(self.menu, text='Selecione o tipo de CPS que deseja fazer:', background='lightblue', font=('arial',20,'bold'))\
        .place(relx=0.15,rely=0.3,relheight=0.15)
        
        #Logo
        self.logo = PhotoImage(file=resource_path('imgs\\cps_horizontal.png')).subsample(2,2)
        
        Label(self.menu, image=self.logo, background='lightblue')\
            .place(relx=0.135,rely=0.05)

        #Pessoa física
        Button(self.menu, text='CPS Pessoa Física',\
            command= lambda: Form('Pessoa Física', IFisica).exibir_page())\
                .place(relx=0.15,rely=0.75,relwidth=0.25,relheight=0.15)

        #Inatividade
        Button(self.menu, text='CPS Inatividade',\
            command= lambda: Form('Inatividade', IJuridica).exibir_page())\
                .place(relx=0.60,rely=0.5,relwidth=0.25,relheight=0.15)

        #Lucro Presumido
        Button(self.menu, text='CPS Lucro Presumido / Real',\
            command= lambda: Form('Lucros', ILucroPresumido).exibir_page())\
                .place(relx=0.15,rely=0.5,relwidth=0.25,relheight=0.15)

        #Simples Nacional
        Button(self.menu, text='CPS Simples Nacional',\
            command= lambda: Form('Simples Nacional',IJuridica).exibir_page())\
                .place(relx=0.60,rely=0.75,relwidth=0.25,relheight=0.15)

App()