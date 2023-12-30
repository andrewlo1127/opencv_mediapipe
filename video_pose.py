import cv2
import mediapipe as mp
import json
import random
import time

def should_draw_connection(i):
    if (0 <= i <= 10) or (17 <= i <= 22) or (29 <= i <= 32):
        return False
    else:
        return True

def img_pose(img):
    mpPose = mp.solutions.pose
    pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    poseLmsStyle = mpDraw.DrawingSpec(color=(255, 0, 255), thickness=3) # 點的顏色
    poseConStyle = mpDraw.DrawingSpec(color=(255, 0, 0), thickness=5) # 連線的顏色

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)

    imgHeight = img.shape[0]
    imgWidth = img.shape[1]

    if result.pose_landmarks:
        for i, lm in enumerate(result.pose_landmarks.landmark):
            xPos = int(lm.x * imgWidth)
            yPos = int(lm.y * imgHeight)

            if should_draw_connection(i):
                cv2.circle(img, (xPos, yPos), 3, (0, 0, 255), -1) # 畫點
                mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS, poseLmsStyle, poseConStyle) # 畫線
    return img

def judge(my_points, random_image_index):
    j11 = [False, False]
    j23 = [False, False]
    file_path = "pose.json"
    with open(file_path, "r") as file:
        json_data = file.read()
    data = json.loads(json_data)
    reference_points = data["reference_points_"+str(random_image_index)]
    threshold = 0.05  # 設定一個閾值
    reference_relative_positions_11_to_16 = {}
    my_relative_positions_11_to_16 = {}
    for i in range(12, 17):
        reference_relative_positions_11_to_16[str(i)] = [
            abs(reference_points[str(i)][0] - reference_points["11"][0]),
            abs(reference_points[str(i)][1] - reference_points["11"][1])
        ]
        my_relative_positions_11_to_16[str(i)] = [
            abs(my_points[str(i)][0] - my_points["11"][0]),
            abs(my_points[str(i)][1] - my_points["11"][1])
        ]
    for z in range(2):
        if all(abs(reference_relative_positions_11_to_16[str(k)][z] - my_relative_positions_11_to_16[str(k)][z]) <= threshold for k in range(12, 17)):
            j11[z] = True

    reference_relative_positions_23_to_28 = {}
    my_relative_positions_23_to_28 = {}
    for i in range(23, 29):
        reference_relative_positions_23_to_28[str(i)] = (
            abs(reference_points[str(i)][0] - reference_points["23"][0]),
            abs(reference_points[str(i)][1] - reference_points["23"][1])
        )
        my_relative_positions_23_to_28[str(i)] = (
            abs(my_points[str(i)][0] - my_points["23"][0]),
            abs(my_points[str(i)][1] - my_points["23"][1])
        )
    for z in range(2):
        if all(abs(reference_relative_positions_23_to_28[str(k)][z] - my_relative_positions_23_to_28[str(k)][z]) <= threshold for k in range(23, 29)):
            j23[z] = True

    if j11[0] and j11[1] and j23[0] and j23[1]:
        return True
    else:
        return False

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    mpPose = mp.solutions.pose
    pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    poseLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)
    poseConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)

    timeout = 20  # 設定時間限制為20秒
    start_time = time.time()
    while True:
        random_image_index = random.randint(1, 15)
        image = cv2.imread(str(random_image_index)+".jpg")
        image = img_pose(image)

        # 獲取畫面寬高
        screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 創建全螢幕視窗
        cv2.namedWindow("Full Screen", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Full Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        start_time = time.time()
        while True:
            ret, img = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                continue  # 继续下一次循环
            if ret:
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                result = pose.process(imgRGB)

                imgHeight = img.shape[0]
                imgWidth = img.shape[1]

                my_points = {}

                if result.pose_landmarks:
                    mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS, poseLmsStyle, poseConStyle)
                    for i, lm in enumerate(result.pose_landmarks.landmark):
                        xPos = int(lm.x * imgWidth)
                        yPos = int(lm.y * imgHeight)

                        if should_draw_connection(i):
                            cv2.circle(img, (xPos, yPos), 3, (0, 0, 255), -1) # 畫點
                            mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS, poseLmsStyle, poseConStyle) # 畫線
                            cv2.putText(img, str(i), (xPos-25, yPos+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2) # 畫座標
                            my_points[str(i)] = [lm.x, lm.y]
            # 將圖片大小設置為畫面大小
            image = cv2.resize(image, (imgWidth, imgHeight))
            
            # 在整個畫面添加圖片殘影
            img = cv2.addWeighted(img, 1, image, 0.5, -10)

            cv2.imshow('Full Screen', img)
            j = judge(my_points, random_image_index)

            if j:
                print(j)
                break
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print("Timeout! Moving to the next random_image_index.")
                j = True
                break
            if cv2.waitKey(1) == ord("q"):
                print(j)
                break
        if j == False:
            break