import math
import random

# Sea X ∼ Exp(λ):
# El algoritmo para simular X es:
# 1. Generar U ∼ U(0,1)
# 2. return X = −(1/λ) * ln(U)
# usando el M´etodo de la transformada inversa

# generate exponential var with parameter lambda
def gen_exp(lambd):
    U = random.random()  # uniform(0,1)
    return -(1 / lambd) * math.log(U)


# Para simular Z ∼ N(0, 1), se puede usar el m´etodo de los rechazos. Como la
# funci´on de densidad de Z es par, para simplificar el procedimiento se simula X = |Z|.
# Algoritmo para simular X:
# 1. Generar Y ∼ Exp(1)
# 2. Generar U ∼ U(0, 1)
# 3. if U ≤ e^((−(Y −1)^2)/2) return X = Y
# 4. else volver al paso 1
# Para simular los valores de Z con probabilidad 1/2
# devuelve X, y con probabilidad 1/2
# devuelve -X
# usando el el m´etodo de los rechazos

# generate normal var with parameters media = 0 and variance=1(standard normal)
def gen_std_normal():
    while True:
        Y = gen_exp(1)  # exponential(1)
        U = random.random()  # uniform(0,1)
        if U <= math.exp(-((Y - 1) ** 2) / 2):
            X = Y
            U = random.random()  # uniform(0,1)
            if U <= 0.5:
                return X
            return -X


# Si X ∼ N(µ, σ2) entonces:
# Z =(X − µ)/σ∼ N(0, 1)
# Luego para generar una normal X con parámetros µ y σ2
# se genera una normal estándar Z y se calcula:
# X = Z*σ + µ

# generate normal var with parameter med: media and var: variance
def gen_normal(med, var):
    return gen_std_normal() * math.sqrt(var) + med
