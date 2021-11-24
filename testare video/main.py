import cv2
from moviepy.editor import VideoFileClip
from datetime import datetime

def pipeline(frame):
    # Window name in which image is displayed
    #window_name = 'Image'

    # font
    #font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    #org = (50, 50)

    # fontScale
    #fontScale = 1

    # Blue color in BGR
    #color = (255, 0, 0)

    # Line thickness of 2 px
    #thickness = 2
    #cv2.putText(image, 'OpenCV', org, font, fontScale, color, thickness, cv2.LINE_AA)
    try:
        cv2.putText(frame, str("Testing"), (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 0, cv2.LINE_AA)

    except StopIteration:
        pass
    # additional frame manipulation
    return frame
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("incep baietii sa incarce la: ", current_time)
video = VideoFileClip("D:\\facultate\\anul 4\\sem1\piu\\vid.mp4")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("s-a incarcat la la: ", current_time)
out_video = video.fl_image(pipeline)
out_video.write_videofile("vidout.mp4", audio=True)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("am scris: ", current_time)