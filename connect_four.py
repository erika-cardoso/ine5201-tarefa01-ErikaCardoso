
import math

import FreeSimpleGUI as sg


LINHAS = 6
COLUNAS = 7
TAMANHO_CASA = 70
MARGEM = 0
MARGEM_SUPERIOR = 42
MARGEM_INFERIOR = 8
LARGURA_TABULEIRO = COLUNAS * TAMANHO_CASA + 2 * MARGEM
ALTURA_TABULEIRO = LINHAS * TAMANHO_CASA + MARGEM_SUPERIOR + MARGEM_INFERIOR
COR_TABULEIRO = "#D3D3D3"
CORES_JOGADORES = {1: "#FFD700", 2: "#171717"}


# FUNÇÃO PARA CRIAR O TABULEIRO

def criar_tabuleiro():

    tabuleiro = []

    for _ in range(LINHAS):

        linha = []

        for _ in range(COLUNAS):

            linha.append(0)

        tabuleiro.append(linha)

    return tabuleiro


# FUNÇÃO PARA INSERIR UMA FICHA

def inserir_ficha(tabuleiro, coluna, jogador):

    # Verifica se a coluna existe
    if coluna < 0 or coluna >= COLUNAS:
        return False

    # Percorre as linhas de baixo para cima
    for linha in range(LINHAS - 1, -1, -1):

        # Verifica se a posição está vazia
        if tabuleiro[linha][coluna] == 0:

            # Insere a ficha do jogador
            tabuleiro[linha][coluna] = jogador

            return True

    # Se chegou aqui, a coluna está cheia
    return False


# FUNÇÃO PARA VERIFICAR A VITÓRIA

def verificar_vitoria(tabuleiro, jogador):

    # Percorre todas as posições do tabuleiro
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):

            # Só verifica posições que pertencem ao jogador
            if tabuleiro[linha][coluna] == jogador:

                # 1. VERIFICAÇÃO HORIZONTAL
                if coluna <= COLUNAS - 4:
                    if all(tabuleiro[linha][coluna + i] == jogador
                           for i in range(4)):
                        return True

                # 2. VERIFICAÇÃO VERTICAL
                if linha <= LINHAS - 4:
                    if all(tabuleiro[linha + i][coluna] == jogador
                           for i in range(4)):
                        return True

                # 3. DIAGONAL CRESCENTE
                if linha >= 3 and coluna <= COLUNAS - 4:
                    if all(tabuleiro[linha - i][coluna + i] == jogador
                           for i in range(4)):
                        return True

                # 4. DIAGONAL DECRESCENTE
                if linha <= LINHAS - 4 and coluna <= COLUNAS - 4:
                    if all(tabuleiro[linha + i][coluna + i] == jogador
                           for i in range(4)):
                        return True

    # Se nenhuma sequência foi encontrada
    return False


# FUNÇÃO PARA VERIFICAR O EMPATE

def verificar_empate(tabuleiro):

    # O empate acontece quando não há mais espaços vazios
    for linha in tabuleiro:
        for casa in linha:
            if casa == 0:
                return False

    return True


def centro_casa(linha, coluna):
    x = MARGEM + coluna * TAMANHO_CASA + TAMANHO_CASA / 2
    y = ALTURA_TABULEIRO - MARGEM_SUPERIOR - linha * TAMANHO_CASA - TAMANHO_CASA / 2
    return x, y


def desenhar_tabuleiro(grafico, tabuleiro, ficha_caindo=None):
    grafico.erase()
    grafico.draw_rectangle(
        (0, ALTURA_TABULEIRO),
        (LARGURA_TABULEIRO, 0),
        fill_color=COR_TABULEIRO,
        line_color=COR_TABULEIRO,
    )

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            centro = centro_casa(linha, coluna)
            jogador = tabuleiro[linha][coluna]
            grafico.draw_circle(
                centro,
                TAMANHO_CASA * 0.36,
                fill_color=CORES_JOGADORES.get(jogador, "#F5F5F5"),
                line_color="#777777" if jogador == 0 else "#555555",
                line_width=2,
            )

    if ficha_caindo is not None:
        coluna, altura, jogador = ficha_caindo
        grafico.draw_circle(
            (MARGEM + coluna * TAMANHO_CASA + TAMANHO_CASA / 2, altura),
            TAMANHO_CASA * 0.36,
            fill_color=CORES_JOGADORES[jogador],
            line_color="#555555",
            line_width=2,
        )


