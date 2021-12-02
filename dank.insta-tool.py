# Note: dank.insta-tool.py is meant to be run as an .exe by default, if you would like to execute the script, make the below changes...
#       - uncomment the following line > filepath = os.path.dirname(__file__) # as .py
#       - comment the following line > filepath = os.path.dirname(sys.argv[0]) # as .exe

import os
import sys
import time
import random
import instaloader
from instabot import Bot
import concurrent.futures
from colorama import init, Fore, Style
from alive_progress import alive_bar

os.system("title dank.insta-tool")

try:
    filepath = os.path.dirname(__file__) # as .py
    #filepath = os.path.dirname(sys.argv[0]) # as .exe
    os.chdir(filepath)
except:
    pass

banner_ascii = '''

      _             _      _           _              _              _ 
   __| | __ _ _ __ | | __ (_)_ __  ___| |_ __ _      | |_ ___   ___ | |
  / _` |/ _` | '_ \| |/ / | | '_ \/ __| __/ _` |_____| __/ _ \ / _ \| |
 | (_| | (_| | | | |   < _| | | | \__ \ || (_| |_____| || (_) | (_) | |
  \__,_|\__,_|_| |_|_|\_(_)_|_| |_|___/\__\__,_|      \__\___/ \___/|_|
                                                                       

'''

# colors

init(autoreset=True)
red = Fore.RED + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT
yellow = Fore.YELLOW + Style.BRIGHT
blue = Fore.BLUE + Style.BRIGHT
magenta = Fore.MAGENTA + Style.BRIGHT
cyan = Fore.CYAN + Style.BRIGHT
white = Fore.WHITE + Style.BRIGHT

# randomized banner color

bad_colors = ['BLACK', 'WHITE', 'LIGHTBLACK_EX', 'LIGHTWHITE_EX', 'RESET']
codes = vars(Fore)
colors = [codes[color] for color in codes if color not in bad_colors]
colored_chars = [random.choice(colors) + char for char in banner_ascii]
banner_colored = ''.join(colored_chars).splitlines()

# constants

def banner():

    width = os.get_terminal_size().columns
    banner_lines = banner_ascii.splitlines()
    for i in range(len(banner_lines)):
        banner_lines[i] = banner_lines[i].center(width).replace(banner_lines[i],banner_colored[i])
    banner_aligned = ''.join(banner_lines)
    return banner_aligned

def multithread(function, list):

    futures = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    for item in list:
        futures.append(executor.submit(function, item))
    with alive_bar(int(len(futures))) as bar:
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
                bar()
            except:
                bar()

