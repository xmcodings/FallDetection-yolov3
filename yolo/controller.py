import live_yolo_opencv as yolocv

yolodetect = yolocv.YoloDetection()



while True:
    yolodetect.toggle_camera = True
    detect, object_diff, center_coordinates = yolodetect.start_detection()
    print(detect)
    print(object_diff)
    print(center_coordinates)

    #yolodetect



