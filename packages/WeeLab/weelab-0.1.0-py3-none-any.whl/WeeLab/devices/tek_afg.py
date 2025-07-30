from os import name
from WeeLab.connections.base import InstrumentConnection
from WeeLab.interfaces.wf_generator import WaveformGenerator

import logging


class Tektronix_AFG3252(WaveformGenerator):
    def __init__(self, conn: InstrumentConnection):
        self.conn = conn
        self.maxpoint = 131072
        self.maxrate = 2e9
        self.max_offset = 2.5
        self.min_offset = -2.5
        self.max_amplitude = 5.0
        self.min_amplitude = 0.05

        logging.debug(__name__ + " :  Get state of the channel 1 output on/off")

    def get_all(self):
        """
        Get all parameters of the intrument

        Input:
            None

        Output:
            None
        """
        logging.info(__name__ + " : get all")
        self.do_get_period_ch1()
        self.do_get_amplitude_ch1()
        self.do_get_offset_ch1()
        self.do_get_phase_ch1()
        self.do_get_status_ch1()
        self.do_get_ncycles_ch1()
        self.do_get_interval()
        self.do_get_reference()

    #########################################################
    #
    #
    #                       Interval between each pulse of the burst mode
    #
    #
    #########################################################

    def do_get_interval(self):
        """
        Get the interval between each cycle

        Input:
            None

        Output:
            interval (float) : The interval between each cycle
        """
        logging.debug(__name__ + " : Get the interval between each cycle")
        return float(self.conn.query("trigger:timer?"))

    def do_set_interval(self, interval=1.0):
        """
        Set the interval between each cycle

        Input:
            interval (float) : interval between each cycle [s]

        Output:
            None
        """
        logging.debug(
            __name__ + " : Set the interval between each cycle to %.6f" % (interval)
        )
        self.conn.write("trigger:timer " + str(interval) + "s")

    #########################################################
    #
    #
    #                       Number of cycle per period
    #
    #
    #########################################################

    def do_get_ncycles_ch1(self):
        """
        Get the number of cycle per period for the channel 1

        Input:
            None

        Output:
            ncycle (Int) : The number of cycle per period of the channel 1
        """
        logging.debug(
            __name__ + " : Get the number of cycle per period for the channel  1"
        )
        return float(self.conn.query("source1:burst:ncycles?"))

    def do_set_ncycles_ch1(self, ncycles=0):
        """
        Set the number of cycle for the channel 1

        Input:
            ncycle (Int) : Number if cycle per period

        Output:
            None
        """
        logging.debug(
            __name__
            + " : Set the number of cycle per period for channel  1 to %.6f" % (ncycles)
        )
        self.conn.write("source1:burst:ncycles " + str(int(ncycles)))

    #########################################################
    #
    #
    #                       Offset
    #
    #
    #########################################################

    def do_get_offset_ch1(self):
        """
        Get the offset for the channel 1

        Input:
            None

        Output:
            Offset (Float) : The offset of the channel 1 in Volts
        """
        logging.debug(__name__ + " : Get offset of channel  1")
        return float(self.conn.query("SOURCE1:VOLTAGE:LEVEL:IMMEDIATE:OFFSET?"))

    def do_set_offset_ch1(self, offset=0):
        """
        Set the offset for the channel 1 to a defined value

        Input:
            offset (float) : offset in Volts

        Output:
            None
        """
        logging.debug(__name__ + " : Set offset of channel  1 to %.6f" % (offset))
        self.conn.write("SOURCE1:VOLTAGE:LEVEL:IMMEDIATE:OFFSET %.6f" % (offset))

    #########################################################
    #
    #
    #                   Amplitude
    #
    #
    #########################################################

    def do_get_amplitude_ch1(self):
        """
        Get the amplitude for the channel 1

        Input:
            None

        Output:
            amplitude (Float) : The amplitude of the channel 1 in Volts, peak to peak
        """

        logging.debug(__name__ + " : Get amplitude of channel  1")

        return float(self.conn.query("source1:voltage:level:immediate:amplitude?"))

    def do_set_amplitude_ch1(self, amplitude=0.1):
        """
        Set the amplitude for the channel 1 to a defined value

        Input:
            amplitude (float) : amplitude in Volts, peak to peak

        Output:
            None
        """
        logging.debug(__name__ + " : Set amplitude of channel  1 to %.6f" % (amplitude))
        self.conn.write("source1:voltage:level:immediate:amplitude %.6f" % (amplitude))

    #########################################################
    #
    #
    #                   Phase
    #
    #
    #########################################################

    def do_get_phase_ch1(self):
        """
        Get the phase for the channel 1

        Input:
            None

        Output:
            phase (Float) : The phase of the channel 1 [rad]
        """
        logging.debug(__name__ + " : Get phase of channel  1")
        return float(self.conn.query("source1:phase?"))

    def do_set_phase_ch1(self, phase=0.0):
        """
        Set the phase for the channel 1 to a defined value

        Input:
            phase (float) : phase of the channel 1 [rad]

        Output:
            None
        """
        logging.debug(__name__ + " : Set phase of channel  1 to %.6f" % (phase))
        self.conn.write("source1:phase:adjust %.6f" % (phase))

    #########################################################
    #
    #
    #                   Frequency
    #
    #
    #########################################################

    def get_frequency_ch1(self):
        """
        Get the frequency for the channel 1

        Input:
            None

        Output:
            frequency (Float) : The frequency of the channel 1 in Hertz
        """
        logging.debug(__name__ + " : Get frequency of channel 1")
        return float(self.conn.query("source1:frequency?"))

    def set_frequency_ch1(self, frequency=1e6):
        """
        Set the frequency for the channel 1 to a defined value

        Input:
            frequency (float) : frequency in Hertz

        Output:
            None
        """
        logging.debug(
            __name__ + " : Set the frequency of channel  1 to %.6f" % (frequency)
        )
        self.conn.write("source1:frequency %.6f" % (frequency))

    #########################################################
    #
    #
    #                   Period
    #
    #
    #########################################################

    def do_get_period_ch1(self):
        """
        Get the period for the channel 1

        Input:
            None

        Output:
            period (Float) : The frequency of the channel 1 in Hertz
        """
        logging.debug(__name__ + " : Get period of channel 1")
        return float(self.conn.query("source1:pulse:period?"))

    def do_set_period_ch1(self, period=1):
        """
        Set the period for the channel 1 to a defined value

        Input:
            frequency (float) : period in Hertz

        Output:
            None
        """
        logging.debug(__name__ + " : Set the period of channel  1 to %.6f" % (period))
        self.conn.write("source1:pulse:period %.6f" % (period))

    #########################################################
    #
    #
    #                   Burst mode
    #
    #
    #########################################################

    def set_run_mode_burst_ch1(self):
        """
        Set the run mode for the channel 1 to burst mode

        Input:
            None

        Output:
            None
        """
        logging.debug(__name__ + " : Set the run mode for the channel 1 to burst mode")
        self.conn.write("source1:burst:state on")

    def set_burst_mode_triger_ch1(self):
        """
        Set the burst mode for the channel 1 to triger mode

        Input:
            None

        Output:
            None
        """
        logging.debug(__name__ + " : Set the burst mode for the channel 1 to triger mode")
        self.conn.write("source1:burst:mode trigered")

    def set_burst_mode_ncycle_ch1(self, number_cycle=1):
        """
        Set the number of cycle of the burst mode for the channel 1

        Input:
            number of cycle (int) : Number of cycle in burst mode
                - 0  : set the number of cycle to infinite count
                - !0 : set the number of cycle to defined value

        Output:
            None
        """

        if int(number_cycle) == 0:

            logging.debug(
                __name__
                + " : Set the number of cycle of the burst mode for the channel 1"
            )
            self.conn.write("source1:burst:ncycles infinity")
        else:

            logging.debug(
                __name__
                + " : Set the number of cycle of the burst mode for the channel 1"
            )
            self.conn.write("source1:burst:ncycles  %.6f" % (int(number_cycle)))

    #########################################################
    #
    #
    #                   Trigger
    #
    #
    #########################################################

    def set_triger_source_external(self):
        """
        Set the trigger to an external source

        Input:
            None

        Output:
            None
        """
        logging.debug(__name__ + " : Set the trigger to an external source")
        self.conn.write("trigger:sequence:source external")

    def set_triger_source_internal(self):
        """
        Set the trigger to an internal source

        Input:
            None

        Output:
            None
        """
        logging.debug(__name__ + " : Set the trigger to an internal source")
        self.conn.write("trigger:sequence:source timer")

    def send_triger_event(self):
        """
        Send a trigger event

        Input:
            None

        Output:
            None
        """
        logging.debug(__name__ + " : Send a trigger event")
        self.conn.write("trigger:sequence:immediate")

    #########################################################
    #
    #
    #                   Memory
    #
    #
    #########################################################

    def set_transfert_ememory_user1(self):
        """
        Set the transfert of the waveform present in the ememory to the user 1 to save it

        Input:
            None

        Output:
            None
        """
        logging.debug(
            __name__ + " : Set the transfert of the waveform present in the ememory"
        )
        self.conn.write("trace:copy user1,ememory")

    def set_function_user1_ch1(self):
        """
        Set the function of the channel 1 to user1

        Input:
            None

        Output:
            None
        """
        logging.debug(__name__ + " : Set the function of the channel 1 to user1")
        self.conn.write("source1:function user1")

    def set_arbitrary_waveform_memory_ch1(self):
        """
        Set the device to the arbitrary waveform menu for the channel 1

        Input:
            None

        Output:
            None
        """
        logging.debug(
            __name__
            + " : Set the device to the arbitrary waveform menu for the channel 1"
        )
        self.conn.write("source1:function ememory")

    ##################################################################
    #
    #
    #                   Status
    #
    #
    ##################################################################

    def do_set_status_ch1(self, state="off"):
        """
        Set channel 1 output on/off. By default off.

        Input:
            state (string) : switch on/off the channel

        Output:
            None
        """
        logging.debug(__name__ + " :  Set channel 1 output on/off")

        if state.lower() == "on":
            self.conn.write("output1:state 1")
        elif state.lower() == "off":
            self.conn.write("output1:state 0")
        else:
            logging.debug(__name__ + " : Status can only set on or off")
            return "Error : Status can only set on or off"

    def do_get_status_ch1(self):
        """
        Get the state of the channel 1 output on/off

        Input:
            state (string) : switch on/off the channel

        Output:
            None
        """
        logging.debug(__name__ + " :  Get state of the channel 1 output on/off")

        if self.conn.query("output1:state?") == "1":
            return "on"
        else:
            return "off"

    ##################################################################
    #
    #
    #                   reference
    #
    #
    ##################################################################

    def do_set_reference(self, val="external"):
        """
        Set the origin of the reference

        Input:
            val (string) : switch the clock on the external or internal reference

        Output:
            None
        """
        logging.debug(__name__ + " :  Set the clock")

        if val.lower() == "external" or val.lower() == "internal":
            self.conn.write("source:roscillator:source " + str(val))
        else:
            raise ValueError('The reference has to be either "Internal" or "external"')

    def do_get_reference(self):
        """
        Get the reference

        Input:
            None

        Output:
            state (string) : reference
        """
        logging.debug(__name__ + " :  Get the reference")
        return self.conn.query("source:roscillator:source?")
        # if self.conn.query('source:roscillator:source?') == 'EXT':
        #     return 'External'
        # else:
        #     return 'Internal'

    ###################################################################
    #
    #
    #                   Waveform
    #
    #
    ####################################################################

    def set_waveform_ch1(self, wave):
        """
        Sends a complete waveform.

        Input:
            w (float[numpoints]) : waveform in V

        Output:
            None
        """
        logging.debug(__name__ + " : set waveform")

        # We check if the waveform if no to long
        if len(wave) > self.maxpoint or len(wave) < 2:

            logging.debug(
                __name__ + " :The waveform is too long or too short (number of points)."
            )
            return "Errors : The waveform is too long or too short (number of points)."

        # We check if the waveform is feasible
        if (
            max(wave) > self.max_amplitude / 2 + self.max_offset
            or min(wave) < -self.max_amplitude / 2 - self.max_offset
            or max(wave) - min(wave) > self.max_amplitude
        ):

            logging.debug(__name__ + " : The waveform is out of the range.")
            return "Errors : The waveform is out of the range."

        # We calculate the amplitude and the offset of the tektro
        amplitude = max(wave) - min(wave)
        offset = (max(wave) + min(wave)) / 2

        # We tune these values
        self.set_amplitude_ch1(amplitude)
        self.set_offset_ch1(offset)

        # We transform all points of the waveforme which are in V in bytes
        wave_bytes = ""
        for i in wave:

            # First we tranform V into bins
            j = int(((i + abs(min(wave))) * (2**14 - 1)) / amplitude)

            wave_bytes = wave_bytes + struct.pack(">H", j)

        # We research the beginning of the message for the tektro
        number_bytes = int(len(wave)) * 2
        number_digits = len(str(number_bytes))

        # We create the final message for the device
        mes = "trace ememory,#" + str(number_digits) + str(number_bytes) + wave_bytes

        # we prepare the device to be configured
        self.set_arbitrary_waveform_memory_ch1()
        self.conn.write(mes)

    def do_set_function_ch1(self, function="sin"):
        """
        Set the function of the channel 1

        Input:
            function (string) : function of the channel 1

        Output:
            None
        """
        logging.debug(__name__ + " : Set the function of the channel 1")
        self.conn.write("source1:function " + str(function))

    def do_set_width_ch1(self, width=0.5):
        """
        Set the duty cycle of the pulse

        Input:
            duty_cycle (float) : duty cycle in seconds

        Output:
            None
        """
        logging.debug(__name__ + " : Set the duty cycle of the pulse")
        self.conn.write(f"SOURce1:PULSe:hold width")
        self.conn.write(f"SOURce1:PULSe:width {width}ns")

    def do_set_high_level(self, level=0.5):
        """
        Set the high level of the pulse

        Input:
            level (float) : high level in seconds

        Output:
            None
        """
        logging.debug(__name__ + " : Set the high level of the pulse")
        assert level >= 0, "Level must be non-negative"
        assert level <= 5, "Level must be less than or equal to 5"
        self.conn.write(f"SOURce1:voltage:level:HIGH {level}")

    def do_set_level_low(self, level=0.5):
        """
        Set the low level of the pulse

        Input:
            level (float) : low level in seconds

        Output:
            None
        """
        logging.debug(__name__ + " : Set the low level of the pulse")
        assert level >= 0, "Level must be non-negative"
        assert level <= 5, "Level must be less than or equal to 5"
        self.conn.write(f"SOURce1:voltage:level:LOW {level}")

    def do_set_voltage_ch1(self, voltage=0.5):
        """
        Set the voltage of the channel 1

        Input:
            voltage (float) : voltage of the channel 1

        Output:
            None
        """
        logging.debug(__name__ + " : Set the voltage of the channel 1")
        self.conn.write(f"SOURce1:voltage:level:IMMediate:HIGH {voltage}")
        self.conn.write(f"SOURce1:voltage:level:IMMediate:LOW {0}")

    def do_set_delay_ch1(self, delay=20):
        """
        Set the delay of the pulse

        Input:
            delay (float) : delay in seconds

        Output:
            None
        """
        logging.debug(__name__ + " : Set the delay of the pulse")
        self.conn.write(f"SOURce1:PULSe:DELay {delay}ns")


