## to install:

```
pip3 install -r requirements.txt
```

## to run:

You have to login to `az` in your terminal.
```
az login
```

after that:"

```
KEY_VAULT_NAME=name-of-your-keyvault python3 kv_secrets.py
```

### FQA

if you are getting error about `No module named _tkinter` you may need to install:

```
brew install python-tk
```
