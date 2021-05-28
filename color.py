# Made by Krukov, Mitrofanov, Patutin

import cv2
import numpy as np


def process(frame, start_point, end_point):
    rect_size = 100
    h_sensitivity = 15
    colors = {
        'green': (60 - h_sensitivity, 60 + h_sensitivity),
        'red': (0, 7),
        'red ': (180 - h_sensitivity, 180),
        'orange': (7, 20),
        'yellow': (20, 30 + h_sensitivity),
        'light_blue': (90 - h_sensitivity, 90 + h_sensitivity),
        'dark_blue': (120 - h_sensitivity, 120 + h_sensitivity),
        'purple': (150 - h_sensitivity, 150 + h_sensitivity),
    }
    color = (255, 255, 255)
    thickness = 2
    rect = cv2.rectangle(frame, start_point, end_point, color, thickness)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_text = 'color not recognized'

    for i in colors:
        s_h, v_h, s_l, v_l = 255, 255, 50, 50
        lower_h, higher_h = colors[i]

        green_upper = np.array([higher_h, s_h, v_h])
        green_lower = np.array([lower_h, s_l, v_l])
        mask_frame = hsv_frame[start_point[1]:end_point[1] + 1, start_point[0]:end_point[0] + 1]
        mask_green = cv2.inRange(mask_frame, green_lower, green_upper)

        green_rate = np.count_nonzero(mask_green) / (rect_size * rect_size)
        if green_rate > 0.9:
            color_text = i
    # color_text.replace('1', '')
    # color_text.replace('2', '')

    org = end_point
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7

    av_hue = np.average(mask_frame[:, :, 0])
    av_sat = np.average(mask_frame[:, :, 1])
    av_val = np.average(mask_frame[:, :, 2])
    average = [int(av_hue), int(av_sat), int(av_val)]

    text = cv2.putText(rect, color_text, (10, 50), font, font_scale, color, thickness,
                       cv2.LINE_AA)
    frame = text
    return frame


def main():
    print('Press Q, W, E to change mode\n')
    print('Press 4 to Quit the Application\n')

    # Open Default Camera
    cap = cv2.VideoCapture(0)  # gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)
    mode = 1

    while cap.isOpened():
        # Take each Frame
        ret, frame = cap.read()
        frame = cv2.flip(frame, 180)

        rect_size = 100
        width, height, channels = frame.shape
        points = {
            1: ((int(height / 3 - rect_size - 50), int(width / 2 - rect_size / 2)),
                (int(height / 3 - 50), int(width / 2 + rect_size / 2))),
            2: ((int(height / 2 - rect_size / 2), int(width / 2 - rect_size / 2)),
                (int(height / 2 + rect_size / 2), int(width / 2 + rect_size / 2))),
            3: ((int(height / 2 + rect_size / 2 + 100), int(width / 2 - rect_size / 2)),
                (int(height / 2 + rect_size / 2 + 100 + rect_size), int(width / 2 + rect_size / 2)))
        }
        start_point, end_point = points[mode]
        process(frame, start_point, end_point)

        # Show video
        cv2.imshow('Cam', frame)

        # Exit if "4" is pressed
        k = cv2.waitKey(1) & 0xFF
        if k == 52:  # ord 4
            # Quit
            print('Good Bye!')
            break
        if k in [ord('q'), ord('Q')]:
            mode = 1
        elif k in [ord('w'), ord('W')]:
            mode = 2
        elif k in [ord('e'), ord('E')]:
            mode = 3
    # Release the Cap and Video
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