import pyvisa
import types
import logging
from numpy import pi
import struct
import time


# class Instrument:
#     def __init__(self, name, tags=None):
#         self.name = name
#         self.tags = tags if tags is not None else []
#         self.conn = None
#         self.parameters = {}
#         pass

#     def add_parameter(self, name, flags, units, minval, maxval, type):
#         self.parameters[name] = {
#             "flags": flags,
#             "units": units,
#             "minval": minval,
#             "maxval": maxval,
#             "type": type,
#         }

#     def get_all(self):
#         """
#         Get all parameters of the intrument

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.info(__name__ + " : get all")
#         self.do_get_period_ch1()
#         self.do_get_amplitude_ch1()
#         self.do_get_offset_ch1()
#         self.do_get_phase_ch1()
#         self.do_get_status_ch1()
#         self.do_get_ncycles_ch1()
#         self.do_get_interval()
#         self.do_get_reference()


# class Tektronix_AFG3252_old(Instrument):
#     """
#     This is the python driver for the Tektronix AFG3252
#     Arbitrary Waveform Generator

#     Usage:
#     Initialize with
#     <name> = instruments.create('name', 'Tektronix_AFG3252', address='<GPIB address>')
#     """

#     def __init__(self, name, address, reset=False):  # , clock=1e9, numpoints=1000):
#         """
#         Initializes the AFG3252.

