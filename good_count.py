import random  # Permet de tirer des nombres au hasard

# ------------------------------------------------------------
#  Création du jeu de 24 plaques
# ------------------------------------------------------------
def create_tile_set() -> list[int]:
    """Crée les 24 plaques : 1 à 10 en double + 25, 50, 75, 100 en un seul exemplaire."""
    return [n for n in range(1, 11) for _ in range(2)] + [25, 50, 75, 100]


# ------------------------------------------------------------
#  Tirage aléatoire de 6 plaques (au moins une grande plaque)
# ------------------------------------------------------------
def draw_tiles(tiles: list[int], count: int = 6) -> list[int]:
    """Tire 6 plaques au hasard, dont au moins une grande (25, 50, 75, 100)."""
    while True:
        drawn = random.sample(tiles, count)
        # Vérifie qu'il y a au moins une grande plaque
        if any(n in (25, 50, 75, 100) for n in drawn):
            return drawn


# ------------------------------------------------------------
#  Génération du nombre cible
# ------------------------------------------------------------
def generate_target() -> int:
    """Génère un nombre aléatoire entre 101 et 999."""
    return random.randint(101, 999)


# ------------------------------------------------------------
#  Vérification de la validité des opérations
# ------------------------------------------------------------
def is_valid(a: int, b: int, op: str) -> bool:
    """Vérifie si l'opération choisie est autorisée."""
    # Division : b ≠ 0 et le résultat doit être un entier
    # Soustraction : a >= b pour éviter les nombres négatifs
    # Addition et multiplication : toujours valides
    return (op == "÷" and b != 0 and a % b == 0) or (op == "-" and a >= b) or op in ("+", "×")


# ------------------------------------------------------------
#  Calcul d’une opération
# ------------------------------------------------------------
def calculate(a: int, b: int, op: str) -> int | None:
    """Effectue le calcul si l’opération est valide, sinon renvoie None."""
    if not is_valid(a, b, op):
        return None
    ops = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "×": lambda x, y: x * y,
        "÷": lambda x, y: x // y  # Division entière
    }
    return ops[op](a, b)


# ------------------------------------------------------------
#  Affichage de l’état du jeu
# ------------------------------------------------------------
def display_state(tiles: list[int], results: list[int], target: int) -> None:
    """Affiche les plaques, les résultats obtenus et la cible."""
    print(f"\nNombre à obtenir : {target}")
    print(f"Plaques : {sorted(tiles) if tiles else 'Aucune'}")
    print(f"Nombres obtenus : {sorted(results) if results else 'Aucun'}")


# ------------------------------------------------------------
#  Lecture et interprétation de la saisie utilisateur
# ------------------------------------------------------------
def parse_input(text: str) -> tuple[int, int, str] | None:
    """Analyse une saisie du type '25 + 3'."""
    try:
        parts = text.replace("×", "*").replace("÷", "/").replace("x", "×").split()
        if len(parts) == 3:
            return (int(parts[0]), int(parts[2]), parts[1].replace("*", "×").replace("/", "÷"))
    except ValueError:
        pass
    return None


# ------------------------------------------------------------
#  Choix de l’utilisateur
# ------------------------------------------------------------
def get_choice(tiles: list[int], results: list[int]) -> tuple[int, int, str] | None:
    """Demande à l’utilisateur une opération ou l’arrêt du jeu."""
    print("\n- Opération (ex: 25 + 3) ou 'stop' pour arrêter")
    inp = input("Votre choix : ").strip().lower()

    if inp in ("stop", ""):
        return None

    parsed = parse_input(inp)
    if not parsed:
        print("\nFormat invalide. Exemple : 25 + 3")
        return get_choice(tiles, results)

    num1, num2, op = parsed
    all_nums = tiles + results

    # Vérifie la disponibilité des nombres
    if num1 not in all_nums or num2 not in all_nums:
        print(f"\nErreur : nombres non disponibles\nDisponibles : {sorted(all_nums)}")
        return get_choice(tiles, results)

    # Vérifie qu'on ne réutilise pas deux fois le même nombre s’il n’existe qu’une fois
    if num1 == num2 and all_nums.count(num1) < 2:
        print("\nErreur : ce nombre n'est disponible qu'une fois")
        return get_choice(tiles, results)

    # Vérifie la validité de l’opération
    if op not in ("+", "-", "×", "÷"):
        print("\nErreur : opération invalide (+, -, ×, ÷)")
        return get_choice(tiles, results)

    return (num1, num2, op)


