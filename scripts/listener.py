#!/usr/bin/env python3
import rospy
import os
import sys
import pygame

from trans_ros_bridge.msg import ExtraMotorState

class MotorTempListener:
    def __init__(self):
        self.topic_name = "/motor_states_low/motor_outer_temp"

        script_dir = os.path.dirname(os.path.abspath(__file__))
        sound_dir = os.path.join(script_dir, '../sounds')
        self.sound1_file = os.path.join(sound_dir, "alert1.mp3")
        self.sound2_file = os.path.join(sound_dir, "alert2.mp3")

        # check sound files
        missing_files = []
        if not os.path.exists(self.sound1_file):
            missing_files.append(self.sound1_file)
        if not os.path.exists(self.sound2_file):
            missing_files.append(self.sound2_file)
            
        if missing_files:
            error_msg = "\n[ERROR]: One or more sound files are missing. Cannot start motor monitor."
            rospy.logerr(error_msg)
            for f in missing_files:
                rospy.logerr(f"[Missing]  Missing file: {f}")
            
            rospy.signal_shutdown("Missing sound files.")
            sys.exit(1)    
        self.temp_critical = 80.0 
        self.temp_warning  = 70.0
        self.temp_reset    = 65.0
        
        self.alert_level = 0 # 0:safe 1:sound1 2:sound2
        
        pygame.mixer.init()
        
        rospy.init_node('motor_temp_listener', anonymous=True)
        
        rospy.Subscriber(self.topic_name, ExtraMotorState, self.callback)
        
        rospy.loginfo(f"--- motor temperature monitoring start ---")

    def play_sound(self, file_name):
        if os.path.exists(file_name):
            try:
                # Stop if already playing (prioritize new alert immediately)
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    
                pygame.mixer.music.load(file_name)
                pygame.mixer.music.play()
                rospy.loginfo(f"♪ Sound playing: {file_name}")
            except pygame.error as e:
                rospy.logerr(f"Playback Error: {e}")
        else:
            rospy.logwarn(f"File not found: {file_name}")

    def callback(self, msg):
        if not msg.data:
            return

        max_temp = max(msg.data)
        
        # rospy.loginfo(f"Max Temp: {max_temp} | Alert Level: {self.alert_level}")
        if max_temp >= self.temp_critical:
            if self.alert_level < 2:
                rospy.logwarn(f"[CRITICAL] Motor temperature rise: {max_temp} -> Playing Sound2")
                self.play_sound(self.sound2_file)
                self.alert_level = 2

        elif max_temp >= self.temp_warning:
            if self.alert_level < 1:
                rospy.logwarn(f"[WARNING] Motor temperature rise: {max_temp} -> Playing Sound1")
                self.play_sound(self.sound1_file)
                self.alert_level = 1
        
        elif max_temp <= self.temp_reset:
            if self.alert_level > 0:
                rospy.loginfo(f"[RESET] Temperature drop confirmed: {max_temp} -> Monitoring state reset")
                self.alert_level = 0
            rospy.loginfo(f"[INFO] Current max temperature: {max_temp} ")

if __name__ == '__main__':
    try:
        listener = MotorTempListener()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
 
