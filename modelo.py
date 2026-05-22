import pandas as pd
import numpy as np

ruta_csv = "data/meli_test_data.csv"
ruta_parquet = "data/meli_train_data.parquet"

archivo_parquet = pd.read_parquet(ruta_parquet)
archivo_csv = pd.read_csv(ruta_csv)

def tasa_ventas_diarias_sku():
    ventas_sku = archivo_parquet.groupby('sku')['sold_quantity'].mean() 
    return ventas_sku

def simular_dias_hasta_agotamiento(tasa_ventas,stock,n_simulaciones=1000):
    simulaciones = []
    for simulacion in range(n_simulaciones):
        ventas = np.random.poisson(tasa_ventas, size=30)
        acumulado = np.cumsum(ventas)
        if acumulado[-1] < stock:
            dia = 30
        else:
            dia = np.argmax(acumulado >= stock) + 1
        simulaciones.append(dia)  
    return simulaciones

def calcular_probabilidades(simulaciones):
    dias_agotados = []
    for dia in range(1,31):
        agotado = simulaciones.count(dia)
        dias_agotados.append(agotado/len(simulaciones))
    return dias_agotados

def predecir(n_simulaciones = 1000):
    predicciones = []
    ventasSku = tasa_ventas_diarias_sku()
    tasa_media = ventasSku.mean()

    for indice,fila in archivo_csv.iterrows():        
        tasa = ventasSku.get(fila['sku'], tasa_media)    
        simulaciones = simular_dias_hasta_agotamiento(tasa,fila['target_stock'])
        diasAgotados = calcular_probabilidades(simulaciones)
        predicciones.append(([fila['sku']] + diasAgotados))
    
    return predicciones

def guardar_resultados(predicciones):
    try:
        columnas = ['sku'] + [f'dia_{i}' for i in range(1, 31)]
        df = pd.DataFrame(predicciones, columns = columnas)
        df.to_csv('data/predicciones.csv',index = False)
    except Exception as e:
        print(f"Error al guardar: {e}")

if __name__ == "__main__":
    print("Iniciando predicciones...")
    predicciones = predecir(n_simulaciones=100)
    guardar_resultados(predicciones)
    print(f"Listo. {len(predicciones)} SKUs procesados.")