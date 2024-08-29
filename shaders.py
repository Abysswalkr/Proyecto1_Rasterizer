import math

from MathLib import *


def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    if len(vertex) + 1 == len(modelMatrix):
        vt = vertex + [1]
    else:
        vt = vertex

    vpMatrix_projectMatrix = matrix_multiply(viewportMatrix, projectionMatrix)

    vpMatrix_projectMatrix_viewMatrix = matrix_multiply(vpMatrix_projectMatrix, viewMatrix)

    vpMatrix_projectMatrix_viewMatrix_model = matrix_multiply(vpMatrix_projectMatrix_viewMatrix, modelMatrix)

    vt = vector_matrix_multiply(vt, vpMatrix_projectMatrix_viewMatrix_model)

    if len(vt) > 3:
        vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]

    return vt


def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual

    # Obtenemos la informacion requeridavt
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    # sabiendo que las coordenadas de textura estan en 4 y quinta posicion del indice del vertice
    # las obtenemos y guardamos

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nB = [C[5], C[6], C[7]]

    r = 1
    g = 1
    b = 1

    # P = uA + vV + wC
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    # Se regresa el color
    return [r, g, b]


def metalShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Interpolación de coordenadas de textura
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Color base metálico (brillante plateado)
    r, g, b = 0.9, 0.9, 0.9

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0] * 0.7 + 0.3  # Ajustado para reflejo metálico brillante
        g *= texColor[1] * 0.7 + 0.3
        b *= texColor[2] * 0.7 + 0.3

    # Reflejo metálico intenso y brillo elevado
    reflection_intensity = 1.0  # Intensidad máxima de reflejo
    reflection_color = 1.0  # Puro blanco para un brillo intenso

    # Añadiendo un reflejo especular fuerte
    r = min(1.0, r * (1.0 - reflection_intensity) + reflection_color * reflection_intensity)
    g = min(1.0, g * (1.0 - reflection_intensity) + reflection_color * reflection_intensity)
    b = min(1.0, b * (1.0 - reflection_intensity) + reflection_color * reflection_intensity)

    # Variación ligera para simular pequeñas imperfecciones pulidas
    imperfection = (u * 0.01 + v * 0.01 + w * 0.01) % 0.01
    r = max(0, r - imperfection * 0.5)
    g = max(0, g - imperfection * 0.5)
    b = max(0, b - imperfection * 0.5)

    return [r, g, b]

def rgbLightShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Interpolación de coordenadas de textura
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Variación RGB basada en las coordenadas de textura
    r = (vtP[0] % 1.0) * 1.0  # Componente roja
    g = (vtP[1] % 1.0) * 1.0  # Componente verde
    b = ((u + v + w) % 1.0) * 1.0  # Componente azul

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    # Asegurarse de que los valores están dentro del rango [0, 1]
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return [r, g, b]

def blueRedStripesShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Interpolación de coordenadas de textura
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Parámetro para determinar el grosor de las franjas
    stripe_width = 0.1

    # Determinación del color basado en la posición
    stripe_pattern = int(vtP[0] / stripe_width) % 2  # Alterna entre 0 y 1

    if stripe_pattern == 0:
        r, g, b = 0.0, 0.0, 1.0  # Azul
    else:
        r, g, b = 1.0, 0.0, 0.0  # Rojo

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    # Añadir un efecto de mezcla en las zonas de transición
    transition = (vtP[0] % stripe_width) / stripe_width
    if stripe_pattern == 0:
        r = r * (1 - transition) + 1.0 * transition  # Mezcla azul a rojo
        g = g * (1 - transition)
        b = b * (1 - transition) + 0.0 * transition
    else:
        r = r * (1 - transition) + 0.0 * transition  # Mezcla rojo a azul
        g = g * (1 - transition)
        b = b * (1 - transition) + 1.0 * transition

    return [r, g, b]

def hologramShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Interpolación de coordenadas de textura
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Calcula un color base que cambia en función de la posición
    r = 0.5 + 0.5 * (u + v + w) % 1.0  # Componente roja
    g = 0.5 + 0.5 * (1.0 - vtP[0] % 1.0)  # Componente verde
    b = 0.5 + 0.5 * (1.0 - vtP[1] % 1.0)  # Componente azul

    # Efecto de "brillo" basado en la posición
    brightness = abs(math.sin(vtP[0] * 10.0) * math.cos(vtP[1] * 10.0))
    r *= brightness
    g *= brightness
    b *= brightness

    # Interacción con la textura
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r = min(1.0, r * texColor[0])
        g = min(1.0, g * texColor[1])
        b = min(1.0, b * texColor[2])

    # Añadir un leve desenfoque para simular la dispersión de la luz en un holograma
    blur_factor = 0.1
    r = r * (1.0 - blur_factor) + blur_factor
    g = g * (1.0 - blur_factor) + blur_factor
    b = b * (1.0 - blur_factor) + blur_factor

    return [r, g, b]

import math

def fireAndSmokeShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Interpolación de coordenadas de textura
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Simulación de partículas de fuego
    # Generación de ruido para la animación del fuego
    noise = math.sin(vtP[1] * 10.0 + math.sin(vtP[0] * 10.0)) * 0.5 + 0.5

    # Color del fuego (naranja-amarillo) y humo (gris)
    if noise > 0.5:
        # Fuego
        r = min(1.0, noise + 0.5)
        g = noise * 0.5
        b = 0.0
    else:
        # Humo
        r = g = b = noise * 0.5 + 0.3

    # Mezcla con la textura si está disponible
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r = min(1.0, r * texColor[0])
        g = min(1.0, g * texColor[1])
        b = min(1.0, b * texColor[2])

    # Efecto de dispersión
    dispersion = abs(math.sin(vtP[0] * 20.0) * math.cos(vtP[1] * 20.0))
    r *= dispersion
    g *= dispersion
    b *= dispersion

    return [r, g, b]

import math

def waterShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Interpolación de coordenadas de textura
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Parámetros de ondas
    wave_speed = 2.0  # Velocidad de las ondas
    wave_amplitude = 0.1  # Amplitud de las ondas
    wave_frequency = 10.0  # Frecuencia de las ondas

    # Simulación del movimiento de las ondas
    time = kwargs.get("time", 0)  # Parámetro de tiempo para animar el agua
    wave_x = math.sin(vtP[0] * wave_frequency + time * wave_speed) * wave_amplitude
    wave_y = math.cos(vtP[1] * wave_frequency + time * wave_speed) * wave_amplitude

    # Combina las ondas en ambas direcciones
    wave = wave_x + wave_y

    # Color base del agua (azul claro con transparencia)
    r = 0.1 + wave * 0.1
    g = 0.5 + wave * 0.2
    b = 0.7 + wave * 0.3

    # Simulación de reflejos y refracciones
    reflection_intensity = 0.8
    refraction_intensity = 0.6

    # Reflejos y refracciones se calculan mediante la manipulación de colores
    reflection = reflection_intensity * (1.0 - vtP[1])
    refraction = refraction_intensity * vtP[1]

    r = r * reflection + refraction
    g = g * reflection + refraction
    b = b * reflection + refraction

    # Mezcla con la textura si está disponible
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r = min(1.0, r * texColor[0])
        g = min(1.0, g * texColor[1])
        b = min(1.0, b * texColor[2])

    # Limitar los valores de color entre 0 y 1
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return [r, g, b]

import math

def heatDistortionShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Interpolación de coordenadas de textura
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Parámetros de distorsión
    distortion_strength = 0.02  # Intensidad de la distorsión
    wave_frequency = 30.0  # Frecuencia de las ondas de calor
    wave_amplitude = 0.05  # Amplitud de las ondas de calor

    # Simulación de las ondas de calor en el aire
    time = kwargs.get("time", 0)  # Parámetro de tiempo para animar el efecto
    distortion_x = math.sin(vtP[0] * wave_frequency + time) * wave_amplitude
    distortion_y = math.cos(vtP[1] * wave_frequency + time) * wave_amplitude

    # Aplicar la distorsión a las coordenadas de la textura
    distorted_vtP = [vtP[0] + distortion_x * distortion_strength, vtP[1] + distortion_y * distortion_strength]

    # Obtener el color de la textura en la coordenada distorsionada
    if texture:
        texColor = texture.getColor(distorted_vtP[0], distorted_vtP[1])
    else:
        texColor = [1.0, 1.0, 1.0]  # Color blanco por defecto si no hay textura

    # Atenuar ligeramente los colores para dar un efecto de calor
    attenuation = 0.9
    r = texColor[0] * attenuation
    g = texColor[1] * attenuation
    b = texColor[2] * attenuation

    # Variación de brillo para simular la distorsión por calor
    brightness_variation = math.sin(vtP[1] * 10.0 + time * 5.0) * 0.1
    r += brightness_variation
    g += brightness_variation
    b += brightness_variation

    # Limitar los valores de color entre 0 y 1
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return [r, g, b]

import math

def dissolveShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]

    # Interpolación de coordenadas de textura
    vtA, vtB, vtC = [A[3], A[4]], [B[3], B[4]], [C[3], C[4]]
    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0], u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Parámetro de disolución (se puede animar este valor para el efecto)
    dissolve_threshold = kwargs.get("dissolve_threshold", 0.5)  # 0.0 a 1.0
    edge_width = 0.1  # Grosor del borde de disolución
    edge_color = [1.0, 0.5, 0.0]  # Color del borde (naranja-rojizo para simular quema)

    # Generación de ruido para la disolución
    noise = math.sin(vtP[0] * 10.0 + math.cos(vtP[1] * 10.0)) * 0.5 + 0.5

    # Obtener el color de la textura
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
    else:
        texColor = [1.0, 1.0, 1.0]  # Color blanco por defecto si no hay textura

    # Aplicar la disolución en función del ruido y el umbral
    if noise < dissolve_threshold:
        # Dentro del rango de disolución, desvanecer el color
        r = texColor[0] * (noise / dissolve_threshold)
        g = texColor[1] * (noise / dissolve_threshold)
        b = texColor[2] * (noise / dissolve_threshold)
    else:
        # En el borde de disolución, aplicar el color del borde
        edge_factor = (noise - dissolve_threshold) / edge_width
        r = edge_color[0] * edge_factor + texColor[0] * (1 - edge_factor)
        g = edge_color[1] * edge_factor + texColor[1] * (1 - edge_factor)
        b = edge_color[2] * edge_factor + texColor[2] * (1 - edge_factor)

    # Limitar los valores de color entre 0 y 1
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return [r, g, b]

