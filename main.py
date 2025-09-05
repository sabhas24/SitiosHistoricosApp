from src import operaciones
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
            print("El resultado es:", num1 + num2)
            
        elif opcion == "2":
            print("El resultado es:", operaciones.restar(num1, num2))
            
        elif opcion == "3":
            print("El resultado es:", operaciones.multiplicar(num1, num2))
            
        elif opcion == "4":
            print("El resultado es:", operaciones.dividir(num1, num2))
    
    else:
        print("Opción no válida")