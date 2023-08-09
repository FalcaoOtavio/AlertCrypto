import telebot
from telebot import TeleBot
import requests
from bs4 import BeautifulSoup
import schedule
import time
from telebot import types

while True:
    try:

        chave_api = '6138948203:AAGll3mwxTcfm5HLyJXQOiMOcCm4TXN0Ios'

        bot = telebot.TeleBot(chave_api)

        print('BOT INICIADO')


        # CRIANDO MENU PRINCIPAL
        @bot.message_handler(commands=['start', 'help'])
        def menu_principal(mensagem):
            
            menu_principal_Keyboard = types.InlineKeyboardMarkup(row_width=2)
            bitcoin_keyboard = types.InlineKeyboardButton('BITCOIN', callback_data='bitcoin')
            etehereum_keyboard = types.InlineKeyboardButton('ETHEREUM', callback_data='ethereum')
            binance_keyboard = types.InlineKeyboardButton('BINANCE COIN', callback_data='binance')
            ripple_keyboard = types.InlineKeyboardButton('RIPPLE', callback_data='ripple')
            parar_alerta = types.InlineKeyboardButton('Parar alerta', callback_data='Parar_alerta')
            menu_principal_Keyboard.add(bitcoin_keyboard, etehereum_keyboard, binance_keyboard, ripple_keyboard, parar_alerta)


            texto = 'Bem vindo ao Alert Crypto! Escolha a opção que deseja: '
            bot.send_message(mensagem.chat.id, texto, reply_markup=menu_principal_Keyboard)



        #-------------------------------------------------------- BITCOIN ----------------------------------------------------------


        # CRIANDO MENU BITCOIN
        @bot.callback_query_handler(func=lambda call: call.data == 'bitcoin')
        def menu_bitcoin(callback_query):

            menu_bitcoin_keyboard = types.InlineKeyboardMarkup(row_width=2)
            valor_bitcoin = types.InlineKeyboardButton('Valor atualizado', callback_data='Valor_atualizado_btc')
            criar_alerta = types.InlineKeyboardButton('Criar alerta', callback_data='Criar_alerta_btc')
            menu_bitcoin_keyboard.add(valor_bitcoin, criar_alerta)
            texto = '''
            BITCOIN
            
        Escolha a opção que deseja :
            
        (caso escolha valor atualizado, a resposta poderá demorar alguns segundos)
            '''
            bot.send_message(callback_query.message.chat.id, texto, reply_markup=menu_bitcoin_keyboard)


        # VALOR BITCOIN -- USADA QUANDO SELECIONADA VALOR_ATUALIZADO
        @bot.callback_query_handler(func=lambda call: call.data == 'Valor_atualizado_btc')
        def bitcoin(callback_query):
            response = requests.get('https://www.google.com/finance/quote/BTC-BRL')
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            preco = site.find('div', attrs={'class': 'YMlKec fxKbKc'})
            variacao = site.find('div', attrs={'class': 'JwB6zf'})
            texto = f'O valor atualizado da Bitcoin é de R${preco.text}\nA variação do preço da BTC é de {variacao.text}'
            bot.send_message(callback_query.message.chat.id, texto)
            

        # VALOR BITCOIN -- USADA PARA OS ALERTAS
        def bitcoin_alerta(message):
            response = requests.get('https://www.google.com/finance/quote/BTC-BRL?sa=X&ved=2ahUKEwj3__mvg53-AhWVu5UCHf6EAFwQ-fUHegQIBhAf')
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            valor = site.find('div', attrs={'class': 'YMlKec fxKbKc'})
            texto = f'O valor atualizado do bitcoin é de R${valor.text}'
            bot.send_message(message.chat.id, texto)


        # CRIAR ALERTA 
        @bot.callback_query_handler(func= lambda call: call.data == 'Criar_alerta_btc')
        def menu_alerta_btc(callback_query):
            menu_alerta_keyboard= types.InlineKeyboardMarkup(row_width=1)
            minutos_Keyboard = types.InlineKeyboardButton('MINUTOS', callback_data='minutos_btc')
            horas_Keyboard = types.InlineKeyboardButton('HORAS', callback_data='horas_btc')
            dias_Keyboard = types.InlineKeyboardButton('DIAS', callback_data='dias_btc')
            menu_alerta_keyboard.add(minutos_Keyboard, horas_Keyboard, dias_Keyboard)

            texto = '''
            BITCOIN
            
        Escolha a opção que deseja ser o intervalo de tempo: '''

            bot.send_message(callback_query.message.chat.id, texto, reply_markup=menu_alerta_keyboard)
            

        # ESCOLHA INTERVALO MINUTOS
        @bot.callback_query_handler(func= lambda call: call.data == 'minutos_btc')
        def minutos_btc(callback_query):
            bot.send_message(callback_query.message.chat.id, 'Digite um número de 1 a 59 (minutos) que você deseja ser o intervalo de tempo: ')
            bot.register_next_step_handler(callback_query.message, check_minutes_btc)

        # ANALISE DAS MENSAGEM  E AGENDAMENTO DA TAREFA -- MINUTOS
        def check_minutes_btc(message):
            if message.text in [str(x) for x in range(1, 60)]:
                min = int(message.text)
                bot.send_message(message.chat.id, f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {min} minutos.')
            
                schedule.every(min).minutes.do(bitcoin_alerta, message) 
                i = 0
                while True:
                    i += 1
                    print(i)
                    schedule.run_pending()
                    time.sleep(1)
            else:
                return False


        # ESCOLHA INTERVALO HORAS 
        @bot.callback_query_handler(func=lambda call: call.data == 'horas_btc')
        def horas_btc(callback_query):
            bot.send_message(callback_query.message.chat.id, 'Digite um número de 1 a 20 (horas) que você deseja ser o intervalo de tempo: ')
            bot.register_next_step_handler(callback_query.message, check_hours_btc)
            
            
        # ANALISE DAS MENSAGEM RECEBIDAS HORAS
        def check_hours_btc(message):
            if message.text in [str(x) for x in range(1, 60)]:
                hours = int(message.text)
                bot.send_message(message.chat.id, f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {hours} horas.')
            
                schedule.every(hours).hours.do(bitcoin_alerta, message)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            else:
                return False
            

        # ESCOLHA INTERVALO -- DIAS 
        @bot.callback_query_handler(func=lambda call: call.data == 'dias_btc')
        def dias_btc(callback_query):
            texto = '''
            Digite um número de 1 a 6 (dias) que você deseja ser o intervalo:

            Ou digite um dia da semana que deseja receber os alertas ( exemplo: segunda, terça; não é necessario escrever -feira, porém digite corretamente) :
            '''
            bot.send_message(callback_query.message.chat.id, texto)
            bot.register_next_step_handler(callback_query.message, check_days_btc)

        # ANALISE DAS MENSAGEMN RECEBIDAS -- DIAS
        def check_days_btc(message):
            lista = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'sabado', 'domingo']
            dias = message.text
            if dias in [str(x) for x in range(1, 7)] or dias.lower() in lista:
                
                if message.text in [str(x) for x in range(1, 7)]:
                    days = int(message.text)
                    texto1 = f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {days} dias.'
                    bot.send_message(message.chat.id, texto1)

                    schedule.every(days).days.do(bitcoin_alerta, message)
                    while True:
                        schedule.run_pending()
                        time.sleep(1)
            
                elif message.text in lista:
                    dias = message.text
                    texto2 = f'Seu alerta foi criado com sucesso !!! A partir de agora, todo(a) {dias} você receberá alertas'
                    
                    if dias.lower() == 'segunda':
                        print('segunda')
                        schedule.every().monday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                    
                    elif dias.lower() == 'terça':
                        print('terça')
                        schedule.every().tuesday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'quarta':
                        print('quarta')
                        schedule.every().wednesday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'quinta':
                        print('quinta')
                        schedule.every().thursday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'sexta':
                        print('sexta')
                        schedule.every().friday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'sábado' or dias == 'sabado':
                        print('sábado')
                        schedule.every().saturday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.Trun_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'domingo':
                        print('domingo')
                        schedule.every().sunday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
            else:
                return False
            


        # ----------------------------------------------------- ETHEREUM ------------------------------------------------------

        #MENU ETHEREUM 
        @bot.callback_query_handler(func=lambda call: call.data == 'ethereum')
        def menu_eth(callback_query):
            menu_ethereum_keyboard = types.InlineKeyboardMarkup(row_width=2)
            valor_ethereum = types.InlineKeyboardButton('Valor atualizado', callback_data='Valor_atualizado_eth')
            criar_alerta = types.InlineKeyboardButton('Criar alerta', callback_data='Criar_alerta_eth')
            menu_ethereum_keyboard.add(valor_ethereum,  criar_alerta)
            texto = '''
            ETHEREUM
            
        Escolha a opção que deseja :
            
        (caso escolha valor atualizado, a resposta poderá demorar alguns segundos)

        '''
            bot.send_message(callback_query.message.chat.id, texto, reply_markup= menu_ethereum_keyboard)


        # VALOR ETHEREUM -- USADO NO BOTÃO VALOR ATUALIZADO
        @bot.callback_query_handler(func=lambda call: call.data == 'Valor_atualizado_eth')
        def ethereum(callback_query):
            response = requests.get('https://www.google.com/finance/quote/ETH-BRL')
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            preco = site.find('div', attrs={'class': 'YMlKec fxKbKc'})
            variacao = site.find('div', attrs={'class': 'JwB6zf'})
            texto = f'O valor atualizado do Ether é de R${preco.text}\nA variação do preço da ETH é de {variacao.text}'
            bot.send_message(callback_query.message.chat.id, texto)

        # VALOR ETHEREUM -- USADO NO AGENDAMENTO DE TAREFAS
        def valor_ethereum(message):
            response = requests.get('https://www.google.com/finance/quote/ETH-BRL')
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            preco = site.find('div', attrs={'class': 'YMlKec fxKbKc'})
            texto = f'O valor atualizado da Ethereum é de R${preco.text}'
            bot.send_message(message.chat.id, texto)


        # CRIAR ALERTAS
        @bot.callback_query_handler(func=lambda call: call.data == 'Criar_alerta_eth')
        def menu_alerta_eth(callback_query):
            menu_alerta_keyboard= types.InlineKeyboardMarkup(row_width=1)
            minutos_Keyboard = types.InlineKeyboardButton('MINUTOS', callback_data='minutos_eth')
            horas_Keyboard = types.InlineKeyboardButton('HORAS', callback_data='horas_eth')
            dias_Keyboard = types.InlineKeyboardButton('DIAS', callback_data='dias_eth')
            menu_alerta_keyboard.add(minutos_Keyboard, horas_Keyboard, dias_Keyboard)
            texto = '''
            ETHEREUM
            
        Escolha a opção que deseja ser o intervalo de tempo :
            '''
            bot.send_message(callback_query.message.chat.id, texto, reply_markup= menu_alerta_keyboard)


        # ESCOLHA INTERVALO MINUTOS
        @bot.callback_query_handler(func=lambda call: call.data == 'minutos_eth')
        def minutos_eth(callback_query):
            bot.send_message(callback_query.message.chat.id, 'Digite um número de 1 a 59 (minutos) que você deseja ser o intervalo de tempo: ')
            bot.register_next_step_handler(callback_query.message, check_minutes_eth)

        # ANALISE DA MENSAGEM E AGENDAMENTO DA TAREFA -- MINUTOS
        def check_minutes_eth(message):
            if message.text in [str(x) for x in range(1, 60)]:
                min = int(message.text)
                bot.send_message(message.chat.id, f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {min} minutos.')

                schedule.every(min).minutes.do(valor_ethereum, message)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            else:
                return False


        # ESCOLHA INTERVALO HORAS
        @bot.callback_query_handler(func=lambda call: call.data == 'horas_eth')
        def horas_eth(callback_query):
            bot.send_message(callback_query.message.chat.id, 'Digite um número de 1 a 20 (horas) que você deseja ser o intervalo de tempo: ')
            bot.register_next_step_handler(callback_query.message, check_hours_eth)

        # ANALISE DA MENSAGEM E AGENDAMENTO DA TAREFA
        def check_hours_eth(message):
            if message.text in [str(x)for x in range(1, 60)]:
                hours = int(message.text)
                bot.send_message(message.chat.id, f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {hours} horas.')

                schedule.every(hours).hours.do(valor_ethereum, message)
                i = 0
                while True:
                    i += 1
                    print(i)
                    schedule.run_pending()
                    time.sleep(1)
            else:
                return False
            

        # ESCOLHA INTERVALO DIAS
        @bot.callback_query_handler(func=lambda call: call.data == 'dias_eth')
        def dias_eth(callback_query):
            texto = ''' BITCOIN

            Digite um número de 1 a 6 (dias) que você deseja ser o intervalo de tempo:

            Ou digite um dia da semana que deseja receber os alertas ( exemplo: segunda, terça; não é necessario escrever -feira, porém digite corretamente) :
            ''' 
            bot.send_message(callback_query.message.chat.id, texto)
            bot.register_next_step_handler(callback_query.message, check_days_eth)


        # ANALISANDO E AGENDANDO A TAREFA 
        def check_days_eth(message):
            lista = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'sabado', 'domingo']
            dias = message.text
            if dias in [str(x) for x in range(1, 7)] or dias.lower() in lista:
                
                if message.text in [str(x) for x in range(1, 7)]:
                    days = int(message.text)
                    texto1 = f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {days} dias.'
                    bot.send_message(message.chat.id, texto1)

                    schedule.every(days).days.do(bitcoin_alerta, message)
                    while True:
                        schedule.run_pending()
                        time.sleep(1)
            
                elif message.text in lista:
                    dias = message.text
                    texto2 = f'Seu alerta foi criado com sucesso !!! A partir de agora, todo(a) {dias} você receberá alertas'
                    
                    if dias.lower() == 'segunda':
                        print('segunda')
                        schedule.every().monday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                    
                    elif dias.lower() == 'terça':
                        print('terça')
                        schedule.every().tuesday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'quarta':
                        print('quarta')
                        schedule.every().wednesday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'quinta':
                        print('quinta')
                        schedule.every().thursday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'sexta':
                        print('sexta')
                        schedule.every().friday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'sábado' or dias == 'sabado':
                        print('sábado')
                        schedule.every().saturday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.Trun_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'domingo':
                        print('domingo')
                        schedule.every().sunday.at('08:00').do(bitcoin_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
            else:
                return False





        #-------------------------------------------------------- BNB ----------------------------------------------------------


        # CRIANDO MENU BNB
        @bot.callback_query_handler(func=lambda call: call.data == 'binance')
        def menu_binance(callback_query):

            menu_binance_keyboard = types.InlineKeyboardMarkup(row_width=2)
            valor_binance = types.InlineKeyboardButton('Valor atualizado', callback_data='Valor_atualizado_bnb')
            criar_alerta = types.InlineKeyboardButton('Criar alerta', callback_data='Criar_alerta_bnb')
            menu_binance_keyboard.add(valor_binance, criar_alerta)
            texto = '''
            Binance Coin (BNB)
            
        Escolha a opção que deseja :
            
        (caso escolha valor atualizado, a resposta poderá demorar alguns segundos)
            '''
            bot.send_message(callback_query.message.chat.id, texto, reply_markup=menu_binance_keyboard)


        # VALOR BINANCE -- USADA QUANDO SELECIONADA VALOR_ATUALIZADO
        @bot.callback_query_handler(func=lambda call: call.data == 'Valor_atualizado_bnb')
        def binance(callback_query):
            response = requests.get('https://www.google.com/finance/quote/BNB-BRL?hl=pt')
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            preco = site.find('div', attrs={'class': 'YMlKec fxKbKc'})
            variacao = site.find('div', attrs={'class': 'JwB6zf'})
            texto = f'O valor atualizado da Bincance Coin é de R${preco.text} \nA variação da BNB é de {variacao.text}'
            bot.send_message(callback_query.message.chat.id, texto)

        # VALOR BINANCE -- USADA PARA OS ALERTAS
        def binance_alerta(message):
            response = requests.get('https://www.google.com/finance/quote/BNB-BRL?hl=pt')
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            preco = site.find('div', attrs={'class': 'YMlKec fxKbKc'})
            variacao = site.find('div', attrs={'class': 'JwB6zf'})
            texto = f'O valor atualizado da Bincance Coin é de R${preco.text} \nA variação da BNB é de {variacao.text}'
            bot.send_message(message.chat.id, texto)


        # CRIAR ALERTA 
        @bot.callback_query_handler(func= lambda call: call.data == 'Criar_alerta_bnb')
        def menu_alerta_bnb(callback_query):
            menu_alerta_keyboard= types.InlineKeyboardMarkup(row_width=1)
            minutos_Keyboard = types.InlineKeyboardButton('MINUTOS', callback_data='minutos_bnb')
            horas_Keyboard = types.InlineKeyboardButton('HORAS', callback_data='horas_bnb')
            dias_Keyboard = types.InlineKeyboardButton('DIAS', callback_data='dias_bnb')
            menu_alerta_keyboard.add(minutos_Keyboard, horas_Keyboard, dias_Keyboard)

            texto = '''
            Binance Coin (BNB)
            
        Escolha a opção que deseja ser o intervalo de tempo: '''

            bot.send_message(callback_query.message.chat.id, texto, reply_markup=menu_alerta_keyboard)
            

        # ESCOLHA INTERVALO MINUTOS
        @bot.callback_query_handler(func= lambda call: call.data == 'minutos_bnb')
        def minutos_bnb(callback_query):
            bot.send_message(callback_query.message.chat.id, 'Digite um número de 1 a 59 (minutos) que você deseja ser o intervalo de tempo: ')
            bot.register_next_step_handler(callback_query.message, check_minutes_bnb)

        # ANALISE DAS MENSAGEM  E AGENDAMENTO DA TAREFA -- MINUTOS
        def check_minutes_bnb(message):
            if message.text in [str(x) for x in range(1, 60)]:
                min = int(message.text)
                bot.send_message(message.chat.id, f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {min} minutos.')
            
                schedule.every(min).minutes.do(binance_alerta, message) 
                i = 0
                while True:
                    i += 1
                    print(i)
                    schedule.run_pending()
                    time.sleep(1)
            else:
                return False


        # ESCOLHA INTERVALO HORAS 
        @bot.callback_query_handler(func=lambda call: call.data == 'horas_bnb')
        def horas_bnb(callback_query):
            bot.send_message(callback_query.message.chat.id, 'Digite um número de 1 a 20 (horas) que você deseja ser o intervalo de tempo: ')
            bot.register_next_step_handler(callback_query.message, check_hours_bnb)
            
            
        # ANALISE DAS MENSAGEM RECEBIDAS HORAS
        def check_hours_bnb(message):
            if message.text in [str(x) for x in range(1, 60)]:
                hours = int(message.text)
                bot.send_message(message.chat.id, f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {hours} horas.')
            
                schedule.every(hours).hours.do(binance_alerta, message)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            else:
                return False
            

        # ESCOLHA INTERVALO -- DIAS 
        @bot.callback_query_handler(func=lambda call: call.data == 'dias_bnb')
        def dias_bnb(callback_query):
            texto = '''
            Digite um número de 1 a 6 (dias) que você deseja ser o intervalo:

            Ou digite um dia da semana que deseja receber os alertas ( exemplo: segunda, terça; não é necessario escrever -feira, porém digite corretamente) :
            '''
            bot.send_message(callback_query.message.chat.id, texto)
            bot.register_next_step_handler(callback_query.message, check_days_bnb)

        # ANALISE DAS MENSAGEMN RECEBIDAS -- DIAS
        def check_days_bnb(message):
            lista = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'sabado', 'domingo']
            dias = message.text
            if dias in [str(x) for x in range(1, 7)] or dias.lower() in lista:
                
                if message.text in [str(x) for x in range(1, 7)]:
                    days = int(message.text)
                    texto1 = f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {days} dias.'
                    bot.send_message(message.chat.id, texto1)

                    schedule.every(days).days.do(binance_alerta, message)
                    while True:
                        schedule.run_pending()
                        time.sleep(1)
            
                elif message.text in lista:
                    dias = message.text
                    texto2 = f'Seu alerta foi criado com sucesso !!! A partir de agora, todo(a) {dias} você receberá alertas'
                    
                    if dias.lower() == 'segunda':
                        print('segunda')
                        schedule.every().monday.at('08:00').do(binance_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                    
                    elif dias.lower() == 'terça':
                        print('terça')
                        schedule.every().tuesday.at('08:00').do(binance_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'quarta':
                        print('quarta')
                        schedule.every().wednesday.at('08:00').do(binance_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'quinta':
                        print('quinta')
                        schedule.every().thursday.at('08:00').do(binance_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'sexta':
                        print('sexta')
                        schedule.every().friday.at('08:00').do(binance_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'sábado' or dias == 'sabado':
                        print('sábado')
                        schedule.every().saturday.at('08:00').do(binance_alerta, message)
                        while True:
                            schedule.Trun_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'domingo':
                        print('domingo')
                        schedule.every().sunday.at('08:00').do(binance_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
            else:
                return False





        # BOTÃO DE PARADA DOS ALERTAS
        @bot.callback_query_handler(func=lambda call: call.data == 'Parar_alerta')
        def parar(callback_query):
            for job in schedule.jobs:
                schedule.cancel_job(job)

            bot.send_message(callback_query.message.chat.id, 'Alerta cancelado')



        #-------------------------------------------------------- XRP ----------------------------------------------------------


        # CRIANDO MENU XRP
        @bot.callback_query_handler(func=lambda call: call.data == 'ripple')
        def menu_ripple(callback_query):

            menu_ripple_keyboard = types.InlineKeyboardMarkup(row_width=2)
            valor_ripple = types.InlineKeyboardButton('Valor atualizado', callback_data='Valor_atualizado_xrp')
            criar_alerta = types.InlineKeyboardButton('Criar alerta', callback_data='Criar_alerta_xrp')
            menu_ripple_keyboard.add(valor_ripple, criar_alerta)
            texto = '''
            Ripple (XRP)
            
        Escolha a opção que deseja :
            
        (caso escolha valor atualizado, a resposta poderá demorar alguns segundos)
            '''
            bot.send_message(callback_query.message.chat.id, texto, reply_markup=menu_ripple_keyboard)


        # VALOR XRP -- USADA QUANDO SELECIONADA VALOR_ATUALIZADO
        @bot.callback_query_handler(func=lambda call: call.data == 'Valor_atualizado_xrp')
        def ripple(callback_query):
            response = requests.get('https://www.google.com/finance/quote/XRP-BRL?hl=pt')
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            preco = site.find('div', attrs={'class': 'YMlKec fxKbKc'})
            variacao = site.find('div', attrs={'class': 'JwB6zf'})
            texto = f'O valor atualizado da Ripple é de R${preco.text} \nA variação da XRP é de {variacao.text}'
            bot.send_message(callback_query.message.chat.id, texto)


        # VALOR RIPPLE -- USADA PARA OS ALERTAS

        def ripple_alerta(message):
            response = requests.get('https://www.google.com/finance/quote/XRP-BRL?hl=pt')
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            preco = site.find('div', attrs={'class': 'YMlKec fxKbKc'})
            variacao = site.find('div', attrs={'class': 'JwB6zf'})
            texto = f'O valor atualizado da Ripple é de R${preco.text} \nA variação da XRP é de {variacao.text}'
            bot.send_message(message.chat.id, texto)


        # CRIAR ALERTA 
        @bot.callback_query_handler(func= lambda call: call.data == 'Criar_alerta_xrp')
        def menu_alerta_xrp(callback_query):
            menu_alerta_keyboard= types.InlineKeyboardMarkup(row_width=1)
            minutos_Keyboard = types.InlineKeyboardButton('MINUTOS', callback_data='minutos_xrp')
            horas_Keyboard = types.InlineKeyboardButton('HORAS', callback_data='horas_xrp')
            dias_Keyboard = types.InlineKeyboardButton('DIAS', callback_data='dias_xrp')
            menu_alerta_keyboard.add(minutos_Keyboard, horas_Keyboard, dias_Keyboard)

            texto = '''
            Ripple (XRP)
            
        Escolha a opção que deseja ser o intervalo de tempo: '''

            bot.send_message(callback_query.message.chat.id, texto, reply_markup=menu_alerta_keyboard)
            

        # ESCOLHA INTERVALO MINUTOS
        @bot.callback_query_handler(func= lambda call: call.data == 'minutos_xrp')
        def minutos_xrp(callback_query):
            bot.send_message(callback_query.message.chat.id, 'Digite um número de 1 a 59 (minutos) que você deseja ser o intervalo de tempo: ')
            bot.register_next_step_handler(callback_query.message, check_minutes_xrp)

        # ANALISE DAS MENSAGEM  E AGENDAMENTO DA TAREFA -- MINUTOS
        def check_minutes_xrp(message):
            if message.text in [str(x) for x in range(1, 60)]:
                min = int(message.text)
                bot.send_message(message.chat.id, f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {min} minutos.')
            
                schedule.every(min).minutes.do(ripple_alerta, message) 
                i = 0
                while True:
                    i += 1
                    print(i)
                    schedule.run_pending()
                    time.sleep(1)
            else:
                return False


        # ESCOLHA INTERVALO HORAS 
        @bot.callback_query_handler(func=lambda call: call.data == 'horas_xrp')
        def horas_xrp(callback_query):
            bot.send_message(callback_query.message.chat.id, 'Digite um número de 1 a 20 (horas) que você deseja ser o intervalo de tempo: ')
            bot.register_next_step_handler(callback_query.message, check_hours_xrp)
            
            
        # ANALISE DAS MENSAGEM RECEBIDAS HORAS
        def check_hours_xrp(message):
            if message.text in [str(x) for x in range(1, 60)]:
                hours = int(message.text)
                bot.send_message(message.chat.id, f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {hours} horas.')
            
                schedule.every(hours).hours.do(ripple_alerta, message)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            else:
                return False
            

        # ESCOLHA INTERVALO -- DIAS 
        @bot.callback_query_handler(func=lambda call: call.data == 'dias_xrp')
        def dias_xrp(callback_query):
            texto = '''
            Digite um número de 1 a 6 (dias) que você deseja ser o intervalo:

            Ou digite um dia da semana que deseja receber os alertas ( exemplo: segunda, terça; não é necessario escrever -feira, porém digite corretamente) :
            '''
            bot.send_message(callback_query.message.chat.id, texto)
            bot.register_next_step_handler(callback_query.message, check_days_xrp)

        # ANALISE DAS MENSAGEMN RECEBIDAS -- DIAS
        def check_days_xrp(message):
            lista = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'sabado', 'domingo']
            dias = message.text
            if dias in [str(x) for x in range(1, 7)] or dias.lower() in lista:
                
                if message.text in [str(x) for x in range(1, 7)]:
                    days = int(message.text)
                    texto1 = f'Seu alerta foi criado com sucesso !!! A partir de agora, você receberá alertas a cada {days} dias.'
                    bot.send_message(message.chat.id, texto1)

                    schedule.every(days).days.do(ripple_alerta, message)
                    while True:
                        schedule.run_pending()
                        time.sleep(1)
            
                elif message.text in lista:
                    dias = message.text
                    texto2 = f'Seu alerta foi criado com sucesso !!! A partir de agora, todo(a) {dias} você receberá alertas'
                    
                    if dias.lower() == 'segunda':
                        print('segunda')
                        schedule.every().monday.at('08:00').do(ripple_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                    
                    elif dias.lower() == 'terça':
                        print('terça')
                        schedule.every().tuesday.at('08:00').do(ripple_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'quarta':
                        print('quarta')
                        schedule.every().wednesday.at('08:00').do(ripple_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'quinta':
                        print('quinta')
                        schedule.every().thursday.at('08:00').do(ripple_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'sexta':
                        print('sexta')
                        schedule.every().friday.at('08:00').do(ripple_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'sábado' or dias == 'sabado':
                        print('sábado')
                        schedule.every().saturday.at('08:00').do(ripple_alerta, message)
                        while True:
                            schedule.Trun_pending()
                            time.sleep(1)
                
                    elif dias.lower() == 'domingo':
                        print('domingo')
                        schedule.every().sunday.at('08:00').do(ripple_alerta, message)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
            else:
                return False
        # LOOP BOT
        bot.polling()
        pass
    except Exception as e:
        print(f"Erro {e}")
        continue