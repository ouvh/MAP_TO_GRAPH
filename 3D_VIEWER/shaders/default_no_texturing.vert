#version 330 core

layout (location = 0) in vec3 in_normal;
layout (location = 1) in vec3 in_position;

out vec3 normal;
out vec3 fragPos;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;


void main() {
    
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}