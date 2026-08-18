print("Hola Mundo")

#for
for numero in range(1, 6):
    print(f"Esta es la repetición número: {numero}")

# Simulando un do-while en Python
contador = 1

while True:
    print("El número es:", contador)
    contador += 1
    
    # Condición para salir del ciclo
    if contador > 3:
        break