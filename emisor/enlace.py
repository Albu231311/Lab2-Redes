
from hamming import hamming_encode
from crc32 import crc32_encode

ALGORITMOS_VALIDOS = ("hamming", "crc32")


def calcular_integridad(mensaje_binario: str, algoritmo: str) -> str:
    
    #mensaje_binario: string de '0'/'1' proveniente de la capa de Presentacion algoritmo: 'hamming' o 'crc32'

    #Regresa la trama completa (mensaje + redundancia) lista para pasar a la capa de Ruido.
    
    algoritmo = algoritmo.lower().strip()
    if algoritmo == "hamming":
        return hamming_encode(mensaje_binario)
    elif algoritmo == "crc32":
        return crc32_encode(mensaje_binario)
    else:
        raise ValueError(
            f"Algoritmo '{algoritmo}' no soportado. "
            f"Opciones validas: {ALGORITMOS_VALIDOS}"
        )
