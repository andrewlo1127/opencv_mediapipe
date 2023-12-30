import cv2
import mediapipe as mp

# global judge_number

def should_draw_connection(i):
    if (0 <= i <= 10) or (17 <= i <= 22) or (29 <= i <= 32):
        return False
    else:
        return True

def judge(my_points):
    j = False
    # 參考的座標值
    reference_points = {
        11: (0.5739479064941406, 0.4265810549259186),
        12: (0.4952430725097656, 0.42230644822120667),
        13: (0.6476616859436035, 0.41710713505744934),
        14: (0.42682498693466187, 0.41259345412254333),
        15: (0.7134471535682678, 0.40873464941978455),
        16: (0.36671704053878784, 0.4023638367652893),
        23: (0.5620903372764587, 0.619877278804779),
        24: (0.5148160457611084, 0.6218931674957275),
        25: (0.6337798833847046, 0.7225762605667114),
        26: (0.42810115218162537, 0.6668710708618164),
        27: (0.7059465646743774, 0.8217892050743103),
        28: (0.4219309985637665, 0.8127726316452026),
    }
    threshold = 0.05  # 設定一個閾值，可以根據實際情況調整
    reference_relative_positions_11_to_16 = {}
    my_relative_positions_11_to_16 = {}
    for i in range(12, 17):
        reference_relative_positions_11_to_16[i] = (
            abs(reference_points[i][0] - reference_points[11][0]),
            abs(reference_points[i][1] - reference_points[11][1])
        )
        my_relative_positions_11_to_16[i] = (
            abs(my_points[i][0] - my_points[11][0]),
            abs(my_points[i][1] - my_points[11][1])
        )
    for z in range(2):
        k = 12
        while abs(reference_relative_positions_11_to_16[k][z] - my_relative_positions_11_to_16[k][z]) <= threshold:
            k+=1
            if k == 17:
                j = True
                break
        if j == False:
            return j

    reference_relative_positions_23_to_28 = {}
    my_relative_positions_23_to_28 = {}
    for i in range(23, 29):
        reference_relative_positions_23_to_28[i] = (
            abs(reference_points[i][0] - reference_points[23][0]),
            abs(reference_points[i][1] - reference_points[23][1])
        )
        my_relative_positions_23_to_28[i] = (
            abs(my_points[i][0] - my_points[23][0]),
            abs(my_points[i][1] - my_points[23][1])
        )
    for z in range(1):
        k = 23
        while abs(reference_relative_positions_23_to_28[k][z] - my_relative_positions_23_to_28[k][z]) <= threshold:
            k+=1
            if k == 29:
                j = True
                break
        return j

if __name__ == "__main__":
    # 讀取圖片
    # for k in range(1, 16):
    img = cv2.imread(str(9) + '.jpg')
    img = cv2.resize(img, None, fx=0.7, fy=0.7)

    mpPose = mp.solutions.pose
    pose = mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    poseLmsStyle = mpDraw.DrawingSpec(color=(255, 0, 255), thickness=3) # 點的顏色
    poseConStyle = mpDraw.DrawingSpec(color=(255, 0, 0), thickness=5) # 連線的顏色

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)

    # print(result.pose_landmarks)
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]

    my_points = {}

    if result.pose_landmarks:
        for i, lm in enumerate(result.pose_landmarks.landmark):
            xPos = int(lm.x * imgWidth)
            yPos = int(lm.y * imgHeight)

            if should_draw_connection(i):
                cv2.circle(img, (xPos, yPos), 3, (0, 0, 255), -1) # 畫點
                mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS, poseLmsStyle, poseConStyle) # 畫線
                cv2.putText(img, str(i), (xPos-25, yPos+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2) # 畫座標
                print(i, lm.x, lm.y)
                my_points[i] = (lm.x, lm.y)
    print(my_points)
    j = judge(my_points)

    cv2.imshow('img' + str(9), img)

    if j:
        print(j)
        cv2.destroyAllWindows()
    else:
        print(j)
        cv2.waitKey(0)
        cv2.destroyAllWindows()