
import socket
import json


def enviar_informacion(host: str, port: int, algoritmo: str,
                        longitud_original: int, trama: str) -> None:
    header = json.dumps({
        "algoritmo": algoritmo,
        "longitud_original": longitud_original,
    })

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((host, port))
        s.sendall((header + "\n").encode("utf-8"))
        s.sendall((trama + "\n").encode("utf-8"))
