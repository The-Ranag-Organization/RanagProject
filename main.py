import os
import requests
import base64
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
    

def gen(uput, api_key):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {api_key}"}
    
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
    
    params = {
        "max_new_tokens": 256,
        "temperature": 0.7,
        "top_p": 0.95,
        "do_sample": True
    }
    
    pload = {
        "inputs": prompt,
        "parameters": params
    }
    
    response = requests.post(API_URL, headers=headers, json=pload)
    
    if response.status_code == 200:
        resp = response.json()
        if isinstance(resp, list) and len(resp) > 0:
            generated = resp[0].get('generated_text', '')
            if generated.startswith(prompt):
                return generated[generated.find("[/INST]") + 7:].strip()
            return generated
        return str(resp)
    else:
        return f"Error: {response.status_code}"

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
    print("——————————————\nRanag File Manager\nV 1.1.4\n–––––––———————\nAdded: Writing inside files support, added support to compiling and running apps, added support to execute all installed global executables.\nModified: nil\nRemoved: nil\n——————————————\nSay ‘exit’ to quit or press CTRL + C")

    with open("APIKEY.txt", "r") as ap:
      api_key = ap.read()
    
    if not api_key:
        print("API key missing")
        return
    
    while True:
        uput = input(">")
        
        if uput.lower() == 'exit':
            print("Quitting…")
            break
        
        try:
            resp = gen(uput, api_key)
            cmds, message = rparse(resp)
            
            if cmds or write_files(uput):
                ok = rcmds(cmds, uput)
                if ok:
                    print(message)
                else:
                    print("There was a failure performing an action.")
            else:
                print(f"{resp}")
        except Exception as e:
            print("Error!")

if __name__ == "__main__":
    manage()
