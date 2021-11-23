# discrete-events
A simulation project in python.
The main objetive of this project is to simulate the events that follow:

Puerto Sobrecargado (Overloaded Harbor)

En un puerto de supertanqueros que cuenta con 3 muelles y un remolcador
para la descarga de estos barcos de manera simultánea se desea conocer el tiempo
promedio de espera de los barcos para ser cargados en el puerto.

El puerto cuenta con un bote remolcador disponible para asistir a los tanqueros. Los tanqueros de cualquier tamaño necesitan de un remolcador para
aproximarse al muelle desde el puerto y para dejar el muelle de vuelta al puerto.

El tiempo de intervalo de arribo de cada barco distribuye mediante una función exponencial con λ = 8 horas. Existen tres tamaños distintos de tanqueros:
pequeño, mediano y grande, la probabilidad correspondiente al tamaño de cada
tanquero se describe en la tabla siguiente. El tiempo de carga de cada tanquero
depende de su tamaño y los parámetros de distribución normal que lo representa
también se describen en la tabla siguiente.

|Tamaño  |Probabilidad de Arribo |Tiempo de Carga|
|:---:|:---:| :---:|
|Pequeño |      0.25             |µ = 9, σ2 = 1  |
|Mediano |      0.25             |µ = 12, σ2 = 2 |
|Grande  |      0.5              |µ = 18, σ2 = 3 | 

De manera general, cuando un tanquero llega al puerto, espera en una cola
(virtual) hasta que exista un muelle vacío y que un remolcador esté disponible
para atenderle. Cuando el remolcador está disponible lo asiste para que pueda
comenzar su carga, este proceso demora un tiempo que distribuye exponencial
con λ = 2 horas. El proceso de carga comienza inmediatamente después de que
el barco llega al muelle. Una vez terminado este proceso es necesaria la asistencia
del remolcador (esperando hasta que esté disponible) para llevarlo de vuelta al
puerto, el tiempo de esta operación distribuye de manera exponencial con λ = 1
hora. El traslado entre el puerto y un muelle por el remolcador sin tanquero
distribuye exponencial con λ = 15 minutos.

Cuando el remolcador termina la operación de aproximar un tanquero al
muelle, entonces lleva al puerto al primer barco que esperaba por salir, en caso de
que no exista barco por salir y algún muelle esté vacío, entonces el remolcador se
dirige hacia el puerto para llevar al primer barco en espera hacia el muelle vacío;
en caso de que no espere ningún barco, entonces el remolcador esperar por
algún barco en un muelle para llevarlo al puerto. Cuando el remolcador termina
la operación de llevar algún barco al puerto, este inmediatamente lleva al primer
barco esperando hacia el muelle vacío. En caso de que no haya barcos en los
muelles, ni barcos en espera para ir al muelle, entonces el remolcador se queda
en el puerto esperando por algún barco para llevar a un muelle.

Simule completamente el funcionamiento del puerto. Determine el tiempo
promedio de espera en los muelles.


-----------------------------------------------------------

Para ejecutar los experimentos correr la l\'inea en una consola en el directorio src del proyecto:

```python main.py sim_time file_name```

por ejemplo:

```python main.py 100 harbor_simulation```

Los parámetros son opcionales. De no proveerlos se asumirá que el tiempo de simulación (sim_time) es de 24 horas y que no se quiere escribir los datos resultantes en un archivo. Si se queren guardar estos especificar un nombre de archivo con el parámetro file_name.

Para ejecutar múltiples simulaciones de una vez correr:

```python test.py sim_time number_s creat_file```

donde sim_time sería el tiempo de duración de las simulaciones, number_s el número de simulaciones deseadas y create_file indica si se quieren registar en varios archivos los datos de estas (cada uno con el nombre correspondiente a su número de simulación).

Los tres parámetros son opcionales. De no proveerlos se toman 1000 simulaciones por default, un tiempo de 24 horas y no se guardan los datos.

-----------------------------------------------------------

El informe del proyecto con todos la explicaciones necesarias se encuentra en la carpeta 'report'.