# ------------------------------------------------------------
#  Suppression d’un nombre utilisé
# ------------------------------------------------------------
def remove_num(num: int, tiles: list[int], results: list[int]) -> None:
    """Supprime un nombre utilisé des listes disponibles."""
    (tiles if num in tiles else results).remove(num)


# ------------------------------------------------------------
#  Choix du nombre final à la fin du jeu
# ------------------------------------------------------------
def choose_final(tiles: list[int], results: list[int]) -> int | None:
    """Permet de choisir le nombre final si l’utilisateur arrête le jeu."""
    all_nums = tiles + results
    if not all_nums:
        return None
    if len(all_nums) == 1:
        return all_nums[0]

    print("\nCHOIX DU NOMBRE FINAL")
    print("Choisissez UN nombre (pas d'opération)")
    print(f"Disponibles : {sorted(all_nums)}")

    while True:
        try:
            inp = input("\nVotre choix : ").strip()
            if not inp or " " in inp:
                print("Erreur : un seul nombre")
                continue
            choice = int(inp)
            if choice in all_nums:
                return choice
            print(f"Erreur : {choice} non disponible")
        except ValueError:
            print("Erreur : nombre entier valide requis")


# ------------------------------------------------------------
#  Affichage du résultat final
# ------------------------------------------------------------
def show_result(final: int, target: int) -> None:
    """Affiche le résultat final et la différence avec la cible."""
    if final == target:
        print(f"\n LE COMPTE EST BON ! Vous avez atteint {target} !")
    else:
        gap = abs(final - target)
        print(f"\nNombre obtenu : {final}\nNombre à obtenir : {target}\nÉcart : {gap}")
        if gap <= 10:
            print("Très proche ! ")


# ------------------------------------------------------------
#  Fonction principale du jeu
# ------------------------------------------------------------
def play() -> None:
    """Lance une partie complète du jeu."""
    tiles = draw_tiles(create_tile_set())  # Tire les plaques (au moins une grande)
    target = generate_target()             # Génère le nombre à atteindre
    results = []                           # Liste pour stocker les résultats intermédiaires

    print("\n LE COMPTE EST BON ")
    print(f"\nNombre à obtenir : {target}\nPlaques : {sorted(tiles)}")
    print("\nRègles :")
    print("- Chaque nombre utilisable une fois")
    print("- Division → résultat entier")
    print("- Soustraction → résultat ≥ 0")

    while True:
        display_state(tiles, results, target)

        # Si toutes les plaques ont été utilisées et qu’il ne reste qu’un nombre
        if not tiles and len(results) <= 1:
            print("\nPartie terminée : plus de plaques et un seul nombre")
            final = results[0] if results else None
            if final is None:
                print("Aucun nombre disponible !")
                return
            break

        # Choix de l’utilisateur
        choice = get_choice(tiles, results)
        if choice is None:
            print("\nArrêt du jeu.")
            final = choose_final(tiles, results)
            if final is None:
                print("Aucun nombre disponible !")
                return
            break

        num1, num2, op = choice
        result = calculate(num1, num2, op)

        if result is None:
            print("\nOpération invalide !")
            print(f"Rappel : {op} → " + ("résultat entier" if op == "÷" else "résultat ≥ 0"))
            continue

        print(f"\nRésultat : {num1} {op} {num2} = {result}")

        # Mise à jour des plaques
        remove_num(num1, tiles, results)
        remove_num(num2, tiles, results)
        results.append(result)

        # Vérifie si le compte est bon
        if result == target:
            print(f"\n LE COMPTE EST BON ! Vous avez atteint {target} !")
            return

    # Fin du jeu : affiche le résultat final
    show_result(final, target)


# ------------------------------------------------------------
#  Lancement du programme
# ------------------------------------------------------------
if __name__ == "__main__":
    play()
