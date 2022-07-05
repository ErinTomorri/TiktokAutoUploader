# This class will be in charge of uploading videos onto tiktok.
from ast import Break
import os, time
from unicodedata import name

import py
from Bot import Bot
import utils
from Browser import Browser
from Cookies import Cookies
from IO import IO
from Video import Video
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common
import pyautogui
list = []
PROTECTED_FILES = ["processed.mp4", "VideosSaveHere.txt"]

class Upload:
    def __init__(self, user):
        self.bot = None
        self.lang = "en"
        self.url = f"https://www.tiktok.com/upload?lang={self.lang}"
        self.cookies = None
        self.userRequest = {"dir": "", "cap": "", "vidTxt": ""}
        self.video = None
        self.IO = IO("hashtags.txt", "schedule.csv")
        self.videoFormats = ["mov", "flv", "avi"]
        self.userPreference = user


    # Class used to upload video.
    def uploadVideo(self, video_dir, videoText, startTime=0, endTime=0, private=True, test=False, scheduled=False, schdate="", schtime=""):

        video_dir = self.downloadIfYoutubeURL(video_dir)
        if not video_dir:
            return

        if self.bot is None:
            self.bot = Browser().getBot()
            self.webbot = Bot(self.bot)

        self.userRequest["dir"] = video_dir
        self.checkFileExtensionValid()
        self.userRequest["cap"] = self.IO.getHashTagsFromFile()
        # Initiate bot if isn't already.
        self.bot.get(self.url)
        self.userRequest["vidTxt"] = videoText

        # Cookies loaded here.
        self.cookies = Cookies(self.bot)
        self.bot.refresh()

        # User now has logged on and can upload videos
        time.sleep(3)
        self.inputVideo(startTime, endTime)
        self.addCaptions()
        utils.randomTimeQuery()
        if private:
            self.webbot.selectPrivateRadio()  # private video selection
        else:
            self.webbot.selectPublicRadio()  # public video selection
        utils.randomTimeQuery()
        if not test:
            self.webbot.uploadButtonClick()  # upload button
        input("Press any button to exit")


    def createVideo(self, video_dir, videoText, startTime=0, endTime=0):
        video_dir = self.downloadIfYoutubeURL(video_dir)
        if not video_dir:
            return
        self.inputVideo(startTime, endTime)
        self.addCaptions()
        print(f"Video has been created: {self.dir}")


    # Method to check file is valid.
    def checkFileExtensionValid(self):
        if self.userRequest["dir"].endswith('.mp4'):
            pass
        else:
            self.bot.close()
            exit(f"File: {self.userRequest['dir']} has wrong file extension.")


    # This gets the hashtags from file and adds them to the website input
    def addCaptions(self, hashtag_file=None):
        if not hashtag_file:
            caption_elem = self.webbot.getCaptionElem()
            for hashtag in self.IO.getHashTagsFromFile():
                caption_elem.send_keys(hashtag)

    def clearCaptions(self):
        caption_elem = self.webbot.getCaptionElem()
        caption_elem.send_keys("")

    def inputScheduler(self, schdate, schtime):
        # In charge of selecting scheduler in the input.
        utils.randomTimeQuery()
        self.webbot.selectScheduleToggle()


    # This is in charge of adding the video into tiktok input element.
    def inputVideo(self, startTime=0, endTime=0):
        try:
            file_input_element = self.webbot.getVideoUploadInput()
        except Exception as e:
            print("Major error, cannot find the upload button, please update getVideoUploadInput() in Bot.py")
            print(f"Actual Error: {e}")
            file_input_element = ""
            exit()
        # Check if file has correct .mp4 extension, else throw error.
        self.video = Video(self.userRequest["dir"], self.userRequest["vidTxt"], self.userPreference)
        print(f"startTime: {startTime}, endTime: {endTime}")
        if startTime != 0 and endTime != 0 or endTime != 0:
            print(f"Cropping Video timestamps: {startTime}, {endTime}")
            self.video.customCrop(startTime, endTime)
        # Crop first and then make video.

        self.video.createVideo()  # Link to video class method
        while not os.path.exists(self.video.dir):  # Wait for path to exist
            time.sleep(1)
        abs_path = os.path.join(os.getcwd(), self.video.dir)
        file_input_element.send_keys(abs_path)


    def downloadIfYoutubeURL(self, video_dir) -> str:
        """
        Function will determine whether given video directory is a youtube link, returning the downloaded video path
        Else it will just return current path.
        """

        url_variants = ["http://youtu.be/", "https://youtu.be/", "http://youtube.com/", "https://youtube.com/",
                        "https://m.youtube.com/", "http://www.youtube.com/", "https://www.youtube.com/"]
        if any(ext in video_dir for ext in url_variants):
            print("Detected Youtube Video...")
            video_dir = Video.get_youtube_video(self.userPreference, video_dir)
        return video_dir


    def directUpload(self, filename, private=False, test=False):
        if self.bot is None:
            self.bot = Browser().getBot()
            self.webbot = Bot(self.bot)
            pass
        self.bot.get(self.url)
        utils.randomTimeQuery()
        self.cookies = Cookies(self.bot)
        self.bot.refresh()
        time.sleep(10)
        WebDriverWait(self.bot, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        self.bot.switch_to.frame(0)
        self.bot.implicitly_wait(1)
        file_uploader = self.bot.find_elements(By.CLASS_NAME, "css-14w2a8u")[0].click()

        time.sleep(4)
        word = ""
        word1 = ""
        for num in range(len(filename)):
            if filename[num] == "\\":
                list.append(num)
        num = 0
        while num!= list[-1]+1:
            word = word + filename[num]
            num+=1
        print (word)
        num = list[-1]+1
        while num != len(filename):
            word1 = word1 + filename[num]
            num+=1
        print (word1)
        pyautogui.click(239, 61)
        time.sleep(2)
        pyautogui.write(word)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.click(891, 1020)
        time.sleep(2)
        #pyautogui.click(891, 1020)
        pyautogui.write(word1)
        pyautogui.press('enter')
        time.sleep(10)
        
        self.addCaptions()
        utils.randomTimeQuery()
        if private == True:
            self.webbot.selectPrivateRadio()  # private video selection
            utils.randomTimeQuery()
        else:
            """
            self.webbot.selectPublicRadio()  # public video selection
            utils.randomTimeQuery()
            """
            pass
        if test == False:
            self.webbot.uploadButtonClick()  # upload button
        file_uploader = self.bot.find_elements(By.CLASS_NAME, "css-n99h88")[0].click()
        time.sleep(15)
        
        # We need to wait until it is uploaded and then clear input.
        self.bot.close()