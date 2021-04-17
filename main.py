import pytesseract as tess
from PIL import Image
from collections import Counter
import praw
import json
import requests
import time


def scan_headings(image):
    im = Image.open(image)
    px = im.load()
    width, height = im.size
    pixels = []

    # gets the first few pixel values
    for i in range(5):
        for j in range(width):
            pixels.append(px[j, i])

    pixel_values = dict(Counter(pixels))
    total = sum(pixel_values.values())
    max_key = max(pixel_values, key=pixel_values.get)
    percentage = pixel_values[max_key] / total * 100
    return percentage


def scan_text(image):
    tess.pytesseract.tesseract_cmd = dictionary['location']
    im = Image.open(image)
    text = tess.image_to_string(im)
    word_count = 0

    # Loops through words
    with open('wordList.txt') as file:
        # Turns all the words into a list
        line_list = []
        for k in file:
            line_list.append(k.strip())

        for m in text.split():
            # Finds if the text is a word
            if ''.join(e for e in m.lower() if e.isalnum()) in line_list:
                word_count += 1
    return word_count


# Loads settings
with open('settings.json') as f:
    dictionary = json.load(f)

# Signs into reddit
reddit = praw.Reddit(client_id=dictionary['clientId'],
                     client_secret=dictionary['clientSecret'],
                     username=dictionary['username'],
                     password=dictionary['password'],
                     user_agent=dictionary['userAgent'])

isText = False
previousPostLink = None
postId = None
postList = []
subreddit = reddit.subreddit(dictionary['subreddit'])
while True:
    # Gets newest submission
    for submission in subreddit.new(limit=1):
        postId = submission.id

    r = requests.get('https://www.reddit.com/{}.json'.format(postId),
                     headers={'User-agent': dictionary['userAgent']})

    # Checking if subreddit is empty
    if postId is None or postId in postList:
        print('There is nothing new in this subreddit, waiting for new posts')
        time.sleep(10)
        continue
    # Gets the link to the image
    postLink = r.json()[0]['data']['children'][0]['data']['url']
    # Checking if it is a link to another post
    while '.jpg' not in postLink and not isText:
        r = requests.get('{}.json'.format(postLink),
                         headers={'User-agent': dictionary['userAgent']})
        postLink = r.json()[0]['data']['children'][0]['data']['url']
        if previousPostLink == postLink and r.json()[0]['data']['children'][0]['data']['is_self']:
            isText = True
        previousPostLink = postLink
    # Checking if the post is text
    if isText:
        isText = False
        print('This is a text post, waiting for image')
        time.sleep(10)
        continue

    print(postLink)

    pic = requests.get(postLink)
    with open("image.jpg", "wb") as f:
        f.write(pic.content)

    imageToScan = 'image.jpg'
    if scan_headings(imageToScan) >= 50 and scan_text(imageToScan) > 3:
        submissionToDelete = reddit.submission(id=postId)
        submissionToDelete.mod.remove(spam=True)
        submissionToDelete.mod.send_removal_message('Sorry, but this post has been detected as '
                                                    'a meme. Please remove any borders or text you have added.')
        time.sleep(10)
    else:
        postList.append(postId)
        time.sleep(10)
