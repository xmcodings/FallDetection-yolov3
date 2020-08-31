
def detectFall(classids, centercoords):
    # takes classids, centers, and calculates detection
    detect_keywords = [0, 34, 41, 60] # person, sports ball, bottle, pottedplant
    ignore_keywords = [14] # bird
    QUEUESIZE = 4
    threshold = 1
    detect = False
    recent = classids[QUEUESIZE-1]
    right_before = classids[QUEUESIZE - 2]
    object_diff = []
    ob_length = len(recent)
    count = 0
    for detect in classids:
        if ob_length != len(detect):
             count = count + 1
    if count > threshold:
        if detect in detect_keywords:
            object_diff = right_before - recent
            detect = True
        else:
            detect = False

    # calculate what object is detected

    return detect, object_diff, centercoords[QUEUESIZE-1]



def warnUser():

    return 1
