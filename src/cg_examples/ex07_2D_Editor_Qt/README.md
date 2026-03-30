# Ex07 – 2D Editor com PyQt5 e OpenGL

## Descrição

O subprojeto ex07_2D_Editor_Qt é um editor gráfico 2D desenvolvido em Python, utilizando PyQt5 para a interface gráfica e PyOpenGL para renderização interativa. O sistema demonstra conceitos de arquitetura MVC (Model–View–Controller) e o padrão de projeto State, permitindo desenhar, selecionar e manipular formas geométricas básicas em um canvas OpenGL.

Este projeto é parte do repositório comp-graph-python, que reúne exemplos de Computação Gráfica desenvolvidos para fins didáticos.

---

## Estrutura do Projeto

```
ex07_2D_Editor_Qt/
│
├── __main__.py              # Ponto de entrada da aplicação
├── mainwindow.py            # Janela principal (QMainWindow)
│
├── globals/
│   └── settings.py          # Definições globais e parâmetros de renderização
│
├── model/                   # Camada de modelo (dados geométricos)
│   ├── ponto.py             # Classe Ponto
│   ├── circulo.py           # Classe Circulo
│   ├── poligono.py          # Classe Poligono
│   └── modelo.py            # Agregador de objetos da cena
│
├── state/                   # Estados do editor (State Pattern)
│   ├── abstract_state.py    # Classe base para estados
│   ├── context.py           # Contexto que gerencia os estados
│   ├── idle_state.py        # Estado ocioso (seleção)
│   ├── draw_circle_state.py # Estado de criação de círculos
│   └── draw_polygon_state.py# Estado de criação de polígonos
│
├── view/                    # Camada de visualização (renderização e UI)
│   ├── glcanvas.py          # Canvas OpenGL (subclasse de QOpenGLWidget)
│   ├── renderers.py         # Funções de desenho OpenGL (círculos, polígonos, eixos, etc.)
│   ├── draw_utils.py        # Conversões e utilitários de desenho
│   └── selection_render.py  # Destaques e efeitos de seleção
│
└── utils/
    └── floatcmp.py          # Comparações de ponto flutuante tolerantes a erro numérico
```

---

## ⚙️ Execução

### Pré-requisitos
- Python ≥ 3.11
- Poetry (para gerenciamento de dependências)

### Instalação

```bash
poetry install
```

### Execução do editor

```bash
poetry run ex07-pyqt-opengl
```

---

## 🧠 Conceitos-Chave

#### 🔸 MVC (Model–View–Controller)

O sistema está organizado em três camadas principais:
- 	Model — Representa os dados geométricos (pontos, círculos, polígonos).
- 	View — Gerencia a renderização OpenGL e a interação visual.
- 	Controller — Implementado indiretamente pelo padrão State, controlando o comportamento do editor conforme o modo ativo.

### 🔸 Padrão State

Cada modo de operação (idle, desenhar círculo, desenhar polígono) é encapsulado em uma classe de estado, que reage de maneira específica aos eventos do mouse e teclado. O objeto Context gerencia a transição entre estados e mantém o estado atual.

---

## 🖱️ Funcionalidades Principais
-	Desenho interativo de polígonos e círculos.
-	Seleção e destaque visual de objetos.
-	Finalização de polígonos com duplo clique, botão direito ou Enter.
-	Cancelamento de ações com Esc.
-	Renderização com anti-aliasing e linhas pontilhadas para pré-visualização.

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo LICENSE no diretório raiz do repositório.

---

## 👨‍💻 Autor

Prof. Paulo Rodacki
Instituto Federal Catarinense (IFC)
Projeto: Computação Gráfica com Python

---

### 🔍 Próximos Passos
- Implementar transformações geométricas (translação, rotação, escala).
- Adicionar ferramentas de manipulação interativa (arrastar, girar, redimensionar).
- Introduzir sistema de camadas (layers) e suporte a gravação de cena.


