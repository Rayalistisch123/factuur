from google_auth_oauthlib.flow import InstalledAppFlow

# Maak de OAuth-flow aan met de juiste scope
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/drive.file']
)

# Luister op poort 8080 zodat de redirect URI "http://localhost:8080/" wordt gebruikt
creds = flow.run_local_server(port=8080)

# Sla de verkregen credentials op in token.json
with open("token.json", "w") as token_file:
    token_file.write(creds.to_json())

print("Token opgeslagen in token.json")
