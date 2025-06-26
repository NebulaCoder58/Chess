import sys

import chess

import chess.engine

def select_mode():

    print("Wähle den Spielmodus:")

    print("1. Spieler vs. Spieler (PvP)")

    print("2. Spieler vs. KI")

    mode = input("Gib 1 oder 2 ein: ")

    return mode

def select_difficulty():

    print("Wähle KI-Schwierigkeitsgrad (0–20):")

    level = input("Gib einen Wert zwischen 0 (einfach) und 20 (schwer) ein: ")

    try:

        level_int = int(level)

        if 0 <= level_int <= 20:

            return level_int

    except ValueError:

        pass

    print("Ungültige Eingabe, Standard 10 wird verwendet.")

    return 10

def print_board(board):

    """Zeigt das Schachbrett in Unicode mit Rahmen an."""

    print(board.unicode(borders=True))

    print()

def get_move(board):                                                   #Zeile 49 bis 94 Chatgpt hilfe

    """Fragt den Spieler nach einem UCI-Zug und validiert ihn."""

    while True:

        move_input = input("Dein Zug (z.B. e2e4): ")

        try:

            move = chess.Move.from_uci(move_input.strip())

            if move in board.legal_moves:

                return move

            else:

                print("Ungültiger Zug, bitte erneut versuchen.")

        except:

            print("Ungültige Notation, bitte im UCI-Format eingeben.")

def analyze_game(initial_board, moves, engine, time_limit=0.1):

    """Analysiert nach Ende der Partie alle Züge mit Stockfish."""

    print("\n--- Spielanalyse ---")

    board = initial_board.copy()

    for i, move in enumerate(moves):

        board.push(move)

        info = engine.analyse(board, chess.engine.Limit(time=time_limit))

        score = info["score"].white()

        best = info["pv"][0]

        print(f"Zug {i+1}: {move} | Bewertung: {score} | Bester Zug: {best}")

    print("---------------------")

def main():

    # 1. Spielbrett und Engine initialisieren

    board = chess.Board()

    engine_path = "stockfish"  # Stelle sicher, dass Stockfish im PATH ist

    try:

        engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    except FileNotFoundError:

        print("Fehler: Stockfish-Engine nicht gefunden. Bitte installieren und im PATH verfügbar machen.")

        sys.exit(1)

    # 2. Modus- und ggf. Schwierigkeitswahl

    mode = select_mode()

    if mode == "2":

        level = select_difficulty()

        engine.configure({"Skill Level": level})

    # 3. Partie-Schleife

    moves = []

    while not board.is_game_over():

        print_board(board)

        if mode == "1" or (mode == "2" and board.turn == chess.WHITE):

            move = get_move(board)

        else:

            print("KI zieht...")

            result = engine.play(board, chess.engine.Limit(time=0.5))

            move = result.move

            print(f"KI wählt: {move}")

        board.push(move)

        moves.append(move)

    # 4. Anzeige Ergebnis und Analyse

    print_board(board)

    print(f"Spiel beendet: {board.result()}")

    analyze_game(chess.Board(), moves, engine)

    engine.quit()

if __name__ == "__main__":

    main()
#Chatgpt hat die Zeile 49 bis 94 gemacht.