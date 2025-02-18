from datetime import datetime

def print_time(message="Current time:"):
    current_time = datetime.now().time()
    print(message, current_time)