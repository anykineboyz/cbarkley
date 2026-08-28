from flask import Flask, request
import requests
import os
import re
import random

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------

BOT_ID = os.environ.get("BOT_ID")

# -----------------------------
# NIKO BANNED WORDS
# -----------------------------

NIKO_ONLY_BANNED_WORDS = [
    "eva",
    "rene",
    "brendon",
    "drill sergeant",
    "clanker",
    "shh",
    "hehe",
    "haha",
    "die",
    "kill",
    "stupid",
    "dumb",
    "mom",
    "dad",
    "shhh",
    "idiot",
    "ass",
    "shut",
    "uncle",
    "aunty",
    "what",
    "no",
    "stop",
    "fine"
]

# -----------------------------
# STORAGE
# -----------------------------

message_count = 0

# -----------------------------
# CHARLES BARKLEY-STYLE MESSAGES
# -----------------------------

barkley_messages = [

    "Niko, I'm gonna be honest with you. Nobody asked.",

    "Niko, that's a terrible message. Just terrible.",

    "Man, Niko, what are you even doing?",

    "Niko, you need to stop talking before you embarrass yourself.",

    "I've seen enough, Niko. Go sit down somewhere.",

    "Niko, you're just running your mouth now.",

    "That might be the worst message I've seen all day, Niko.",

    "Niko, please. You're killing me with this.",

    "Niko, I don't know what you're talking about, but I know it ain't right.",

    "Niko, I'm trying to figure out what your point is. I really am.",

    "Man, nobody wants to hear all that, Niko.",

    "Niko, you're talking like you know something. You don't.",

    "That's a terrible take, Niko. You gotta do better than that.",

    "Niko, just because you can talk doesn't mean you should.",

    "Niko, I'm gonna need you to think before you send these messages.",

    "Man, Niko, you're making absolutely no sense right now.",

    "Niko, go ahead and delete that message. I'll wait.",

    "Niko, I've heard enough. Pack it up.",

    "Niko, you're doing too much. Just relax.",

    "Niko, nobody is impressed. Trust me.",

    "Man, Niko, what kind of nonsense is this?",

    "Niko, you had a chance to say something smart and you chose THAT.",

    "Niko, I'm not mad. I'm just confused.",

    "Niko, you gotta stop giving us these terrible messages.",

    "That's not even a good argument, Niko. Come on, man.",

    "Niko, you're making this way harder than it needs to be.",

    "Man, Niko, just take the L and move on.",

    "Niko, I don't know who told you that was a good idea, but they lied.",

    "Niko, please stop before you make this worse.",

    "I've watched enough basketball to know when something is bad. That message was bad.",

    "Niko, that's a first-ballot Hall of Fame terrible message.",

    "Niko, you're shooting 0-for-10 from the GroupMe right now.",

    "Man, Niko, pass the phone to somebody else.",

    "Niko, the GroupMe is not your personal television show.",

    "Niko, you're talking like you're getting paid for this.",

    "Niko, I respect the confidence, but the message was awful.",

    "Man, Niko, just go sit down somewhere and think about this.",

    "Niko, that's enough. Even I don't have time for this.",

    "Niko, I'm begging you. Stop talking.",

    "Niko, this is why we can't have nice things.",

    "Man, you can't keep sending messages like that and expect us to take you seriously."

]

# -----------------------------
# SEND MESSAGE
# -----------------------------

def send_message(text):

    if not BOT_ID:
        print("BOT_ID missing")
        return

    try:
        response = requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": BOT_ID,
                "text": text
            },
            timeout=10
        )

        print("GroupMe response:", response.status_code)

    except Exception as error:
        print("Error sending GroupMe message:", error)

# -----------------------------
# WEBHOOK
# -----------------------------

@app.route("/", methods=["POST"])
def webhook():

    global message_count

    data = request.json

    if not data:
        return "ok", 200

    # Ignore bot messages
    if data.get("sender_type") == "bot":
        return "ok", 200

    name = data.get(
        "name",
        "Unknown"
    )

    name_lower = name.lower()

    message = data.get(
        "text",
        ""
    ).strip()

    message_lower = message.lower()

    # -----------------------------
    # ONLY WATCH NIKO OR ITACHI
    # -----------------------------

    if "niko" not in name_lower and "itachi" not in name_lower:
        return "ok", 200

    # -----------------------------
    # COUNT MESSAGES
    # -----------------------------

    message_count += 1

    print(
        f"Tracked message #{message_count} from {name}"
    )

    # -----------------------------
    # BANNED WORD CHECK
    # -----------------------------

    for word in NIKO_ONLY_BANNED_WORDS:

        if re.search(
            rf"\b{re.escape(word)}\b",
            message_lower
        ):

            send_message(
                f"Niko, I respect the confidence, but the message was awful."
            )

            break

    # -----------------------------
    # EVERY 3RD MESSAGE
    # -----------------------------

    if message_count % 5 == 0:

        send_message(
            random.choice(
                barkley_messages
            )
        )

    return "ok", 200


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
