import math

from MathLib import matrix_multiply, vector_matrix_multiply, barycentricCoords


def vertexShader(vertex, **kwargs):

    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    # Agregar el componente W al vértice
    vt = [vertex[0], vertex[1], vertex[2], 1]

    # Transformar el vértice por las matrices en el orden correcto
    vt = vector_matrix_multiply(vt, matrix_multiply(
        matrix_multiply(
            matrix_multiply(viewportMatrix, projectionMatrix),
            viewMatrix),
        modelMatrix))

    # Normalizar las coordenadas homogéneas si es necesario
    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]

    return vt


def fragmentShader(**kwargs):

    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs.get("texture", None)
    dirLight = kwargs["dirLight"]

    # Interpolar las coordenadas de textura y normales
    interpolatedTexCoords = [
        u * A[3] + v * B[3] + w * C[3],  # Asumiendo que A, B, C tienen coordenadas de textura en el índice 3
        u * A[4] + v * B[4] + w * C[4]  # Asumiendo que A, B, C tienen normales en el índice 4
    ]

    # Si hay una textura, obtener el color de la textura y aplicarlo
    if texture:
        texColor = texture.get_color(interpolatedTexCoords)  # Método get_color de la textura
    else:
        texColor = [1, 1, 1]  # Color blanco por defecto si no hay textura

    # Aplicar la dirección de la luz y la textura interpolada
    color = [
        texColor[0] * dirLight[0],
        texColor[1] * dirLight[1],
        texColor[2] * dirLight[2]
    ]

    return color


def flatShader(**kwargs):

    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs.get("texture", None)
    dirLight = kwargs["dirLight"]

    # Interpolar las coordenadas de textura
    interpolatedTexCoords = [
        u * A[3] + v * B[3] + w * C[3],
        u * A[4] + v * B[4] + w * C[4]
    ]

    # Si hay una textura, obtener el color de la textura y aplicarlo
    if texture:
        texColor = texture.get_color(interpolatedTexCoords)
    else:
        texColor = [1, 1, 1]  # Blanco por defecto si no hay textura

    # Devolver el color sin aplicar efectos adicionales (flat shading)
    color = [
        texColor[0] * dirLight[0],
        texColor[1] * dirLight[1],
        texColor[2] * dirLight[2]
    ]

    return color

def stripedShader(**kwargs):

    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]

    # Interpolate the Y-coordinate
    y = u * A[1] + v * B[1] + w * C[1]

    # Use a sinusoidal function to create stripes
    frequency = 20.0
    stripes = math.sin(y * frequency)

    # Map the stripes to a color pattern
    if stripes > 0:
        color = [1, 0, 0]  # Red
    else:
        color = [0, 1, 0]  # Green

    return color


def toonShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    dirLight = kwargs["dirLight"]

    normal = [
        u * A[5] + v * B[5] + w * C[5],
        u * A[6] + v * B[6] + w * C[6],
        u * A[7] + v * B[7] + w * C[7]
    ]

    norm = (normal[0]**2 + normal[1]**2 + normal[2]**2) ** 0.5
    normal = [normal[i] / norm for i in range(3)]

    intensity = max(0, sum([normal[i] * dirLight[i] for i in range(3)]))

    if intensity > 0.95:
        color = [1, 1, 1]  # Bright color
    elif intensity > 0.5:
        color = [0.6, 0.6, 0.6]  # Mid-tone color
    else:
        color = [0.3, 0.3, 0.3]  # Dark tone color

    return color
