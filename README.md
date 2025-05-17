# ResoluciónCódigoConcurrente
>El código implementa un juego en el que dos jugadores eligen cartas y el que tiene el valor más alto gana. Se enfrentan durante 3 rondas.
>Este código tiene problemas de concurrencia y hay que refactorizarlo.

## Tabla de Contenidos
- [Características](#características)
- [Desarrollo de la Resolución](#desarrollo-de-la-resolución)
- [Código recibido](#código-recibido)
- [Se notó que:](#se-notó-que)
- [Identificaciones](#identificaciones)
- [Ejecución](#ejecución)
- [Sección Crítica](#sección-crítica)
- [Resolución Propuesta](#resolución-propuesta)
- [Antes](#antes)
- [Después](#después)
- [Continuación de la Resolución](#continuación-de-la-resolución)
- [Última Parte](#última-parte)

## Características 
- [x] Encontrar Sección Crítica
- [x] Manejar la concurrencia de hilos para asegurar la correcta impresión del estado del juego

## Desarrollo de la Resolución
- El principal problema en el código recibido radica en problemas de concurrencia, que depende de la ejecución, puede generar errores o mostrar resultados inesperados.
  >Ya se desarrollará más sobre estos problemas.
  
 ## Código Recibido 
![códigoRecibido](https://github.com/user-attachments/assets/f6d43bdc-f01a-4140-8849-358fed3db163)

![códigoRecibido2](https://github.com/user-attachments/assets/11b56936-e771-4bb3-a037-3c32bb41ec14)

## Se notó que
- Cuando ambos jugadores deben sacar una carta para definir quién gana, en ocasiones el juego no espera a que ambos jugadores elijan antes de decidir el ganador de la ronda. 
- En ese caso, el jugador que no haya sacado carta, estaría jugando con la carta de la ronda anterior. 
- Si esto ocurre en la primera ronda, se produciría un error, ya que el jugador 2 no habría sacado ninguna carta.

## Identificaciones
- Jugadores en espera.
- Jugadores de la partida.
- print_lock para que solo un hilo imprima en la consola a la vez.
- cards_played es un diccionario compartido, donde el acceso y modificación son críticos, ya que varios hilos podrían intentar leer o escribir datos simultáneamente.
- Luego la función, que simula la partida y da como resultado al ganador con un contador interno de puntos para un solo jugador (para cada hilo) “total_points”.
- Por último la iniciación y ejecución de los hilos (estos esperan a que todos terminen con el ".join").

## Ejecución
>La ejecución puede resultar en errores, esto sucede cuando en la primera ronda, jugador uno sacó su carta, jugador dos no, y la ronda intenta definirse.
![ejecuciónCódigo](https://github.com/user-attachments/assets/eb0cc345-c853-4697-a9a0-698c853740ad)

>A la hora de ejecutar el código, este se ejecuta de forma desordenada  por no tener un correcto control de los procesos intervinientes, como podemos ver en este caso donde el jugador 2 terminó el juego antes de terminar la ronda 3.
![ejecuciónCódigo2](https://github.com/user-attachments/assets/76c9b92f-580a-4075-affe-7b0b2ab728df)

## Sección Crítica
>[!NOTE]
>Definimos sección crítica como el acceso concurrente de un recurso compartido por dos o mas hilos.
- Esta sección crítica se encuentra a la hora de intentar definir el resultado de la ronda, ya que esta no espera a que cada jugador elija su carta.
  
![secciónCrítica](https://github.com/user-attachments/assets/6cc566aa-6f83-4b97-9a96-3cfea02980ec)

## Resolución Propuesta
- se decidió implementar Barrier para que los hilos no continúen su ejecución hasta que se encuentren en la misma etapa de ejecución definida por el Barrier.
- Para esto utilizamos threading.Barrier().
- Dicho de otra forma, los dos jugadores no pueden continuar su ejecución hasta que hayan elegido los dos por igual, las cartas para decidir la ronda.

```bash 
round_barrier = threading.Barrier(2)
```
![implementaciónBarrier](https://github.com/user-attachments/assets/dee13170-d313-4b43-9b46-1d66253f67c1)

### Antes
- Anteriormente se definía los jugadores esperando de forma global, lo que imposibilitaba que jueguen más jugadores que el 1 y 2.
-  Y para mejorar el uso de cards_played, se decidió definirlo también dentro de la ronda.
  
>Antes:
>
>![codigóAntes](https://github.com/user-attachments/assets/3529c8c6-881b-44c5-9516-442d6753364a)

### Después
- Se planteó un bucle while, que se ejecuta mientras la cantidad de jugadores esperando sea mayor a uno, para tener mínimo 2 jugadores para una partida.
- Y cuando esta finaliza elimina a los jugadores que jugaron, de la lista de espera.

>Después:
>
>![codigóDespués](https://github.com/user-attachments/assets/0873df28-c361-401e-9c56-469c3dc8f22e)

### Continuación de la Resolución
- Ahora cards_played se define dentro de la función play_round, para que se actualice en cada ronda.
- El siguiente cambio, es la implementación de el barrier, para que todos los hilos, esperen a que ambos jugadores levanten su carta antes de definir al ganador de la misma.

![nuevoCodigó](https://github.com/user-attachments/assets/40f8694f-9a1b-4c3c-86e6-475a77b55a4e)
 - Anteriormente, se producía el error de que a veces se intentaba definir la ronda sin que ambos jugadores hayan levantado su carta, o si sucedía en una ronda posterior a la primera, algún jugador podría jugar con su carta de la ronda anterior.
    >Ya no.
 - El segundo Barrier, se utiliza al finalizar cada ronda del juego, y se espera a que se imprima el resultado para poder iniciar la próxima ronda o partida sin problemas.
 - El uso de print_lock asegura que la salida en consola no se mezcle con las impresiones de otros hilos. Esto es importante en un entorno multihilo.
  
![segundoBarrier](https://github.com/user-attachments/assets/cecb791a-7c12-4be0-922c-17e1ddad6cfd)

### Última Parte
- Lo último del código es la inicialización de los hilos y la determinación de quien es el ganador de la ronda.
- Cuando haya uno o menos jugadores en espera, que no alcanza para poder completar una partida, se nos mostrará un print que nos avisa que no hay jugadores suficientes y la ejecución del código finaliza.
 
![últimaParteDelCodigó](https://github.com/user-attachments/assets/aef5064c-9f71-424b-90f7-bb29ed6c47cd)
