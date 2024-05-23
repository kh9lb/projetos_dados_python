#Calculadora usando função while

while True:
    numero_1 = input('Digite o primeiro número: ')
    numero_2 = input('Digite o segundo número: ')
    operador = input('Digite o operador (+-/*): ')

    numeros_validos = None
    num_1_flt = 0
    num_2_flt = 0

    
    try:
        num_1_flt = float(numero_1)
        num_2_flt = float(numero_2)
        numeros_validos = True
    except:    
         numeros_validos = None

    if numeros_validos is None:
        print('Um ou ambos os números digitados são inválidos.')
        continue
    
    operadores_permitidos = '+-/*'

    if operador not in operadores_permitidos:
        print('Operador inválido')
        continue

    if len(operador)>1:
        print('Digite apenas 1 operador.')
        continue

    print('Realizando sua operação')    
    if operador == '+':
        print(f'{num_1_flt} + {num_2_flt} = ', num_1_flt + num_2_flt)
    elif operador == '-':
        print(f'{num_1_flt} - {num_2_flt} = ', num_1_flt - num_2_flt)
    elif operador == '*':
        print(f'{num_1_flt} * {num_2_flt} = ', num_1_flt * num_2_flt)
    elif operador == '/':
        print(f'{num_1_flt} / {num_2_flt} = ', num_1_flt / num_2_flt)

    
    sair = input('Quer sair? [s]sim: ').lower().startswith('s')

    if sair is True:
        break