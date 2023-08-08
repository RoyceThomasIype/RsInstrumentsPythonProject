"""The field 'Alias' defines the variable name with which
you are going to address the instrument in your python scripts.
For the RTB2004, the alias is 'rtb'
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.53.0')
rtb = None
try:
    # Adjust the VISA Resource string to fit your instrument
    rtb = RsInstrument('TCPIP::192.168.178.32::INSTR', True, False)
    rtb.visa_timeout = 3000  # Timeout for VISA Read Operations
    rtb.opc_timeout = 15000  # Timeout for opc-synchronised operations
    rtb.instrument_status_checking = True  # Error check after each command
except Exception as ex:
    print('Error initializing the instrument session:\n' + ex.args[0])
    exit()

print(f'RTB2000 IDN: {rtb.idn_string}')
print(f'RTB2000 Options: {",".join(rtb.instrument_options)}')

rtb.clear_status()
rtb.reset()

# Set up the measurement
#rtb.write_str(":TIMebase:MODE MAIN")  # Set the timebase mode to Main
rtb.write_str("ACQuire:MODE RTIMe")  # Set the acquisition mode to Real-Time

# -----------------------------------------------------------
# Trigger Settings:
# -----------------------------------------------------------
rtb.write_str("TRIG:A:MODE NORM")  # Trigger Auto mode in case of no signal is applied
rtb.write_str("TRIG:A:TYPE EDGE;:TRIG:A:EDGE:SLOP POS")  # Trigger type Edge Positive
rtb.write_str("TRIG:A:SOUR CH1")  # Trigger source CH1
rtb.write_str("TRIG:A:LEV1 1.00")  # Trigger level 0.05V
rtb.query_opc()  # Using *OPC? query waits until all the instrument settings are finished

# Enable the trigger count
rtb.write_str("MEASure:COUNt:STATe ON")

# Trigger the oscilloscope to start the measurement
rtb.write_str("SINGle")

# Wait for the acquisition to complete
rtb.query_str("*OPC?")

# Read the trigger count
trigger_count = rtb.query_str(":MEASure:COUNt:VALue?")
print("Trigger Count:", trigger_count)

# Close the session
rtb.close()
