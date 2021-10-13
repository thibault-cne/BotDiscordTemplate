"""
    Author : @Vladou
    Discord : Thibô#0001
"""

import requests
from bs4 import BeautifulSoup
from random import shuffle, choice
import asyncpraw
import os
from dotenv import load_dotenv, find_dotenv
import asyncio


dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

USER = os.getenv('REDDIT_USER')
SECRET = os.getenv('REDDIT_SECRET')
PASSWORD = os.getenv('REDDIT_PASSWORD')


def get_images(number, word):
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
    content = requests.get(url).content
    soup = BeautifulSoup(content, features="html.parser")
    images = shuffle([i.get('src') for i in soup.findAll('img')])
    shuffle(images)
    pointer = 0
    return_images = []

    while number>0:
        if images[pointer][:4] == 'http':
            number -= 1
            pointer += 1
            return_images.append(images[pointer])
        else:
            pointer += 1
    
    return return_images


async def get_meme(number):
    reddit = asyncpraw.Reddit(
        client_id=USER,
        client_secret=SECRET,
        username="Python_Praw_Vladou",
        password=PASSWORD,
        user_agent="pythonPraw"
    )
    all_subs = []
    
    subreddit = await reddit.subreddit("memes")
    async for submission in subreddit.hot(limit=25):
        all_subs.append(submission)
    
    await reddit.close()
    shuffle(all_subs)
    return [all_subs.pop() for i in range(number)]