"""This is a Hello-World example for communicating with your RTB2004 instrument.
The field 'Alias' defines the variable name with which 
you are going to address the instrument in your python scripts.
For the RTB2004, the alias is 'rtb'
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *

# Initialize the session
rtb = RsInstrument('TCPIP::192.168.178.32::INSTR', reset=False, options='AddTermCharToWriteBinData = ON, DataChunkSize = 100000')

rtb.write('*RST')
idn = rtb.query('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'Instrument installed options: {",".join(rtb.instrument_options)}')

# Enter your code here...
# resp = rtb.query('*IDN?')

# Close the session
rtb.close()
