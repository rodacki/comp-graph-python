# Ex09 — CAD 2D incremental com Pyglet

## Objetivo

Este subprojeto é um protótipo educacional de CAD 2D criado para estudar, com
calma e em pequenas etapas, a arquitetura de uma aplicação gráfica interativa
baseada em Python, Pyglet e OpenGL moderno.

O objetivo não é criar rapidamente um editor completo. Cada etapa deve
introduzir poucos conceitos, permanecer executável e ser estudada antes da
próxima alteração.

Princípios adotados:

- código explícito e fácil de acompanhar;
- shaders, VAOs e VBOs do OpenGL moderno;
- separação futura entre modelo, câmera, ferramenta e renderer somente quando
  cada responsabilidade se tornar necessária;
- modelo CAD na CPU como fonte da verdade;
- buffers OpenGL como caches gráficos derivados e descartáveis;
- coordenadas do modelo armazenadas como `float` do Python e conversão para
  `float32` somente no envio à GPU.

## Estado atual

O exemplo contém:

- janela Pyglet redimensionável de 800 × 600 unidades lógicas;
- contexto OpenGL 3.3 com double buffering;
- tratamento explícito de telas HiDPI/Retina;
- vertex shader e fragment shader próprios;
- um VAO e um VBO persistente;
- eixo X vermelho e eixo Y verde;
- liberação dos recursos OpenGL no fechamento.

Os eixos ainda estão definidos diretamente em NDC. Isso é proposital nesta
etapa: permite estudar o pipeline básico antes de introduzir coordenadas de
mundo, matrizes e câmera.

## Execução

```bash
poetry run ex09-pyglet-cad
```

Ao executar, deve aparecer uma janela de 800 × 600 unidades lógicas com fundo
azul-escuro. A opção de DPI `stretch` permite que, em uma tela Retina com escala
2x, o framebuffer OpenGL tenha 1600 × 1200 pixels físicos.

O terminal também informa os tamanhos lógico e físico observados pelo Pyglet.

## Estrutura atual

```text
ex09_pyglet_cad/
├── __init__.py  # Define o pacote Python
├── __main__.py  # Janela, recursos OpenGL, eventos e desenho
├── shaders.py   # Código-fonte GLSL dos dois shaders
└── README.md    # Resumo e estado do subprojeto
```

Por enquanto, os recursos OpenGL permanecem na classe `CADWindow`. Eles serão
extraídos para um renderer somente quando o crescimento do código justificar a
nova abstração.

## Nomenclatura

- **janela da aplicação**: janela do sistema operacional criada por
  `pyglet.window.Window`;
- **tamanho lógico**: dimensões usadas pela janela e pelos eventos da interface;
- **framebuffer**: memória em pixels físicos onde o OpenGL desenha;
- **viewport OpenGL**: retângulo do framebuffer utilizado na renderização;
- **espaço do mundo**: sistema de coordenadas no qual existirão as entidades do
  CAD;
- **câmera 2D**: definição da região do mundo que está visível;
- **NDC**: espaço normalizado do OpenGL, com X e Y entre `-1` e `1` após as
  transformações do vertex shader.

## Pipeline atual

Cada vértice armazenado no VBO possui cinco valores:

```text
x, y, vermelho, verde, azul
```

O VAO descreve ao OpenGL como interpretar esses valores. A posição alimenta o
`location = 0` do vertex shader e a cor alimenta o `location = 1`.

```text
array ctypes na CPU
        │ glBufferData (durante a inicialização)
        ▼
VBO persistente
        │ layout registrado no VAO
        ▼
vertex shader → fragment shader → framebuffer
```

Em cada redesenho, o programa apenas ativa o shader e o VAO e chama:

```python
glDrawArrays(GL_LINES, 0, 4)
```

Os vértices `0–1` formam o eixo X e os vértices `2–3` formam o eixo Y. O VBO
não é reenviado a cada frame.

## Limitações intencionais desta etapa

Ainda não existem:

- coordenadas do mundo;
- projeção ortográfica;
- câmera 2D;
- pan ou zoom;
- conversão de tela para mundo;
- modelo de documento;
- criação interativa de linhas;
- VBO de preview, grade, snap ou seleção.

## Próximas etapas planejadas

1. Definir os eixos em coordenadas do mundo.
2. Introduzir projeção ortográfica para visualizar inicialmente uma região de
   80 × 60 unidades, centrada na origem.
3. Criar o modelo `Document` na CPU.
4. Implementar câmera, pan e zoom.
5. Implementar conversão de coordenadas da tela para o mundo.
6. Criar uma ferramenta interativa de linha.
7. Separar o VBO permanente do VBO dinâmico de preview.
8. Acrescentar grade, snap e seleção em etapas posteriores.

## Conceitos demonstrados até agora

- criação de uma janela com `pyglet.window.Window`;
- solicitação de um contexto OpenGL 3.3;
- limpeza do framebuffer no evento `on_draw`;
- shaders de vértice e fragmento escritos em GLSL;
- armazenamento persistente dos vértices em VAO e VBO;
- desenho dos eixos com `glDrawArrays(GL_LINES)`;
- execução do loop de eventos do Pyglet.
