# throttle.py

# Simple topic based throttle
# string topic, float detection_time, int throttle_timeout
# detected object list with label->time accociation
throttle_list = {}
def throttle_output( topic, timestamp, throttle_timeout):
    if topic in throttle_list:
        # check if time since last detection
        # if less than THROTTLE_TIME, return true, we are throttling
        # if greater than THROTTLE_TIME, return false, we are not throttling
        if timestamp - throttle_list[topic] < throttle_timeout:
            return True
        else:
            throttle_list[topic] = timestamp
            return False
    else:
        # set time in dictionary for this object
        # return false meaning we are not throttling for this object
        throttle_list[object_label] = timestamp
        return False
