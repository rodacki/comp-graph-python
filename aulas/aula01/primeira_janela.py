"""
CCB0941 — Computacao Grafica | Aula 01 (M1)
Primeira janela interativa: primitivas, loop de eventos e resposta a input.

Objetivo pedagogico
--------------------
Este NAO e um programa para voce escrever do zero. E um *scaffold* para voce
LER, PREVER, RODAR e MODIFICAR. A saida e visual: um bug vira uma imagem
visivelmente errada. Entender CG e ligar "o que aparece na tela" a "a causa
geometrica/matematica no codigo".

Como usar em aula (familias de atividade 2 e 3)
-----------------------------------------------
1. PREVER ANTES DE RODAR: leia o codigo e desenhe no papel o que espera ver.
2. Rode:  python primeira_janela.py
3. Reconcilie: o que apareceu bate com o seu desenho? Onde errou e por que?
4. MODIFIQUE os pontos marcados com  # >>> EXPERIMENTE  e preveja de novo.

Conceitos de CG que aparecem aqui (e onde)
------------------------------------------
- Sistema de coordenadas da tela (origem, eixo y para cima) .......... secao 1
- Framebuffer, limpar a tela e double buffering ...................... secao 1 / on_draw
- Primitivas graficas e o que e "alto nivel" vs. "pipeline" .......... secao 2
- Modelo de cor RGB (aditivo, 8 bits por canal) ...................... secao 2
- Modo retido (retained mode) vs. modo imediato ..................... secao 2 / batch
- Loop de eventos e inversao de controle ............................ secao 3

Requisitos:  pip install pyglet   (ver requirements.txt)
Controles:   [C] muda a cor do circulo | [setas] move o quadrado |
             [clique] adiciona um ponto | [ESC] sai
"""

import pyglet
from pyglet import shapes

# ======================================================================
# 1. A JANELA  ->  o "dispositivo de saida" do nosso sistema grafico.
# ======================================================================
# A janela e uma grade de LARGURA x ALTURA *pixels* (o pixel e o menor
# elemento enderecavel da imagem). Essa grade e o FRAMEBUFFER: uma matriz
# de cores na memoria que a placa de video envia para o monitor.
#
# SISTEMA DE COORDENADAS (grave isto — e origem de MUITO bug em CG):
#   - a origem (0, 0) fica no canto INFERIOR-ESQUERDO;
#   - x cresce para a DIREITA, y cresce para CIMA (como no plano cartesiano).
# Cuidado: uma imagem "crua" (arquivo PNG, array numpy) costuma ter a origem
# no canto SUPERIOR-esquerdo, com y crescendo para BAIXO. Misturar as duas
# convencoes e o classico "desenhou tudo de cabeca para baixo". Voltaremos a
# converter entre sistemas de coordenadas no modulo M3.
LARGURA, ALTURA = 800, 600
janela = pyglet.window.Window(LARGURA, ALTURA, caption="Aula 01 — Primeira janela")

# Um BATCH agrupa varias primitivas para serem desenhadas de uma so vez.
# Por que isso importa: cada "chamada de desenho" (draw call) enviada a GPU
# tem custo. Desenhar 1000 formas em um batch e muito mais barato que mandar
# 1000 comandos separados. E tambem um primeiro contato com o MODO RETIDO
# (retained mode): em vez de redesenhar tudo "na mao" a cada quadro (o antigo
# modo imediato do OpenGL/GLUT), nos CRIAMOS objetos que persistem e a
# biblioteca cuida de redesenha-los.
batch = pyglet.graphics.Batch()

# ======================================================================
# 2. AS PRIMITIVAS  ->  o vocabulario visual do sistema.
# ======================================================================
# No fundo, uma placa grafica sabe desenhar pouca coisa: PONTOS, SEGMENTOS de
# reta e TRIANGULOS. Todo o resto e composicao disso. Um Circle e um Rectangle
# aqui sao primitivas de ALTO NIVEL: o pyglet os quebra internamente em
# triangulos, que o pipeline entao "rasteriza" (converte em pixels). Ver o
# slide "Primitivas de desenho".
#
# IMPORTANTE (o arco do curso): o pyglet DESENHA USANDO OPENGL por baixo. Aqui
# ficamos na camada de ALTO NIVEL (shapes), que esconde os shaders e os buffers
# de vertice. Isso e proposital: hoje vemos o "o que" (primitivas, eventos).
# O "como" da GPU — escrever shaders GLSL na mao — vem em M6, depois do
# rasterizador em software. Para uma espiada no contraste ja, veja o apendice
# opcional: apendice_opengl_triangulo.py (mesmo triangulo, feito "na GPU crua").
#
# COR — modelo RGB (aditivo): cada cor e (R, G, B), a intensidade de luz
# Vermelha, Verde e Azul que se SOMAM. Aqui cada canal usa 8 bits, ou seja
# vai de 0 a 255 (2^8 = 256 niveis). (0,0,0) = preto; (255,255,255) = branco.
# Por que 255 e nao 100? E a resolucao de 1 byte por canal. Veremos modelos e
# espacos de cor a fundo no modulo M2.
#
# As coordenadas abaixo estao em PIXELS da janela (espaco de tela). Ainda nao
# ha transformacoes nem matrizes — isso chega no M3.
COR_CIRCULO = (46, 204, 113)      # (R, G, B), 0..255  # >>> EXPERIMENTE
circulo = shapes.Circle(x=200, y=300, radius=60, color=COR_CIRCULO, batch=batch)

