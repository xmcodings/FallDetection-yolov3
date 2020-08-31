
def detectFall(classids, centercoords):
    # takes classids, centers, and calculates detection
    QUEUESIZE = 4
    threshold = 1
    detect = False
    recent = classids[QUEUESIZE-1]
    ob_length = len(recent)
    count = 0
    for detect in classids:
        if ob_length != len(detect):
             count = count + 1
    if count > threshold:
        detect = True

    # calculate what object is detected

    return detect, recent, centercoords[QUEUESIZE-1]



def warnUser():

    

    return 1
