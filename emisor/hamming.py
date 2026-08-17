
def _is_power_of_two(x: int) -> bool:
    return x != 0 and (x & (x - 1)) == 0


def _bits_necesarios(m: int) -> int:
    #Encuentra el minimo r tal que (m + r + 1) <= 2^r
    r = 0
    while (m + r + 1) > 2 ** r:
        r += 1
    return r


def hamming_encode(data_bits: str) -> str:
    
    #Recibe un string de '0'/'1' (el mensaje original) y regresa el
    #string de '0'/'1' codificado en Hamming (datos + paridad intercalados).
    
    if not data_bits or any(b not in "01" for b in data_bits):
        raise ValueError("data_bits debe ser un string no vacio de '0'/'1'")

    m = len(data_bits)
    r = _bits_necesarios(m)
    n = m + r

    # Indexado 1..n (se ignora la posicion 0 para que la aritmetica de
    # bits calce directamente con el numero de posicion)
    encoded = [0] * (n + 1)

    data_idx = 0
    for pos in range(1, n + 1):
        if not _is_power_of_two(pos):
            encoded[pos] = int(data_bits[data_idx])
            data_idx += 1

    # Calcular cada bit de paridad
    for i in range(r):
        parity_pos = 2 ** i
        parity_val = 0
        for pos in range(1, n + 1):
            if pos == parity_pos:
                continue
            if pos & parity_pos:
                parity_val ^= encoded[pos]
        encoded[parity_pos] = parity_val

    return "".join(str(b) for b in encoded[1:])


if __name__ == "__main__":
    # Sanity check contra el ejemplo clasico de libro de texto:
    # datos "1011" -> Hamming(7,4) -> "0110011"
    resultado = hamming_encode("1011")
    print(f"hamming_encode('1011') = {resultado}")
    assert resultado == "0110011", "No coincide con el ejemplo de referencia"
    print("OK: coincide con el ejemplo de referencia de Hamming(7,4)")
