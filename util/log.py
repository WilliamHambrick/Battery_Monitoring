from datetime import date, datetime
import os

# func: get_12time
# args: none
# desc: return the 12 hour formatted time with afternoon/morning
def get_12time():
    time = datetime.now()
    time = time.strftime("%I:%M:%S %p")
    return time

# func: get_date
# args: none
# desc: return the 12 hour formatted time with afternoon/morning
def get_date():
    local_date = date.today().strftime("%b-%d-%Y")
    return local_date

# func: log
# args: string or integer concat
# desc: Writes to console in log format. Utilizes log.log to enable output > text
def log(string):
    #log.log(get_12time() + " - " + string);
    print(get_12time() + " - " + string  + "\n")
    with open(os.path.join('./logs/',get_date()+".txt"), "a") as the_file:
        the_file.write(get_12time() + " - " + string  + "\n")