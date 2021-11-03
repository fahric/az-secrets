import os
import tkinter as tk
import tkinter as tk
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from tkinter import messagebox
from tkinter import filedialog

OPTIONS = [
"prov-frontend-expo-local-config-file",
"prov-frontend-expo-dev-config-file",
"prov-frontend-expo-qa-config-file",
"prov-backend-local-env-file",
"prov-backend-dev-env-file",
"prov-backend-qa-env-file"
] #etc


keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)


root = tk.Tk()
root.title('Compate and update secrets in AZURE')
root.geometry("1200x600")

selectedSecret = tk.StringVar(root)
selectedSecret.set(OPTIONS[0]) # default value


f = tk.Frame(root, width=80, height=40)
f.place(x=10, y=20)
f.pack()
leftframe = tk.Frame(root)  
leftframe.pack(side = tk.LEFT)  

rightframe = tk.Frame(root)  
rightframe.pack(side = tk.RIGHT)  
  
  
# Create label
label = tk.Label(leftframe, text = "Secret in Azure")
label.config(font =("Courier", 14))
label.pack(side=tk.TOP)


w = tk.OptionMenu(leftframe, selectedSecret, *OPTIONS)
w.config(width=40)
w.pack(side=tk.TOP)

secretValueTextBox = tk.Text(leftframe, height=70, width=90, background="white",insertbackground="black",  foreground="black")
secretValueTextBox.pack(side=tk.LEFT)


def getSecretCallBack():
    retrieved_secret = client.get_secret(selectedSecret.get())
    secretValueTextBox.insert(tk.END, retrieved_secret.value)

def saveSecretCallBack():
    secretValue = secretValueTextBox.get(1.0, "end-1c")
    MsgBox = tk.messagebox.askquestion ('Saving',f"Are you sure you want to update the {selectedSecret.get()}",icon = 'warning')
    if MsgBox == 'yes':
        client.set_secret(selectedSecret.get(), secretValue)
        messagebox.showinfo("Information","Secret has been updated")
    else:
        messagebox.showinfo("Information","Better to be safe then sorry")

def getLocalEvnFile():
    global df

    import_file_path = filedialog.askopenfilename()
    if import_file_path:
        f = open(import_file_path, "r")
        data = f.read()
        localSecretValueTextBox.insert(tk.END, data)

  
# Create button for next text.
getSecretValueButton = tk.Button(leftframe, text = "Get Value",command=getSecretCallBack)
getSecretValueButton.pack(side=tk.TOP)

saveSecretValueButton = tk.Button(leftframe, text = "Save Value",command=saveSecretCallBack)
saveSecretValueButton.pack(side=tk.TOP)

# Create an Exit button.
exitButton = tk.Button(leftframe, text = "Exit", command = root.destroy)
exitButton.pack(side=tk.TOP)


labelRight = tk.Label(rightframe, text = "Local env file")
labelRight.config(font =("Courier", 14))
labelRight.pack(side=tk.TOP)

browseButton_Excel = tk.Button(rightframe, text='Import .env File', command=getLocalEvnFile, bg='black', fg='black',
                               font=('helvetica', 12, 'bold'))
  
browseButton_Excel.pack(side=tk.TOP)

localSecretValueTextBox = tk.Text(rightframe, height=70, width=90, background="white",insertbackground="black", foreground="black")
localSecretValueTextBox.pack(side=tk.LEFT)
  
tk.mainloop()