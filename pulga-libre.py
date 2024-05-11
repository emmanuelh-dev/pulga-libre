import random

class CEDIS:
    def __init__(self):
        self.bloques = []
        self.zonas = list(range(1, 11))  # Zonas del 1 al 10

    def generar_bloques(self):
        self.bloques = [
            [Paquete(id_paquete, random.choice(self.zonas)) for id_paquete in range(1, 11)],
            [Paquete(id_paquete, random.choice(self.zonas)) for id_paquete in range(11, 26)],
            [Paquete(id_paquete, random.choice(self.zonas)) for id_paquete in range(26, 46)]
        ]


    def asignar_zonas(self, bloque_index, paquetes_por_zona):
        bloque = self.bloques[bloque_index]
        zonas_asignadas = {}

        for zona, cantidad in paquetes_por_zona.items():
            paquetes_disponibles = [paquete for paquete in bloque if paquete.zona is None]
            for _ in range(cantidad):
                if not paquetes_disponibles:
                    print(f"No hay suficientes paquetes para asignar a la zona {zona}")
                    break
                paquete = paquetes_disponibles.pop(0)
                paquete.zona = zona
                zonas_asignadas.setdefault(zona, 0)
                zonas_asignadas[zona] += 1

        return zonas_asignadas




class Paquete:
    def __init__(self, id_paquete, zona):
        self.id = id_paquete
        self.zona = zona
        self.estado = "pendiente"
        self.ubicacion = self.generar_ubicacion()

    def generar_ubicacion(self):
        grados = random.randint(0, 180)
        minutos = random.randint(0, 59)
        segundos = random.randint(0, 59)
        punto_cardinal = random.choice(['N', 'S', 'E', 'O'])

        latitud = f"{grados}° {minutos}' {segundos}\" {punto_cardinal}"

        grados = random.randint(0, 180)
        minutos = random.randint(0, 59)
        segundos = random.randint(0, 59)
        punto_cardinal = random.choice(['N', 'S', 'E', 'O'])

        longitud = f"{grados}° {minutos}' {segundos}\" {punto_cardinal}"

        return {
            "zona": self.zona,
            "latitud": latitud,
            "longitud": longitud
        }

    def marcar_entregado(self):
        self.estado = "entregado"

    def marcar_no_entregado(self):
        self.estado = "no entregado"

