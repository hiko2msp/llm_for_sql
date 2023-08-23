import os
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

endpoint = os.environ["ENDPOINT"]
app = App(token=os.environ["SLACK_BOT_TOKEN"])


LOCKFILE = 'lock.txt'
def lockable():
    if os.path.exists(LOCKFILE):
        return False
    
    try:
        with open(LOCKFILE, 'w') as f:
            f.write(str(os.getpid()))
    except:
        return False
    return True

def delete_lock():
    if not os.path.exists(LOCKFILE):
        return
    
    with open(LOCKFILE) as f:
        pid = f.read()

    if str(os.getpid()) != pid:
        return

    os.remove(LOCKFILE)
    

@app.message("llm")
def message_res(message, say):
    if not lockable():
        say(f"現在 {message['user']} さんが利用中です")
        return
    
    input_text = message["text"][4:]
    res = requests.post(f'{endpoint}/chat', json={
        'user_id': message['user'],
        'message': input_text,
    })
    res = res.json()
    say(res)
    delete_lock()

@app.message("reset")
def message_reset(message, say):
    requests.post(f'{endpoint}/reset', json={
        'user_id': message['user'],
    })
    say(f"{message['user']}さんの会話をリセットします")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