def desenhar_mensagem_resultado(grafico, texto):
    centro_y = ALTURA_TABULEIRO / 2
    grafico.draw_rectangle(
        (LARGURA_TABULEIRO / 2 - 125, centro_y - 20),
        (LARGURA_TABULEIRO / 2 + 125, centro_y + 20),
        fill_color="#FFFFFF",
        line_color="#1F2937",
        line_width=2,
    )
    grafico.draw_text(
        texto,
        (LARGURA_TABULEIRO / 2, centro_y),
        color="#1F2937",
        font=("Arial", 19, "bold"),
    )


def animar_queda(janela, grafico, tabuleiro, linha, coluna, jogador):
    _, altura_final = centro_casa(linha, coluna)
    _, altura_inicial = centro_casa(0, coluna)
    altura_inicial += TAMANHO_CASA
    quadros = max(10, (linha + 1) * 7)

    for quadro in range(1, quadros + 1):
        progresso = quadro / quadros
        altura = altura_inicial + (altura_final - altura_inicial) * progresso
        desenhar_tabuleiro(grafico, tabuleiro, (coluna, altura, jogador))
        evento, _ = janela.read(timeout=20)
        if evento == sg.WIN_CLOSED:
            return "sair"
        if evento == "-REINICIAR-":
            return "reiniciar"

    return None


def animar_foguetes(janela, grafico, tabuleiro, jogador):
    explosoes = [
        (LARGURA_TABULEIRO * 0.25, ALTURA_TABULEIRO * 0.72, 0),
        (LARGURA_TABULEIRO * 0.50, ALTURA_TABULEIRO * 0.82, 12),
        (LARGURA_TABULEIRO * 0.75, ALTURA_TABULEIRO * 0.72, 24),
    ]
    cores = ["#FF3B30", "#FFD700", "#00A8E8", "#FFFFFF", "#FF7F11"]
    quadros = 72

    for quadro in range(quadros):
        desenhar_tabuleiro(grafico, tabuleiro)
        desenhar_mensagem_resultado(grafico, f"Jogador {jogador} venceu!")

        for indice, (x, y_alvo, atraso) in enumerate(explosoes):
            fase = quadro - atraso
            if fase < 0:
                continue
            if fase < 18:
                y = 8 + (y_alvo - 8) * fase / 18
                grafico.draw_line((x, y - 13), (x, y - 2), color="#FF7F11", width=4)
                grafico.draw_circle((x, y), 4, fill_color="#FFD700", line_color="#FFD700")
            elif fase < 43:
                raio = (fase - 18) * 2.2
                for particula in range(12):
                    angulo = 2 * math.pi * particula / 12
                    ponto = (x + math.cos(angulo) * raio, y_alvo + math.sin(angulo) * raio)
                    cor = cores[(particula + indice) % len(cores)]
                    grafico.draw_circle(ponto, 3, fill_color=cor, line_color=cor)

        evento, _ = janela.read(timeout=30)
        if evento == sg.WIN_CLOSED:
            return "sair"
        if evento == "-REINICIAR-":
            return "reiniciar"

    return None