#         Input:
#             name (string)    : name of the instrument
#             address (string) : GPIB address
#             reset (bool)     : resets to default values, default=false

#         Output:
#             None
#         """

#         logging.debug(__name__ + " : Initializing instrument")
#         Instrument.__init__(self, name, tags=["physical"])
#         rm = pyvisa.ResourceManager()

#         self._address = address
#         try:
#             self._visainstrument = rm.open_resource(self._address)
#         except:
#             raise SystemExit

#         # self.add_parameter('period_ch1', flags=Instrument.FLAG_GETSET, units='s', minval=16.67e-9, maxval=1e3, type=types.FloatType)
#         # self.add_parameter('amplitude_ch1', flags=Instrument.FLAG_GETSET, units='V', minval=0.05, maxval=5.0, type=types.FloatType)
#         # self.add_parameter('offset_ch1', flags=Instrument.FLAG_GETSET, units='V', minval=-2.5, maxval=2.5, type=types.FloatType)
#         # self.add_parameter('phase_ch1', flags=Instrument.FLAG_GETSET, units='rad', minval=-pi, maxval=pi, type=types.FloatType)
#         # self.add_parameter('status_ch1', option_list=('off', 'on'), flags=Instrument.FLAG_GETSET, type=types.StringType)
#         # self.add_parameter('ncycles_ch1', minval=1, maxval= 1000000, flags=Instrument.FLAG_GETSET, type=types.IntType)
#         # self.add_parameter('interval', minval=1e-3, maxval= 500, units='s', flags=Instrument.FLAG_GETSET, type=types.FloatType)
#         # self.add_parameter('reference', option_list=['Internal', 'External'], flags=Instrument.FLAG_GETSET, type=types.StringType)

