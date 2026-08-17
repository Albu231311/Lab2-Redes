
import csv
import random
import string

from presentacion import codificar_mensaje
from enlace import calcular_integridad
from ruido import aplicar_ruido

ALGORITMOS = ["hamming", "crc32"]
TAMANOS_MENSAJE = [1, 2, 4, 8, 16, 32, 64, 128]      # en caracteres
PROBABILIDADES_ERROR = [0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1]
REPETICIONES = 20  # por combinacion, para promediar el efecto aleatorio del ruido


def texto_aleatorio(n_chars: int) -> str:
    return "".join(random.choice(string.ascii_letters + " ") for _ in range(n_chars))


def correr_pruebas():
    filas = []
    for algoritmo in ALGORITMOS:
        for n_chars in TAMANOS_MENSAJE:
            for prob in PROBABILIDADES_ERROR:
                for rep in range(REPETICIONES):
                    texto = texto_aleatorio(n_chars)
                    mensaje_binario = codificar_mensaje(texto)
                    trama = calcular_integridad(mensaje_binario, algoritmo)
                    _, alteradas = aplicar_ruido(trama, prob)

                    filas.append({
                        "algoritmo": algoritmo,
                        "tamano_chars": n_chars,
                        "tamano_bits_mensaje": len(mensaje_binario),
                        "tamano_bits_trama": len(trama),
                        "overhead_bits": len(trama) - len(mensaje_binario),
                        "overhead_pct": round(
                            100 * (len(trama) - len(mensaje_binario)) / len(mensaje_binario), 2
                        ),
                        "prob_error": prob,
                        "bits_alterados": len(alteradas),
                        "repeticion": rep,
                    })
    return filas


def guardar_csv(filas, ruta="resultados.csv"):
    if not filas:
        return
    with open(ruta, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=filas[0].keys())
        writer.writeheader()
        writer.writerows(filas)
    print(f"Guardado: {ruta} ({len(filas)} filas)")


def graficar(filas):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from collections import defaultdict

    # Grafica 1: overhead % vs tamano del mensaje, por algoritmo
    overhead_por_algo = defaultdict(dict)
    for fila in filas:
        key = (fila["algoritmo"], fila["tamano_chars"])
        overhead_por_algo[key] = fila["overhead_pct"]  # es constante (no depende del ruido)

    plt.figure(figsize=(8, 5))
    for algoritmo in ALGORITMOS:
        xs = TAMANOS_MENSAJE
        ys = [overhead_por_algo[(algoritmo, n)] for n in xs]
        plt.plot(xs, ys, marker="o", label=algoritmo)
    plt.xlabel("Tamano del mensaje (caracteres)")
    plt.ylabel("Overhead (%)")
    plt.title("Overhead vs. tamano del mensaje, por algoritmo")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("overhead_vs_tamano.png", dpi=150)
    plt.close()

    # Grafica 2: bits alterados promedio vs probabilidad de error
    
    tamano_fijo = TAMANOS_MENSAJE[-1]
    plt.figure(figsize=(8, 5))
    for algoritmo in ALGORITMOS:
        xs = PROBABILIDADES_ERROR
        ys = []
        for prob in xs:
            vals = [
                f["bits_alterados"] for f in filas
                if f["algoritmo"] == algoritmo
                and f["tamano_chars"] == tamano_fijo
                and f["prob_error"] == prob
            ]
            ys.append(sum(vals) / len(vals) if vals else 0)
        plt.plot(xs, ys, marker="o", label=algoritmo)
    plt.xlabel("Probabilidad de error por bit")
    plt.ylabel(f"Bits alterados promedio (mensaje de {tamano_fijo} caracteres)")
    plt.title("Bits alterados vs. probabilidad de error")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("bits_alterados_vs_prob.png", dpi=150)
    plt.close()

    print("Guardado: overhead_vs_tamano.png")
    print("Guardado: bits_alterados_vs_prob.png")


if __name__ == "__main__":
    filas = correr_pruebas()
    guardar_csv(filas)
    graficar(filas)
