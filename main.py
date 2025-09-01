
print("=== CALCULADORA ===")

while True:
    print("\n1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("5. Salir")
    
    opcion = input("\nElige una opción: ")
    
    if opcion == "5":
        print("¡Adiós!")
        break
    
    if opcion in ["1", "2", "3", "4"]:
        num1 = float(input("Primer número: "))
        num2 = float(input("Segundo número: "))
        
        if opcion == "1":
            # TODO: Agregar suma
            print("Suma pendiente")
            
        elif opcion == "2":
            # TODO: Agregar resta
            print("Resta pendiente")
            
        elif opcion == "3":
            # TODO: Agregar multiplicación
            print("Multiplicación pendiente")
            
        elif opcion == "4":
            # TODO: Agregar división
            print("División pendiente")
    
    else:
        print("Opción no válida")