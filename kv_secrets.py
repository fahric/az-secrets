import os
import tkinter as tk
import tkinter as tk
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from tkinter import messagebox
from tkinter import filedialog

OPTIONS = [
"Please select a secret name",
"prov-frontend-expo-local-config-file",
"prov-frontend-expo-dev-config-file",
"prov-frontend-expo-qa-config-file",
"prov-backend-local-env-file",
"prov-backend-dev-env-file",
"prov-backend-qa-env-file",
"prov-db-mgr-local-env-file",
"prov-db-mgr-dev-env-file",
"prov-db-mgr-qa-env-file"
] #etc


keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)


def getSecretCallBack():
    try:
        selected_secret_name = selectedSecret.get()
        if selected_secret_name == "Please select a secret name":
            messagebox.showwarning("Warning","Please select a secret")
        else:
            retrieved_secret = client.get_secret(selected_secret_name)
            secretValueTextBox.delete('1.0', tk.END)
            secretValueTextBox.insert(tk.END, retrieved_secret.value)
    except:
        secretValueTextBox.delete('1.0', tk.END)
        messagebox.showerror("Error","There was an error getting the secret")


def saveSecretCallBack():
    selected_secret_name = selectedSecret.get()
    if selected_secret_name == "Please select a secret name":
            messagebox.showwarning("Warning","Please select a secret")
    else:
        secretValue = secretValueTextBox.get(1.0, "end-1c")
        MsgBox = messagebox.askquestion ('Saving',f"Are you sure you want to update the {selected_secret_name}",icon = 'warning')
        if MsgBox == 'yes':
            client.set_secret(selected_secret_name, secretValue)
            messagebox.showinfo("Information","Secret has been updated")
        else:
            messagebox.showinfo("Information","Better to be safe then sorry")

def getLocalEvnFile():
    global df

    import_file_path = filedialog.askopenfilename()
    if import_file_path:
        localSecretValueTextBox.delete('1.0', tk.END)
        f = open(import_file_path, "r")
        data = f.read()
        localSecretValueTextBox.insert(tk.END, data)

def OptionMenu_SelectionEvent(event): # I'm not sure on the arguments here, it works though
    ## do something
    selectedSecret.set(event)
    if event != "Please select a secret name":
        getSecretCallBack()
    else:
        secretValueTextBox.delete('1.0', tk.END)
    pass

root = tk.Tk()
root.title('Compare and update secrets in AZURE')
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

w = tk.OptionMenu(leftframe, selectedSecret, *OPTIONS, command = OptionMenu_SelectionEvent)
w.event_add
w.config(width=40)
w.pack(side=tk.TOP)

secretValueTextBox = tk.Text(leftframe, height=70, width=90, background="white",insertbackground="black",  foreground="black")
secretValueTextBox.pack(side=tk.LEFT)

saveSecretValueButton = tk.Button(leftframe, text = "Save Value",command=saveSecretCallBack)
saveSecretValueButton.pack(side=tk.TOP)

# Create an Exit button.
exitButton = tk.Button(leftframe, text = "Exit", command = root.destroy)
exitButton.pack(side=tk.TOP)


labelRight = tk.Label(rightframe, text = "Local env file")
labelRight.config(font =("Courier", 14))
labelRight.pack(side=tk.TOP)

browseButton_Files = tk.Button(rightframe, text='Import .env File', command=getLocalEvnFile, bg='black', fg='black',
                               font=('helvetica', 12, 'bold'))
  
browseButton_Files.pack(side=tk.TOP)

localSecretValueTextBox = tk.Text(rightframe, height=70, width=90, background="white",insertbackground="black", foreground="black")
localSecretValueTextBox.pack(side=tk.LEFT)
  
tk.mainloop()