#         #        self.add_function('get_all')
#         # self.add_function('reset')

#         self.maxpoint = 131072
#         self.maxrate = 2e9

#         self.max_offset = 2.5
#         self.min_offset = -2.5

#         self.max_amplitude = 5.0
#         self.min_amplitude = 0.05

#         if reset:

#             self.reset()

#         self.get_all()

#     # Functions
#     def reset(self):
#         """
#         Resets the instrument to default values

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.info(__name__ + " : Reset the instrument")
#         self._visainstrument.write("*RST")

#     def get_all(self):
#         """
#         Get all parameters of the intrument

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.info(__name__ + " : get all")
#         self.do_get_period_ch1()
#         self.do_get_amplitude_ch1()
#         self.do_get_offset_ch1()
#         self.do_get_phase_ch1()
#         self.do_get_status_ch1()
#         self.do_get_ncycles_ch1()
#         self.do_get_interval()
#         self.do_get_reference()

#     def get_maxpoint(self):
#         """
#         Return the max number of point that the tektro can handle

#         Input:
#             None

#         Output:
#             maxpoint (int) : the max number of point that the tektro can handle
#         """

#         return self.maxpoint

#     def get_maxrate(self):
#         """
#         Return the maw rate of the tektro

#         Input:
#             None

#         Output:
#             maxrate (int) : the max rate of the tektro
#         """

