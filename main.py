# main.py
# Programa principal que usa las funciones del módulo conversor

import conversor

def mostrar_menu():
    """Muestra el menú de opciones"""
    print("\n" + "="*50)
    print("  CONVERSOR TEXTO - SISTEMAS NUMÉRICOS")
    print("="*50)
    print("1. Texto a Binario")
    print("2. Binario a Texto")
    print("3. Texto a Hexadecimal")
    print("4. Hexadecimal a Texto")
    print("5. Detección automática de formato")
    print("6. Salir")
    print("="*50)


def main():
    #Función principal del programa
    while True:
        mostrar_menu()
        opcion = input("\nElige una opción (1-6): ").strip()
        
        if opcion == '1':
            # Texto a Binario
            texto = input("Ingresa el texto: ")
            try:
                resultado = conversor.texto_a_binario(texto)
                print(f"\nBinario: {resultado}")
                print(f"   (Longitud: {len(resultado)} caracteres)")
            except Exception as e:
                print(f" Error: {e}")
        
        elif opcion == '2':
            # Binario a Texto
            binario = input("Ingresa el binario (separado por espacios): ")
            try:
                resultado = conversor.binario_a_texto(binario)
                print(f"\nTexto: {resultado}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif opcion == '3':
            # Texto a Hexadecimal
            texto = input("Ingresa el texto: ")
            try:
                resultado = conversor.texto_a_hexadecimal(texto)
                print(f"\nHexadecimal: {resultado}")
                print(f"   (Longitud: {len(resultado)} caracteres)")
            except Exception as e:
                print(f"Error: {e}")
        
        elif opcion == '4':
            # Hexadecimal a Texto
            hex_str = input("Ingresa el hexadecimal (ej: 486F6C61): ")
            try:
                resultado = conversor.hexadecimal_a_texto(hex_str)
                print(f"\nTexto: {resultado}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif opcion == '5':
            # Detección automática
            entrada = input("Ingresa el texto o código: ")
            try:
                formato = conversor.detectar_formato(entrada)
                print(f"\nFormato detectado: {formato.upper()}")
                
                # Convertir automáticamente según el formato detectado
                if formato == 'binario':
                    resultado = conversor.binario_a_texto(entrada)
                    print(f"Traducción a texto: {resultado}")
                elif formato == 'hexadecimal':
                    resultado = conversor.hexadecimal_a_texto(entrada)
                    print(f"Traducción a texto: {resultado}")
                else:
                    # Es texto, mostrar ambas conversiones
                    binario = conversor.texto_a_binario(entrada)
                    hexa = conversor.texto_a_hexadecimal(entrada)
                    print(f"Binario: {binario}")
                    print(f"Hexadecimal: {hexa}")
            except Exception as e:
                print(f" Error: {e}")
        
        elif opcion == '6':
            print("\n ¡Hasta luego! Gracias por usar el conversor.")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")
        
        # Pausa para que el usuario vea el resultado
        input("\nPresiona Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()