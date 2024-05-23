# Exercícios
# Crie funções que duplicam, triplicam e quadruplicam
# o número recebido como parâmetro.

# def duplicar(numero):
#     return numero *2

# def triplicar(numero):
#     return numero * 3

# def quadriplicar(numero):
#     return numero * 4

# print(duplicar(4), triplicar(4), quadriplicar(4))

def criar_multiplicador(multiplicador):
    def multiplicar(numero):
        return numero * multiplicador
    return multiplicar

duplicar = criar_multiplicador(2)
triplicar = criar_multiplicador(3)
quadriplicar = criar_multiplicador(4)

print(duplicar(2))
print(triplicar(2))
print(quadriplicar(2))





