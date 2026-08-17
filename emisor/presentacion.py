

def codificar_mensaje(texto: str) -> str:
    
    #Convierte un string de texto a su representacion ASCII binaria
    #(8 bits por caracter, concatenados).
    #Ej: 'A' -> '01000001'
    
    return "".join(format(ord(c), "08b") for c in texto)


if __name__ == "__main__":
    resultado = codificar_mensaje("A")
    print(f"codificar_mensaje('A') = {resultado}")
    assert resultado == "01000001"
    print("OK")
