"""
Parse command data out of an http request. Asumption is that this is a
PUT request, which keeps the data out of the webpage url. The response is
searched for the beginning of our cmd parms: 'cmd="
This routing takes in the url, presumably gotten from request.url
and returns a dictionary containing the key-value tuples making up the command.
keys are cmd (command), dir (direction), and dist (distance in inches). Other
commands have different parm counts.
"""

from machine import Pin
import stepper_movement as stepper


def init_cmd_call_dict():
    cmd_keys  = [ 'move_rel', 'nop', 'led', 'move_abs']
    cmd_funcs = [ move_relative, nop, led, nop ]
    return dict(list(zip(cmd_keys, cmd_funcs)))


def extract_cmd( chunk):
    cmd_start = chunk.find('cmd=')
    #assert non 0
    cmd_parms = chunk[cmd_start:]
    cmd_parms = cmd_parms.split('&')
    
    cmd_tuples =  [tuple(element.split('=')) for element in cmd_parms]
    return dict(cmd_tuples)
 
 
def move_relative ( parms ):
    inches = float( str( parms['dist']))
    direction = str( parms['dir'])
    print('move_relative() dir:{}, dist:{}'.format(direction, str(inches)))
    stepper.move_stepper( inches, direction)

def nop(parms):
    print('nop() does nothin')


def led(parms):
    print("led() lights!")
    led = Pin(12, Pin.OUT)
    led.value(0)
    
    state = parms['ledstate']
    print(state)
    if state == "on'":
        led.value(1)
    else:
        led.value(0)


def run_cmd( chunk):
    cmd_parms_dict = extract_cmd(chunk)
    cmd_functions = init_cmd_call_dict()
    cmd = cmd_parms_dict.pop('cmd')
    cmd_functions[cmd](cmd_parms_dict)


#url_str = 'http://192.168.101.2/my-form-page/post?cmd=move_rel&dir=forward&dist=10.375'

#run_url_cmd(url_str)

    