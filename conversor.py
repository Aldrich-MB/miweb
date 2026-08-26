# conversor.py
# Módulo con funciones de conversión entre texto y sistemas numéricos

def texto_a_binario(texto):
    """
    Convierte un texto a binario (ASCII de 8 bits)
    Ejemplo: "Hola" -> "01001000 01101111 01101100 01100001"
    """
    if not texto:
        return ""
    
    resultado = []
    for caracter in texto:
        # Obtener código ASCII y convertirlo a binario de 8 bits
        codigo_ascii = ord(caracter)
        binario = format(codigo_ascii, '08b')  # 08b = 8 bits con ceros a la izquierda
        resultado.append(binario)
    
    return ' '.join(resultado)


def binario_a_texto(binario_str):
    """
    Convierte una cadena binaria (separada por espacios) a texto
    Ejemplo: "01001000 01101111 01101100 01100001" -> "Hola"
    """
    if not binario_str:
        return ""
    
    # Eliminar espacios extra y separar por espacios
    binario_limpio = binario_str.strip().split()
    
    resultado = []
    for binario in binario_limpio:
        # Validar que solo tenga 0s y 1s
        if not all(c in '01' for c in binario):
            raise ValueError(f"Caracter inválido en binario: {binario}")
        
        # Convertir de binario a entero y luego a carácter ASCII
        codigo_ascii = int(binario, 2)
        caracter = chr(codigo_ascii)
        resultado.append(caracter)
    
    return ''.join(resultado)


def texto_a_hexadecimal(texto):
    """
    Convierte texto a hexadecimal
    Ejemplo: "Hola" -> "486F6C61"
    """
    if not texto:
        return ""
    
    resultado = []
    for caracter in texto:
        hex_val = format(ord(caracter), '02X')  # 02X = 2 dígitos hexadecimales mayúsculas
        resultado.append(hex_val)
    
    return ''.join(resultado)


def hexadecimal_a_texto(hex_str):
    """
    Convierte hexadecimal a texto
    Ejemplo: "486F6C61" -> "Hola"
    """
    if not hex_str:
        return ""
    
    # Limpiar espacios y convertir a lista de pares
    hex_limpio = hex_str.replace(' ', '').replace('0x', '')
    
    # Si es longitud impar, agregar cero a la izquierda
    if len(hex_limpio) % 2 != 0:
        hex_limpio = '0' + hex_limpio
    
    resultado = []
    for i in range(0, len(hex_limpio), 2):
        par_hex = hex_limpio[i:i+2]
        try:
            codigo_ascii = int(par_hex, 16)
            caracter = chr(codigo_ascii)
            resultado.append(caracter)
        except ValueError:
            raise ValueError(f"Hexadecimal inválido: {par_hex}")
    
    return ''.join(resultado)


# Función de utilidad para detectar automáticamente si es binario o texto
def detectar_formato(entrada):
    """
    Detecta si una cadena es binario (0s y 1s separados por espacios)
    o texto normal
    """
    entrada_limpia = entrada.strip()
    
    # Si tiene solo 0s, 1s y espacios, probablemente es binario
    if all(c in '01 ' for c in entrada_limpia):
        # Verificar que cada grupo tenga 8 dígitos (opcional pero útil)
        grupos = entrada_limpia.split()
        if all(len(g) == 8 for g in grupos):
            return 'binario'
        elif all(len(g) <= 8 for g in grupos):
            return 'binario'  # Aceptar binarios de longitud variable
    
    # Si tiene solo dígitos hexadecimales (0-9A-F) sin espacios largos
    if all(c in '0123456789ABCDEFabcdef ' for c in entrada_limpia):
        # Verificar si es un texto hexadecimal válido (longitud par sin espacios)
        sin_espacios = entrada_limpia.replace(' ', '')
        if len(sin_espacios) % 2 == 0 and len(sin_espacios) > 2:
            return 'hexadecimal'
    
    return 'texto'