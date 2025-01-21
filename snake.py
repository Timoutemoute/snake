import tkinter as tk
import random

# Dimensions de la grille
taille_grille = 20
taille_case = 20

def deplacer():
    global direction, serpent, nourriture, pieges, score, game_over

    if game_over:
        return

    x, y = serpent[-1]

    if direction == 'haut':
        y -= 1
    elif direction == 'bas':
        y += 1
    elif direction == 'gauche':
        x -= 1
    elif direction == 'droite':
        x += 1

    if (x < 0 or x >= taille_grille or y < 0 or y >= taille_grille or (x, y) in serpent):
        canvas.create_text(taille_grille * taille_case // 2, taille_grille * taille_case // 2, text="Game Over!", fill="red", font=("Arial", 24))
        game_over = True
        return

    serpent.append((x, y))

    if (x, y) in nourriture:
        score += 1
        nourriture.remove((x, y))
        nourriture.append(generer_nourriture())
        if score >= 10:
            nourriture.append(generer_nourriture())
        if score >= 20 and len(pieges) < 5:
            pieges.append(generer_piege())
    elif (x, y) in pieges:
        canvas.create_text(taille_grille * taille_case // 2, taille_grille * taille_case // 2, text="Game Over!", fill="red", font=("Arial", 24))
        game_over = True
        return
    else:
        serpent.pop(0)

    mise_a_jour_grille()
    root.after(100, deplacer)

def generer_nourriture():
    while True:
        x = random.randint(0, taille_grille - 1)
        y = random.randint(0, taille_grille - 1)
        if (x, y) not in serpent and (x, y) not in nourriture and (x, y) not in pieges:
            return (x, y)

def generer_piege():
    while True:
        x = random.randint(0, taille_grille - 1)
        y = random.randint(0, taille_grille - 1)
        if (x, y) not in serpent and (x, y) not in nourriture and (x, y) not in pieges:
            return (x, y)

def mise_a_jour_grille():
    canvas.delete("all")

    for x, y in serpent:
        canvas.create_rectangle(x * taille_case + 1, y * taille_case + 1, (x + 1) * taille_case - 1, (y + 1) * taille_case - 1, fill="green", outline="darkgreen")

    for nx, ny in nourriture:
        canvas.create_oval(nx * taille_case + 2, ny * taille_case + 2, (nx + 1) * taille_case - 2, (ny + 1) * taille_case - 2, fill="red", outline="darkred")

    for px, py in pieges:
        canvas.create_rectangle(px * taille_case + 3, py * taille_case + 3, (px + 1) * taille_case - 3, (py + 1) * taille_case - 3, fill="black", outline="darkgrey")

    canvas.create_text(100, 10, text=f"Score: {score}", fill="blue", font=("Arial", 14))

def changer_direction(nouvelle_direction):
    global direction

    oppositions = {
        "haut": "bas",
        "bas": "haut",
        "gauche": "droite",
        "droite": "gauche"
    }

    if nouvelle_direction != oppositions.get(direction):
        direction = nouvelle_direction

def restart_game():
    global direction, serpent, nourriture, pieges, score, game_over
    direction = 'droite'
    serpent = [(10, 10)]
    nourriture.clear()
    nourriture.append(generer_nourriture())
    pieges.clear()
    score = 0
    game_over = False
    mise_a_jour_grille()
    deplacer()

def save_score():
    with open("snake_score.txt", "a") as f:
        f.write(f"Score: {score}\n")

# Configuration de la fenêtre
root = tk.Tk()
root.title("Snake Game")

canvas = tk.Canvas(root, width=taille_grille * taille_case, height=taille_grille * taille_case, bg="white")
canvas.pack()

# Boutons
frame = tk.Frame(root)
frame.pack()

btn_restart = tk.Button(frame, text="Restart", command=restart_game, bg="lightblue", font=("Arial", 12))
btn_restart.pack(side="left", padx=10)

btn_save = tk.Button(frame, text="Save Score", command=save_score, bg="lightgreen", font=("Arial", 12))
btn_save.pack(side="left", padx=10)

# Initialisation du jeu
direction = 'droite'
serpent = [(10, 10)]
nourriture = []
nourriture.append(generer_nourriture())
pieges = []  # Initialisation de la liste des pièges
score = 0
game_over = False

# Contrôles du clavier
root.bind("<Up>", lambda event: changer_direction("haut"))
root.bind("<Down>", lambda event: changer_direction("bas"))
root.bind("<Left>", lambda event: changer_direction("gauche"))
root.bind("<Right>", lambda event: changer_direction("droite"))

mise_a_jour_grille()
deplacer()

root.mainloop()
