import random, os, copy

#| CLASE INTERACCION |#
class Interaccion:
    def __init__(self, inputJugador):
        self.inputJugador = inputJugador

    def solicitarInput(self, cantidadEnemigosSala):
        inputValido = False

        while not inputValido:
            opcionSeleccionada = input("Escribe tu respuesta: ")
            print("")
            try:
                opcionSeleccionada = int(opcionSeleccionada)
                for x in range(cantidadEnemigosSala):
                    if opcionSeleccionada == x + 1 or opcionSeleccionada == 0:
                        inputValido = True
                        break
                else:
                    raise ValueError("Opcion escrita no valida")
            except ValueError:
                print("Opcion no valida, por favor intentalo nuevamente...\n")

        self.inputJugador = opcionSeleccionada

        return opcionSeleccionada

#| CLASE PERSONAJE |#
class Personaje:
    def __init__(self, nombre, vida, daño):
        self.nombre = nombre
        self.vida = vida
        self.daño = daño
    
    def mostrarAtributos(self):
        print(">> Vida:", self.vida,
        "\n>> Daño:", self.daño, "\n")

    def estaVivo(self):
        return self.vida > 0
    
    def morir(self):
        self.vida = 0
        print("|!|", self.nombre, "ha muerto")

    def atacar(self, rival):
        rival.vida = rival.vida - self.daño

        print("|?|", self.nombre, "ha realizado", self.daño,
        "puntos de daño a", rival.nombre)

        if not rival.estaVivo():
            rival.morir()

#| CLASE ACCIONES PARA LA HABITACION NORMAL |#
class HabitacionNormal:
    def __init__(self, enemigoSeleccionado):
        self.enemigoSeleccionado = enemigoSeleccionado

    @staticmethod
    def accionHabitacion():
        global turno

        #| INICIALIZAR ENEMIGOS |#
        generarEnemigos()

        #| BUCLE COMBATE (NO ACABA HASTA QUE NO HAYA NADIE O JUGADOR MUERA) |#
        while True:
            #| LIMPIAR LA PANTALLA |#
            borrarPantalla()

            #| AUMENTAR TURNO |#
            turno += 1

            #| MOSTRAR LAS ESTADISTICAS DEL JUGADOR EN ESTE TURNO |#
            uiEstadisticas()

            #| IMPRIMIR ENEMIGOS EN PANTALLA |#
            bucleMostrarEnemigos = 0
            while bucleMostrarEnemigos < len(enemigosActivos):
                print(bucleMostrarEnemigos + 1, ". ", enemigosActivos[bucleMostrarEnemigos].nombre, sep = "")
                enemigosActivos[bucleMostrarEnemigos].mostrarAtributos()
                bucleMostrarEnemigos += 1

            #| MOSTRAR TURNO |#
            print("##> TURNO", turno, "<##\n")

            #| PREGUNTAR A QUE ENEMIGO ATACAR |#
            if MostrarTextos.preguntaEnemigo(len(enemigosActivos)) == 0:
                break

            #| JUGADOR ATACA A ENEMIGO |#
            jugador.atacar(enemigosActivos[habitacionNormal.enemigoSeleccionado - 1])

            #| SI ENEMIGO ESTA MUERTO, RETIRARLO DE LA LISTA |#
            if enemigosActivos[habitacionNormal.enemigoSeleccionado - 1].vida == 0:
                enemigosActivos.pop(habitacionNormal.enemigoSeleccionado - 1)

            #| ENEMIGOS ATACAN JUGADOR |#
            bucleEnemigosAtacan = 0

            while bucleEnemigosAtacan < len(enemigosActivos):
                enemigosActivos[bucleEnemigosAtacan].atacar(jugador)

                #| SI JUGADOR ESTA MUERTO, GAME OVER |#
                if jugador.vida == 0:
                    interaccion.inputJugador = 0
                    break

                bucleEnemigosAtacan += 1

            #| SOLICITAR SI ACABAR TURNO |#
            if MostrarTextos.preguntarAcabarTurno() == 1 and jugador.vida == 0:
                interaccion.inputJugador = 0

            #| COMPROBAR SI EL COMBATE HA TERMINADO |#
            if len(enemigosActivos) == 0 or jugador.vida == 0 or interaccion.inputJugador == 0:
                break

        #| BORRAR ENEMIGOS DE LA LISTA DE LA HABITACION |#
        borrarEnemigos()

#| CLASE ACCIONES PARA LA HABITACION ESPECIAL |#
class HabitacionEspecial:
    @staticmethod
    def accionHabitacion():
        #| LIMPIAR LA PANTALLA |#
        borrarPantalla()

        #| MOSTRAR LAS ESTADISTICAS DEL JUGADOR EN ESTA RONDA |#
        uiEstadisticas()

        #| ACCION DEL JUGADOR |#
        interaccion.solicitarInput(4)

