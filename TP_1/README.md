# Autor 
Facundo Mesa 
Universidad de Mendoza 
Ingeniería en Informatica
---

# TP Analisis Biométrico

Este proyecto implementa un sistema de análisis biométrico que genera datos de frecuencia cardíaca, presión arterial y niveles de oxígeno. Utiliza una arquitectura de procesos en Python para analizar y verificar los datos en tiempo real, almacenándolos en una cadena de bloques.
--- 

# Requisitos
- Python
- Librerías:
  - `json`
  - `hashlib`
  - `random`
  - `time`
  - `multiprocessing`
  - `queue`
  - `os`
  - `datetime`
  - `statistics`
  - `collections`
---

## Ejecucíon 

### 1 Ejecuta el programa principal:

Abre una terminal y navega al directorio del proyecto.
Ejecuta el siguiente comando: python analisis_biometrico.py 

### 2 Observa la salida:

El programa generará datos biométricos y los procesará. Verás la salida en la terminal, incluyendo alertas si los datos están fuera de los parámetros normales.

### 3 Revisa los resultados:

Los datos se almacenarán en un archivo 'blockchain.json' en el mismo directorio.
Se generará un archivo 'reporte.txt' con un resumen de los bloques procesados y alertas.

### 4 Verifica la cadena de bloques:

Después de ejecutar el programa principal, puedes verificar la integridad de la cadena de bloques utilizando el script 'verificar_cadena.py'.
Ejecuta el siguiente comando:
'python verificar_cadena.py'