#         return self.maxrate

#     #########################################################
#     #
#     #
#     #                       Interval between each pulse of the burst mode
#     #
#     #
#     #########################################################

#     def do_get_interval(self):
#         """
#         Get the interval between each cycle

#         Input:
#             None

#         Output:
#             interval (float) : The interval between each cycle
#         """
#         logging.debug(__name__ + " : Get the interval between each cycle")
#         return float(self._visainstrument.query("trigger:timer?"))

#     def do_set_interval(self, interval=1.0):
#         """
#         Set the interval between each cycle

#         Input:
#             interval (float) : interval between each cycle [s]

#         Output:
#             None
#         """
#         logging.debug(
#             __name__ + " : Set the interval between each cycle to %.6f" % (interval)
#         )
#         self._visainstrument.write("trigger:timer " + str(interval) + "s")

#     #########################################################
#     #
#     #
#     #                       Number of cycle per period
#     #
#     #
#     #########################################################

#     def do_get_ncycles_ch1(self):
#         """
#         Get the number of cycle per period for the channel 1

#         Input:
#             None

#         Output:
#             ncycle (Int) : The number of cycle per period of the channel 1
#         """
#         logging.debug(
#             __name__ + " : Get the number of cycle per period for the channel  1"
#         )
#         return float(self._visainstrument.query("source1:burst:ncycles?"))

#     def do_set_ncycles_ch1(self, ncycles=0):
#         """
#         Set the number of cycle for the channel 1

#         Input:
#             ncycle (Int) : Number if cycle per period

#         Output:
#             None
#         """
#         logging.debug(
#             __name__
#             + " : Set the number of cycle per period for channel  1 to %.6f" % (ncycles)
#         )
#         self._visainstrument.write("source1:burst:ncycles " + str(int(ncycles)))

