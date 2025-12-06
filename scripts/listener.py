#!/usr/bin/env python3
import rospy
import os
import pygame

from trans_ros_bridge.msg import ExtraMotorState

class MotorTempListener:
    def __init__(self):
        self.topic_name = "/motor_states_low/motor_outer_temp"
        
        self.sound1_file = "sound1.mp3"
        self.sound2_file = "sound2.mp3"
        
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
                # 既に再生中なら止める（新しい警告を即座に優先）
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    
                pygame.mixer.music.load(file_name)
                pygame.mixer.music.play()
                rospy.loginfo(f"♪ Sound playing: {file_name}")
            except pygame.error as e:
                rospy.logerr(f"再生エラー: {e}")
        else:
            rospy.logwarn(f"ファイルが見つかりません: {file_name}")

    def callback(self, msg):
        if not msg.data:
            return

        max_temp = max(msg.data)
        
        # rospy.loginfo(f"Max Temp: {max_temp} | Alert Level: {self.alert_level}")
        if max_temp >= self.temp_critical:
            if self.alert_level < 2:
                rospy.logwarn(f"[CRITICAL] モーター温度上昇: {max_temp}℃ -> Sound2再生")
                self.play_sound(self.sound2_file)
                self.alert_level = 2

        elif max_temp >= self.temp_warning:
            if self.alert_level < 1:
                rospy.logwarn(f"[WARNING] モーター温度上昇: {max_temp}℃ -> Sound1再生")
                self.play_sound(self.sound1_file)
                self.alert_level = 1
        
        elif max_temp <= self.temp_reset:
            if self.alert_level > 0:
                rospy.loginfo(f"[RESET] 温度低下を確認: {max_temp}℃ -> 監視状態リセット")
                self.alert_level = 0

if __name__ == '__main__':
    try:
        listener = MotorTempListener()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
