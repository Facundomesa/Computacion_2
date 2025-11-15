from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
import time
import random

def tarea_impredecible(id):
    """Tarea que puede fallar o tardar mucho"""
    tipo = random.choice(['rapida', 'lenta', 'error'])
    
    if tipo == 'rapida':
        time.sleep(1)
        return f"Tarea {id}: OK (rápida)"
    
    elif tipo == 'lenta':
        time.sleep(10)
        return f"Tarea {id}: OK (lenta)"
    
    else:  # error
        time.sleep(0.5)
        raise ValueError(f"Tarea {id} falló intencionalmente")

def ejecutar_con_manejo_errores(num_tareas, timeout_por_tarea=3):
    """Ejecuta tareas con manejo robusto de errores y timeouts"""
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Enviar todas las tareas
        futures = {
            executor.submit(tarea_impredecible, i): i 
            for i in range(num_tareas)
        }
        
        resultados_exitosos = []
        errores = []
        timeouts = []
        
        # Procesar según terminan
        for future in as_completed(futures, timeout=15):  # Timeout global
            task_id = futures[future]
            
            try:
                # Timeout individual por tarea
                resultado = future.result(timeout=timeout_por_tarea)
                resultados_exitosos.append(resultado)
                print(f"✓ {resultado}")
                
            except TimeoutError:
                timeouts.append(task_id)
                print(f"⏱️  Tarea {task_id}: Timeout (>{timeout_por_tarea}s)")
                future.cancel()  # Intentar cancelar
                
            except Exception as e:
                errores.append((task_id, str(e)))
                print(f"✗ Tarea {task_id}: {e}")
    
    # Reporte final
    print(f"\n📊 Resumen:")
    print(f"  Exitosas: {len(resultados_exitosos)}")
    print(f"  Timeouts: {len(timeouts)}")
    print(f"  Errores: {len(errores)}")
    
    return resultados_exitosos, errores, timeouts

# Uso
if __name__ == "__main__":
    ejecutar_con_manejo_errores(num_tareas=10, timeout_por_tarea=3)