#     #########################################################
#     #
#     #
#     #                       Offset
#     #
#     #
#     #########################################################

#     def do_get_offset_ch1(self):
#         """
#         Get the offset for the channel 1

#         Input:
#             None

#         Output:
#             Offset (Float) : The offset of the channel 1 in Volts
#         """
#         logging.debug(__name__ + " : Get offset of channel  1")
#         return float(
#             self._visainstrument.query("SOURCE1:VOLTAGE:LEVEL:IMMEDIATE:OFFSET?")
#         )

#     def do_set_offset_ch1(self, offset=0):
#         """
#         Set the offset for the channel 1 to a defined value

#         Input:
#             offset (float) : offset in Volts

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set offset of channel  1 to %.6f" % (offset))
#         self._visainstrument.write(
#             "SOURCE1:VOLTAGE:LEVEL:IMMEDIATE:OFFSET %.6f" % (offset)
#         )

#     #########################################################
#     #
#     #
#     #                   Amplitude
#     #
#     #
#     #########################################################

#     def do_get_amplitude_ch1(self):
#         """
#         Get the amplitude for the channel 1

#         Input:
#             None

#         Output:
#             amplitude (Float) : The amplitude of the channel 1 in Volts, peak to peak
#         """

#         logging.debug(__name__ + " : Get amplitude of channel  1")

#         return float(
#             self._visainstrument.query("source1:voltage:level:immediate:amplitude?")
#         )

#     def do_set_amplitude_ch1(self, amplitude=0.1):
#         """
#         Set the amplitude for the channel 1 to a defined value

#         Input:
#             amplitude (float) : amplitude in Volts, peak to peak

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set amplitude of channel  1 to %.6f" % (amplitude))
#         self._visainstrument.write(
#             "source1:voltage:level:immediate:amplitude %.6f" % (amplitude)
#         )

#     #########################################################
#     #
#     #
#     #                   Phase
#     #
#     #
#     #########################################################

#     def do_get_phase_ch1(self):
#         """
#         Get the phase for the channel 1

#         Input:
#             None

#         Output:
#             phase (Float) : The phase of the channel 1 [rad]
#         """
#         logging.debug(__name__ + " : Get phase of channel  1")
#         return float(self._visainstrument.query("source1:phase?"))

#     def do_set_phase_ch1(self, phase=0.0):
#         """
#         Set the phase for the channel 1 to a defined value

#         Input:
#             phase (float) : phase of the channel 1 [rad]

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set phase of channel  1 to %.6f" % (phase))
#         self._visainstrument.write("source1:phase:adjust %.6f" % (phase))

#     #########################################################
#     #
#     #
#     #                   Frequency
#     #
#     #
#     #########################################################

#     def get_frequency_ch1(self):
#         """
#         Get the frequency for the channel 1

#         Input:
#             None

#         Output:
#             frequency (Float) : The frequency of the channel 1 in Hertz
#         """
#         logging.debug(__name__ + " : Get frequency of channel 1")
#         return float(self._visainstrument.query("source1:frequency?"))

#     def set_frequency_ch1(self, frequency=1e6):
#         """
#         Set the frequency for the channel 1 to a defined value

#         Input:
#             frequency (float) : frequency in Hertz

#         Output:
#             None
#         """
#         logging.debug(
#             __name__ + " : Set the frequency of channel  1 to %.6f" % (frequency)
#         )
#         self._visainstrument.write("source1:frequency %.6f" % (frequency))

#     #########################################################
#     #
#     #
#     #                   Period
#     #
#     #
#     #########################################################

#     def do_get_period_ch1(self):
#         """
#         Get the period for the channel 1

#         Input:
#             None

#         Output:
#             period (Float) : The frequency of the channel 1 in Hertz
#         """
#         logging.debug(__name__ + " : Get period of channel 1")
#         return float(self._visainstrument.query("source1:pulse:period?"))

#     def do_set_period_ch1(self, period=1):
#         """
#         Set the period for the channel 1 to a defined value

#         Input:
#             frequency (float) : period in Hertz

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the period of channel  1 to %.6f" % (period))
#         self._visainstrument.write("source1:pulse:period %.6f" % (period))

#     #########################################################
#     #
#     #
#     #                   Burst mode
#     #
#     #
#     #########################################################

