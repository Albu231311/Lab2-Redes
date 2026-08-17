
from enlace import ALGORITMOS_VALIDOS


def solicitar_mensaje() -> dict:
    print("Emisor - Lab #2 Redes")
    texto = input("Mensaje a enviar: ")

    while True:
        algoritmo = input(
            f"Algoritmo a usar {ALGORITMOS_VALIDOS}: "
        ).lower().strip()
        if algoritmo in ALGORITMOS_VALIDOS:
            break
        print(f"Opcion invalida. Elige uno de {ALGORITMOS_VALIDOS}.")

    while True:
        try:
            prob_str = input(
                "Probabilidad de error (ej. 1/100 o 0.01): "
            ).strip()
            if "/" in prob_str:
                num, den = prob_str.split("/")
                prob_error = float(num) / float(den)
            else:
                prob_error = float(prob_str)
            if not (0 <= prob_error <= 1):
                raise ValueError
            break
        except (ValueError, ZeroDivisionError):
            print("Probabilidad invalida, intenta de nuevo (ej. 1/100).")

    host = input("Host del receptor [default: 127.0.0.1]: ").strip() or "127.0.0.1"

    while True:
        port_str = input("Puerto del receptor [default: 5005]: ").strip() or "5005"
        try:
            port = int(port_str)
            break
        except ValueError:
            print("Puerto invalido, debe ser un numero.")

    return {
        "texto": texto,
        "algoritmo": algoritmo,
        "prob_error": prob_error,
        "host": host,
        "port": port,
    }
