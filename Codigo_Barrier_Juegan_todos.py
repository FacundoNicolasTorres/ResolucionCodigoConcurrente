import threading
import time
import random

# Lista de jugadores en el servidor
players_waiting = ["Player1", "Player2", "Player3", "Player4", "Player5"]

# Lock para imprimir el estado del juego
print_lock = threading.Lock()

def play_round(player, points, round_barrier, cards_played):
    for round_num in range(1, 4):  # El juego tiene 3 rondas
        # Simula el tiempo para elegir una carta
        time.sleep(random.uniform(0.5, 1.5))
        
        # Elige una carta aleatoria entre 1 y 13
        card = random.randint(1, 13)
        cards_played[player] = card

        with print_lock:
            print(f"{player} ha elegido su carta para la ronda {round_num}.")
        
        # Esperamos a que ambos jugadores hayan elegido sus cartas
        round_barrier.wait()

        # Solo el primer jugador imprime el resultado de la ronda
        if player == list(cards_played.keys())[0]:
            opponent = list(cards_played.keys())[1]
            with print_lock:
                print(f"Ronda {round_num} - {player} jugó: {cards_played[player]}, {opponent} jugó: {cards_played[opponent]}")
            
            # Determina el ganador de la ronda y muestra el resultado
            if cards_played[player] > cards_played[opponent]:
                print(f"{player} gana la ronda {round_num}!\n")
                points[player] += 1
            elif cards_played[player] < cards_played[opponent]:
                print(f"{opponent} gana la ronda {round_num}!\n")
                points[opponent] += 1
            else:
                print(f"La ronda {round_num} termina en empate!\n")

        # Esperamos a que se muestre el resultado antes de pasar a la siguiente ronda
        round_barrier.wait()
        
    # Resultado final del jugador
    with print_lock:
        print(f"{player} ha terminado el juego con {points[player]} puntos.")

while len(players_waiting) >= 2:
    # Tomamos los primeros dos jugadores de la lista de espera para una nueva partida
    game_players = players_waiting[:2]

    # Inicializamos los puntos y las cartas jugadas de los jugadores
    points = {game_players[0]: 0, game_players[1]: 0}
    cards_played = {}
    
    # Crear una barrera nueva para cada partida
    round_barrier = threading.Barrier(2)

    # Crear los hilos para los dos jugadores de la partida
    player_threads = [
        threading.Thread(target=play_round, args=(game_players[0], points, round_barrier, cards_played)),
        threading.Thread(target=play_round, args=(game_players[1], points, round_barrier, cards_played))
    ]

    # Iniciamos ambos hilos de jugadores
    for t in player_threads:
        t.start()

    # Esperamos a que ambos hilos terminen
    for t in player_threads:
        t.join()

    # Determinar y anunciar el ganador final
    if points[game_players[0]] > points[game_players[1]]:
        print(f"{game_players[0]} gana el juego con {points[game_players[0]]} puntos!")
    elif points[game_players[0]] < points[game_players[1]]:
        print(f"{game_players[1]} gana el juego con {points[game_players[1]]} puntos!")
    else:
        print("El juego termina en empate!")

    # Retiramos a los jugadores de la lista de espera
    players_waiting = players_waiting[2:]
    if len(players_waiting) > 1:
        print("\nEsperando nuevos jugadores para la próxima partida...\n")
    else:
        print("\nNo hay jugadores suficientes para una nueva partida...\n")