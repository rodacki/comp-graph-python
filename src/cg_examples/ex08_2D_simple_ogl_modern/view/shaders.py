"""Fontes GLSL usadas pelo renderer do ex08.

Didaticamente, este módulo separa o código de shader em strings nomeadas
para facilitar leitura e manutenção.

Resumo dos shaders:
- Vertex shader: recebe posição 2D em NDC e escreve `gl_Position`.
- Fragment shader: aplica cor uniforme e, opcionalmente, simula linha tracejada.
"""

VERTEX_SHADER_SOURCE = """
#version 330 core
layout (location = 0) in vec2 a_pos;

void main() {
    gl_Position = vec4(a_pos, 0.0, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
out vec4 FragColor;
uniform vec3 u_color;
uniform int u_use_dashed;
uniform float u_dash_length;
uniform float u_gap_length;

void main() {
    // Em core profile, line stipple legado não está disponível.
    // Este padrão simples usa coordenadas de tela para simular traçado.
    // É suficiente para fins didáticos, embora não preserve "comprimento real"
    // em unidade de mundo quando há redimensionamento.
    if (u_use_dashed == 1) {
        float period = u_dash_length + u_gap_length;
        float t = mod(gl_FragCoord.x + gl_FragCoord.y, period);
        if (t > u_dash_length) {
            discard;
        }
    }
    FragColor = vec4(u_color, 1.0);
}
"""
