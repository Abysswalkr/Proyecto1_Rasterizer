from math import pi, sin, cos, isclose

def barycentricCoords(A, B, C, P):
    areaPCB = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) -
                  (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))

    areaACP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) -
                  (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))

    areaABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) -
                  (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))

    areaABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) -
                  (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    if areaABC == 0:
        return None

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1 and isclose(u + v + w, 1.0):
        return (u, v, w)
    else:
        return None

def TranslationMatrix(x, y, z):
    return [
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]

def ScaleMatrix(x, y, z):
    return [
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]

def RotationMatrix(pitch, yaw, roll):
    pitch = pi / 180 * pitch
    yaw = pi / 180 * yaw
    roll = pi / 180 * roll

    cos_pitch, sin_pitch = cos(pitch), sin(pitch)
    cos_yaw, sin_yaw = cos(yaw), sin(yaw)
    cos_roll, sin_roll = cos(roll), sin(roll)

    # Matriz de rotación combinada
    return [
        [
            cos_yaw * cos_roll,
            cos_yaw * sin_roll * sin_pitch - sin_yaw * cos_pitch,
            cos_yaw * sin_roll * cos_pitch + sin_yaw * sin_pitch,
            0
        ],
        [
            sin_yaw * cos_roll,
            sin_yaw * sin_roll * sin_pitch + cos_yaw * cos_pitch,
            sin_yaw * sin_roll * cos_pitch - cos_yaw * sin_pitch,
            0
        ],
        [
            -sin_roll,
            cos_roll * sin_pitch,
            cos_roll * cos_pitch,
            0
        ],
        [0, 0, 0, 1]
    ]

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix.")

    result = [[0] * len(B[0]) for _ in range(len(A))]

    for i in range(len(A)):
        for k in range(len(B)):
            if A[i][k] != 0:
                for j in range(len(B[0])):
                    result[i][j] += A[i][k] * B[k][j]

    return result

def inversed_matrix(matrix):
    n = len(matrix)

    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    augmented_matrix = [row + identity_row for row, identity_row in zip(matrix, identity)]

    for i in range(n):
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            raise ValueError("Matrix is not invertible.")

        for j in range(2 * n):
            augmented_matrix[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(2 * n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

    inverse_matrix = [row[n:] for row in augmented_matrix]

    return inverse_matrix

def vector_matrix_multiply(vector, matrix):
    if len(matrix[0]) != len(vector):
        raise ValueError("The number of columns in the array must match the size of the vector.")

    result = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] += matrix[i][j] * vector[j]

    return result
