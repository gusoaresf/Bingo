import random
import re

# Classe para representar uma cartela
class Cartela:
    def __init__(self):
        # Gere uma lista de 25 números aleatórios distintos entre 1 e 50
        self.numeros = random.sample(range(1, 51), 25)
        # Crie uma matriz 5x5 para a cartela
        self.matriz = [self.numeros[i:i+5] for i in range(0, 25, 5)]
        # Inicialize a marcação de números na cartela como Falso
        self.marca = [[False] * 5 for _ in range(5)]

# Função para gerar cartelas para os jogadores
def gerar_cartelas(num_jogadores):
    cartelas = []
    for _ in range(num_jogadores):
        cartela = Cartela()
        cartelas.append(cartela)
    return cartelas

# Função para sortear números
def sortear_numero():
    numeros_disponiveis = list(range(1, 51))
    return random.choice(numeros_disponiveis)

# Função para verificar ganhadores
def verificar_ganhador(cartela):
    # Verifique se há uma linha completa marcada
    for linha in cartela.matriz:
        if all(cartela.marca[cartela.matriz.index(linha)]):
            return True
    # Verifique se há uma coluna completa marcada
    for col in range(5):
        if all(cartela.marca[i][col] for i in range(5)):
            return True
    # Verifique se há uma diagonal completa marcada
    if all(cartela.marca[i][i] for i in range(5)) or all(cartela.marca[i][4 - i] for i in range(5)):
        return True
    return False

# Função para exibir todas as cartelas
def exibir_cartelas(jogadores):
    for jogador in jogadores:
        print(f"Cartela de {jogador['nome']}:")
        exibir_cartela(jogador['cartela'])
        print()

# Função para exibir uma cartela
def exibir_cartela(cartela):
    for linha in cartela.matriz:
        for num, marcado in zip(linha, cartela.marca[cartela.matriz.index(linha)]):
            if marcado:
                print("XX", end=' ')
            else:
                print(f"{num:02d}", end=' ')
        print()

# Função para atualizar o ranking
def atualizar_ranking(jogadores):
    with open("ranking.txt", "w") as file:
        for jogador in jogadores:
            file.write(f"{jogador['nome']} {jogador['vitorias']}\n")

# Função para validar entrada de número entre min_value e max_value
def validar_entrada(prompt, min_value, max_value):
    while True:
        entrada = input(prompt)
        if re.match(r"^\d+$", entrada):
            valor = int(entrada)
            if min_value <= valor <= max_value:
                return valor
            else:
                print(f"Por favor, escolha um valor entre {min_value} e {max_value}.")
        else:
            print("Entrada inválida. Digite um número válido.")

# Função principal
def main():
    print("Bem-vindo ao Jogo de Bingo!")
    continuar_jogando = True

    while continuar_jogando:
        num_jogadores = validar_entrada("Quantos jogadores vão participar (de 2 a 5)? ", 2, 5)

        jogadores = []
        for i in range(num_jogadores):
            nome = input(f"Nome do Jogador {i+1}: ")
            jogadores.append({"nome": nome, "cartela": gerar_cartelas(1)[0], "vitorias": 0})

        jogo_terminado = False

        while not jogo_terminado:
            numero_sorteado = sortear_numero()
            input("Pressione Enter para sortear um número.")
            print(f"Número sorteado: {numero_sorteado}")

            for jogador in jogadores:
                print(f"Cartela de {jogador['nome']}:")
                exibir_cartela(jogador["cartela"])
                jogador["cartela"].marca = [
                    [num == numero_sorteado or marcado for num, marcado in zip(linha, jogador["cartela"].marca[linha_idx])]
                    for linha_idx, linha in enumerate(jogador["cartela"].matriz)
                ]

                if verificar_ganhador(jogador["cartela"]):
                    jogador["vitorias"] += 1
                    print(f"{jogador['nome']} ganhou!")
                    atualizar_ranking(jogadores)
                    exibir_cartelas(jogadores)
                    resposta = validar_entrada("Escolha uma opção:\n1 - Continuar com os mesmos jogadores\n2 - Recomeçar o jogo\n3 - Finalizar jogo\nOpção: ", 1, 3)
                    if resposta == 1:
                        for jogador in jogadores:
                            jogador['cartela'] = gerar_cartelas(1)[0]
                        jogo_terminado = False
                    elif resposta == 2:
                        jogo_terminado = True
                    elif resposta == 3:
                        jogo_terminado = True
                        continuar_jogando = False
                    break

        for jogador in jogadores:
            print(f"{jogador['nome']} venceu {jogador['vitorias']} vezes.")

if __name__ == "__main__":
    main()