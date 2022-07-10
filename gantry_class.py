"""  gantry.py
This is the class mdodule for the control of a compliance machine's gantries,
which are moved by stepper motors and servos. It is not clear that there is a
need to subclass different types of gantries, but that may be the case in the
future.

version 0.0
 Initial creation
 
"""





class Gantry:
    
  speeds = {'OFF', 'SLOW', 'MED', 'FAST'}
  
    
  def __init__(self, n='unnamed', mc=None, o=0, mxb=0, mnb=0, cl=0,
            ts = 'SLOW', nwd=False, ncb=None):
    self._name = n
    self._movement_controller = mc
    self._origin=o
    self._max_bound=mxb
    self._min_bound=mnb
    self._current_location=cl
    self._travel_speed= ts
    self._notify_when_done=nwd
    self._notify_callback=ncb
    

  def set_origin(self):
    """sets coordinate origin (0) to the current location"""
    self._origin=self._current_location
    
    
  def set_min_boundary(self):
    """sets the coodinate minimum boundary to the current location"""
    self.__min_bound = self._current_location

  def set_max_boundary(self):
    """sets the coodinate maximum boundary to the current location"""
    self.__max_bound = self._current_location
    
  def move_relative(self, direction, distance):
    """gantry moves the given distance unless it would move beyond a boundary"""
    pass
    
  def move_absolute(self, location):
    """Move to the specified location unless a boundary would be crossed."""
    pass

  def jog_start(self, travel_speed):
      
    """continuous movement until a stop command is issued."""
    
    pass
  
  def jog_stop(self):
    """stop a jog movement"""
    pass

  def set_done_notification(self, on_or_off=False, callback=None):
    """instruct whether to turn "done" notification on or off. If on_or_off is
       set to True, and the callback is set, the callback will be called when
       a given command has completed. If False, no notification is sent."""
    pass

    
x_gantry = Gantry()



    
  
  