#     def set_run_mode_burst_ch1(self):
#         """
#         Set the run mode for the channel 1 to burst mode

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the run mode for the channel 1 to burst mode")
#         self._visainstrument.write("source1:burst:state on")

#     def set_burst_mode_triger_ch1(self):
#         """
#         Set the burst mode for the channel 1 to triger mode

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the burst mode for the channel 1 to triger mode")
#         self._visainstrument.write("source1:burst:mode trigered")

#     def set_burst_mode_ncycle_ch1(self, number_cycle=1):
#         """
#         Set the number of cycle of the burst mode for the channel 1

#         Input:
#             number of cycle (int) : Number of cycle in burst mode
#                 - 0  : set the number of cycle to infinite count
#                 - !0 : set the number of cycle to defined value

#         Output:
#             None
#         """

#         if int(number_cycle) == 0:

#             logging.debug(
#                 __name__
#                 + " : Set the number of cycle of the burst mode for the channel 1"
#             )
#             self._visainstrument.write("source1:burst:ncycles infinity")
#         else:

#             logging.debug(
#                 __name__
#                 + " : Set the number of cycle of the burst mode for the channel 1"
#             )
#             self._visainstrument.write(
#                 "source1:burst:ncycles  %.6f" % (int(number_cycle))
#             )

#     #########################################################
#     #
#     #
#     #                   Trigger
#     #
#     #
#     #########################################################

#     def set_triger_source_external(self):
#         """
#         Set the trigger to an external source

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the trigger to an external source")
#         self._visainstrument.write("trigger:sequence:source external")

#     def set_triger_source_internal(self):
#         """
#         Set the trigger to an internal source

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the trigger to an internal source")
#         self._visainstrument.write("trigger:sequence:source timer")

#     def send_triger_event(self):
#         """
#         Send a trigger event

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Send a trigger event")
#         self._visainstrument.write("trigger:sequence:immediate")

#     #########################################################
#     #
#     #
#     #                   Memory
#     #
#     #
#     #########################################################