def criar_janela():
    botoes_colunas = [
        sg.Column(
            [[sg.Button(
                f"▼ {coluna + 1}",
                key=f"-COLUNA-{coluna}",
                size=(6, 1),
                pad=(0, 0),
                tooltip=f"Jogar na coluna {coluna + 1}",
            )]],
            size=(TAMANHO_CASA, 36),
            pad=(0, 0),
            element_justification="center",
            vertical_alignment="center",
        )
        for coluna in range(COLUNAS)
    ]
    layout = [
        [sg.Text("Connect Four", font=("Arial", 22, "bold"), justification="center", expand_x=True)],
        [
            sg.Text("Vez: Jogador 1 (amarelo)", key="-VEZ-", font=("Arial", 13, "bold")),
            sg.Push(),
            sg.Button("Reiniciar partida", key="-REINICIAR-"),
        ],
        [sg.Text("Jogador 1: amarelo     Jogador 2: preto", key="-STATUS-", size=(48, 1))],
        botoes_colunas,
        [
            sg.Graph(
                canvas_size=(LARGURA_TABULEIRO, ALTURA_TABULEIRO),
                graph_bottom_left=(0, 0),
                graph_top_right=(LARGURA_TABULEIRO, ALTURA_TABULEIRO),
                background_color=COR_TABULEIRO,
                key="-TABULEIRO-",
            )
        ],
    ]
    return sg.Window("Connect Four", layout, finalize=True, resizable=False)


def executar_jogo():
    janela = criar_janela()
    grafico = janela["-TABULEIRO-"]
    tabuleiro = criar_tabuleiro()
    jogador = 1
    partida_encerrada = False
    desenhar_tabuleiro(grafico, tabuleiro)

    while True:
        evento, _ = janela.read()
        if evento == sg.WIN_CLOSED:
            break

        if evento == "-REINICIAR-":
            tabuleiro = criar_tabuleiro()
            jogador = 1
            partida_encerrada = False
            janela["-VEZ-"].update("Vez: Jogador 1 (amarelo)")
            janela["-STATUS-"].update("Partida reiniciada.")
            desenhar_tabuleiro(grafico, tabuleiro)
            continue

        if partida_encerrada:
            continue

        if not isinstance(evento, str) or not evento.startswith("-COLUNA-"):
            continue

        coluna = int(evento[len("-COLUNA-"):])
        linha_destino = next(
            (linha for linha in range(LINHAS - 1, -1, -1) if tabuleiro[linha][coluna] == 0),
            None,
        )
        if linha_destino is None:
            janela["-STATUS-"].update(f"Coluna {coluna + 1} cheia. Escolha outra.")
            continue

        janela["-STATUS-"].update(f"Jogador {jogador} está jogando...")
        janela.refresh()
        resultado_animacao = animar_queda(
            janela, grafico, tabuleiro, linha_destino, coluna, jogador
        )
        if resultado_animacao == "sair":
            break
        if resultado_animacao == "reiniciar":
            tabuleiro = criar_tabuleiro()
            jogador = 1
            partida_encerrada = False
            janela["-VEZ-"].update("Vez: Jogador 1 (amarelo)")
            janela["-STATUS-"].update("Partida reiniciada.")
            desenhar_tabuleiro(grafico, tabuleiro)
            continue

        tabuleiro[linha_destino][coluna] = jogador
        desenhar_tabuleiro(grafico, tabuleiro)

        if verificar_vitoria(tabuleiro, jogador):
            partida_encerrada = True
            janela["-VEZ-"].update("Partida encerrada")
            janela["-STATUS-"].update(f"Jogador {jogador} venceu!")
            resultado_animacao = animar_foguetes(janela, grafico, tabuleiro, jogador)
            if resultado_animacao == "sair":
                break
            if resultado_animacao == "reiniciar":
                tabuleiro = criar_tabuleiro()
                jogador = 1
                partida_encerrada = False
                janela["-VEZ-"].update("Vez: Jogador 1 (amarelo)")
                janela["-STATUS-"].update("Partida reiniciada.")
                desenhar_tabuleiro(grafico, tabuleiro)
            continue

        if verificar_empate(tabuleiro):
            partida_encerrada = True
            janela["-VEZ-"].update("Partida encerrada")
            janela["-STATUS-"].update("Empate! O tabuleiro está cheio.")
            desenhar_mensagem_resultado(grafico, "Empate!")
            continue

        jogador = 2 if jogador == 1 else 1
        cor = "amarelo" if jogador == 1 else "preto"
        janela["-VEZ-"].update(f"Vez: Jogador {jogador} ({cor})")
        janela["-STATUS-"].update(f"Jogador {jogador}, escolha uma coluna.")

    janela.close()


if __name__ == "__main__":
    executar_jogo()
