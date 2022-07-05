from TiktokBot import TiktokBot
import glob
import os
import time
a = glob.glob('C:/Users/Erin Tomorri/Desktop/tiktok/tiktok-askreddit-main123 - Copy/render/*.mp4')
num = 0
def repeat(num):
    if __name__ == "__main__":
        # Example Usage
        # pip install git+https://github.com/pytube/pytube
        
        tiktok_bot = TiktokBot()  # "VideosDirPath", is the default directory where images edited will be saved.
            
        # Use a video from your directory.
        # tiktok_bot.upload.uploadVideo("test1.mp4", "This is test", 1, 2, private=True)

        # Or use youtube url as video source. [Simpsons Meme 1:16 - 1:32 Example]

        # tiktok_bot.upload.uploadVideo("https://www.youtube.com/watch?v=4eegr0W_C5c", "", private=True, test=False)
        # tiktok_bot.upload.uploadVideo("test.mp4", "Hi", private=False, test=False)


        # You can also choose to upload a file directly with no editing or cropping of the video.

        tiktok_bot.upload.directUpload(a[num], private=False, test=False)

        ####################################################################################################################
        # Scheduling does not work currently.

        # tiktok_bot.schedule.printSchedule()
        # playlist = https://www.youtube.com/playlist?list=PLiMQfyKvRdimHicuw1cAmwS7d_UiANXcj
        '''
            while True:
                url = input("Enter a url for uploading:: ")
                caption = input("Enter a caption for the video:: ")
                timeStart = input("Enter Start Time:: ")
                timeEnd = input("Enter End Time:: ")
                # Add this video into the csv so that you can upload yourself, by putting test parameter on and just showing you.
                tiktok_bot.schedule.scheduleVideo(url, caption, timeStart, timeEnd)
        '''
        # We can add task schedule from read from a csv: url, caption, startTime, endTime, time_to_release.
        # tiktok_bot.schedule.submit_all_schedule()
        # tiktok_bot.schedule.scheduleVideo("https://www.youtube.com/watch?v=yxErIigWRv4", "why do these never have my name!!", 115, 125)
        # Default params: Videos are separated by a day each "", time is constant: "20:10" ;
        os.remove(a[num])
        time.sleep(180)
while num != len(a):#stopped after 13
    repeat(num)
    num+=1
