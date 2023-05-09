# -*- coding: utf-8 -*-
#Luis Portilla
#Resolucion de Prueba para Postulantes de Practicas Pre-Profesionales Ergostats 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
"""
Ejercicios sobre manipulacion de datos
"""

#%% Ejercicio 1 : Comprension y Manipulacion de Base de Datos
#Importacion de la base de datos

# Debemos usar proyectos
# path = 'C:\\Users\\LuisPortilla\\Downloads\\Prueba Ergostats\\Tomo I\\'
df = pd.read_csv('data/INEC_Encuesta Estructural Empresarial_Tomo I_2021.csv', delimiter = ';')

 
#Impresion de las primeras 10 filas de la base de datos
print (df.head(10))

#Creacion de una nueva base con las variables de identificador, actividad economica y provincia
df1 = df[['id_empresa','provincia','cod_letra','des_letra',
          'cod_ciiu2d','des_ciiu2d']]

#%% Ejercicio 2 : Generacion de Estadisticas de Resumen
#Obteniendo la estadistica descriptiva del numero de trabajadores afiliados en las empresas
print (df['v5090'].describe())

#Ahora, para obtener el numero de empresas por provincia
conteo_provincia = df.groupby('provincia')['id_empresa'].count()
print(conteo_provincia)

#%% Ejercicio 3 : Comparacion de grupos dentro de los datos
#Calculo del numero de empresas en Pichincha que pertenecen a cada una de las actividades economicas
df_pichincha = df[df['provincia'] == 17]
conteo_actividad_pichincha = df_pichincha.groupby('des_letra')['id_empresa'].count()
print(conteo_actividad_pichincha)

#Calculo del numero de trabajadores promedio para cada una de las actividades en Pichincha
prom_trab_pich = df_pichincha.groupby('des_letra')['v5090'].mean()
print(prom_trab_pich)

#%% Ejercicio 4 : Analisis de Patrones
#Tabla de frecuencias de empresas con tienen personal ocupado mayor a 50 por provincia
df_50trab = df[df['v5090'] > 50 ]
tab_freq_emp = df_50trab.groupby('provincia')['id_empresa'].count()
acumulado = tab_freq_emp.cumsum()
freq_df = pd.concat([tab_freq_emp, acumulado], axis=1)
freq_df.columns = ['Frequencia', 'Frecuencia Acumulada']
print(freq_df)

#Calculando el porcentaje de empresas con personal mayor a 50 por provincia

total = df.groupby('provincia')['id_empresa'].nunique()
porcentaje = tab_freq_emp / total 

resumen = pd.concat([tab_freq_emp, acumulado, porcentaje], axis=1)
resumen.columns = ['Frecuencia', 'Frecuencia Acumulada', 'Porcentaje']

print(resumen)

#%% Ejercicio 5 : Manipulacion avanzada de bases de datos
#Creacion de una variable binaria que indica con 1 si la empresa tiene mas de 10 años y 0 caso contrario

df['Mayor10a'] = df['anio_ruc_dis'].apply(lambda x: 1 if (2023 - x) > 10 else 0) 

#Creacion de una nueva base de datos donde esten unicamente los establecimientos con mas de 10 años y con mas de 10 trabajadores
df_final = df[(df['v5090']>20) & (df['Mayor10a']== 1)]
print(df_final)



#%%
"""
Ejercicios sobre visualizacion de datos
"""
#%%Ejercicio 1: Diagrama de Barras por Provincia

#Creando el grafico de barras con los nombres de las provincias
provincias ={
    1:'Azuay',
    2:'Bolivar',
    3:'Cañar',
    4:'Carchi',
    5:'Cotopaxi',
    6:'Chimborazo',
    7:'El Oro',
    8:'Esmeraldas',
    9:'Guayas',
    10:'Imbabura',
    11:'Loja',
    12:'Los Rios',
    13:'Manabi',
    14:'Morona Santiago',
    15:'Napo',
    16:'Pastaza',
    17:'Pichincha',
    18: 'Tungurahua',
    19: 'Zamora Chinchipe',
    20: 'Galapagos',
    21: 'Sucumbios',
    22: 'Orellana',
    23: 'Santo Domingo de los Tsachilas',
    24: 'Santa Elena'}

df['des_provincias'] = df['provincia'].map(provincias)

conteo_provincias = df.groupby('des_provincias')['id_empresa'].count()
conteo_provincias.plot(kind='bar')

plt.title('Numero de Compañias por Provincia')
plt.xlabel('Provincia')
plt.ylabel('Compañias')
plt.savefig('Empresas_Provincia.png', bbox_inches='tight', dpi= 600)
plt.show()

#%% Ejercicio 2: Diagrama de Dispersion del numero de empresas y valor agregado bruto

#Buscando el Valor Agregado Bruto por Provincia y representandolo en el diagrama de dispersion

df_agrupado = df.groupby('des_provincias')['valag', 'id_empresa'].agg({'valag':'sum', 'id_empresa':'count'})

plt.figure(figsize=(10,6))
scatter = plt.scatter(df_agrupado['valag'], df_agrupado['id_empresa'], c=range(len(df_agrupado)), cmap='viridis')
plt.xlabel('Valor Agregado Bruto')
plt.ylabel('Numero de Empresas')
plt.title('Relacion Valor Agregado Bruto y Numero de Empresas')
plt.grid(True)
plt.savefig('NumEmpresas_ValorAgregado.png', bbox_inches='tight', dpi= 600)
<<<<<<< HEAD
plt.show()
=======
plt.show()
>>>>>>> e5d0c97c2ae7a62b4723e910897ffa6e23b7964e
