import webbrowser

# Client Credentials
response_type = '{code or token}'
scope = '{required signature, space separated}' # signature organization_read user_read user_write
client_id = '{Integration Key}'
state = '{Custome Value}'
redirect_uri = '{REDIRECT URI}' # http://localhost:8000/callback/

# Contruct the URL for Implicit Grant Flow - Response contains access token
implicitGrantUrl = "https://account-d.docusign.com/oauth/auth?response_type={}&scope={}&client_id={}&state={}&redirect_uri={}".format(
    response_type, # token
    scope,
    client_id,
    state,
    redirect_uri
)

# Construct the URL for Auth Code Grant Flow - Response contains Code, which is exchanged for access token and refresh token.
authUrl = 'https://account-d.docusign.com/oauth/auth?response_type={}&scope={}&client_id={}&state={}&redirect_uri={}'.format(
    response_type, # code
    scope,
    client_id,
    state,
    redirect_uri
)

# Open the URL in default browser for token/code
webbrowser.open({'implicitGrantUrl or authUrl'})