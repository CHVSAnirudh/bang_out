import cv2
import mediapipe as mp
import numpy as np
from punch_detect import punch_detect
import requests
import threading
from playsound import playsound
URL = "http://127.0.0.1:5000/get_body"
class tracking():
  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles
  mp_pose = mp.solutions.pose
  cap = cv2.VideoCapture(0)
  score = 0
# For webcam input:
  def play_punch_sound(self):
    playsound("p1.mp3")


  def detect(self):
    right_punch = punch_detect()
    left_punch = punch_detect()
    with self.mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
      while self.cap.isOpened():
        success, image = self.cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        if results is not None:
          punch, sevearity = right_punch.punch_detect(results.pose_landmarks.landmark[20])
          if punch:
            response = requests.get(URL)
            res = response.json()
            try:
              c1,c2 = res[0][0],res[0][1]
            except:
              c1,c2 = (0,0),(0,0)
            self.is_punch(results.pose_landmarks.landmark[20].x, results.pose_landmarks.landmark[20].y,c1,c2)
          punch, sevearity = left_punch.punch_detect(results.pose_landmarks.landmark[19])
          if punch:
            try:
              c1,c2 = self.get_body()
            except:
              c1,c2 = (0,0),(0,0)
            self.is_punch(results.pose_landmarks.landmark[20].x, results.pose_landmarks.landmark[20].y,c1,c2)
          
          image.flags.writeable = True
          image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
          self.mp_drawing.draw_landmarks(
              image,
              results.pose_landmarks,
              self.mp_pose.POSE_CONNECTIONS,
              landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
          

          # Flip the image horizontally for a selfie-view display.
          cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
          if cv2.waitKey(5) & 0xFF == 27:
            break
    self.cap.release()
  
  def get_body(self):
    try:
      if self.cap.isOpened():
        with self.mp_pose.Pose(
          min_detection_confidence=0.5,
          min_tracking_confidence=0.5) as pose:
          success, image = self.cap.read()
          image.flags.writeable = False
          image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          results = pose.process(image)
          x1,y1 = results.pose_landmarks.landmark[11].x,results.pose_landmarks.landmark[11].y
          # x2,y2 = results.pose_landmarks.landmark[12].x,results.pose_landmarks.landmark[12].y
          # x3,y3 = results.pose_landmarks.landmark[23].x,results.pose_landmarks.landmark[23].y
          if results.pose_landmarks.landmark[24].visibility > 0.5:
            x4,y4 = results.pose_landmarks.landmark[24].x,results.pose_landmarks.landmark[24].y
          else:
            x4,y4 = results.pose_landmarks.landmark[12].x,1.0
          return (x1,y1),(x4,y4)
    except:
      self.get_body()

  def is_punch(self,x,y,c1,c2):
    if x <c1[0]+0.1 and x>c2[0] - 0.1 and y>c1[1]-0.1 and y<c2[1]+0.1:
      self.score += 5
      my_thread = threading.Thread(target=self.play_punch_sound)
      my_thread.start()
      print(self.score)


if __name__ == "__main__":
  track = tracking()
  track.detect()