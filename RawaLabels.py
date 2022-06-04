from os import path, stat, getcwd
from tkinter import *
from tkinter.filedialog import askdirectory
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import gmtime, strftime

# Global vars
last_scan = ""
auto_search = False  # Flag
valid_link = False  # Flag
valid_path = False  # Flag
first = str("")
second = str("")
third = str("")
followers = 0
viewers = 0

def scanning():
    global auto_search
    global valid_link
    global valid_path
    if auto_search:
        extract_info()

    root.after(10000, scanning)


def save_path_file(location):
    global labels_path
    labels_path = location
    with open("savePath.txt", 'w', encoding="utf-8") as Path_file:
        Path_file.write(location)
        Path_file.close()
    return True


def channel_link_file(link="https://rawa.tv/"):
    global channel_link
    channel_link = link
    with open("Link.txt", 'w', encoding="utf-8") as Link_file:
        Link_file.write(link)
        Link_file.close()
    return True

def Driver():
    args = ["hide_console", ]
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/85.0.4183.83 Safari/537.36 "
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('headless')
    driver = webdriver.Chrome("chromedriver.exe", options=options, service_args=args)
    return driver

def channel_exists():
    driver = Driver()
    driver.get(channel_link)
    try:
        WebDriverWait(driver, 1).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'bg-im-err')))
        driver.quit()
        return False
    except TimeoutException:
        driver.quit()
        return True


def check():
    # global values reset to False!
    global valid_link
    global valid_path
    valid_link = False
    valid_path = False

    # channel link check..
    if channel_link_entry.get() == "https://rawa.tv/" or "https://rawa.tv/" != channel_link_entry.get()[0:16] \
            or len(channel_link_entry.get()) == 0:
        msg.set("Invalid link!")
        return False
    if not channel_exists():
        msg.set("Channel dose not exist!")
        return False
    else:
        valid_link = True
    if not valid_link:
        channel_link_entry.delete(0, END)
        tmp = open("Link.txt", 'r', encoding='utf-8')
        channel_link_entry.insert(0, tmp.read())
        tmp.close()
        return False
    channel_link_file(channel_link_entry.get())

    # save path check..
    if not path.exists(save_path_entry.get()) or len(save_path_entry.get()) == 0:
        msg.set("Invalid save path, save path reset!!!")
        save_path_entry.delete(0, END)
        tmp = open("savePath.txt", 'r', encoding='utf-8')
        save_path_entry.insert(0, tmp.read())
        tmp.close()
        return False
    else:
        valid_path = True
        save_path_file(save_path_entry.get())
    return True


def browse():
    global auto_search
    if auto_search:
        stop()
    direc = askdirectory(parent=root, title='Choose a save folder')
    if direc:
        save_path_entry.delete(0, END)
        save_path_entry.insert(0, direc)
        save_path_file(direc)
        msg.set("Output Folder Saved Successfully..!")
        save_path_file(direc)
        current_path.set(labels_path)
    return True


def save():
    if not check():
        return False
    msg.set("Saved Successfully..!")
    current_path.set(labels_path)
    current_link.set(channel_link)
    return True


def start():
    global auto_search
    if not valid_link:
        msg.set("Invalid link!")
        return False
    else:
        auto_search = True
        channel_link_entry.config(state='disabled')
        save_path_entry.config(state='disabled')
        start_text.set("App is running..")
        msg.set("")
        return True


def stop(stop_msg=""):
    global auto_search
    if auto_search:
        auto_search = False
        start_text.set("Start Searching (AUTO)")
        msg.set(stop_msg + " App stopped..!, " + "Last scan: " + last_scan)
        channel_link_entry.config(state='normal')
        save_path_entry.config(state='normal')
    return True


def search():
    global auto_search
    if auto_search:
        return None
    if not valid_link:
        msg.set("Invalid link!")
        return None
    else:
        extract_info()


def fill_files():
    firstPath = path.join(labels_path, "First.txt")
    secondPath = path.join(labels_path, "Second.txt")
    thirdPath = path.join(labels_path, "Third.txt")
    followersPath = path.join(labels_path, "Followers.txt")
    viewsPath = path.join(labels_path, "Viewers.txt")
    first_file = open(firstPath, 'w', encoding='utf-8')
    first_file.write(first)
    first_file.close()
    second_file = open(secondPath, 'w', encoding='utf-8')
    second_file.write(second)
    second_file.close()
    third_file = open(thirdPath, 'w', encoding='utf-8')
    third_file.write(third)
    third_file.close()
    followers_file = open(followersPath, 'w', encoding='utf-8')
    followers_file.write(str(followers))
    followers_file.close()
    viewers_file = open(viewsPath, 'w', encoding='utf-8')
    viewers_file.write(str(viewers))
    viewers_file.close()


def fill_labels():
    first_var.set("First: " + first)
    second_var.set("Second: " + second)
    third_var.set("Third: " + third)
    followers_var.set("Followers: " + str(followers))


