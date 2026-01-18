from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "tic_tac_toe_secret"

# Check winner
def check_winner(board):
    win_patterns = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in win_patterns:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None


@app.route("/", methods=["GET", "POST"])
def index():

    # Initialize session data
    if "board" not in session:
        session["board"] = [""] * 9
        session["current_player"] = "X"
        session["score_x"] = 0
        session["score_o"] = 0
        session["winner"] = None
        session["pause"] = False

    board = session["board"]
    current_player = session["current_player"]
    winner = session["winner"]
    pause = session.get("pause", False)  # <-- FIXED

    # If paused, do not allow moves
    if request.method == "POST" and not winner and not pause:
        cell = int(request.form["cell"])

        if board[cell] == "":
            board[cell] = current_player
            winner = check_winner(board)

            if winner == "X":
                session["score_x"] += 1
            elif winner == "O":
                session["score_o"] += 1
            elif winner is None:
                session["current_player"] = "O" if current_player == "X" else "X"

        session["board"] = board
        session["winner"] = winner

    return render_template(
        "index.html",
        board=board,
        current_player=current_player,
        winner=winner,
        score_x=session["score_x"],
        score_o=session["score_o"],
        pause=pause
    )


@app.route("/reset", methods=["POST"])
def reset():
    session["board"] = [""] * 9
    session["current_player"] = "X"
    session["winner"] = None
    session["pause"] = False
    return redirect(url_for("index"))


@app.route("/pause", methods=["POST"])
def pause():
    session["pause"] = not session.get("pause", False)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
