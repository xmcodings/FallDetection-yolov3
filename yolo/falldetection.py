
def detectFall(classids, centercoords):
    # takes classids, centers, and calculates detection
    # returns 0 if no detect, 1 if warn, and 2 if human

    red_detect_keywords = [0] # person,
    orange_detect_keywords = [24, 25, 26, 32, 39, 41, 60, 67, 78, 79] #  sports ball, bottle, cup pottedplant, hairdryer, toothbrush
    ignore_keywords = [14] # bird
    QUEUESIZE = 4
    threshold = 1
    detect = 0
    recent = classids[QUEUESIZE-1]
    right_before = classids[QUEUESIZE - 2]
    object_diff = []
    ob_length = len(recent)
    count = 0
    '''
    for detects in classids:
        if ob_length != len(detects):
             count = count + 1
    if count > threshold:
        if detects in detect_keywords:
            object_diff = right_before - recent
            detect = True
        else:
            detect = False
    '''
    # calculate what object is detected
    ret_coords = []
    is_human = False
    for idx, objects in enumerate(recent):

        if objects in orange_detect_keywords:
            detect = 1
            object_diff.append(objects)
            ret_coords.append(centercoords[QUEUESIZE-1][idx])

        if objects in red_detect_keywords:
            detect = 2
            is_human = True
            object_diff.append(objects)
            ret_coords.append(centercoords[QUEUESIZE-1][idx])

    if is_human:
        detect = 2

    return detect, object_diff, ret_coords



def warnUser():

    return 1
