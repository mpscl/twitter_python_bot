# bots.py

import random
from io import BytesIO

import requests
import logging
import warnings
import tweepy
from PIL import Image
from PIL import ImageFile
from tweepy.auth import OAuthHandler

from secrets import *

logging.getLogger("main").setLevel(logging.INFO)
ImageFile.LOAD_TRUNCATED_IMAGES = True

auth = OAuthHandler(consumer_key, consumer_secret) # Twitter requires all requests to use OAuth for authentication
auth.set_access_token(access_token, access_secret) 
api = tweepy.API(auth)

def tweet_image(url, username, status_id):
    filename = 'temp.png'
    # send a get request
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        # read data from downloaded bytes and returns a PIL.Image.Image object
        i = Image.open(BytesIO(request.content))
        # Saves the image under the given filename
        i.save(filename)
        scramble(filename)
        # Update the authenticated user’s status
        api.update_with_media('scramble.png', status='@{0}'.format(username), in_reply_to_status_id=status_id)
    else:
        print("unable to download image")

def scramble(filename):
    BLOCKLEN = 64  # Adjust and be careful here.

    img = Image.open(filename)
    width, height = img.size

    xblock = width // BLOCKLEN
    yblock = height // BLOCKLEN
    # creates sequence of 4-tuples (box) defining the left, upper, right, and lower pixel coordinate
    blockmap = [(xb * BLOCKLEN, yb * BLOCKLEN, (xb + 1) * BLOCKLEN, (yb + 1) * BLOCKLEN)
                for xb in range(xblock) for yb in range(yblock)]

    shuffle = list(blockmap)

    # shuffle the sequence
    random.shuffle(shuffle)

    # Creates a new image with the given mode and size.
    result = Image.new(img.mode, (width, height))
    for box, sbox in zip(blockmap, shuffle):
        # Returns a rectangular region from this original image.
        crop = img.crop(sbox)
        # Pastes the cropped pixel into the new image Object
        result.paste(crop, box)
    result.save('scramble.png')

# create a class inheriting from the tweepy  StreamListener
class BotStreamer(tweepy.StreamListener):
    # Called when a new status arrives which is passed down from the on_data method of the StreamListener
    def on_status(self, status):
        username = status.user.screen_name
        status_id = status.id
        # print(status.id_str).encode('utf8')
        
        try:
            api.create_friendship(status.user.id)
            # print(status.user.id).encode('utf8')
            api.retweet(status.id)
            api.create_favorite(status.id)
        except Exception as ex:
            logging.error(ex)
        # # entities provide structured data from Tweets including resolved URLs, media, hashtags and mentions without having to parse the text to extract that information
        # if 'media' in status.entities:
        #     for image in status.entities['media']:
                # tweet_image(image['media_url'], username, status_id)

myStreamListener = BotStreamer()
# Construct the Stream instance
# api.update_status('Hello i am a twitter bot!')
stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['#trululu'])