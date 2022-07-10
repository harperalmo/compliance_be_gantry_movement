
import debug_setup as setup

class Debug:
  """
  debug - a library for monitoring a program's progress. Basic model is to
  output a series of messages and notifications indicating where the program is
  and what is going on.

  Public Functions:

  .in(<func_name>), .out(<func_name)
  These trace the code as it enters and leaves functions. Each in() call
  indents, out() outdents.

  .msg(<message string>)
   outputs a user defined message at the current indent level

  .reset()
  moves indents back to 0, moves current position to 0,0 in display device.

  .sleep(), .wake()
  turns off debugging, but leaves current position and indent levels alone,
  .wake() turns output back on
  
  .scroll_on(), .scroll_off()
  Turns scrolling on and off. Default is to scroll after an in(), out(), or
  .msg() is called. This will not happen if scroll is turned off. Turn back
  on to continue scrolling. Default at startup is to have scrolling on.

  Display hardware and setup is handled by importing a module that has the
  necessary connection stuff. The idea is to separate the code that changes when
  display hardware or connection method changes from the main application code.
  Whenever new hardware or connection method is used, the main application code
  should not have to be changed.

  The setup module should follow this naming convention:
  debug_xxxxxx_setup.py  where xxxxxx is an identifying name for the disp/conn.
  """
  
  def __init__(self):
  
    #state information
    self._indent_dx    = setup.get_indent_dx()  #number of positions to indent
    self._indent_level = -self._indent_dx  # indent position will be zero when first called
    #current cursor position in x,y coordinates
    self._loc_x = 0
    self._loc_y = 0
    #scroll control
    self._scroll_is_on = True
    self._sleeping = False
    self._disp_wait = 0
    setup.clear_disp()
  
  
  def _set_deep_print(self, t_or_f):
      setup.set_deep_print( t_or_f)

  
  def _sendt(self, text_string):
    """
    This is a private function and should not be called from app
    using the debug library.
    """
    if not self._sleeping:
      self._loc_y = setup.text(self._loc_x, self._loc_y, text_string,
                               self._scroll_is_on)
      
      
  def inf( self, func_name ):
    self._indent_level += self._indent_dx
    self._loc_x = self._indent_level
    self._sendt( "In {}".format( func_name ))
      
  def outf(self, func_name):
    self._loc_x = self._indent_level
    self._sendt( "Out {}".format( func_name ))
    self._indent_level -= self._indent_dx

  def msg(self, msg_string):
    self._sendt(msg_string)
    
  def reset(self):
    self._index_level = -self._indent_dx
    self._loc_x = 0
    self._loc_y = 0
    self._scroll_is_on = True
    self._disp_wait = 0
    setup.clear_disp()
    setup.set_deep_print(False)
    
  def set_disp_pause(self, sec):
    self._disp_wait = sec
    setup.set_disp_pause(sec)
      
  def sleep(self):
    self._sleeping = True
      
  def wake(self):
    self._sleeping = False
      
      
      