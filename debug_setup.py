"""
real name: debug_oled128x32_i2c_feather32_setup.py

This is the code used to support the use of the .9 inch oled 128x32 display
for debug output in Adafruit feather esp32 mpython programming. A file like this
needs to be written for any hardware/connection protocol changes. The module
debug.py uses a program like this to set up the various parameters for a
particular hardware/connection protocol that is displaying debug output in an
application program. The application program calls methods from the debug class,
which insulates the app layer from the hardware or protocol.

Use: copy this program into a file called debug_setup.py on the esp32.
debug.py will import debug_setup.py, so no changes need to be made to
debug.py.
"""

from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
from time import sleep

#pins for i2c connection
scl_pin = 22
sda_pin = 23

#for our testing of this module
sleep_time = 0

# parms that control the display use
disp_width  = 128
disp_height = 32
char_height = 8
disp_lines  = 4 #0, 1, 2, 3,...
indent_dx =   2
deep_print = False

i2c = SoftI2C(scl=Pin(22), sda=Pin(23))
disp = SSD1306_I2C( disp_width, disp_height, i2c)

def clear_disp():
  disp.fill(0)

def get_indent_dx():
  global indent_dx
  """ how much to add for 1 indent.
  """
  return indent_dx

def set_disp_pause(sec):
  global sleep_time
  sleep_time = sec
  
def set_deep_print( true_false ):
    global deep_print
    deep_print = true_false
    
  
def prnt0(s):
    if deep_print:
      print(s)

def prnt1(s,v):
    if deep_print:
        print(s.format(v))
        
def prnt2(s, v1, v2):
    if deep_print:
        print(s.format(v1, v2))
        
def prnt3(s, v1, v2, v3):
    if deep_print:
        print(s.format(v1, v2, v3))
        
def text(x, y, text_string, do_scroll):
  global disp_width
  global disp_height
  global char_height
  global disp_lines
  
  
  prnt3("in text({}) x={}y={}",text_string,x,y)
  
  if y > disp_height-char_height:
    new_y = disp_height-char_height #stay on last line
    if do_scroll:
      #scroll and erase remnants. framebuf is broken (IMO)
      disp.scroll(0,-char_height)
      disp.rect(0,new_y,disp_width,char_height,0,True, 0)
    prnt2("ts at {},{}",x,new_y)
    disp.text(text_string, x, new_y)
    new_y += char_height
  else:
    prnt2("t at {},{}",x,y)
    disp.text(text_string, x,y)
    new_y = y+char_height
  
  disp.show()
  prnt0("leaving text()")
  sleep(sleep_time)
  return new_y