# (x, y) e o canto inferior-esquerdo do retangulo; width/height sao positivos
# para cima e para a direita (coerente com o eixo y apontando para cima).
quadrado = shapes.Rectangle(x=380, y=260, width=80, height=80,
                            color=(52, 152, 219), batch=batch)

# Um triangulo e dado por seus TRES vertices. Repare que a "forma" e so a
# lista de vertices — a primitiva mais fundamental do 3D tambem sera o
# triangulo (no M5 rasterizamos triangulos "na mao", em software).
triangulo = shapes.Triangle(x=560, y=240, x2=720, y2=240, x3=640, y3=380,
                            color=(231, 76, 60), batch=batch)

linha = shapes.Line(50, 50, 750, 50, thickness=3, color=(149, 165, 166),
                    batch=batch)

# Pontos adicionados pelo mouse ficam aqui. Detalhe de MODO RETIDO: a
# primitiva so continua na tela enquanto existir uma referencia viva a ela.
# Se nao guardarmos o objeto nesta lista, o coletor de lixo do Python o
# destroi e a forma "some" da tela. (No modo imediato esse problema nem
# existiria, porque nada persiste entre quadros.)
pontos_do_mouse = []

# ESTADO da aplicacao. Os handlers de evento (secao 3) apenas LEEM e ALTERAM
# este estado; o loop de eventos decide quando redesenhar a partir dele.
cores_ciclo = [(46, 204, 113), (155, 89, 182), (241, 196, 15), (26, 188, 156)]
indice_cor = 0


# ======================================================================
# 3. O LOOP DE EVENTOS  ->  o coracao de todo sistema grafico interativo.
# ======================================================================
# INVERSAO DE CONTROLE: nos NAO escrevemos um "while True: desenhe()". Em vez
# disso, REGISTRAMOS funcoes (handlers) e entregamos o controle ao pyglet. Ele
# fica em um laco escondido lendo eventos do sistema operacional (teclado,
# mouse, "precisa repintar") e CHAMA o nosso handler correspondente. Nos so
# dizemos "o que fazer quando X acontecer" — o "quando" e com o loop.
@janela.event
def on_draw():
    """Repinta a janela. Chamado pelo loop sempre que a tela precisa ser refeita."""
    # clear() preenche TODO o framebuffer com a cor de fundo. Sem isso, o
    # desenho do quadro anterior permaneceria por baixo do novo (as vezes um
    # bug, as vezes um efeito de "rastro" proposital — experimente comentar).
    janela.clear()
    # Desenha todas as primitivas do batch. Como estamos em modo retido, nao
    # recriamos as formas aqui: so pedimos que sejam pintadas no estado atual.
    batch.draw()
    # (O pyglet usa DOUBLE BUFFERING: desenhamos em um buffer "de tras" e ele
    # troca com o "da frente" so quando o quadro esta pronto. Por isso a
    # animacao nao "pisca" enquanto e montada.)


@janela.event
def on_key_press(simbolo, modificadores):
    """Chamado UMA vez quando uma tecla e pressionada (simbolo = qual tecla)."""
    global indice_cor
    # Repare o padrao: o handler nao "desenha" nada. Ele so muda o ESTADO
    # (a cor, a posicao). O on_draw seguinte e que reflete a mudanca na tela.
    if simbolo == pyglet.window.key.C:
        # >>> EXPERIMENTE: cicla a cor do circulo entre as de cores_ciclo
        indice_cor = (indice_cor + 1) % len(cores_ciclo)
        circulo.color = cores_ciclo[indice_cor]
    elif simbolo == pyglet.window.key.RIGHT:
        # Mover = TRANSLADAR: somamos um deslocamento a coordenada. Aqui e
        # "na mao"; no M3 isso vira uma matriz de translacao. PREVEJA: com o
        # eixo y para cima, qual seta deve subir o quadrado?
        quadrado.x += 20        # >>> EXPERIMENTE: e se somar em .y? e se subtrair?
    elif simbolo == pyglet.window.key.LEFT:
        quadrado.x -= 20
    elif simbolo == pyglet.window.key.UP:
        quadrado.y += 20
    elif simbolo == pyglet.window.key.DOWN:
        quadrado.y -= 20
    elif simbolo == pyglet.window.key.ESCAPE:
        janela.close()


@janela.event
def on_mouse_press(x, y, botao, modificadores):
    """Chamado quando um botao do mouse e apertado."""
    # (x, y) ja chega no sistema de coordenadas da JANELA (origem embaixo a
    # esquerda) — o mesmo das nossas primitivas, entao o ponto cai exatamente
    # sob o cursor. Se a origem fosse no topo (como em imagens), precisariamos
    # corrigir com  y = ALTURA - y. Esse tipo de conversao e o assunto de M3.
    # >>> EXPERIMENTE: troque o raio, a cor, ou desenhe um Rectangle no lugar.
    ponto = shapes.Circle(x=x, y=y, radius=5, color=(236, 240, 241), batch=batch)
    pontos_do_mouse.append(ponto)   # guarda a referencia (modo retido!)
    print(f"clique em ({x}, {y})   ->   {len(pontos_do_mouse)} ponto(s)")


# ======================================================================
# 4. INICIA O LOOP.
# ======================================================================
# A partir daqui o controle e do pyglet: ele le eventos e chama nossos
# handlers ate a janela fechar. Nada escrito DEPOIS desta linha executa
# enquanto a janela estiver aberta (o run() so retorna quando ela fecha).
if __name__ == "__main__":
    pyglet.app.run()
