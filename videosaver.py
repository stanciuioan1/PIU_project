import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
from datetime import datetime
import os

curr_subtitle = " "
def pipeline(frame):
    global curr_subtitle
    try:
        cv2.putText(frame, curr_subtitle, (600, 1000), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 0, cv2.LINE_AA)
    except StopIteration:
        pass
    return frame

def to_ascii(text):
    ascii_values = [ord(character) for character in text]
    return ascii_values

def parse_video(link_to_vid):
    global curr_subtitle
    ixi = 0
    video = VideoFileClip(link_to_vid)
    video_out = video.subclip(0,0)
    f2 = open("out.srt", "r")
    content = f2.readlines()
    for i in content:
        parts = i.split("|")
        time = parts[0]
        text = parts[1]
        split_sec = time.split(":")
        beg = int(split_sec[0])
        end = int(split_sec[1])
        vid = video.subclip(beg/1000, end/1000)
        text = text[0:-1]
        curr_subtitle = str(text)
        
        print(curr_subtitle)
        out_video = vid.fl_image(pipeline)
        file_name = "vidout"+str(ixi)+".mp4"
        print(file_name)
        out_video.write_videofile(file_name, audio=True)
        ixi = ixi+1

    print("Valoarea lui ixi este: "+str(ixi))
    for i in range(0, ixi):
        file_name = "vidout"+str(i)+".mp4"
        print("Incercam sa deschidem "+file_name)
        video = VideoFileClip(file_name)   
        video_out = concatenate_videoclips([video_out,video]) 
        os.remove(file_name)
    
    video_out.write_videofile("vidout.mp4", audio=True)

