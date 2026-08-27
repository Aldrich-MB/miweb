# conversor_avanzado.py
# Módulo con funciones de conversión avanzadas

from conversor import texto_a_binario, binario_a_texto, texto_a_hexadecimal, hexadecimal_a_texto

def texto_a_base64(texto):
    """
    Convierte texto a Base64 (codificación estándar)
    Ejemplo: "Hola" -> "SG9sYQ=="
    """
    import base64
    texto_bytes = texto.encode('utf-8')
    base64_bytes = base64.b64encode(texto_bytes)
    return base64_bytes.decode('utf-8')


def base64_a_texto(base64_str):
    """
    Convierte Base64 a texto
    Ejemplo: "SG9sYQ==" -> "Hola"
    """
    import base64
    base64_bytes = base64_str.encode('utf-8')
    texto_bytes = base64.b64decode(base64_bytes)
    return texto_bytes.decode('utf-8')


def texto_a_binario_con_espacios(texto, separador=' '):
    """
    Convierte texto a binario con separador personalizado
    """
    binario = texto_a_binario(texto)
    return binario.replace(' ', separador)


def binario_con_espacios_a_texto(binario_str, separador=' '):
    """
    Convierte binario con separador personalizado a texto
    """
    # Reemplazar separador por espacio
    binario_normalizado = binario_str.replace(separador, ' ')
    return binario_a_texto(binario_normalizado)


def texto_a_octal(texto):
    """
    Convierte texto a octal
    Ejemplo: "Hola" -> "110 157 154 141"
    """
    if not texto:
        return ""
    
    resultado = []
    for caracter in texto:
        codigo_ascii = ord(caracter)
        if codigo_ascii > 255:
            raise ValueError(f"Caracter no compatible con ASCII: '{caracter}'")
        octal = format(codigo_ascii, 'o')
        resultado.append(octal.zfill(3))  # Asegurar 3 dígitos
    
    return ' '.join(resultado)


def octal_a_texto(octal_str):
    """
    Convierte octal a texto
    Ejemplo: "110 157 154 141" -> "Hola"
    """
    if not octal_str:
        return ""
    
    octal_limpio = octal_str.strip().split()
    resultado = []
    
    for octal in octal_limpio:
        try:
            codigo_ascii = int(octal, 8)
            if codigo_ascii > 255:
                raise ValueError(f"Código ASCII fuera de rango: {codigo_ascii}")
            resultado.append(chr(codigo_ascii))
        except ValueError:
            raise ValueError(f"Octal inválido: {octal}")
    
    return ''.join(resultado)


def detectar_formato_avanzado(entrada):
    """
    Detecta el formato de una cadena (incluye octal y base64)
    """
    entrada_limpia = entrada.strip()
    
    if not entrada_limpia:
        return 'texto'
    
    # Detectar Base64 (contiene A-Z, a-z, 0-9, +, /, =)
    if all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in entrada_limpia):
        if len(entrada_limpia) % 4 == 0:
            try:
                # Intentar decodificar para confirmar
                import base64
                base64.b64decode(entrada_limpia)
                return 'base64'
            except:
                pass
    
    # Detectar binario (0s y 1s)
    if all(c in '01 ' for c in entrada_limpia):
        grupos = entrada_limpia.split()
        if grupos and all(len(g) in [7, 8] for g in grupos):
            return 'binario'
    
    # Detectar octal (0-7 separados por espacios)
    if all(c in '01234567 ' for c in entrada_limpia):
        grupos = entrada_limpia.split()
        if grupos and all(len(g) in [1, 2, 3] for g in grupos):
            return 'octal'
    
    # Detectar hexadecimal
    if all(c in '0123456789ABCDEFabcdef ' for c in entrada_limpia):
        sin_espacios = entrada_limpia.replace(' ', '')
        if len(sin_espacios) % 2 == 0 and len(sin_espacios) > 2:
            return 'hexadecimal'
    
    return 'texto'