while True:

    os.system('cls')
    print(banner())

    print(f"\n  {white}> {magenta}1. Get and save {white}ghosts {magenta}/ {white}non-ghosts")
    print(f"\n  {white}> {magenta}2. Remove {white}ghost {magenta}followers")
    print(f"\n  {white}> {magenta}3. Exit")
    choice = int(input(f"\n  {white}> {magenta}Enter Choice{white}: {magenta}"))

    def one():

        login_username = str(input(f"\n  {white}> {magenta}Enter your instagram username{white}: {magenta}")).lower()

        # instaloader login

        print("")
        os.system(f"instaloader --login={login_username}")
        L = instaloader.Instaloader()
        L.load_session_from_file(login_username)
        profile = instaloader.Profile.from_username(L.context, login_username)

        os.system('cls')
        print(banner())

        # get usernames of likers and commenters on all your posts

        print(f"\n  {white}> {magenta}Getting {white}likers {magenta}and {white}commenters [ {magenta}this might take a while {white}]\n")

        liked_users = []
        commented_users = []
        followers = []

        def get_users(post):

            post_likes = post.get_likes()
            post_comments = post.get_comments()
            for like in post_likes:
                liked_users.append(str(like.username))
            for comment in post_comments: 
                commented_users.append(str(comment.owner.username))

        multithread(get_users, profile.get_posts())

        # get usernames of your followers

        print(f"\n  {white}> {magenta}Getting {white}follower usernames...\n")

        def get_follower_usernames(follower):
            followers.append(str(follower.username))

        multithread(get_follower_usernames, profile.get_followers())

        # get ghosts and non ghosts

        print(f"\n  {white}> {magenta}Getting {white}ghosts {magenta}and {white}non_ghosts\n")

        def find_non_ghosts():
            non_ghosts = []
            for user in followers:
                if user in liked_users or user in commented_users:
                    non_ghosts.append(user)
            return list(set(non_ghosts))

        def find_ghosts():
            ghosts = []
            for user in followers:
                if user not in non_ghosts:
                    ghosts.append(user)
            return list(set(ghosts))

        liked_users = list(set(liked_users))
        commented_users = list(set(commented_users))
        non_ghosts = find_non_ghosts()
        ghosts = find_ghosts()

        os.system('cls')
        print(banner())

        # save txt files
        
        def create_txt(name):
            try:
                open(f"{name}.txt","x")
            except:
                pass
            
        txt_files = ['likers','commenters','non_ghosts','ghosts','followers','removed_ghosts','unremoved_ghosts']
        for name in txt_files:
            create_txt(name)

        print(f"\n  {white}> {magenta}Saving {white}likers.txt")
        open('likers.txt','w+').write('\n'.join(liked_users))

        print(f"\n  {white}> {magenta}Saving {white}commenters.txt")
        open('commenters.txt','w+').write('\n'.join(commented_users))

        print(f"\n  {white}> {magenta}Saving {white}non_ghosts.txt")
        open('non_ghosts.txt','w+').write('\n'.join(non_ghosts))

        print(f"\n  {white}> {magenta}Saving {white}ghosts.txt")
        open('ghosts.txt','w+').write('\n'.join(ghosts))

        print(f"\n  {white}> {magenta}Saving {white}followers.txt")
        open('followers.txt','w+').write('\n'.join(followers))
        
        print(f"\n  {white}> {magenta}Tasks Complete! Sleeping 5s...")
        time.sleep(5)
        
    def two():

        # check if ghosts.txt exists
        
        try:
            ghosts = list(set(open("ghosts.txt","r").read().splitlines()))
        except:
            print(f"  {white}> {red}The file {white}ghosts.txt {red}does not exist! Please use {white}option 1 {red}first before using {white}option 2{red}!")
            print(f"  {white}> {red}Going to menu in 5s...")
            time.sleep(5)
            return 

        bot = Bot()

        while True:
            try:
                bot.login()
                break
            except Exception as e:
                wait = input(f"\n  {white}> {red}Failed! Press {white}ENTER {red}to try again! | {str(e)}")

        removed_ghosts = []
        unremoved_ghosts = []
        
        # remove ghosts

        def remove_follower(user):

            errors = 0
            while True:
                try:
                    user_id = bot.get_user_id_from_username(user)
                    bot.api.remove_follower(user_id)
                    removed_ghosts.append(user)
                    print(f"\n  {white}> {green}Removed {white}{user}{green}!")
                    time.sleep(.3)
                    break
                except Exception as e:
                    errors += 1
                    if errors >= 4:
                        unremoved_ghosts.append(user)
                        print(f"\n  {white}> {red}Failed {white}{user} {red}| {str(e)}")
                        break
                    print(f"\n  {white}> {red}Retrying {white}{user}")
                    time.sleep(10)

        os.system('cls')
        print(banner())

        print(f"\n  {white}> {magenta}Removing {white}ghosts...\n")
        multithread(remove_follower, ghosts)
        
        # save txt files

        os.system('cls')
        print(banner())

        print(f"\n  {white}> {magenta}Removed {white}{len(removed_ghosts)} {magenta}ghosts!")
        print(f"\n  {white}> {red}Failed to remove {white}{len(unremoved_ghosts)} {red}ghosts!")

        print(f"\n  {white}> {magenta}Saving {white}removed_ghosts.txt")
        open('removed_ghosts.txt','w+').write('\n'.join(removed_ghosts))

        print(f"\n  {white}> {magenta}Saving {white}unremoved_ghosts.txt")
        open('unremoved_ghosts.txt','w+').write('\n'.join(unremoved_ghosts))
        
        print(f"\n  {white}> {magenta}Tasks Complete! Sleeping 5s...")
        time.sleep(5)
        
    # input
        
    os.system('cls')
    print(banner())

    if choice == 1:
        one()

    elif choice == 2:
        two()
        
    elif choice == 3:
        break