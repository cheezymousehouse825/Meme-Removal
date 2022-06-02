import pytesseract as tess
from PIL import Image
import praw
import json
import requests
import time


def scan_headings(image):
    im = Image.open(image)
    px = im.load()
    width, height = im.size
    pixels = []
    sums = []

    # gets the first few pixel values
    for i in range(5):
        for j in range(width):
            pixels.append(px[j, i])

    for i in pixels:
        sums.append(sum(i))

    lowestValue = min(sums)
    highestValue = max(sums)
    skew = highestValue - lowestValue
    return skew


def scan_text(image):
    tess.pytesseract.tesseract_cmd = dictionary['location']
    im = Image.open(image)
    text = tess.image_to_string(im, lang='eng')
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
        time.sleep(10)
        continue
    # Gets the link to the image
    postLink = r.json()[0]['data']['children'][0]['data']['url']
    # Checking if it is a link to another post
    while '.jpg' not in postLink and '.png' not in postLink and not isText:
        r = requests.get('{}.json'.format(postLink),
                         headers={'User-agent': dictionary['userAgent']})
        postLink = r.json()[0]['data']['children'][0]['data']['url']
        if previousPostLink == postLink and r.json()[0]['data']['children'][0]['data']['is_self']:
            isText = True
        previousPostLink = postLink
    # Checking if the post is text
    if isText:
        isText = False
        time.sleep(10)
        continue

    print(postLink)

    pic = requests.get(postLink)

    if '.png' in postLink:
        with open("image.png", "wb") as f:
            f.write(pic.content)
        impng = Image.open("image.png")
        rgb_impng = impng.convert("RGB")
        rgb_impng.save("image.jpg")

    else:
        with open("image.jpg", "wb") as f:
            f.write(pic.content)

    imageToScan = 'image.jpg'
    headingsValue = scan_headings(imageToScan)
    textValue = scan_text(imageToScan)
    print("Headings Value:", headingsValue)
    print("Text Value:", textValue)

    if headingsValue < 130 and textValue > 3:
        print('This post has been detected as a meme')
        submissionToDelete = reddit.submission(id=postId)
        submissionToDelete.mod.remove(spam=True)
        submissionToDelete.mod.send_removal_message('Sorry, but this post has been detected as '
                                                    'a meme. Please remove any borders or text you have added.'
                                                    ' If this is NOT a meme, please reply to this comment, and '
                                                    'do not delete the post.')
        time.sleep(10)
    else:
        print("This post is not a meme")
        postList.append(postId)
        time.sleep(10)