def extract_info():
    global followers
    global first
    global second
    global third
    global last_scan
    global viewers
    driver = Driver()
    driver.get(channel_link)
    # locating top 3 weekly leaderboard
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'chatHeaderLeaderboardName')))
        result = driver.find_elements_by_class_name('chatHeaderLeaderboardName')
        last_scan = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        msg.set("Last successful scan: " + last_scan)
        counter = len(result)
        first = result[0].text
        if counter >= 2:
            second = result[1].text
            if counter == 3:
                third = result[2].text
    except TimeoutException:
        last_scan = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        msg.set("None found, last scan: " + last_scan)
    # followers locating
    followers_xpath = '//*[@id="main"]/div[1]/div[2]/div[1]/table/tbody/tr/td[2]/a/p[1]'
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, followers_xpath)))
        followers = driver.find_element_by_xpath(followers_xpath).text
    except TimeoutException:
        followers = followers
    # viewers locating
    viewers_xpath = '/html/body/div/div/div[2]/div[3]/div[1]/section/div[2]/p[2]/span'
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, viewers_xpath)))
        viewers = driver.find_element_by_xpath(viewers_xpath).text
    except TimeoutException:
        viewers = viewers
    fill_files()
    fill_labels()
    driver.quit()


def init_labels():
    global first
    global second
    global third
    global followers
    with open(path.join(labels_path, "First.txt"), 'r', encoding='utf-8') as f:
        first = f.read()
        first_var.set("First: " + first)
    with open(path.join(labels_path, "Second.txt"), 'r', encoding='utf-8') as s:
        second = s.read()
        second_var.set("Second: " + second)
    with open(path.join(labels_path, "Third.txt"), 'r', encoding='utf-8') as t:
        third = t.read()
        third_var.set("Third: " + third)
    with open(path.join(labels_path, "Followers.txt"), 'r', encoding='utf-8') as fo:
        followers = fo.read()
        followers_var.set("Followers: " + followers)


root = Tk()

root.geometry('500x400+150+150')
root.title('Rawa Labels By Err0R')
root.resizable(width=FALSE, height=FALSE)
root.iconbitmap('rawa-default.ico')
root.configure(bg='#161616')

# channel link label and entry
channel_link_label = Label(fg='#ff7500', bg='#161616', text="Channel Link")
channel_link_label.place(x=10, y=10)
channel_link_entry = Entry(root, width='50')

# if file not created yet or empty, create and/or fill with default..!
if not (path.exists("Link.txt")) or stat("Link.txt").st_size == 0:
    channel_link_file()

link_file = open("Link.txt", 'r', encoding='utf-8')
channel_link = link_file.read()
link_file.close()

if channel_link != "https://rawa.tv/":
    valid_link = True

channel_link_entry.insert(0, channel_link)
channel_link_entry.place(x=100, y=10, height=25)

# save path label and entry
save_path_label = Label(fg='#ff7500', bg='#161616', text="Save Path")
save_path_label.place(x=10, y=65)
save_path_entry = Entry(root, width="50")

# if file not created yet or empty, create and/or fill with default..!
if not (path.exists("savePath.txt")) or stat("savePath.txt").st_size == 0:
    save_path_file(path.abspath(getcwd()))

savePath_file = open("savePath.txt", 'r', encoding='utf-8')
labels_path = savePath_file.read()
savePath_file.close()

if not path.exists(labels_path):
    save_path_file(path.abspath(getcwd()))

valid_path = True

save_path_entry.insert(0, labels_path)
save_path_entry.place(x=100, y=65, height=25)

# current data labels..
current_link = StringVar()
current_link.set(channel_link)
current_link_label = Label(fg='#ff7500', bg='#161616', textvariable=current_link).place(x=100, y=40)

current_path = StringVar()
current_path.set(labels_path)
current_path_label = Label(fg='#ff7500', bg='#161616', textvariable=current_path).place(x=100, y=95)

# buttons..
start_text = StringVar()
start_text.set("Start Searching (AUTO)")

save_button = Button(text="Save", fg='#161616', bg='#ff7500', width='12', command=save).place(x=100, y=120)

auto_search_button = Button(textvariable=start_text, fg='#161616', bg='#ff7500', width='20', command=start).place(x=200,
                                                                                                                  y=120)

stop_button = Button(text="Stop", fg='#161616', bg='#ff7500', width='12', command=stop).place(x=355, y=120)

search_button = Button(text="Search", fg='#161616', bg='#ff7500', width='7', command=search).place(x=25, y=120)

browse_button = Button(text="Browse", fg='#161616', bg='#ff7500', command=browse).place(x=410, y=65)

# message to user..
msg = StringVar()
msg_label = Label(fg='#ff7500', bg='#161616', textvariable=msg).place(x=190, y=150)

# CR MARK
follow_label = Label(fg='#ff7500', bg='#161616', text="FOLLOW ME https://rawa.tv/Err0R").place(y=380)

# Current leaderboard..
first_var = StringVar()
second_var = StringVar()
third_var = StringVar()
followers_var = StringVar()

followers_label = Label(fg='#ff7500', bg='#161616', textvariable=followers_var).place(x=80, y=175)
first_label = Label(fg='#ff7500', bg='#161616', textvariable=first_var).place(x=100, y=200)
second_label = Label(fg='#ff7500', bg='#161616', textvariable=second_var).place(x=100, y=225)
third_label = Label(fg='#ff7500', bg='#161616', textvariable=third_var).place(x=100, y=250)
if not path.exists(path.join(labels_path, "First.txt")):
    fill_files()
init_labels()

root.after(1000, scanning)
root.mainloop()
