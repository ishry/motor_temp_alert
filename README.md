# motor_temp_alert

- モータの温度を監視し，温度に応じて警告音を鳴らすROSパッケージ．
- loopback処理は neuro_vm のプラグインとして実装しているためこのパッケージとは関係ないことに注意．

## 環境構築

### 前提
- trans_ros_bridgeが同じcatkinワークスペースに存在する必要がある

### 依存解決
```bash
cd ~/catkin_ws/manta_ws
rosdep install --from-paths src/motor_temp_alert/ --ignore-src -r -y
catkin build motor_temp_alert
source devel/setup.bash
```

## 実行手順

- まず実機を立ち上げる
- その後，
```bash
rossetmanta
rosrun motor_temp_alert motor_temp_alert.py
```
