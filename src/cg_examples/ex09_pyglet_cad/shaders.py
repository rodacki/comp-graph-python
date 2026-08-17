"""Shaders GLSL usados para desenhar os eixos do sistema de coordenadas."""

VERTEX_SHADER_SOURCE = """
#version 330 core

// Os locations correspondem aos índices usados em glVertexAttribPointer.
layout (location = 0) in vec2 position;
layout (location = 1) in vec3 color;

// Valor enviado deste vertex shader para o fragment shader.
out vec3 vertex_color;

void main()
{
    // A posição já está em NDC nesta etapa. Acrescentamos z=0 e w=1 para
    // formar o vec4 exigido por gl_Position.
    gl_Position = vec4(position, 0.0, 1.0);

    // A cor de cada vértice segue para a próxima etapa do pipeline.
    vertex_color = color;
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core

in vec3 vertex_color;
out vec4 fragment_color;

void main()
{
    // Usa a cor RGB recebida e acrescenta alpha=1 (totalmente opaco).
    fragment_color = vec4(vertex_color, 1.0);
}
"""
