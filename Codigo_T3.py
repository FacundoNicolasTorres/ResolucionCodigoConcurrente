import threading
import time
import random

# Lista de jugadores en el servidor
players_waiting = ["Player1", "Player2", "Player3", "Player4", "Player5"]
# Seleccionamos dos jugadores para la partida
game_players = players_waiting[:2]

# Lock para imprimir el estado del juego
print_lock = threading.Lock()
# Variables para almacenar la carta jugada por cada jugador en la ronda
cards_played = {}

def play_round(player):
    total_points = 0
    for round_num in range(1, 4):  # El juego tiene 3 rondas
        # Simula el tiempo para elegir una carta
        time.sleep(random.uniform(0.5, 1.5))
        
        # Elige una carta aleatoria entre 1 y 13
        card = random.randint(1, 13)
        with print_lock:
            print(f"{player} ha elegido su carta para la ronda {round_num}.")
        
        # Guardamos la carta jugada en la ronda actual
        cards_played[player] = card
        
        # Solo el primer jugador imprime el resultado de la ronda
        if player == game_players[0]:
            with print_lock:
                print(f"Ronda {round_num} - {game_players[0]} jugó: {cards_played[game_players[0]]}, {game_players[1]} jugó: {cards_played[game_players[1]]}")
            
            # Determina el ganador de la ronda y muestra el resultado
            if cards_played[game_players[0]] > cards_played[game_players[1]]:
                print(f"{game_players[0]} gana la ronda {round_num}!\n")
            elif cards_played[game_players[0]] < cards_played[game_players[1]]:
                print(f"{game_players[1]} gana la ronda {round_num}!\n")
            else:
                print(f"La ronda {round_num} termina en empate!\n")
        
        
    # Resultado final del jugador
    with print_lock:
        print(f"{player} ha terminado el juego con {total_points} puntos.")

# Crear los hilos para los dos jugadores de la partida
player_threads = [
    threading.Thread(target=play_round, args=(game_players[0],)),
    threading.Thread(target=play_round, args=(game_players[1],))
]

# Iniciamos ambos hilos de jugadores
for t in player_threads:
    t.start()

# Esperamos a que ambos hilos terminen
for t in player_threads:
    t.join()

print("La partida ha terminado.")
