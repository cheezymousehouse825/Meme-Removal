# Meme-Removal
> This removes memes from your subreddit and sends them to your spam section automatically.

I made this because a lot of people are having issues with memes being spammed in subreddits. I have nothing against memes, in fact I really love them. Somtimes, it's too much though. With the press of a button, this simple bot will make your subreddit meme free!

![](header.png)

## Installation

### Windows

For this, all you need to do is go to the [releases](https://github.com/ohgodmanyo/Meme-Removal/releases/latest/) section of this project, and download the latest release.

Now that you are done, we can get to setting up the file for use. First we are going to need to install [tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Once you have installed that, you will need to create a reddit account. Once that is finished, go to [apps](https://www.reddit.com/prefs/apps/) and hit create a new app. Call it whatever you want, select the script button (it is default to web app) and add descriptions and urls. After this, you run the settings file you downloaded from me and put in the location of the tesseract.exe file, the client id, client secret, reddit username, reddit passowrd, user agent, and subreddit you would like to moderate (don't forget to set your bot as administrator for this!)

## Usage example

Finally, you are done the installation process. Now all you have to do is run the main file, and you should be good to go! I am not responsible for anything that happens to your subreddit with this bot.

## Development setup

For this way, you will need python installed. Run the following lines of code in your command prompt to get all the libraries used in this program.

```pip install pytesseract```

```pip install pillow```

```pip install praw```

```pip install requests```

```git clone https://github.com/ohgodmanyo/Meme-Removal/```

Now, the repository and the modules have been installed.

After this, you can just follow the other steps as shown in the Installation section

## Release History

* 0.0.1
    * Work in progress

## Meta

Ohgodmanyo – [@Ohgodmanyo](https://twitter.com/Ohgodmanyo) – Ohgodmanyo@protonmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/ohgodmanyo](https://github.com/ohgodmanyo/)
