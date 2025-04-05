import csv
import sys
from decimal import Decimal

def leer_archivo_csv(nombre_archivo):
    """
    Lee un archivo CSV y devuelve sus filas como una lista de diccionarios.
    
    Args:
        nombre_archivo (str): Ruta al archivo CSV a leer
        
    Returns:
        list: Lista de diccionarios, cada uno representa una fila del CSV
        None: Si ocurre algún error al leer el archivo
    """
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
                return None
            
            # Convertimos el lector a una lista para poder usarlo múltiples veces
            return list(lector_csv)
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
        return None
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
        return None


def validar_monto(monto_str, id_transaccion):
    """
    Convierte una cadena de texto a un valor Decimal y valida que sea un número válido.
    
    Args:
        monto_str (str): El monto como cadena de texto
        id_transaccion (str): ID de la transacción para reportar errores
        
    Returns:
        Decimal: El monto convertido a Decimal
        None: Si el monto no es válido
    """
    try:
        # Intentamos convertir el monto a Decimal
        return Decimal(monto_str)
    except ValueError:
        print(f"Error: Monto inválido en la transacción {id_transaccion}: {monto_str}")
        return None


def clasificar_transaccion(tipo):
    """
    Determina si el tipo de transacción es crédito, débito u otro.
    
    Args:
        tipo (str): El tipo de transacción del CSV
        
    Returns:
        str: 'credito', 'debito' o 'desconocido'
    """
    # Convertimos a minúsculas y eliminamos acentos para comparar
    tipo_lower = tipo.lower()
    
    if tipo_lower == 'crédito' or tipo_lower == 'credito':
        return 'credito'
    elif tipo_lower == 'débito' or tipo_lower == 'debito':
        return 'debito'
    else:
        return 'desconocido'


def calcular_estadisticas(transacciones):
    """
    Calcula todas las estadísticas necesarias para el reporte.
    
    Args:
        transacciones (list): Lista de diccionarios con las transacciones
        
    Returns:
        dict: Diccionario con todas las estadísticas calculadas
    """
    # Inicializamos las variables para almacenar los resultados
    suma_creditos = Decimal('0')
    suma_debitos = Decimal('0')
    transaccion_mayor = {'id': None, 'monto': Decimal('0')}
    contador_creditos = 0
    contador_debitos = 0
    
    # Procesamos cada transacción
    for transaccion in transacciones:
        # Validamos y convertimos el monto
        monto = validar_monto(transaccion['monto'], transaccion['id'])
        if monto is None:
            continue  # Saltamos esta transacción si el monto no es válido
        
        # Clasificamos la transacción
        tipo = clasificar_transaccion(transaccion['tipo'])
        
        # Actualizamos estadísticas según el tipo
        if tipo == 'credito':
            suma_creditos += monto
            contador_creditos += 1
        elif tipo == 'debito':
            suma_debitos += monto
            contador_debitos += 1
        else:
            print(f"Advertencia: Tipo de transacción desconocido: {transaccion['tipo']} en ID: {transaccion['id']}")
        
        # Verificamos si esta transacción tiene el mayor monto hasta ahora
        if monto > transaccion_mayor['monto']:
            transaccion_mayor['id'] = transaccion['id']
            transaccion_mayor['monto'] = monto
    
    # Calculamos el balance final
    balance_final = suma_creditos - suma_debitos
    
    # Retornamos todas las estadísticas en un diccionario
    return {
        'suma_creditos': suma_creditos,
        'suma_debitos': suma_debitos,
        'balance_final': balance_final,
        'transaccion_mayor': transaccion_mayor,
        'contador_creditos': contador_creditos,
        'contador_debitos': contador_debitos
    }


def generar_reporte(estadisticas):
    """
    Genera y muestra un reporte formateado con las estadísticas calculadas.
    
    Args:
        estadisticas (dict): Diccionario con todas las estadísticas calculadas
    """
    print("\n===== REPORTE DE TRANSACCIONES BANCARIAS =====")
    
    # Mostramos el resumen de montos
    print("\nResumen de Montos:")
    print(f"  - Total Créditos: ${estadisticas['suma_creditos']}")
    print(f"  - Total Débitos: ${estadisticas['suma_debitos']}")
    print(f"Balance Final: ${estadisticas['balance_final']}")
    
    # Mostramos la transacción de mayor monto
    mayor = estadisticas['transaccion_mayor']
    print(f"\nTransacción de Mayor Monto: ID {mayor['id']} con ${mayor['monto']}")
    
    # Mostramos el conteo de transacciones
    creditos = estadisticas['contador_creditos']
    debitos = estadisticas['contador_debitos']
    print("\nConteo de Transacciones:")
    print(f"  - Créditos: {creditos}")
    print(f"  - Débitos: {debitos}")
    print(f"  - Total: {creditos + debitos}")


def guardar_reporte(estadisticas, nombre_archivo_salida):
    """
    Guarda el reporte en un archivo de texto.
    
    Args:
        estadisticas (dict): Diccionario con todas las estadísticas calculadas
        nombre_archivo_salida (str): Nombre del archivo donde guardar el reporte
    """
    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo:
            # Escribimos el encabezado
            archivo.write("===== REPORTE DE TRANSACCIONES BANCARIAS =====\n")
            
            # Escribimos el resumen de montos
            archivo.write("\nResumen de Montos:\n")
            archivo.write(f"  - Total Créditos: ${estadisticas['suma_creditos']}\n")
            archivo.write(f"  - Total Débitos: ${estadisticas['suma_debitos']}\n")
            archivo.write(f"Balance Final: ${estadisticas['balance_final']}\n")
            
            # Escribimos la transacción de mayor monto
            mayor = estadisticas['transaccion_mayor']
            archivo.write(f"\nTransacción de Mayor Monto: ID {mayor['id']} con ${mayor['monto']}\n")
            
            # Escribimos el conteo de transacciones
            creditos = estadisticas['contador_creditos']
            debitos = estadisticas['contador_debitos']
            archivo.write("\nConteo de Transacciones:\n")
            archivo.write(f"  - Créditos: {creditos}\n")
            archivo.write(f"  - Débitos: {debitos}\n")
            archivo.write(f"  - Total: {creditos + debitos}\n")
            
        print(f"\nReporte guardado exitosamente en '{nombre_archivo_salida}'")
    except Exception as e:
        print(f"Error al guardar el reporte: {e}")


def procesar_archivo_csv(nombre_archivo):
    """
    Procesa un archivo CSV de transacciones bancarias y genera un reporte.
    
    Args:
        nombre_archivo (str): Ruta al archivo CSV a procesar
    """
    # Leemos el archivo CSV
    transacciones = leer_archivo_csv(nombre_archivo)
    
    # Verificamos si pudimos leer el archivo correctamente
    if transacciones is None:
        return
    
    # Calculamos todas las estadísticas
    estadisticas = calcular_estadisticas(transacciones)
    
    # Generamos y mostramos el reporte
    generar_reporte(estadisticas)
    
    # Preguntamos al usuario si quiere guardar el reporte
    respuesta = input("\n¿Desea guardar el reporte en un archivo? (s/n): ")
    if respuesta.lower() == 's':
        nombre_archivo_base = nombre_archivo.split('.')[0]
        nombre_archivo_salida = f"{nombre_archivo_base}_reporte.txt"
        guardar_reporte(estadisticas, nombre_archivo_salida)


def main():
    """
    Función principal que maneja la lógica del programa.
    """
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
   
       
      
  
