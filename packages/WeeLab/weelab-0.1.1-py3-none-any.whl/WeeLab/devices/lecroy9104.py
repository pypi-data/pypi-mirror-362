import time
from WeeLab.connections.base import InstrumentConnection
from WeeLab.interfaces.oscilloscope import Oscilloscope

import os


class LeCroyWaveRunner(Oscilloscope):
    def __init__(self, conn: InstrumentConnection):
        self.conn = conn

    def clear_sweeps(self):
        self.conn.write(r"""vbs 'app.clearsweeps' """)

    def save_insitu_waveforms(self):
        self.conn.query(r"""vbs 'app.SaveRecall.Waveform.SaveFile' """)

    def get_waveforms(self, output_folder, filename):
        self.conn.write("TRMD STOP")

        # method 2 in 1 step
        deltaT_suffix = "F1"
        LG_sh_amplitude_master_suffix = "F3"
        LG_sh_amplitude_slave_suffix = "F2"
        TOT_width_master_suffix = "F4"
        TOT_width_slave_suffix = "F5"
        file_start_index = 12
        file_stop_index = -1
        index_step = 14
        trace_list = [
            deltaT_suffix,
            LG_sh_amplitude_master_suffix,
            LG_sh_amplitude_slave_suffix,
            TOT_width_master_suffix,
            TOT_width_slave_suffix,
        ]

        trace_data_list = []
        for trace in trace_list:
            trace_data_list.append(
                self.conn.query(trace + ":INSP? 'DATA_ARRAY_2',FLOAT").replace("\r\n", "")
            )  # truncate header and footer

            # trace_data_list.append(scopeLecroy.oscillo.query(trace + ":INSP? 'DATA_ARRAY_2',FLOAT")
            #             .replace("\r\n", '')[file_start_index:file_stop_index]  # truncate header and footer
            #             .replace('   ', '\n').replace('  ', '\n'))  # deal with spaces for + and - float

        events_number = int((len(trace_data_list[0]) - 10) / 14)
        # all col have the same events_number since trend mode = average and scope stopped between data fetches "

        # csv_file = ','.join([f'{trace=}'.split('=')[0] for trace in trace_list])
        csv_file = "deltaT,LG_sh_amplitude_master,LG_sh_amplitude_slave,TOT_width_master,TOT_width_slave\n"
        for i in range(events_number):
            for ti, trace in enumerate(trace_data_list):
                csv_file += trace[12 + i * 14 : 10 + 13 + i * 14]
                if ti != len(trace_data_list) - 1:
                    csv_file += ","
                else:
                    csv_file += "\n"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        with open(output_folder + filename, "w") as text_file:
            text_file.write(csv_file)

        text_file.close()

        pass
        self.conn.write("TRMD NORM")

        # method 1 in 2 steps
        # scopeLecroy.oscillo.query("STO ALL_DISPLAYED,FILE")
        # for trace in trace_list:
        #     with open(trace+output_file, "w") as text_file:
        # scopeLecroy.oscillo.query("TRFL? DISK,HDD,FILE,'D:\\file.txt'")

        # method 3
        # to get byte to save and recall, not to read
        # scopeLecroy.oscillo.ask_raw(str("CHDR SHORT; C1:WaveForm?").encode("utf-8"))

    def getMeasure(self, channel: int, measureType: str, exponent=0):
        """
        Get the measure value from the oscilloscope.
        :param channel: Channel number (1, 2, 3, or 4)
        :param measureType: Type of measure to retrieve (e.g., "mean", "sdev", "num")
        :param exponent: Exponent to apply to the measure value (default is 0)

        :return: The measure value as a float
        """
        validMeasureType = {"mean", "sdev", "num", "min", "max"}
        measureType = measureType.lower()
        if measureType not in validMeasureType:
            raise ValueError(
                "Lecroy measure function call has received a wrong measure type :"
                + str(measureType)
            )
        stringAnswer = self.conn.query(
            f"""vbs? 'return=app.measure.p{channel}.{measureType}.result.value' """
        )
        try:
            # val = float(stringAnswer.split()[1]) * 10 ** exponent
            val = float(stringAnswer.split()[1])
        except:
            val = 0

        # val = '%.3f' % val
        return val

    def getSetupChannel(self, channel):
        return self.conn.query("C" + str(channel) + ":PAVA?")

    def getSetupMeasure(self, measureNumber):
        return self.conn.query("PACU? " + str(measureNumber))

    def setTimebase(self, time):  # unit : second
        self.conn.write(
            r"""vbs? 'app.Acquisition.Horizontal.HorScale = {:.0e}' """.format(time)
        )

    def write(self, measure):
        self.conn.write(measure)

    def query(self, measure):
        return self.conn.query(measure)

    def read(self):
        return self.conn.read()

    def save_setup(self, filepath):
        self.conn.write("*SAV 2")
        setup = self.conn.query("PANEL_SETUP?")
        output_folder = os.path.dirname(filepath)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        with open(filepath, "w") as text_file:
            text_file.write(setup)
        text_file.close()

    def load_setup(self, filepath):
        with open(filepath, "r") as text_file:
            read_setup = text_file.read()
        text_file.close()
        self.conn.write(read_setup)
        self.conn.write("*RCL 2")

    def query_float(self, command):
        """
        Query the oscilloscope for a float value using a VBS command.
        :param command: The VBS command to execute
        :return: The float value read from the oscilloscope
        """
        self.write(command)
        try:
            return float(self.read().split()[-1])
        except:
            time.sleep(1)
            return self.query_float(command)

    def find_scale(self, channel):
        """
        Find the vertical scale for a given channel.
        :param channel: Channel number (1, 2, 3, or 4)
        :return: The scale value as a float
        """
        self.write(f"VBS app.Acquisition.C{channel}.FindScale")

    def find_scale_man(self, pos=False, channel=1, pkpk_channel=2):
        """
        Find the vertical scale and offset for a given channel based on the peak-to-peak amplitude.
        :param pos: If True, assumes a positive signal, otherwise assumes a negative signal (default is False)
        :param channel: Channel number to set the scale and offset for (default is 1)
        :param pkpk_channel: Channel number to measure the peak-to-peak amplitude from (default is 2)
        """
        self.find_scale(channel=channel)
        self.clear_sweeps()
        time.sleep(3)
        ampl = self.query_float(
            f"VBS? 'return=app.Measure.P{pkpk_channel}.Mean.Result.Value"
        )
        if pos:
            sign = -1
        else:
            sign = 1

        if ampl < 0.01:
            scale = abs(ampl) / 2
            self.write(f"VBS app.Acquisition.C{channel}.VerScale = {scale}")
            scale = self.query_float(f"VBS? 'return=app.Acquisition.C{channel}.VerScale")
            offset = sign * 2 * scale
            self.write(f"VBS app.Acquisition.C{channel}.VerOffset = {offset}")
            # print(f"Signal amplitude {ampl}: set scale to {scale} and offset to {offset}")
        else:
            scale = abs(ampl) / 4
            self.write(f"VBS app.Acquisition.C{channel}.VerScale = {scale}")
            scale = self.query_float(f"VBS? 'return=app.Acquisition.C{channel}.VerScale")
            offset = sign * 3 * scale
            self.write(f"VBS app.Acquisition.C{channel}.VerOffset = {offset}")
            # print(f"Signal amplitude {ampl}: set scale to {scale} and offset to {offset}")

    def print_id(self):
        """
        Print the ID of the oscilloscope.
        """
        idn = self.conn.query("*IDN?")
        print(idn)
