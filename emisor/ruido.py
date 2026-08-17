
import random


def aplicar_ruido(trama: str, prob_error: float):
    
    #trama: string de '0'/'1' (mensaje + redundancia)
    #prob_error: probabilidad de que UN bit individual sea alterado
                

    #Regresa una tupla (trama_con_ruido, posiciones_alteradas) para
    #poder loggear / graficar cuantos y cuales bits cambiaron.
    
    if not (0 <= prob_error <= 1):
        raise ValueError("prob_error debe estar entre 0 y 1")

    resultado = []
    posiciones_alteradas = []

    for i, bit in enumerate(trama):
        if random.random() < prob_error:
            nuevo_bit = "1" if bit == "0" else "0"
            posiciones_alteradas.append(i)
        else:
            nuevo_bit = bit
        resultado.append(nuevo_bit)

    return "".join(resultado), posiciones_alteradas


if __name__ == "__main__":
    trama = "0110011"
    con_ruido, alteradas = aplicar_ruido(trama, 0.3)
    print(f"trama original:  {trama}")
    print(f"trama con ruido: {con_ruido}")
    print(f"bits alterados en posiciones: {alteradas}")
