# Prompts user for automating sending metrics or logs
# ANYTHING, other than a 2** response breaks the automation. This is to prevent overflowing errors.
# to run script -> DD_SITE="datadoghq.com" DD_API_KEY="<API_KEY>" python3 automate.py
# CTRL+C to break loop
import time
import send_logs
from send_logs import *
import send_metric
from send_metric import *

# define counter variable
# useful for triggering some sort of alternative automation
counter = 0

# get input from the user on what they want to do
get_function_script = int(input("1. Logs 2. Metrics: "))
function_frequency = int(input("Frequency in seconds: "))

# runs the make_call function in the send_logs file
def automate_log_script():
    #import counter variable
    global counter
    # run loading sequence, would be nice to run a validate API key in the loading sequence
    loading_sequence()
    print("running log script with a", function_frequency, "second interval")
    print("Press CTRL+C to break if no errors are found")
    print("Valid responses look like -> {}")
    time.sleep(1.7)
    while True:
        time.sleep(function_frequency)
        # while(counter<10):
        #     time.sleep(function_frequency)
        #     send_logs.make_call_missing_value()
        #     counter = counter + 1
        send_logs.make_call()
        # valid response comes from send_logs.py
        # check to see if the response was valid, break if not
        if send_logs.response == {}:
            print("Next call in", function_frequency, "seconds...")
        else:  
            print("Error found, stopping script")
            break 

def automate_metric_script():
    # import counter variable
    global counter
    # run loading sequence, would be nice to run a validate API key in the loading sequence
    loading_sequence()
    print("running metrics script with a", function_frequency, "second interval")
    print("press CTRL+C to break")
    print("Valid responses look like -> {'errors': []}")
    time.sleep(1.7)
    while True:
        time.sleep(function_frequency)
        # valid response comes from send_metric.py
        # check to see if the response was valid, break if not
        send_metric.metric_call()
        if send_metric.response.errors == []:
            print("Next call in", function_frequency, "seconds...")
        else:  
            print("Error found, stopping scripts")
            break 

def loading_sequence():
    tick = 0
    while tick < 3:
        time.sleep(.8)
        print("...")
        tick = tick +1 
    time.sleep(.8)

if get_function_script == 1:
    automate_log_script()
    print("chose logs")
elif get_function_script == 2:
    automate_metric_script()
else:
    print("error, rerun script")