import random
import time

def determinarGanador(sumaJugador, sumaComputadora, dinero, dineroApostado, nombre):
    if sumaJugador <= 21 and sumaComputadora > 21:
        print("💥 Crupier se pasó de 21. ¡Victoria automática!")
        dinero += dineroApostado * 2
        print(f"🎉 ¡{nombre} gana la ronda! Te llevás ${dinero:.2f} 🪙")
    elif sumaJugador > 21 and sumaComputadora <= 21:
        print("❌ Crupier gana esta vez.")
    elif sumaJugador <= 21 and sumaComputadora <= 21:
        if sumaJugador == sumaComputadora:
            print("🤝 ¡Empate! Recuperás tu apuesta.")
            dinero += dineroApostado
        elif sumaJugador > sumaComputadora:
            dinero += dineroApostado * 2
            print(f"🎉 ¡{nombre} gana la ronda! Te llevás ${dinero:.2f} 🪙")
        else:
            print("❌ Crupier gana esta vez.")
    else:
        print("🤝 ¡Empate! Recuperás tu apuesta.")
    return dinero

def calcularSuma(mano):
    total = 0
    ases = 0
    for valor, _ in mano:
        total += valor
        if valor == 11:
            ases += 1
    while total > 21 and ases:
        total -= 10
        ases -= 1
    return total

def turnoDeJugador(mazo, manos, nombre, dinero, dineroApostado):
    jugadorSePlanto = False
    sumaJugador = calcularSuma(manos[nombre])

    while not jugadorSePlanto and sumaJugador < 21:
        print(f"\n🃏 Cartas actuales: {', '.join([c[1] for c in manos[nombre]])}")
        print(f"🧮 Total actual: {sumaJugador}")
        print("1⃣  Plantarse")
        print("2⃣  Pedir carta")
        print("3⃣  Duplicar apuesta (recibís solo una carta más)")
        print("4⃣  Dividir mano (Split)")

        try:
            respuesta = int(input("Ingrese su elección: "))
            while respuesta not in [1, 2, 3, 4]:
                respuesta = int(input("Opción inválida. Elegí 1, 2, 3 o 4: "))
        except:
            print("Entrada inválida.")
            continue

        if respuesta == 1:
            jugadorSePlanto = True
        elif respuesta == 2:
            nuevaCarta = mazo.pop()
            manos[nombre].append(nuevaCarta)
            print(f"🃏 Nueva carta: {nuevaCarta[1]}")
            sumaJugador = calcularSuma(manos[nombre])
        elif respuesta == 3:
            if dinero >= dineroApostado:
                dinero -= dineroApostado
                dineroApostado *= 2
                nuevaCarta = mazo.pop()
                manos[nombre].append(nuevaCarta)
                print(f"🃏 Nueva carta: {nuevaCarta[1]}")
                sumaJugador = calcularSuma(manos[nombre])
                jugadorSePlanto = True
            else:
                print("❌ No tenés suficiente dinero para duplicar la apuesta. Elegí otra opción.")
        elif respuesta == 4:
            if dinero >= dineroApostado and manos[nombre][0][0] == manos[nombre][1][0]:
                carta1 = manos[nombre][0]
                carta2 = manos[nombre][1]
                dinero -= dineroApostado
                mano1 = [carta1, mazo.pop()]
                mano2 = [carta2, mazo.pop()]

                print("✂️ ¡Dividiste tu mano! Ahora jugás dos manos independientes.")

                for i, mano in enumerate([mano1, mano2], start=1):
                    print(f"\n🎮 Jugando mano {i}:")
                    suma = calcularSuma(mano)
                    sePlanto = False
                    while not sePlanto:
                        print(f"🃏 Cartas: {', '.join([c[1] for c in mano])}")
                        print(f"🧮 Total: {suma}")
                        if suma >= 21:
                            break
                        opcion = input("¿Querés otra carta en esta mano? (s/n): ").strip().lower()
                        if opcion == 's':
                            nueva = mazo.pop()
                            mano.append(nueva)
                            print(f"🃏 Nueva carta: {nueva[1]}")
                            suma = calcularSuma(mano)
                        else:
                            sePlanto = True
                    manos[f"{nombre}_split_{i}"] = mano
                jugadorSePlanto = True
                sumaJugador = -1
            else:
                print("❌ No podés dividir esa mano. Elegí otra opción.")
    return sumaJugador, dinero, dineroApostado, manos

def turnoDeComputadora(mazo, manos, nombre):
    while calcularSuma(manos["Computadora"]) < 17:
        carta = mazo.pop()
        manos["Computadora"].append(carta)
        print(f"🤖 Crupier recibe: {carta[1]}")
        time.sleep(1)
    return calcularSuma(manos["Computadora"])

def crearMazo():
    valores = [(11, 'A'), (10, 'K'), (10, 'Q'), (10, 'J')] + [(i, str(i)) for i in range(2, 11)]
    palos = ['♠', '♥', '♦', '♣']
    return [(valor, f"{nombre} de {palo}") for valor, nombre in valores for palo in palos]

def main():
    dinero = 100
    nombre = input("🎮 Ingresá tu nombre: ")
    print(f"💰 Comenzás con ${dinero}")

    while True:
        if dinero <= 0:
            print(f"\nTe quedaste sin dinero, {nombre}. ¡Gracias por jugar! 💸")
            break

        try:
            dineroApostado = int(input(f"\n¿Cuánto querés apostar, {nombre}? (Saldo: ${dinero}): "))
            while dineroApostado <= 0 or dineroApostado > dinero:
                dineroApostado = int(input("Apuesta inválida. Ingresá una cantidad válida: "))
        except:
            print("Entrada inválida.")
            continue

        dinero -= dineroApostado
        mazo = crearMazo()
        random.shuffle(mazo)

        manos = {
            nombre: [mazo.pop(), mazo.pop()],
            "Computadora": [mazo.pop(), mazo.pop()]
        }

        cartasJugador = ', '.join([c[1] for c in manos[nombre]])
        print(f"🃏 {nombre} recibe: {cartasJugador}")
        print(f"🃏 Crupier muestra: {manos['Computadora'][0][1]}")

        sumaJugador, dinero, dineroApostado, manos = turnoDeJugador(mazo, manos, nombre, dinero, dineroApostado)
        sumaComputadora = turnoDeComputadora(mazo, manos, nombre)

        cartasCrupier = ', '.join([c[1] for c in manos["Computadora"]])
        print("🧾 RESUMEN DE LA RONDA")
        print(f"{nombre}: {cartasJugador}")
        print(f"Crupier: {cartasCrupier} (Total: {sumaComputadora})")

        dinero = determinarGanador(sumaJugador, sumaComputadora, dinero, dineroApostado, nombre)
        print("\n" + "=" * 50 + "\n")

        if dinero > 0:
            continuar = input("¿Querés jugar otra ronda? (S/N): ").strip().lower()
            if continuar != "s":
                print(f"\nGracias por jugar, {nombre}. Terminaste con ${dinero:.2f} ¡Hasta la próxima!")
                break

if __name__ == "__main__":
    main()
