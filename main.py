import cv2
from threading import Thread
import time
import os
from datetime import datetime
import shutil
import subprocess

class VideoRecorder:
    def __init__(self,stream_source_index):

        self.video=cv2.VideoCapture(stream_source_index)
        self.codec=cv2.VideoWriter_fourcc(*"X264")
        self.frame_rate=20
        self.frame_size=(int(self.video.get(3)),int(self.video.get(4)))

        self.motion_detection_status=False
        self.drive_recording_status=False

        self.start_time=0
        self.start_time_status=False

        if self.video.isOpened() == False:
            print("Errro accessing the camera")
            exit(0)
        
        ret,frame=self.video.read()

        if ret == False:
            print("no frames to read")
            exit(0)
    def command_executer(self,command):
        try:
            subprocess.run(command,shell=True)
            print("upload complete..")
        except subprocess.CalledProcessError as e:
            print(e)

    def drive_uploader(self):
     
        while True:
            if self.motion_detection_status == True and self.start_time_status == False:
                self.start_time=time.time()
                self.start_time_status=True
            
            current_time=time.time()

            elapsed_time=current_time-self.start_time

            if self.start_time_status == True:
                if elapsed_time > 30:
                    self.drive_recording_status=False
    
                    print("upload started...")
                    self.command_executer(f"rclone copy temp/drive.mp4 /home/kirankashyap/gdrive/Test --vfs-cache-mode writes")
                    self.motion_detection_status=False
                    self.start_time_status=False

            
    def start_video_recorder(self,local_clip_path,drive_clip_path):

        local_clip_file=cv2.VideoWriter(os.path.join(local_clip_path,f"local.mp4"),self.codec,self.frame_rate,self.frame_size)
        drive_clip_file=cv2.VideoWriter(os.path.join(drive_clip_path,f"drive.mp4"),self.codec,self.frame_rate,self.frame_size)

        drive_uploader_thread=Thread(target=self.drive_uploader)
        drive_uploader_thread.start()

        _,frame1=self.video.read()
        while True:
            _,frame2=self.video.read()

            diff = cv2.absdiff(frame1, frame2)
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours: 
                if cv2.contourArea(contour) > 1000 and self.motion_detection_status == False:
                    print("motion detected...")

                    self.motion_detection_status=True
                    self.drive_recording_status=True

            resized_frame=cv2.resize(frame1,self.frame_size)
            
            if self.motion_detection_status == True and self.drive_recording_status == True:
                drive_clip_file.write(resized_frame)
                
            
            local_clip_file.write(frame1)
            
            frame1=frame2

            cv2.imshow("video",frame1)

            if cv2.waitKey(1) == ord("s"):
                break

        cv2.destroyAllWindows()

recorder=VideoRecorder(stream_source_index=2)
recorder.start_video_recorder(local_clip_path="media",drive_clip_path="temp")
  
                
                    



