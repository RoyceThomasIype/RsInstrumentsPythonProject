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
    rtb.visa_timeout = 10000  # Timeout for VISA Read Operations
    rtb.opc_timeout = 15000  # Timeout for opc-synchronised operations
    rtb.instrument_status_checking = True  # Error check after each command
except Exception as ex:
    print('Error initializing the instrument session:\n' + ex.args[0])
    exit()

print(f'RTB2000 IDN: {rtb.idn_string}')
print(f'RTB2000 Options: {",".join(rtb.instrument_options)}')

rtb.clear_status()
rtb.reset()

# -----------------------------------------------------------
# Basic Settings:
# ---------------------------- -------------------------------
rtb.write_str("TIM:ACQT 0.01")  # 10ms Acquisition time
rtb.write_str("CHAN1:RANG 10.0")  # Horizontal range 10V (1V/div)
rtb.write_str("TIMebase:SCALe 0.1")  # Horizontal Time scale 100ms
rtb.write_str("CHAN1:OFFS 0.0")  # Offset 0
rtb.write_str("CHAN1:COUP ACL")  # Coupling AC 1MOhm
rtb.write_str("CHAN1:STAT ON")  # Switch Channel 1 ON

# Set up the measurement
rtb.write_str("ACQuire:MODE RTIMe")  # Set the acquisition mode to Real-Time
# -----------------------------------------------------------
# Trigger Settings:
# -----------------------------------------------------------
rtb.write_str("TRIG:A:MODE NORM")  # Trigger Auto mode in case of no signal is applied
rtb.write_str("TRIG:A:TYPE EDGE;:TRIG:A:EDGE:SLOP POS")  # Trigger type Edge Positive
rtb.write_str("TRIG:A:SOUR CH1")  # Trigger source CH1
rtb.write_str("TRIG:A:LEV1 1.50")  # Trigger level 1.5V
rtb.write_str("TCOunter:ENABle ON")  # Enable Trigger counter
rtb.write_str("TCOunter:SOURce CH1")  # TCounter source CH1
rtb.query_opc()  # Using *OPC? query waits until all the instrument settings are finished

# Trigger the oscilloscope to start the measurement
rtb.write_str("ACQuire:STATe RUN")

# Wait for the acquisition to complete
rtb.query_str("*OPC?")

# Actions on Trigger Settings:
rtb.write_str("TRIGger:EVENt:ENABle ON")  # Enable the Trigger events
rtb.write_str("TRIGger:EVENt:SOUNd ON")  # Turn ON Sound on trigger
rtb.write_str("TRIGger:EVENt:SCRSave ON")  # Enable Take screenshot on trigger
rtb.write_str("TRIGger:EVENt:SCRSave:DESTination '/USB_FRONT/PIX'")  # Set destination path to USB
rtb.write_str("HCOP:COL:SCH COL")  # Screenshot colour scheme set to Colour/Gray scale
rtb.write_str("HCOP:FORMat PNG")  # File format - png

# Read the trigger count
trigger_count = rtb.query_str("TCOunter:RESult:ACTual:FREQuency?")
print("Trigger Count frequency:", trigger_count)

# Close the session
rtb.close()