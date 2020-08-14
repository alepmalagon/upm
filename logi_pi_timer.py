"""
Interface with a hardware timer implemented as a counter on a ValentF(x) LOGI
Pi FPGA board.
"""

#import logi
import datetime as dt
import ntplib

def microseconds_past_the_hour(t2):
    return t2.microsecond + 1000000*(t2.minute*60 + t2.second)

def get_ntp_time():
    ntp_pool = '0.pool.ntp.org'
    call = ntplib.NTPClient()
    response = call.request(ntp_pool, version=3)
    t = dt.datetime.fromtimestamp(response.orig_time)
    return t

#stime = get_ntp_time()
#phase = dt.datetime.now() - stime
print(str(dt.datetime.now()))

counter_timestep_us = 1
max_counter_value = 65535

def read_counter():
    """
    Read the current value of the counter.
    """
    #address = 0
    #type_size = 2
    #n_reads = 1
    tnow = microseconds_past_the_hour(dt.datetime.now())
    #print (str(tnow))
    #print (str(t2))
    #print(int((t2.total_seconds())*1000))
    #microseconds_past_the_hour = t2.microseconds + 1000000*(t2.minutes*60 + t2.seconds)
    #print (int(t2))
    return int(tnow)

def counter_delta(counter_value_2, counter_value_1):
    """
    Calculate counter_value_2 - counter_value_1 (accounting for wraparound)
    """
    delta = counter_value_2 - counter_value_1
    if delta < 0:
        # counter has wrapped around
        delta += max_counter_value
    return delta

def counter_delta_to_us(delta):
    """
    Convert a difference in counter values to a time difference.
    """
    return delta * counter_timestep_us
