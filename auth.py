

# JWT (JSON Web Token) is a compact, secure way to pass identity data (like a user's email) between the client and server.
# It's used in stateless authentication — no sessions stored on the server.
# Once the user logs in, they receive a token.
# That token is sent with each request to protected endpoints (like /wallet/send or /balance).



#jwt-Json web token: 
#session token: are encripted string that are used to Identfy a setion between 2 parties
#if you were on call with a CSR after the convo they fgive you a caseNumber, thei case number would be equal to a session token, next time you can look up the case number to get case history

# Sessiontokebns can only be used on a servewer that issued them (imagine a bank issuing a token while using the webservice, now you can not get the same token for mobile app as it might be issued by adiffent server)

# JWT can be used on mutile servers
# So we are using JWT to authenicate the user befor they can access API or DB protecting application from unauthorized payments


# server will issue the user a jwt that conatins role username and password and arandom token 
# user will store toekn in local storage
# when the user makes a requiest to theh api it will sent the token api will verify the token and check the user's role. if verified the data can be sent back

#  -->



from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
from pathlib import Path
import os

# Add this to explicitly load your .env file from the right place
env_path = Path("C:/Users/areab/Desktop/Projects/python/wallet/.env")
load_dotenv(dotenv_path=env_path)

# SECRET_KEY is used to sign the token. Keep this private!
# <!-- The secret key is a long random string that your app uses to sign JWT tokens — it's like your app's private stamp.

# It ensures that only your server can create or verify tokens.

# If someone tries to forge a token, it won't match your secret key — and the server will reject it.

# You should never share it or commit it to GitHub. 
# python -c "import secrets; print(secrets.token_hex(32))"
# -->


#load_dotenv()  # Load variables from .env file
SECRET_KEY = os.getenv("SECRET_KEY")
print(f"SECRET_KEY loaded: {SECRET_KEY}") 


ALGORITHM = "HS256"  # Standard JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token will expire after 30 minutes

#data: This is info about the user. Usually just their email.
# expires_delta: How long the token should last.
# to_encode: The user info + expiration time.
# jwt.encode(...): This turns that info into a secure token you can give to the user.
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# jwt.decode(...) tries to decode and check the token using the same secret key.
# If it’s valid, it gives back the user info (like their email).
# If it’s invalid or expired, it returns None.
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # 'sub' means subject (the user)
    except JWTError:
        return None