class Repartidor:
    def __init__(self):
        self.bloque_asignado = None
        self.paquetes_entregados = []
        self.paquetes_no_entregados = []
        self.pago_total = 0

    def asignar_bloque(self, cedis, bloque_index):
        if self.bloque_asignado is not None:
            print("Aún tiene paquetes pendientes del bloque anterior.")
            return

        self.bloque_asignado = cedis.bloques[bloque_index]

        print(f"Se le ha asignado el bloque {bloque_index + 1} con {len(self.bloque_asignado)} paquetes.")

    def siguiente_paquete(self):
        if self.bloque_asignado is None:
            print("No tiene un bloque asignado.")
            return

        for paquete in self.bloque_asignado:
                if paquete.estado == "pendiente":
                    ubicacion = paquete.ubicacion
                    print(f"Zona: {ubicacion['zona']}")
                    print(f"Latitud: {ubicacion['latitud']}")
                    print(f"Longitud: {ubicacion['longitud']}")
                    return

        print("No hay más paquetes pendientes en este bloque.")

    def marcar_paquete(self, entregado):
        if self.bloque_asignado is None:
            print("No tiene un bloque asignado.")
            return

        for paquete in self.bloque_asignado:
            if paquete.estado == "pendiente":
                if entregado:
                    paquete.marcar_entregado()
                    self.paquetes_entregados.append(paquete)
                else:
                    paquete.marcar_no_entregado()
                    self.paquetes_no_entregados.append(paquete)

                print(f"Paquete {paquete.id} marcado como {paquete.estado}.")
                return

        print("No hay más paquetes pendientes en este bloque.")

    def ver_estatus(self):
        if self.bloque_asignado is None:
            print("No puedes ver el status de entregas puesto que no tienen un bloque asignado.")
            return

        entregados = len(self.paquetes_entregados)
        no_entregados = len(self.paquetes_no_entregados)
        pendientes = sum(1 for paquete in self.bloque_asignado if paquete.estado == "pendiente")

        print(f"Paquetes entregados: {entregados}")
        print(f"Paquetes no entregados (cliente no estaba en el domicilio): {no_entregados}")
        print(f"Paquetes pendientes por entregar: {pendientes}")

        zonas = {}
        for paquete in self.bloque_asignado:
            zona = paquete.zona
            zonas.setdefault(zona, {"iniciales": 0, "entregados": 0, "no_entregados": 0, "pendientes": 0})
            zonas[zona]["iniciales"] += 1

            if paquete.estado == "entregado":
                zonas[zona]["entregados"] += 1
            elif paquete.estado == "no entregado":
                zonas[zona]["no_entregados"] += 1
            else:
                zonas[zona]["pendientes"] += 1

        print("\nona\tCantidad de\tEntregados\tNo está\t\tPendientes")
        print("\t\tpaquetes\t\t\tcliente en su")
        print("\t\tiniciales\t\t\tdomicilio")
        for zona, datos in zonas.items():
            print(f"{zona}\t{datos['iniciales']}\t\t{datos['entregados']}\t\t{datos['no_entregados']}\t\t{datos['pendientes']}")

    def calcular_pago(self):
        self.pago_total = 0

        tarifas = {
            1: {"entregado": 15, "no_entregado": 21},
            2: {"entregado": [5, 5, 2], "no_entregado": [5, 5, 2]},
            3: {"entregado": [5, 5, 2], "no_entregado": [8, 8, 1]},
            4: {"entregado": [20, 20, 10], "no_entregado": [57, 0, 0]},
            5: {"entregado": [15, 15, 2], "no_entregado": [89, 0, 0]},
            6: {"entregado": [35, 35, 2], "no_entregado": [45, 0, 0]},
            7: {"entregado": [45, 45, 2], "no_entregado": [90, 0, 0]},
            8: {"entregado": [12, 12, 2], "no_entregado": [22, 0, 0]},
            9: {"entregado": [3, 3, 1], "no_entregado": [13, 0, 0]},
            10: {"entregado": [45, 45, 22], "no_entregado": [89, 0, 0]}
        }

        for paquete in self.paquetes_entregados:
            zona = paquete.zona
            tarifa = tarifas[zona]["entregado"]
            if isinstance(tarifa, list):
                pago = tarifa[0] if len(self.paquetes_entregados) >= 1 else 0
                pago += tarifa[1] if len(self.paquetes_entregados) >= 2 else 0
                pago += tarifa[2] * (len(self.paquetes_entregados) - 2)
            else:
                pago = tarifa
            self.pago_total += pago

        for paquete in self.paquetes_no_entregados:
            zona = paquete.zona
            tarifa = tarifas[zona]["no_entregado"]
            if isinstance(tarifa, list):
                pago = tarifa[0] if len(self.paquetes_no_entregados) >= 1 else 0
                pago += tarifa[1] if len(self.paquetes_no_entregados) >= 2 else 0
                pago += tarifa[2] * (len(self.paquetes_no_entregados) - 2)
            else:
                pago = tarifa
            self.pago_total += pago

        print(f"SU PAGO ES DE: ${self.pago_total}")

def menu():
    opciones = {
        '1': 'Seleccionar bloque de entrega',
        '2': 'Siguiente paquete para entregar',
        '3': 'Marcar paquete como entregado o no se encontró cliente',
        '4': 'Ver estatus de entregas',
        '5': 'Ver pago actual',
        '6': 'Salir'
    }

    print("Menú de opciones:")
    for opcion, descripcion in opciones.items():
        print(f"{opcion}. {descripcion}")

    opcion_elegida = input("Ingrese el número de la opción deseada: ")
    return opcion_elegida

def mostrar_mensaje(mensaje):
    print(mensaje)

def preguntar_opcion(mensaje):
  while True:
    cantidad = input(mensaje)
    try:
      if cantidad.strip():
        cantidad = int(cantidad)
        if cantidad >= 0:
            return cantidad
        else:
          print("Ingresa un numero valido")
    except ValueError:
          print("Ingresa un numero valido")


def main():
    opciones_validas = ['1', '2', '3', '4', '5', '6']
    continuar = True
    cedis = CEDIS()
    repartidor = Repartidor()
    cedis.generar_bloques()

    while continuar:
        opcion = menu()

        if opcion in opciones_validas:
            if opcion == '1':
                if repartidor.bloque_asignado:
                  print("Faltan paquetes del bloque por entregar")
                else:
                  bloque_index = int(input("Seleccione el bloque de entrega (1, 2 o 3): ")) - 1
                  if bloque_index < 0 or bloque_index >= len(cedis.bloques):
                      print("Bloque inválido. Intente de nuevo.")
                  else:
                      repartidor.asignar_bloque(cedis, bloque_index)
            elif opcion == '2':
                repartidor.siguiente_paquete()
            elif opcion == '3':
              if repartidor.bloque_asignado == None:
                print("No hay un bloque asignado")
              else:
                entregado = preguntar_opcion("Marcar como entregado \n 1: Si \n 2:No habia nadie  \n 3: Volver")
                if entregado == 1:
                  repartidor.marcar_paquete(True)
                elif entregado == 2:
                  repartidor.marcar_paquete(False)

            elif opcion == '4':
                repartidor.ver_estatus()
            elif opcion == '5':
                repartidor.calcular_pago()
            elif opcion == '6':
                continuar = False
                print("Saliendo del programa...")
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()