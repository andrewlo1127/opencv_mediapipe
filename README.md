## test.py
可以將想要的圖片放進去，找出想要圖片的各個座標點，再將那些座標點放入pose.json即可。

## pose.json
每張圖片人體的各個座標點

## video_pose.py
流程：
要與圖片做出相同的動作，才會跳下一張圖，並輸出True
若在規定時間內做不出來，也會跳下一張圖，並輸出Timeout
若想結束程式可以按下q來結束，並會輸出False

44行可以調整要與模仿的圖片的相關性
88行可以調整多久會換下一張圖片
