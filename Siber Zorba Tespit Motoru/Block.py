import tkinter as tk
from tkinter import *
from Test import user
import tweepy
import time

consumer_key = ""
consumer_key_secret = ""
access_key = ""
access_key_secret = ""

# Yukarıdaki kısımlara sizin api keyleriniz gelmelidir

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_key, access_key_secret)
api = tweepy.API(auth)
user2 = api.get_user("")

window = tk.Tk(className="Minus 100 Data Science")
logo = tk.PhotoImage(file="trdogaldilisleme.png")
headline = tk.Label(image=logo)
window.geometry("1600x900")
window.configure(bg="#2d7dbf")
headline.pack()
window.update()


def main():

    while TRUE:
        following = []
        friend = user2.friends()
        for fr in friend:
            following.append(fr.screen_name)
        mentions = api.mentions_timeline(count=5)
        for ment in mentions:
            prediction = user(ment.text)
            if prediction == "Negatif":
                api.create_block(screen_name=ment.user.screen_name)
                message = ("TWEET:" + ment.text + " " + "KULLANICI: " + str(
                    ment.user.screen_name) + " " + "DURUM: ENGELLENDİ")
                neg = tk.Label(text=message, font=('Verdana', 15), borderwidth=2, relief="solid")
                neg.pack()
                window.update()
            else:
                print(ment.text)
        window.update()
        time.sleep(5)


main()
