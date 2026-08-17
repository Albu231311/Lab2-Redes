
CRC32_POLY_STD = 0x04C11DB7          # polinomio estandar, 32 bits
CRC32_POLY_FULL = 0x104C11DB7        # con el bit lider (grado 32) explicito
POLY_BITLEN = 33                     # longitud en bits de CRC32_POLY_FULL


def _pad_mensaje(data_bits: str) -> str:
    #Garantiza n > 32 rellenando con ceros a la izquierda si hace falta
    if len(data_bits) <= 32:
        return data_bits.zfill(33)
    return data_bits


def crc32_encode(data_bits: str) -> str:
    
    #Recibe un string de '0'/'1' y regresa data_bits (con padding si aplico)
    #+ 32 bits de residuo CRC-32 concatenados al final.
    
    if not data_bits or any(b not in "01" for b in data_bits):
        raise ValueError("data_bits debe ser un string no vacio de '0'/'1'")

    data_bits = _pad_mensaje(data_bits)

    # Mensaje aumentado: se le agregan 32 ceros al final (equivalente a
    # multiplicar el mensaje por x^32) para poder calcular el residuo.
    augmented = [int(b) for b in data_bits] + [0] * 32
    poly_bits = [int(b) for b in format(CRC32_POLY_FULL, "033b")]

    n = len(poly_bits)
    largo_mensaje = len(data_bits)

    for i in range(largo_mensaje):
        if augmented[i] == 1:
            for j in range(n):
                augmented[i + j] ^= poly_bits[j]

    residuo = "".join(str(b) for b in augmented[-32:])
    return data_bits + residuo


if __name__ == "__main__":
    # Sanity check: el residuo de un mensaje sobre si mismo (mensaje+crc)
    # dividido entre el polinomio debe dar 0 -> es la propiedad que el
    # receptor usara para verificar integridad.
    msg = "0100000101000010"  # "AB" en ASCII binario (16 bits)
    codificado = crc32_encode(msg)
    print(f"mensaje original ({len(msg)} bits): {msg}")
    print(f"codificado ({len(codificado)} bits):  {codificado}")

    # Verificacion: dividir 'codificado' completo entre el polinomio
    # debe dar residuo 0
    bits = [int(b) for b in codificado]
    poly_bits = [int(b) for b in format(CRC32_POLY_FULL, "033b")]
    n = len(poly_bits)
    for i in range(len(bits) - 32):
        if bits[i] == 1:
            for j in range(n):
                bits[i + j] ^= poly_bits[j]
    residuo_final = "".join(str(b) for b in bits[-32:])
    print(f"residuo al re-verificar: {residuo_final}")
    assert residuo_final == "0" * 32, "El residuo deberia ser 0 (sin errores)"
    print("OK: el mensaje codificado es divisible exactamente por el polinomio")
