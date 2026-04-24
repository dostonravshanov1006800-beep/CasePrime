from fastapi import FastAPI
import random
import time

app = FastAPI()

users = {}
leaderboard = []
daily_reset_time = time.time()

# -----------------
# USERS
# -----------------
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"balance": 1000, "wins": 0}
    return users[user_id]

# -----------------
# SLOT GAME
# -----------------
def slot_game():
    symbols = ["🍒", "💎", "7", "⭐"]
    result = [random.choice(symbols) for _ in range(3)]

    win = result[0] == result[1] == result[2]

    reward = 500 if win else -50
    return result, reward

# -----------------
# CASE GAME
# -----------------
def open_case():
    roll = random.randint(1, 100)

    if roll < 70:
        return "Common NFT", 50
    elif roll < 92:
        return "Rare NFT", 150
    elif roll < 99:
        return "Epic NFT", 400
    else:
        return "Legendary NFT", 1000

# -----------------
# LEADERBOARD RESET (DAILY)
# -----------------
def reset_if_needed():
    global leaderboard, daily_reset_time
    if time.time() - daily_reset_time > 86400:
        leaderboard = []
        daily_reset_time = time.time()

# -----------------
# UPDATE LEADERBOARD
# -----------------
def update_lb(user_id, score):
    leaderboard.append({"user": user_id, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard[:10]

# -----------------
# API
# -----------------

@app.get("/balance/{user_id}")
def balance(user_id: int):
    return get_user(user_id)

@app.post("/slot/{user_id}")
def slot(user_id: int):
    user = get_user(user_id)

    result, reward = slot_game()
    user["balance"] += reward

    if reward > 0:
        user["wins"] += reward
        update_lb(user_id, reward)

    return {
        "result": result,
        "reward": reward,
        "balance": user["balance"]
    }

@app.post("/case/{user_id}")
def case(user_id: int):
    user = get_user(user_id)

    item, reward = open_case()
    user["balance"] += reward

    if reward > 0:
        update_lb(user_id, reward)

    return {
        "item": item,
        "reward": reward,
        "balance": user["balance"]
    }

@app.get("/leaderboard")
def lb():
    reset_if_needed()
    return leaderboard[:10]
