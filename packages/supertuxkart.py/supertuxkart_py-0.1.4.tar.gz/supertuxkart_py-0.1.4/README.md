# SuperTuxKart API Wrapper for Python
A library that allows for interacting with teh SuperTuxKart API.

# Example:
```py
>>> import supertuxkart
>>> client = supertuxkart.SuperTuxKartClient(userid=513714, token="<token here>")
>>> # You can also use username/password auth, though
>>> # userid/token is prioritized if both specified
>>> client = supertuxkart.SuperTuxKartClient(username="Sayori", password="password")
>>> session = client.account.saved_session()
>>> session.userid
513714
>>> session.username
'Sayori'
```

# License
This project is licensed under the MIT license.
