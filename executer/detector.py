import time
import git
import subprocess
import os
import signal


REPO_PATH = "./.watching"
BRANCH_NAME = "master"
POLL_INTERVAL = 5

def save_sha(sha):
    with open("sha.txt", "w") as f:
        f.write(sha)
        f.close()

def get_save_sha():
    try:
        with open("sha.txt", "r") as f:
            sha = f.read().strip()
            f.close()
            return sha
    except FileNotFoundError:
        return None

def main():
    repo = git.Repo(REPO_PATH)
    repo.git.checkout(BRANCH_NAME)
    remote = repo.remotes["origin"]
    remote.fetch()
    repo.git.pull("origin", BRANCH_NAME)
    print('iniciando')
    while True:
        time.sleep(POLL_INTERVAL)
        repo.git.pull("origin", BRANCH_NAME)
        sha_ = repo.git.log(-1).split("\n")[0].split(" ")[-1].strip()
        if get_save_sha() != sha_:
            sha = sha_
            save_sha(sha)
            # Save the PID of the running process
            pid_file = "watching_pid.txt"

            # Kill the previous process if it exists
            if os.path.exists(pid_file):
                with open(pid_file, "r") as f:
                    old_pid = f.read().strip()
                try:
                    os.kill(int(old_pid), signal.SIGTERM)
                except ProcessLookupError:
                    pass  # Process already terminated

            # Start the new process
            try:
                process = subprocess.Popen(["python3", ".watching/main.py", ".watching/"], preexec_fn=os.setsid)
            except Exception as e:
                open("/error.txt", "w").write(str(e))
                print(f"Error starting process: {e}")
            with open(pid_file, "w") as f:
                f.write(str(process.pid))

            print(f"New commit detected: {sha}")


if __name__ == "__main__":
    main()
