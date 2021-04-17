import json

dictionary = {
    'location': input('Where is your tesseract file located? '),
    'clientId': input('What is the client id of your reddit bot? '),
    'clientSecret': input('What is the client secret of your reddit bot? '),
    'username': input('What is the username of your reddit account? '),
    'password': input('What is the password of your reddit account? '),
    'userAgent': input('What is your user agent?\neg. <platform>:<app ID>:<version string> (by /u/<reddit username>) '),
    'subreddit': input('What is the subreddit you would like to moderate?\n(without the r/) ')
}

with open('settings.json', 'w') as f:
    f.write(json.dumps(dictionary, indent=4))
