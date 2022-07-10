'''
Stepper distance exerciser. With a digital rule attached, we can see how many steps are needed per some distance.
A loop allows as many measurements made as desired.
Wiring:
  GPIO5 - pulse pin      to logic level convertor (LLC) LV1
  GPIO 18 direction pin  to LLC LV2
  3.3v                   to LLC LV
  GND                    to LLC GND
  a 3-5 volt logic level convertor is placed between uproc and DM542 and the 5v power for the DM542 is supplied
  externally.
  
  DM542 Settings and pins
  Set at 800 pulses per revolution. This affects steps per inch calculations as well as 8mm Lead screw thread pitch
  Pulse +5v       to LLC HV1
  Direction +5    to LLC HV2
  Both minus pins to LLC GND
  
  External 5v power source
  +5v to LLC HV
  GND to LLC GND
  
  Distances and Error
  If the DM542 is set at 800 steps per revolution and an 8mm lead screw is used, the calculated distance per 1 step
  is 8mm/1rev*1rev/800steps = .01mm/step = .0003937in/step
  This results in an overtravel error of 0.82%
  
  Setting the DM542 to 1600 steps per revolution and an 8mm lead screw yields:
  8mm/1rev*1rev/1600 = .005mm/step = .00019685in/step
  This also results in an overtravel distance of 0.817%
  
  TODO: Need to test small distance increments. It appears that these are not too precise using .00817. Great for
  longer distances at 800 and 1600 steps/rev.
'''
from machine import Pin, PWM
import math
import utime

#Changing step wait alters gantry cart travel speed.
#The DN542 requires a pulse up time of >2.5usec
step_wait = 100 #usec
pulse_uptime = 30 #usec

#Settings for DM542 set at 800 steps/rev
steps_per_inch = 2540  # for 800 steps/rev
#at 800 steps/rev distance moved is 0.817% too far, so divide by this number
distance_error = 1.00817 

#Settings for DM542 set at 1600 steps/rev
#steps_per_inch = 5080
#distance_error = 1.00817 #This is the same as 800 steps/rev

pulse_pin = Pin(5, Pin.OUT)
pulse_pin.value(0)

dir_forward = 1
dir_backward = 0
direction_pin = Pin(18, Pin.OUT)
direction_pin.value(dir_forward)

def _pulse_one_step():
    global pulse_uptime
    
    pulse_pin.value(0)
    pulse_pin.value(1)
    utime.sleep_us(pulse_uptime)
    pulse_pin.value(0)
    
def move_stepper( inches_to_travel, direction):
    global steps_per_inch
    global distance_error
    
    print("In move_stepper() - setting direction pin")
    #depends on wiring!!! be careful to get wiring right!!!!
    if direction == 'forward':
        direction_pin.value(dir_forward)
    else:
        direction_pin.value(dir_backward)

    steps_to_take = int(round(steps_per_inch*inches_to_travel/distance_error))
    print("  taking {} steps".format(str(steps_to_take)))
    for step_count in range (steps_to_take ):
      _pulse_one_step()
      utime.sleep_us(step_wait)
    print("move_stepper() done")
    



