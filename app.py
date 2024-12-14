from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Глобальное состояние игры
game_state = {
    "stage": "intro",
    "player_grid": [[False] * 10 for _ in range(10)],
    "enemy_grid": [[False] * 10 for _ in range(10)],
    "enemy_coords": (random.randint(0, 9), random.randint(0, 9)),
    "player_coords": None,
    "output": (
        "SHOOT<br>CREATIVE COMPUTING<br>MORRISTOWN, NEW JERSEY<br><br><br>DO YOU WANT INSTRUCTIONS? (Y/N)"
    ),
}


@app.route("/", methods=["GET", "POST"])
def index():
    global game_state

    if request.method == "POST":
        command = request.form.get("command", "").strip().lower()

        if game_state["stage"] == "intro":
            if command == "y":
                # Показать инструкции
                game_state["output"] = (
                    "BUT TO LIVE IN PEACE. HOWEVER IT HAS BECOME APPARENT THAT HE<br>"
                    "FEELS HIS PEACE THREATENED AND IS PREPARING AN ATTACK. BOTH<br>"
                    "YOU AND HE HAVE SCANNERS THAT WILL WARN YOU OF HIS MOVEMENTS<br>"
                    "AND TRACK THE FLIGHT OF HIS ATOMIC MISSILES, THUS HE IS WORKING<br>"
                    "SLOWLY. THE ENEMY, LIKE YOURSELF, HAS A MISSILE GRID NEARLY<br>"
                    "IDENTICAL IN STRUCTURE AND OPERATION TO YOURS, BECAUSE YOU<br>"
                    "ARE THE ONLY ONE LEFT, IT WILL BE NECESSARY TO FIRE ALL YOUR<br>"
                    "MISSILES MANUALLY. ONCE THE FUSE IS SET, YOU MUST FLEE THE<br>"
                    "AREA AND GET TWO GRID UNITS AWAY. YOU MAY NEVER RETURN TO<br>"
                    "THIS SPOT, OR A SPOT WHERE A MISSILE HAS LANDED; THE RADIATION<br>"
                    "IS INTENSE AND WOULD MEAN AN INSTANT, PAINFUL DEATH.<br>"
                    "PRESS ENTER."
                )
                game_state["stage"] = "instructions"
            elif command == "n":
                # Пропустить инструкции и перейти к выбору координат
                game_state["output"] = f"SCANNER COMPUTER: ENEMY ACTIVITY ON GRID AT {game_state['enemy_coords'][0] + 1} , {game_state['enemy_coords'][1] + 1}<br>YOUR STARTING CO-ORDINATES? (1-10, 1-10):"
                game_state["stage"] = "get_player_coords"

        elif game_state["stage"] == "instructions" and command == "":
            game_state["output"] = f"SCANNER COMPUTER: ENEMY ACTIVITY ON GRID AT {game_state['enemy_coords'][0] + 1} , {game_state['enemy_coords'][1] + 1}<br>YOUR STARTING CO-ORDINATES? (1-10, 1-10):"
            game_state["stage"] = "get_player_coords"

        elif game_state["stage"] == "get_player_coords":
            try:
                x, y = map(int, command.split(","))
                if 1 <= x <= 10 and 1 <= y <= 10:
                    game_state["player_coords"] = (x - 1, y - 1)
                    game_state["player_grid"][x - 1][y - 1] = True
                    game_state["output"] = render_grid() + "<br>MISSILE CO-ORDINATES? (1-10, 1-10):"
                    game_state["stage"] = "missile_phase"
                else:
                    game_state["output"] += "<br>Invalid coordinates. Try again."
            except ValueError:
                game_state["output"] += "<br>Invalid input. Use format x,y (e.g., 1,5)."

        elif game_state["stage"] == "missile_phase":
            try:
                missile_x, missile_y = map(int, command.split(","))
                if 1 <= missile_x <= 10 and 1 <= missile_y <= 10:
                    missile_coords = (missile_x - 1, missile_y - 1)
                    game_state["player_grid"][missile_coords[0]][missile_coords[1]] = True

                    if missile_coords == game_state["enemy_coords"]:
                        game_state["output"] = "YOU GOT HIM!!<br>GAME OVER"
                        game_state["stage"] = "game_over"
                    else:
                        game_state["output"] = (
                            render_grid() + "<br>WHERE TO MOVE? (1-10, 1-10):"
                        )
                        game_state["stage"] = "move_phase"
                else:
                    game_state["output"] += "<br>Invalid missile coordinates. Try again."
            except ValueError:
                game_state["output"] += "<br>Invalid input. Use format x,y (e.g., 1,5)."

        elif game_state["stage"] == "move_phase":
            try:
                move_x, move_y = map(int, command.split(","))
                if 1 <= move_x <= 10 and 1 <= move_y <= 10:
                    move_coords = (move_x - 1, move_y - 1)
                    if game_state["player_grid"][move_coords[0]][move_coords[1]]:
                        game_state["output"] += "<br>You cannot move to a previously occupied location."
                    else:
                        game_state["player_grid"][move_coords[0]][move_coords[1]] = True
                        game_state["output"] = render_grid() + "<br>MISSILE CO-ORDINATES? (1-10, 1-10):"
                        game_state["stage"] = "missile_phase"
                else:
                    game_state["output"] += "<br>Invalid move coordinates. Try again."
            except ValueError:
                game_state["output"] += "<br>Invalid input. Use format x,y (e.g., 1,5)."

        return redirect(url_for("index"))

    return render_template("index.html", output=game_state["output"])


def render_grid():
    header = " -12345678910"
    player_grid = game_state["player_grid"]
    enemy_grid = game_state["enemy_grid"]
    rows = [header + " " * 4 + header]
    for i in range(10):
        row_number = f"{i + 1:<2}"
        player_row = ''.join('*' if cell else ':' for cell in player_grid[i])
        enemy_row = ''.join('*' if cell else ':' for cell in enemy_grid[i])
        rows.append(f"{row_number}{player_row}     {row_number}{enemy_row}")
    return "<br>".join(rows)


if __name__ == "__main__":
    app.run(debug=True)
