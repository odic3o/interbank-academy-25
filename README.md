# Reto Técnico: Procesamiento de Transacciones Bancarias (CLI)
## Introducción: 
Esta pequeña aplicacion realizada en python para ejecutarla en la  linea de comandos se realiza con la finalidad de dar una solución al reto técnico de interbank academia y demostrar el dominio sobre el uso de archivos y las operaciones aritmeticas teniendo como fuente de información un archivo CSV. 
La aplicacion debe cumplir con tres objetivos principales 
1.Balance Final que es la diferencia entre creditos y debitos 
2.Mostrar la transaccion con mayor monto
3.Mostrar el numero de transacciones totales en el archivo 

## Instrucciones de Ejecución: 
Es indispensable contar con el lenguaje python 3 instalado en su computadora en el caso del sistema operativo windows lo puede bajar en su pagina https://www.python.org/downloads/release/python-3132/ e instalarlo. En el caso que estes en un SO linux debian o derivados digitar en consola o terminal 

 > sudo apt install python3

 si su sistema operativo es redhat o derivados puede digitar lo siguiente
 
 > sudo yum install python3

luego de instalar vamos al terminal de lineas de comandos, nos situamos en el directorio o carpeta donde esta nuestro proyecto y digitamos lo siguiente para correr la solución de la manera siguiente.

> python3 movimientos.py data.csv

y nos va a imprimir en pantalla lo siguiente 

> ===== REPORTE DE TRANSACCIONES BANCARIAS =====
> 
>  Balance Final: $10985.85
> Transacción de Mayor Monto: ID 222 con $499.69

> Conteo de Transacciones:
 >  - Créditos: 508
 >  - Débitos: 492
 >  - Total: 1000

## Enfoque y Solución: Lógica implementada y decisiones de diseño.
En el  programa por cada tarea  se impleemntó una función  para que realice lo necesario para llegar a la solución que se desea

leer_archivo_csv() - Solo se preocupa por leer el archivo

validar_monto() - Solo valida que un monto sea correcto

clasificar_transaccion() - Solo identifica el tipo de transacción

calcular_estadisticas() - Solo calcula los números

generar_reporte() - Solo muestra los resultados

guardar_reporte() - Solo guarda los datos en un archivo

El flujo de Datos es unidireccional 
>  Archivo CSV → Validación → Cálculos → Reporte (pantalla/archivo)

## Estructura del Proyecto: 
El proyecto consta de 1 archivo CSV de donde se toman los datos y un archivo py donde se realiza las funciones para la dar la solución del problema. hay que destacar que esto puede ser punto de partida para hacer un libro diario o una pequeña app de control de ingresos y egresos.
Se debe tener instalado el lenguaje de programación python y un emulador de terminal en mi caso use qterminal. 

