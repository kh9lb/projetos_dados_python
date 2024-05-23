#Refinando o codigo do exercício anterior
#importar re para usar função sub para alterar o cpf do usuario apenas para numeros
# importar sys e usar função exit, encerra o programa na hora desejada
import re
import sys

entrada = input('Digite seu CPF: ')
cpf_usuario = re.sub(
    r'[^0-9]',
    '',
    entrada
)

#verificando se o input é sequencial
entrada_sequencial = entrada == entrada[0] * len(entrada)

if entrada_sequencial:
    print('Você digitou dados sequenciais.')
    sys.exit()

nove_digitos = cpf_usuario[:9]
contador_regressivo_1 = 10

resultado = 0
for digito in nove_digitos:
    resultado += int(digito) * contador_regressivo_1
    contador_regressivo_1 -= 1
digito_1 = (resultado * 10) % 11
digito_1 = digito_1 if digito_1 <= 9 else 0

#Segundo digito
dez_digitos = nove_digitos + str(digito_1)
contador_regressivo_2 = 11

resultado_2 = 0
for digito in dez_digitos:
    resultado_2 += int(digito) * contador_regressivo_2
    contador_regressivo_2 -= 1
digito_2 = ((resultado_2 * 10) % 11)
digito_2 = digito_2 if digito_2 <= 9 else 0

#Validar o CPF
cpf_calculo = f'{nove_digitos}{digito_1}{digito_2}'

if cpf_usuario == cpf_calculo:
    print(f'{cpf_usuario} é válido.')
else:
    print('CPF Inválido.')