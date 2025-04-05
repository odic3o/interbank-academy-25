import csv
import sys
from decimal import Decimal

def procesar_archivo_csv(nombre_archivo):
    """
    Procesa un archivo CSV de transacciones bancarias y genera un reporte.
    
    Args:
        nombre_archivo (str): Ruta al archivo CSV a procesar
    """
    # Inicializamos las variables para almacenar los resultados
    suma_creditos = Decimal('0')
    suma_debitos = Decimal('0')
    transaccion_mayor = {'id': None, 'monto': Decimal('0')}
    contador_creditos = 0
    contador_debitos = 0
    
    try:
        # Abrimos el archivo CSV para lectura
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            # Creamos un lector CSV que interpretará la primera fila como encabezados
            lector_csv = csv.DictReader(archivo)
            
            # Verificamos que el archivo tenga las columnas necesarias
            columnas_requeridas = {'id', 'tipo', 'monto'}
            columnas_archivo = set(lector_csv.fieldnames)
            
            if not columnas_requeridas.issubset(columnas_archivo):
                print(f"Error: El archivo CSV debe contener las columnas: {', '.join(columnas_requeridas)}")
                return
            
            # Procesamos cada fila (transacción) del archivo
            for fila in lector_csv:
                # Convertimos el monto a Decimal para evitar problemas con números decimales
                try:
                    monto = Decimal(fila['monto'])
                except ValueError:
                    print(f"Error: Monto inválido en la transacción {fila['id']}: {fila['monto']}")
                    continue
                
                # Procesamos según el tipo de transacción
                if fila['tipo'].lower() == 'crédito' or fila['tipo'].lower() == 'credito':
                    suma_creditos += monto
                    contador_creditos += 1
                elif fila['tipo'].lower() == 'débito' or fila['tipo'].lower() == 'debito':
                    suma_debitos += monto
                    contador_debitos += 1
                else:
                    print(f"Advertencia: Tipo de transacción desconocido: {fila['tipo']} en ID: {fila['id']}")
                
                # Verificamos si esta transacción tiene el mayor monto hasta ahora
                if monto > transaccion_mayor['monto']:
                    transaccion_mayor['id'] = fila['id']
                    transaccion_mayor['monto'] = monto
        
        # Calculamos el balance final
        balance_final = suma_creditos - suma_debitos
        
        # Generamos el reporte
        print("\n===== REPORTE DE TRANSACCIONES BANCARIAS =====")
        print(f"Balance Final: ${balance_final}")
        print(f"Transacción de Mayor Monto: ID {transaccion_mayor['id']} con ${transaccion_mayor['monto']}")
        print("\nConteo de Transacciones:")
        print(f"  - Créditos: {contador_creditos}")
        print(f"  - Débitos: {contador_debitos}")
        print(f"  - Total: {contador_creditos + contador_debitos}")
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
    except Exception as e:
        print(f"Error inesperado: {e}")

def main():
    # Verificamos si se proporcionó un nombre de archivo como argumento
    if len(sys.argv) < 2:
        print("Uso: python procesador_transacciones.py [archivo_csv]")
        print("Ejemplo: python procesador_transacciones.py transacciones.csv")
        return
    
    # Obtenemos el nombre del archivo del primer argumento
    nombre_archivo = sys.argv[1]
    
    # Procesamos el archivo
    procesar_archivo_csv(nombre_archivo)

# Punto de entrada del programa
if __name__ == "__main__":
    main()
