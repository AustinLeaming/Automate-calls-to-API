# Prompts user for automating sending metrics or logs
# ANYTHING, other than a 2** response breaks the automation. This is to prevent overflowing errors.
# to run script -> DD_SITE="datadoghq.com" DD_API_KEY="<API_KEY>" python3 automate.py
# CTRL+C to break loop
import time
import send_logs
from send_logs import *
import send_metric
from send_metric import *
from datetime import datetime
import validate_api_key 
from validate_api_key import *
from ddtrace import config, patch_all
import random
# from ddtrace.opentracer import Tracer, set_global_tracer

patch_all()

# define counter variable
# useful for triggering some sort of alternative automation
# for example, you can send a set of logs with a certain type of tag for a defined limit, then switch to a different tag
counter = 0

# define user inputs for functions
get_function_script = 0
function_frequency = 0

# used to check if user has started a call before or not
loop_count = 0

# used to validate API, don't start script if the API key is bad
def check_api():
    validate_api_key.make_call()
    if validate_api_key.response.valid == True:
        next
    else:
        print("bad API")
    time.sleep(.4)

check_api()

# get input from the user on what they want to do
def get_user_params():
    global get_function_script
    global function_frequency
    get_function_script = int(input("1. Logs 2. Metrics: "))
    function_frequency = int(input("Frequency in seconds: "))
    choose_script()

def start_script():
    global loop_count
    if loop_count == 0:
        loop_count = loop_count + 1
        get_user_params()
    else:
        continue_loop_prompt = (input("run another call? Y/N:")).lower()
        if continue_loop_prompt == "y":
            get_user_params()
        else:
            print("Bye!")

# runs the make_call function in the send_logs file
def automate_log_script():
    global counter
    print("running log script with a", function_frequency, "second interval")
    print("Press CTRL+C to break if no errors are found")
    print("Valid responses look like -> {}")
    time.sleep(.8)
    log_sub_input = int(input("1. Normal Log Post 2. Random value logs "))
    if log_sub_input == 1:
        normal_logs()
    elif log_sub_input == 2:
        random_logs()
    else:
        print("sub function not found")

def random_logs():
    print("Running a randomized log call...")
    try:
        while True:
            time.sleep(function_frequency)
            send_logs.make_call_random_service()
            if send_logs.response == {}:
                now = datetime.now().time()
                print(send_logs.response, "timestamp:", now)
            else:  
                print("Error found, stopping script")
                break 
    except KeyboardInterrupt:
        print("")
        start_script()

def normal_logs():
    print("Running a normal log call...")
    try:
        while True:
            time.sleep(function_frequency)
            send_logs.make_call()
            print(send_logs.response,"in automate")
            if send_logs.response == {}:
                now = datetime.now().time()
                print(send_logs.response, "timestamp:", now)
            else:  
                print("Error found, stopping script")
                break 
    except KeyboardInterrupt:
        print("")
        start_script()

def automate_metric_script():
    # import counter variable
    global counter
    print("running metrics script with a", function_frequency, "second interval")
    print("press CTRL+C to break")
    print("Valid responses look like -> {'errors': []}")
    time.sleep(.8)
    try:
        while True:
            time.sleep(function_frequency)
            # valid response comes from send_metric.py
            # check to see if the response was valid, break if not
            send_metric.metric_call()
            if send_metric.response.errors == []:
                now = datetime.now().time()
                print(send_metric.response, "timestamp:", now)
            else:  
                print("Error found, stopping scripts")
                break 
    except KeyboardInterrupt:
        print("")
        start_script()

def choose_script():
    if get_function_script == 1:
        automate_log_script()
    elif get_function_script == 2:
        automate_metric_script()
    else:
        print("error, rerun script")

start_script()