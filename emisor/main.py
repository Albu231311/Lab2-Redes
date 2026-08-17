

import argparse
import sys

from aplicacion import solicitar_mensaje
from presentacion import codificar_mensaje
from enlace import calcular_integridad
from ruido import aplicar_ruido
from transmision import enviar_informacion


def ejecutar_envio(texto: str, algoritmo: str, prob_error: float,
                    host: str, port: int, verbose: bool = True) -> dict:
    
    #Ejecuta el flujo completo de envio y regresa un dict con toda la
    #informacion intermedia (util para logging / pruebas / graficas).
    
    mensaje_binario = codificar_mensaje(texto)
    trama_integridad = calcular_integridad(mensaje_binario, algoritmo)
    trama_con_ruido, posiciones_alteradas = aplicar_ruido(trama_integridad, prob_error)

    if verbose:
        print(f"\n--- Resumen de envio ---")
        print(f"Texto original:        {texto!r}")
        print(f"Binario (Presentacion): {mensaje_binario}")
        print(f"Algoritmo:              {algoritmo}")
        print(f"Trama con redundancia:  {trama_integridad}  ({len(trama_integridad)} bits)")
        print(f"Trama con ruido:        {trama_con_ruido}")
        print(f"Bits alterados:         {len(posiciones_alteradas)} -> posiciones {posiciones_alteradas}")

    enviar_informacion(
        host=host,
        port=port,
        algoritmo=algoritmo,
        longitud_original=len(mensaje_binario),
        trama=trama_con_ruido,
    )

    if verbose:
        print(f"Trama enviada a {host}:{port}")

    return {
        "texto": texto,
        "algoritmo": algoritmo,
        "prob_error": prob_error,
        "mensaje_binario": mensaje_binario,
        "longitud_original": len(mensaje_binario),
        "trama_integridad": trama_integridad,
        "overhead_bits": len(trama_integridad) - len(mensaje_binario),
        "trama_con_ruido": trama_con_ruido,
        "bits_alterados": len(posiciones_alteradas),
        "posiciones_alteradas": posiciones_alteradas,
    }


def main():
    parser = argparse.ArgumentParser(description="Emisor - Lab #2 Redes")
    parser.add_argument("--texto", type=str, help="Mensaje a enviar")
    parser.add_argument("--algoritmo", type=str, choices=["hamming", "crc32"])
    parser.add_argument("--prob-error", type=float, help="Probabilidad de error por bit (ej. 0.01)")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5005)
    args = parser.parse_args()

    if args.texto is not None and args.algoritmo is not None and args.prob_error is not None:
        # Modo no interactivo (usado por pruebas.py)
        ejecutar_envio(args.texto, args.algoritmo, args.prob_error, args.host, args.port)
    else:
        # Modo interactivo normal
        datos = solicitar_mensaje()
        try:
            ejecutar_envio(
                datos["texto"], datos["algoritmo"], datos["prob_error"],
                datos["host"], datos["port"],
            )
        except (ConnectionRefusedError, TimeoutError) as e:
            print(f"\nERROR: no se pudo conectar al receptor en "
                  f"{datos['host']}:{datos['port']} -> {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