#     def set_transfert_ememory_user1(self):
#         """
#         Set the transfert of the waveform present in the ememory to the user 1 to save it

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.debug(
#             __name__ + " : Set the transfert of the waveform present in the ememory"
#         )
#         self._visainstrument.write("trace:copy user1,ememory")

#     def set_function_user1_ch1(self):
#         """
#         Set the function of the channel 1 to user1

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the function of the channel 1 to user1")
#         self._visainstrument.write("source1:function user1")

#     def set_arbitrary_waveform_memory_ch1(self):
#         """
#         Set the device to the arbitrary waveform menu for the channel 1

#         Input:
#             None

#         Output:
#             None
#         """
#         logging.debug(
#             __name__
#             + " : Set the device to the arbitrary waveform menu for the channel 1"
#         )
#         self._visainstrument.write("source1:function ememory")

#     ##################################################################
#     #
#     #
#     #                   Status
#     #
#     #
#     ##################################################################

#     def do_set_status_ch1(self, state="off"):
#         """
#         Set channel 1 output on/off. By default off.

#         Input:
#             state (string) : switch on/off the channel

#         Output:
#             None
#         """
#         logging.debug(__name__ + " :  Set channel 1 output on/off")

#         if state.lower() == "on":
#             self._visainstrument.write("output1:state 1")
#         elif state.lower() == "off":
#             self._visainstrument.write("output1:state 0")
#         else:
#             logging.debug(__name__ + " : Status can only set on or off")
#             return "Error : Status can only set on or off"

#     def do_get_status_ch1(self):
#         """
#         Get the state of the channel 1 output on/off

#         Input:
#             state (string) : switch on/off the channel

#         Output:
#             None
#         """
#         logging.debug(__name__ + " :  Get state of the channel 1 output on/off")

#         if self._visainstrument.query("output1:state?") == "1":
#             return "on"
#         else:
#             return "off"

#     ##################################################################
#     #
#     #
#     #                   reference
#     #
#     #
#     ##################################################################

#     def do_set_reference(self, val="external"):
#         """
#         Set the origin of the reference

#         Input:
#             val (string) : switch the clock on the external or internal reference

#         Output:
#             None
#         """
#         logging.debug(__name__ + " :  Set the clock")

#         if val.lower() == "external" or val.lower() == "internal":
#             self._visainstrument.write("source:roscillator:source " + str(val))
#         else:
#             raise ValueError('The reference has to be either "Internal" or "external"')

#     def do_get_reference(self):
#         """
#         Get the reference

#         Input:
#             None

#         Output:
#             state (string) : reference
#         """
#         logging.debug(__name__ + " :  Get the reference")
#         return self._visainstrument.query("source:roscillator:source?")
#         # if self._visainstrument.query('source:roscillator:source?') == 'EXT':
#         #     return 'External'
#         # else:
#         #     return 'Internal'

#     ###################################################################
#     #
#     #
#     #                   Waveform
#     #
#     #
#     ####################################################################

#     def set_waveform_ch1(self, wave):
#         """
#         Sends a complete waveform.

#         Input:
#             w (float[numpoints]) : waveform in V

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : set waveform")

#         # We check if the waveform if no to long
#         if len(wave) > self.maxpoint or len(wave) < 2:

#             logging.debug(
#                 __name__ + " :The waveform is too long or too short (number of points)."
#             )
#             return "Errors : The waveform is too long or too short (number of points)."

#         # We check if the waveform is feasible
#         if (
#             max(wave) > self.max_amplitude / 2 + self.max_offset
#             or min(wave) < -self.max_amplitude / 2 - self.max_offset
#             or max(wave) - min(wave) > self.max_amplitude
#         ):

#             logging.debug(__name__ + " : The waveform is out of the range.")
#             return "Errors : The waveform is out of the range."

#         # We calculate the amplitude and the offset of the tektro
#         amplitude = max(wave) - min(wave)
#         offset = (max(wave) + min(wave)) / 2

#         # We tune these values
#         self.set_amplitude_ch1(amplitude)
#         self.set_offset_ch1(offset)

#         # We transform all points of the waveforme which are in V in bytes
#         wave_bytes = ""
#         for i in wave:

#             # First we tranform V into bins
#             j = int(((i + abs(min(wave))) * (2**14 - 1)) / amplitude)

#             wave_bytes = wave_bytes + struct.pack(">H", j)

#         # We research the beginning of the message for the tektro
#         number_bytes = int(len(wave)) * 2
#         number_digits = len(str(number_bytes))

#         # We create the final message for the device
#         mes = "trace ememory,#" + str(number_digits) + str(number_bytes) + wave_bytes

#         # we prepare the device to be configured
#         self.set_arbitrary_waveform_memory_ch1()
#         self._visainstrument.write(mes)

#     def do_set_function_ch1(self, function="sin"):
#         """
#         Set the function of the channel 1

#         Input:
#             function (string) : function of the channel 1

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the function of the channel 1")
#         self._visainstrument.write("source1:function " + str(function))

#     def do_set_width_ch1(self, width=0.5):
#         """
#         Set the duty cycle of the pulse

#         Input:
#             duty_cycle (float) : duty cycle in seconds

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the duty cycle of the pulse")
#         self._visainstrument.write(f"SOURce1:PULSe:hold width")
#         self._visainstrument.write(f"SOURce1:PULSe:width {width}ns")

#     def do_set_high_level(self, level=0.5):
#         """
#         Set the high level of the pulse

#         Input:
#             level (float) : high level in seconds

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the high level of the pulse")
#         assert level >= 0, "Level must be non-negative"
#         assert level <= 5, "Level must be less than or equal to 5"
#         self._visainstrument.write(f"SOURce1:voltage:level:HIGH {level}")

#     def do_set_level_low(self, level=0.5):
#         """
#         Set the low level of the pulse

#         Input:
#             level (float) : low level in seconds

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the low level of the pulse")
#         assert level >= 0, "Level must be non-negative"
#         assert level <= 5, "Level must be less than or equal to 5"
#         self._visainstrument.write(f"SOURce1:voltage:level:LOW {level}")

#     def do_set_voltage_ch1(self, voltage=0.5):
#         """
#         Set the voltage of the channel 1

#         Input:
#             voltage (float) : voltage of the channel 1

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the voltage of the channel 1")
#         self._visainstrument.write(f"SOURce1:voltage:level:IMMediate:HIGH {voltage}")
#         self._visainstrument.write(f"SOURce1:voltage:level:IMMediate:LOW {0}")

#     def do_set_delay_ch1(self, delay=20):
#         """
#         Set the delay of the pulse

#         Input:
#             delay (float) : delay in seconds

#         Output:
#             None
#         """
#         logging.debug(__name__ + " : Set the delay of the pulse")
#         self._visainstrument.write(f"SOURce1:PULSe:DELay {delay}ns")
