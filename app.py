from flask import Flask, send_from_directory
import os
import git
from other import PORT, SECOND_PORT
from config import LOCAL_REPO_PATH, REPO_URL
import threading
app = Flask(__name__)
def clone_repository():
    if not os.path.exists(LOCAL_REPO_PATH):
        os.makedirs(LOCAL_REPO_PATH)  
        print(f"Directory {LOCAL_REPO_PATH} created.")
    if not os.listdir(LOCAL_REPO_PATH):
        print("Cloning repository...")
        git.Repo.clone_from(REPO_URL, LOCAL_REPO_PATH)
        print("Repository cloned successfully.")
    else:
        print(f"Directory {LOCAL_REPO_PATH} is not empty. Clone operation aborted.")
clone_repository()
@app.route('/<path:subpath>')
def send_static(path):
    return send_from_directory(LOCAL_REPO_PATH, path)
@app.route('/')
def index():
    return send_from_directory(LOCAL_REPO_PATH, 'index.html')
app2 = Flask(__name__)
@app2.route('/public2')
def another_index():
    return "This is another server!"
def run_first_server():
    app.run(host='0.0.0.0', port=PORT)
def run_second_server():
    app2.run(host='0.0.0.0', port=SECOND_PORT)
if __name__ == '__main__':
    thread1 = threading.Thread(target=run_first_server)
    thread2 = threading.Thread(target=run_second_server)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()