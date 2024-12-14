import random

def print_intro():
    print(" " * 27 + "SHOOT")
    print(" " * 20 + "CREATIVE COMPUTING")
    print(" " * 18 + "MORRISTOWN, NEW JERSEY")
    print("\n" * 3)

def print_instructions():
    print("IT IS THE FINAL HOUR OF MAN. YOU AND A WARRING NATION")
    print("HAVE ENTERED INTO A LAST CONTEST. ALL THE LIFE NOW LEFT ON")
    print("EARTH ARE YOU AND YOUR ENEMY. BOTH HE AND YOU HAVE FOUND THE")
    print("LAST REMAINING ATOMIC MISSILE SILO MATRICES ESTABLISHED BY")
    print("THE NOW-DEAD SUPERPOWERS. HE, LIKE YOU, WISHES NOT TO DIE")
    print("BUT TO LIVE IN PEACE. HOWEVER IT HAS BECOME APPARENT THAT HE")
    print("FEELS HIS PEACE THREATENED AND IS PREPARING AN ATTACK. BOTH")
    print("YOU AND HE HAVE SCANNERS THAT WILL WARN YOU OF HIS MOVEMENTS")
    print("AND TRACK THE FLIGHT OF HIS ATOMIC MISSILES, THUS HE IS WORKING")
    print("SLOWLY. THE ENEMY, LIKE YOURSELF, HAS A MISSILE GRID NEARLY")
    print("IDENTICAL IN STRUCTURE AND OPERATION TO YOURS, BECAUSE YOU")
    print("ARE THE ONLY ONE LEFT, IT WILL BE NECESSARY TO FIRE ALL YOUR")
    print("MISSILES MANUALLY. ONCE THE FUSE IS SET, YOU MUST FLEE THE")
    print("AREA AND GET TWO GRID UNITS AWAY. YOU MAY NEVER RETURN TO")
    print("THIS SPOT, OR A SPOT WHERE A MISSILE HAS LANDED; THE RADIATION")
    print("IS INTENSE AND WOULD MEAN AN INSTANT, PAINFUL DEATH.")

def print_grid(player_grid, enemy_grid):
    header = " -12345678910"
    print(header + " " * 4 + header)
    for i in range(10):
        row_number = f"{i + 1:<2}"  # Row number with padding
        player_row = ''.join('*' if cell else ':' for cell in player_grid[i])
        enemy_row = ''.join('*' if cell else ':' for cell in enemy_grid[i])
        print(f"{row_number}{player_row}     {row_number}{enemy_row}")

def get_coordinates(prompt):
    while True:
        try:
            coords = input(prompt).split(',')
            x, y = int(coords[0]), int(coords[1])
            if 1 <= x <= 10 and 1 <= y <= 10:
                return x - 1, y - 1  # Convert to 0-based index
            else:
                print("Coordinates must be between 1 and 10.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter in the format x,y where x and y are numbers.")

def main():
    print_intro()

    if input("DO YOU WANT INSTRUCTIONS?").lower() == 'y':
        print_instructions()

    player_grid = [[False] * 10 for _ in range(10)]
    enemy_grid = [[False] * 10 for _ in range(10)]

    enemy_x, enemy_y = random.randint(0, 9), random.randint(0, 9)
    enemy_grid[enemy_x][enemy_y] = True

    print("SCANNER COMPUTER: ENEMY ACTIVITY ON GRID AT", enemy_x + 1, ',', enemy_y + 1)

    player_x, player_y = get_coordinates("YOUR STARTING CO-ORDINATES? (1-10, 1-10): ")
    player_grid[player_x][player_y] = True

    print_grid(player_grid, enemy_grid)

    while True:
        missile_x, missile_y = get_coordinates("MISSILE CO-ORDINATES? (1-10, 1-10): ")
        move_x, move_y = get_coordinates("WHERE TO MOVE? (1-10, 1-10): ")

        if player_grid[move_x][move_y]:
            print("You cannot move to a previously occupied location.")
            continue

        player_grid[missile_x][missile_y] = True
        player_grid[move_x][move_y] = True

        print_grid(player_grid, enemy_grid)

        if (missile_x, missile_y) == (enemy_x, enemy_y):
            print("YOU GOT HIM!!")
            break

        if (move_x, move_y) == (enemy_x, enemy_y):
            print("YOU MOVED RIGHT UNDER HIS MISSILE!!")
            break

        print("Enemy is moving...")
        enemy_x, enemy_y = random.randint(0, 9), random.randint(0, 9)
        enemy_grid[enemy_x][enemy_y] = True

        print_grid(player_grid, enemy_grid)

if __name__ == "__main__":
    main()
