import os
import requests
import base64
from bugfinder import finder
import re


fpath = os.path.expanduser("~/RanagData")
flpath = os.path.join(fpath, "os.txt")

if not os.path.exists(fpath):
    os.makedirs(fpath)

if not os.path.exists(flpath):
    with open(flpath, "w") as f:
        os_name = input("What is your OS? ")
        f.write(os_name)

with open(flpath, "r") as f:
    filect = f.read()
    
def bfrequest(resp):
    if resp.lower() == "{specific}":
        resp = resp.replace("{specific}", "").strip()
        tofindfile = resp.strip()

        try:
            with open(tofindfile, "r") as content:
                contentf = content.read()
                bugs = finder(contentf)

                if bugs == "NIL":
                    return "No Bugs Were Found"
                else:
                    matches = re.findall(r"£(.*?)£", bugs)
                    corrects = re.findall(r"¥(.*?)¥", bugs)

                    for match, correct in zip(matches, corrects):
                        print(f"Bug found in: {match}")
                        print(f"It should be in this way: {correct}")
                        print("---------------------")

                    fix = input("Would you like to fix these bugs? (y/n): ")
                    if fix.lower() == "y":
                        with open(tofindfile, "r") as fixer:
                            content = fixer.read()

                        for match, correct in zip(matches, corrects):
                            content = content.replace(match, correct)

                        with open(tofindfile, "w") as fixer:
                            fixer.write(content)

                        print(f"All the bugs found on {tofindfile} have been fixed.")

        except FileNotFoundError:
            print(f"Error: The file '{tofindfile}' was not found.")

    else:
        print(f"{resp}")
        
def gen(uput):
    API_URL = "https://api-ranagproject.onrender.com/process"
    
    prompt = f"""
<s>[INST] 
You are an AI file manager and terminal assistant for the {filect} When the user asks to perform file operations, respond with:
1. The bash commands that accomplish the task.
2. If writing inside a file, always format it as: filename&content&.
3. Always ensure files are created before writing to them.
4. A short message describing what was done.

Format your response exactly like this:
$command1$
$command2$
$command3$
Short description message

The user's request is: {uput} 
[/INST]"""

    
    data = {"prompt": prompt}

    headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    try:
            response = requests.post(API_URL, json=data, headers=headers)

            if response.status_code == 200:
                resp = response.json()
                resp = resp['generated']
                return str(resp)
            else:
                return f"Error: {response.status_code}\n{response.text}"
    except requests.exceptions.RequestException as e:
            return f"Request Error: {str(e)}"




def rparse(resp):
    parts = resp.split('$')
    cmds = [parts[i].strip() for i in range(1, len(parts), 2) if parts[i].strip()]
    message = parts[-1].strip() if len(parts) % 2 == 0 else parts[-1].strip()
    return cmds, message

def write_files(uput):
    matches = re.findall(r"(\S+)&(.+?)&", uput)
    for filename, content in matches:
        with open(filename, "w") as f:
            f.write(content)
    return bool(matches)

def rcmds(cmds, uput):
    if write_files(uput):
        return True
    for cmd in cmds:
        try:
            os.system(cmd)
        except Exception:
            return False
    return True

def manage():
    print("——————————————\nRanag File Manager\nV 1.3.8\n–––––––———————\nAdded: Bug Finder 0.3.2\nModified: Migrated api to the oficial site.\nRemoved: nil\n——————————————\nSay ‘exit’ to quit or press CTRL + C")

    
    while True:
        uput = input(">")
        
        if uput.lower() == 'exit':
            print("Quitting…")
            break
        
        try:
            resp = gen(uput)
            cmds, message = rparse(resp)
            
            if cmds or write_files(uput):
                ok = rcmds(cmds, uput)
                if ok:
                    print(message)
                else:
                    print("There was a failure performing an action.")
            else:
                bfrequest(resp)
        except Exception as e:
            print("Error!")

if __name__ == "__main__":
    manage()