#| CLASE TEXTOS A MOSTRARA |#
class MostrarTextos:
    @staticmethod
    def preguntaEnemigo(cantidadEnemigosSala):
        print("➤  ¿A que enemigo quieres atacar? (Ej: 1)")
        habitacionNormal.enemigoSeleccionado = interaccion.solicitarInput(cantidadEnemigosSala)
        
        if interaccion.inputJugador == 0:
            return interaccion.inputJugador
        else:
            print("|*| Seleccionaste a (", habitacionNormal.enemigoSeleccionado, ") ",
            enemigosActivos[habitacionNormal.enemigoSeleccionado - 1].nombre,
            " como objetivo", sep = "")
            return interaccion.inputJugador
    
    @staticmethod
    def preguntarAcabarTurno():
        print("\n➤  Acabar turno: 1 / Game Over: 0")
        return interaccion.solicitarInput(1)

#| VARIABLES |#
ronda = 0
turno = 0
tipoHabitacionActual = 0
noEspecial = 1

#| CREAR INTERACCION |#
interaccion = Interaccion(1)

#| CREAR SALAS |#
habitacionNormal = HabitacionNormal(0)

#| CREAR LISTA DE TIPOS DE HABITACION |#
listaTiposHabitaciones = [HabitacionNormal, HabitacionEspecial]

#| CREAR JUGADOR |#
jugador = Personaje("Jugador", random.randint(3, 6), random.randint(1, 3))

#| CREAR LISTA ENEMIGOS (USAR ID) |#
def crearEnemigos():
    e00 = Personaje("Jeringa", 2, 1)
    e01 = Personaje("Glucometro", 3, 1)
    e02 = Personaje("Yelco", 1, 1)
    e03 = Personaje("Sonda", 1, 2)
    e04 = Personaje("Nefrostomia", 2, 1)
    return [e00, e01, e02, e03, e04]

enemigos = crearEnemigos()
enemigosActivos = []

#| DEFINIR TIPOS DE HABITACIONES |#
tiposHabitaciones = {
    0: "NORMAL",
    1: "ESPECIAL ★"
}

#| CALCULAR TIPO DE HABITACION |#
# 0: HABITACION NORMAL, 1: HABITACION ESPECIAL #
def calcularTipoHabitacion():
    global noEspecial

    opciones = [0, 1] if noEspecial == 0 else [0]
    probabilidades = [0.7, 0.3] if noEspecial == 0 else [1]
    tipoHabitacionElegido = random.choices(opciones, weights = probabilidades)[0]

    if tipoHabitacionElegido == 1 and noEspecial == 0:
        noEspecial = 1
        return tipoHabitacionElegido
    else:
        noEspecial = 0
        return tipoHabitacionElegido

#| BUSCAR ENEMIGOS PARA LA HABITACION ACTUAL |#
def generarEnemigos():
    global enemigosActivos
    bucleGenerarEnemigos = 0

    while bucleGenerarEnemigos <= ronda + 2:
        if random.randint(1, 100) <= 5 or len(enemigosActivos) == 0:
            enemigosActivos.insert(bucleGenerarEnemigos, copy.deepcopy(random.choice(enemigos)))
        bucleGenerarEnemigos += 1

#| BORRAR ENEMIGOS DE LA LISTA ACTUAL |#
def borrarEnemigos():
    bucleBorrarEnemigos = len(enemigosActivos)

    while bucleBorrarEnemigos > 0:
        enemigosActivos.remove(enemigosActivos[bucleBorrarEnemigos - 1])
        bucleBorrarEnemigos -= 1

#| BORRAR PANTALLA |#
def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

#| MOSTRAR UI DE LAS ESTADISTICAS DEL JUGADOR |#
def uiEstadisticas():
    print("#-----------------#")
    print("# > HABITACION", ronda)
    print("#-----------------#")
    
    tipoHabitacionUI = tiposHabitaciones.get(tipoHabitacionActual, "DESCONOCIDA")
    print("# >", tipoHabitacionUI)
    print("#-----------------#")
    
    print("#    + Vida:", jugador.vida)
    print("#    + Daño:", jugador.daño)
    print("#-----------------#\n")

#| LOOP DE JUEGO|#
while True:
    #| LIMPIAR LA PANTALLA |#
    borrarPantalla()

    #| AUMENTAR EL NUMERO DE LA RONDA |#
    ronda += 1

    #| CALCULAR DE QUE TIPO VA A SER LA HABITACION EN ESTA RONDA |#
    tipoHabitacionActual = calcularTipoHabitacion()

    #| EJECUTAR LA RESPECTIVA FUNCION DEPENDIENDO DE QUE HABITACION ES |#
    listaTiposHabitaciones[tipoHabitacionActual].accionHabitacion()
    
    #| REINICIAR TURNO |#
    turno = 0

    #| COMPROBAR SI NO HAY UN CASO DE GAME OVER |#
    if interaccion.inputJugador == 0:
        borrarPantalla()
        print("###|! FIN DEL JUEGO !|###")
        break