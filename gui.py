import tkinter as tk
from tkinter import filedialog
import PyPDF2
import pdfplumber
import re



informacoes_usuario = []


def is_monetary_format(s):
    # Verifica se a string está no formato monetário brasileiro
    return bool(re.match(r'^\d{1,3}(\.\d{3})*,\d{2}$', s))

def safe_convert_to_float(s):
    if(is_monetary_format(s)):

        try:
            #s = re.sub(r'[^\d,]', '', s)
            s = s.replace('.','')
            s = s.replace(',','.')

            return float(s)
        except ValueError:
            return None
    else:
        return None

def extrair_informacoes_boleto(filename):
    with pdfplumber.open(filename) as pdf:
        primeira_pagina = pdf.pages[0]
        text = primeira_pagina.extract_words()

        
        
        i = 0
        
        for conteudo in text:
            i+=1

            
            if conteudo['text'] == 'Valor' and text[i]['text'] == 'do' and text[i+1]['text'] == 'Documento' :
                while safe_convert_to_float(text[i+2]['text']) == None:
                    i+=1
                valor = text[i+2]['text']
                    
            #print(conteudo['text'])

        informacoes_usuario.append(
            {
                #'nome': nome,
                'valor': valor
            }
        )  

        for boleto in informacoes_usuario:
            print('valor: ' + boleto['valor'])
        

        
        return text
    
def importar_boleto():
    filename = filedialog.askopenfilename(initialdir="/", title="Selecione o boleto", filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
    if filename:
        print('Arquivo importado: ' + filename)
        
        extrair_informacoes_boleto(filename)

        
        return filename

janela = tk.Tk()
janela.geometry('700x700')

label = tk.Label(janela, text='Insira um boleto para importar')
label.pack()

botao_importar_boleto = tk.Button(janela, text="Importar boleto", command=importar_boleto)
botao_importar_boleto.pack()


janela.mainloop()
 