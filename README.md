# Connect Four

Uma versão para dois jogadores do jogo Connect Four, feita em Python com interface gráfica usando FreeSimpleGUI.

## Sobre o jogo

Os jogadores se alternam colocando fichas em um tabuleiro de 6 linhas por 7 colunas. O objetivo é formar uma sequência de quatro fichas da própria cor na horizontal, na vertical ou na diagonal.

- **Jogador 1:** fichas amarelas.
- **Jogador 2:** fichas pretas.
- **Empate:** ocorre quando o tabuleiro fica cheio sem que um jogador vença.

## Recursos

- Interface gráfica com tabuleiro cinza-claro.
- Botões numerados acima e alinhados com cada coluna.
- Animação das fichas caindo.
- Indicação do jogador da vez e da cor de suas fichas.
- Animação de foguetes quando há uma vitória.
- Mensagem centralizada para vitória e empate.
- Botão para reiniciar a partida.
- Colunas cheias não aceitam novas fichas.
- A partida termina após uma vitória ou empate, até ser reiniciada.

## Requisitos

- Python 3.8 ou superior.
- FreeSimpleGUI 5.3.0.post1.

## Instalação

Abra um terminal na pasta do projeto e instale a dependência:

```bash
python -m pip install -r requirements.txt
```

## Como executar

Na mesma pasta, inicie o jogo com:

```bash
python connect_four.py
```

## Como jogar

1. Clique no botão numerado da coluna onde deseja colocar sua ficha.
2. Aguarde a animação da ficha e, em seguida, jogue quando for sua vez.
3. Faça uma linha de quatro fichas na horizontal, vertical ou diagonal para vencer.
4. Se todas as posições forem ocupadas antes de alguém vencer, a partida termina empatada.
5. Clique em **Reiniciar partida** para começar novamente. Esse botão também está disponível durante a partida.

## Arquivos

| Arquivo | Descrição |
| --- | --- |
| `connect_four.py` | Regras do jogo, interface, animações e execução da partida. |
| `requirements.txt` | Dependências Python do projeto. |

## Funções principais

- `criar_tabuleiro()`: cria um tabuleiro vazio.
- `inserir_ficha(tabuleiro, coluna, jogador)`: coloca uma ficha na coluna indicada, se houver espaço.
- `verificar_vitoria(tabuleiro, jogador)`: verifica se o jogador formou uma sequência de quatro fichas.
- `verificar_empate(tabuleiro)`: verifica se o tabuleiro está cheio.
- `executar_jogo()`: cria a interface e executa o ciclo da partida.
