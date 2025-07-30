# -*- coding: utf-8 -*-

"""package ad9xdds
author    Benoit Dubois
copyright FEMTO ENGINEERING, 2020
license   GPL v3.0+
brief     API to control AD9915 DDS development board from BBB.
details   AD9915 development board is configurable from Beagle Bone Black.
          Class allows configuration of principle DDS parameters (frequency,
          phase, amplitude, PLL handling, output handling...).

Beagle Bone Black cable connection:
    BBB                           AD9915 Dev Board
    P9_1 | P9_2     <-------------->  GND
    P9_17 (GPIO_4)  <-------------->  MPI00 (CSB)
    P9_22 (GPIO_2)  <-------------->  MPI01 (SCLK)
    P9_18 (GPIO_5)  <-------------->  MPI02 (SDIO)
    P9_21 (GPIO_3)  <-------------->  MPI03 (SDO)
    P9_15 (GPIO_48) <-------------->  IO_UPDATE (GPLIO0)
    P9_16 (GPIO_51) <-------------->  RESET_BUFF (GPLIO1)

    Profile selection (currently not implemented)
    PS0-BUF <---> GND
    PS1-BUF <---> GND
    PS2-BUF <---> GND

Configuration of AD9915 Dev Board jumpers:
    Disable USB communication
    P203 <---> Vcc (Disable)
    P204 <---> Vcc (Disable)
    P205 <---> Vcc (Disable)

    Serial programming mode (Datasheet AD9915 p.28):
    IOCFG3 <---> GND
    IOCFG2 <---> GND
    IOCFG1 <---> GND
    IOCFG0 <---> Vdd

    Others jumpers configuration
    SYNC_IO_BUFF <---> GND  (Disable I/O reset)
    EXTPDCTL-BUF <---> GND
    RESET-BUF    <---> OPEN
    DROVR-BUF    <---> GND
    DRHOLD-BUF   <---> GND
    DRCTL-BUF    <---> GND

"""

import logging
import time
from array import array
import usb.core
from binascii import hexlify
from Adafruit_BBIO.SPI import SPI
import Adafruit_BBIO.GPIO as GPIO


DEBUG = True

SPI_CLOCK_FREQUENCY = 100000
SPI_MODE = 0

RESET_PIN = "P9_16"
IOUPDATE_PIN = "P9_15"

IFMAX = 2500000000    # Input maximum frequency (Hz)
FTW_SIZE = 32         # Frequency Tuning Word register size (bit)
PHASE_SIZE = 16       # Phase register size (bit)
DAC_OUT_SIZE = 12     # Output DAC resolution (bit)
AMAX = (1 << DAC_OUT_SIZE) - 1  # Output maximum amplitude (a.u.)

regname_2_addr = {'CFR1': 0x0, 'CFR2': 0x1, 'CFR3': 0x2, 'CFR4': 0x3,
                  'DigRampLowerLimit': 0x4, 'DigRampUpperLimit': 0x5,
                  'RisingDigRampStepSize': 0x6, 'FallingDigRampStepSize': 0x7,
                  'DigRampRate': 0x8,
                  'LowerFreqJump': 0x9, 'UpperFreqJump': 0xA,
                  'P0Ftw': 0xB, 'P0PhaseAmp': 0xC,
                  'P1Ftw': 0xD, 'P1PhaseAmp': 0xE,
                  'P2Ftw': 0xF, 'P2PhaseAmp': 0x10,
                  'P3Ftw': 0x11, 'P3PhaseAmp': 0x12,
                  'P4Ftw': 0x13, 'P4PhaseAmp': 0x14,
                  'P5Ftw': 0x15, 'P5PhaseAmp': 0x16,
                  'P6Ftw': 0x17, 'P6PhaseAmp': 0x18,
                  'P7Ftw': 0x19, 'P7PhaseAmp': 0x1A,
                  'USR0': 0x1B}


class Ad9915DevBbb():
    """Class representing AD9915 development board through BeagleBoneBlack
    board. Currently class use profile mode P0 only
    """

    def __init__(self, ifreq=IFMAX):
        """The constructor.
        :param ifreq: Current input frequency in Hz (float))
        :returns: None
        """
        # Init properties related to FTDI device
        self._spi = SPI(0, 0)  # SPI bus
        self._init_spi()
        self._init_gpio()
        # Init class properties
        self._ifreq = ifreq
        self._profile = 0
        self._ofreq = None
        self._phy = None
        self._amp = None
        self._pll_state = None
        self._pll_doubler_state = None
        self._pll_factor = None

    def __del__(self):
        GPIO.cleanup()
        self._spi.close()

    def _init_spi(self):
        self._spi.msh = SPI_CLOCK_FREQUENCY
        self._spi.mode = SPI_MODE
        self._spi.bpw = 8  # Bits per word
        self._spi.threewire = False
        self._spi.cshigh = False
        self._spi.lsbfirst = False

    def _init_gpio(self):
        GPIO.setup(channel=RESET_PIN, direction=GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(channel=IOUPDATE_PIN, direction=GPIO.OUT, initial=GPIO.LOW)

    def connect(self):
        # Configure/Init DDS device
        ## Reset: needed at power-up (see datasheet p.40)
        self._master_reset()
        ## Default + SDIO input only
        self.write_w16(regname_2_addr['CFR1'], [0x00, 0x01, 0x00, 0x0A])
        ## Default Default + Enable profile mode
        self.write_w16(regname_2_addr['CFR2'], [0x00, 0x80, 0x09, 0x00])
        ## DAC cal: needed at power-up (see datasheet p.40)
        self.dac_calibration()
        self._init_properties()

    def _init_properties(self):
        """Init properties
        """
        # !warning! parameter order initialisation is important
        '''
        if self._pll_state is None:
            self._pll_state = self.get_pll_state()
        else:
            self.set_pll_state(self._pll_state)
        if self._pll_doubler_state is None:
            self._pll_doubler_state = self.get_pll_doubler_state()
        else:
            self.set_pll_doubler_state(self._pll_doubler_state)
        if self._pll_factor is None:
            self._pll_factor = self.get_pll_multiplier_factor()
        else:
            self.set_pll_multiplier_factor(self._pll_factor)
        '''
        if self._ofreq is None:
            self._ofreq = self.get_ofreq()
        else:
            self.set_ofreq(self._ofreq)
        if self._phy is None:
            self._phy = self.get_phy()
        else:
            self.set_phy(self._phy)
        if self._amp is None:
            self._amp = self.get_amp()
        else:
            self.set_amp(self._amp)

    def is_connected(self):
        """Return True if interface to DDS board is ready else return False.
        """
        '''if isinstance(self._spi, spi.SpiPort):
            return True
        return False
        '''
        return True

    def read(self, address, length=4):
        """
        :param register: register address(int)
        :param length: size of register in byte (int)
        :returns: register value (int)
        """
        msg = [0x80 + address]
        self._spi.writebytes(msg)
        self._io_update()
        reg_value = self._spi.readbytes(length)
        retval = 0
        for i, x in enumerate(reg_value):
            retval += x << (8*(len(reg_value)-i-1))
        return retval

    def write(self, address, value):
        """
        :param address: (int)
        :param value: (int)
        :returns: None
        """
        msg = [address]
        for i in range(3, -1, -1):
            msg.append((value >> (i * 8)) & 0xff)
        self._spi.writebytes(msg)
        self._io_update()
        self._spi.writebytes([])

    def read_w16(self, address, length=4):
        """
        :param register: register address(int)
        :param length: size of register in byte (int)
        :returns: register value in 16 bits word size (list of int)
        """
        msg = [0x80 + address]
        self._spi.writebytes(msg)
        self._io_update()
        retval = self._spi.readbytes(length)
        retval = [x for x in retval]
        return retval

    def write_w16(self, address, values):
        """
        :param address: (int)
        :param value: (list of int)
        :returns: None
        """
        msg = [address]
        for value in values:
            msg.append(value)
        self._spi.writebytes(msg)
        self._io_update()
        '''
        for value in msg:
            
            print("write_16.value:", value)
            
            self._spi.xfer2([value])
            self._io_update()
        '''
        #self._spi.writebytes([])

    def dac_calibration(self):
        """DAC calibration, needed after each power-up and every time REF CLK or
        the internal system clock is changed.
        :returns: None
        """
        # Calibration 1/2: enable
        self.write_w16(regname_2_addr['CFR4'], [0x01,0x05,0x21,0x20])
        # Calibration 2/2: disable
        self.write_w16(regname_2_addr['CFR4'], [0x00,0x05,0x21,0x20])

    def set_profile(self, profile):
        """Set profile currently in use. Curently not implemented.
        :param profile: Select profile in use between 0 to 7 (int)
        :returns: None
        """
        if profile not in range(0, 8):
            raise ValueError("Profile must be in range 0 to 7, here: %r",
                             profile)
        ## self._profile = profile

    def get_profile(self):
        """Get profile currently in use. Curently not implemented.
        :returns: profile currently in use (int)
        """
        return self._profile

    def get_sysfreq(self):
        """Get system frequency.
        Currently, does not support PLL.
        :returns: Current system frequency value (float)
        """
        '''if self._pll_state is True:
            if self._pll_doubler_state is True:
                doubler = 2.0
            else:
                doubler = 1.0
            factor = self._pll_factor
            sfreq = self._ifreq * doubler * factor
        else:
            sfreq = self._ifreq
        return sfreq
        '''
        return self._ifreq

    def set_ifreq(self, value):
        """Set input frequency.
        :param value: Input frequency value (float)
        :returns: None
        """
        self._ifreq = value
        self.dac_calibration()  # Needed!
        logging.debug("Set input frequency: %r", value)
        # Update DDS device because ofreq = f(ifreq)
        self.set_ofreq(self._ofreq)

    def get_ifreq(self):
        """Get input frequency.
        :returns: Current input frequency value (float)
        """
        return self._ifreq

    def set_ofreq(self, value, profile=None):
        """Set output frequency to current DDS profile if profile parameter is
        None or set output frequency of requested DDS profile.
        Return the actual output frequency (see _actual_ofreq() method).
        :param value: Output frequency value (float).
        :param profile: Profile to update between 0 to 7 (int)
        :returns: Actual output frequency (float)
        """
        if self.is_connected() is False:
            logging.error("Device is not connected.")
            return None
        if profile not in range(0, 8) and profile is not None:
            raise ValueError("Profile not in range 0 to 7, here: %r", profile)
        if profile is None:
            profile = 0
        regname = 'P{:d}Ftw'.format(profile)
        # Compute the Frequency Tuning Word (FTW).
        ftw = int((value * (1 << FTW_SIZE)) / self.get_sysfreq())
        
        print("set_ofreq.ftw", ftw)
        
        # Send data to device
        self.write(regname_2_addr[regname], ftw)
        # Return the actual output frequency.
        self._ofreq = self._actual_ofreq(self.get_sysfreq(), ftw, FTW_SIZE)
        logging.debug("Set output frequency: %r", self._ofreq)
        return self._ofreq

    def get_ofreq(self, profile=None):
        """Get output frequency of current DDS profile if profile parameter is
        None or return output frequency of requested DDS profile.
        :param profile: Profile output frequency requested (int)
        :returns: Output frequency of DDS profile (float).
        """
        if self.is_connected() is False:
            logging.error("Device is not connected.")
            return None
        if profile not in range(0, 8) and profile is not None:
            raise ValueError("Profile not in range 0 to 7, here: %r", profile)
        if profile is None:
            profile = 0
        regname = 'P{:d}Ftw'.format(profile)
        ftw = self.read(regname_2_addr[regname])

        print("get_ofreq.ftw", ftw)
        
        self._ofreq = self._actual_ofreq(self.get_sysfreq(), ftw, FTW_SIZE)
        return self._ofreq

    def set_phy(self, value, profile=None):
        """Set phase of output signal on DDS.
        Take the queried output phase (in degree) as argument and set
        the adequat register in the DDS.
        :param value: Output phase value (float).
        :param profile: Profile to update between 0 to 7 (int)
        :returns: Actual output phase (float)
        """
        if self.is_connected() is False:
            logging.error("Device is not connected.")
            return None
        if profile not in range(0, 8) and profile is not None:
            raise ValueError("Profile not in range 0 to 7, here: %r", profile)
        if profile is None:
            profile = 0
        regname = 'P{:d}PhaseAmp'.format(profile)
        # Phase and amplitude output is handled by a common register.
        # Before writing new phase, we need to get current amplitude
        # and take care to not reset its value.
        reg_value = self.read_w16(regname_2_addr[regname])
        asf_list = reg_value[2:]
        phy = int((value * (1 << PHASE_SIZE)) / 360)
        phy_list = self._int_2_byte_list(phy, 2)
        msg = asf_list + phy_list
        self.write_w16(regname_2_addr[regname], msg)
        phy = self._actual_phy(phy, PHASE_SIZE)  # Return the actual phase
        logging.debug("Set phase: %r", phy)
        return phy

    def get_phy(self, profile=None):
        """Get output phase of profile..
        :param profile: Profile phase requested (int)
        :returns: Output phase of DDS (float).
        """
        if self.is_connected() is False:
            logging.error("Device is not connected.")
            return None
        if profile not in range(0, 8) and profile is not None:
            raise ValueError("Profile not in range 0 to 7, here: %r", profile)
        if profile is None:
            profile = 0
        regname = 'P{:d}PhaseAmp'.format(profile)
        reg_value = self.read_w16(regname_2_addr[regname])
        # Extract phase value from register value.
        phy = (reg_value[1] << 8) + reg_value[0]
        return self._actual_phy(phy, PHASE_SIZE)  # return the actual phase.

    def set_amp(self, value, profile=None):
        """Set amplitude tuning word of output signal on DDS.
        Take the input and output frequency as argument and set the adequat
        register in the DDS.
        :param value: Output amplitude value (int)
        :param profile: Profile to update between 0 to 7 (int)
        :returns: fsc register value if transfert is ok (int)
        """
        if self.is_connected() is False:
            logging.error("Device is not connected.")
            return None
        if profile not in range(0, 8) and profile is not None:
            raise ValueError("Profile not in range 0 to 7, here: %r", profile)
        if profile is None:
            profile = 0
        # If value is out of range, bound value and raise Warning.
        if not(0 <= value <= AMAX):
            logging.warning("Amplitude value out of range: %r", value)
            value = self._bound_value(value, 0, AMAX)
        regname = 'P{:d}PhaseAmp'.format(profile)
        # Phase and amplitude output is handled by a common register.
        # Before writing new amplitude, we need to get current phase
        # and take care to not reset its value.
        reg_value = self.read_w16(regname_2_addr[regname])
        phy_list = reg_value[:2]
        asf_list = self._int_2_byte_list(value, 2)
        msg = asf_list + phy_list
        self.write_w16(regname_2_addr[regname], msg)
        logging.debug("Set output amplitude: %r", value)
        return value

    def get_amp(self, profile=None):
        """Get output amplitude tuning word of DDS.
        :param profile: Profile phase requested (int)
        :returns:  Output amplitude tuning of DDS (float).
        """
        if self.is_connected() is False:
            logging.error("Device is not connected.")
            return None
        if profile not in range(0, 8) and profile is not None:
            raise ValueError("Profile not in range 0 to 7, here: %r", profile)
        if profile is None:
            profile = 0
        regname = 'P{:d}PhaseAmp'.format(profile)
        reg_value = self.read_w16(regname_2_addr[regname])
        # Extract amplitude value from register value.
        asf = (reg_value[3] << 8) + reg_value[2]
        return asf

    def set_output_state(self, state=False):
        """Set output state.
        :param state: - False  Disable output. (bool)
                      - True   Enable CMOS output.
        :returns: None
        """
        raise NotImplemented

    def get_output_state(self):
        """Get output state.
        :returns: Output state (bool)
        """
        reg_value = self.read(regname_2_addr['CFR1'])
        output_state_bit = 16
        return self._check_bit_set(reg_value, output_state_bit)

    def set_pll_state(self, state=False):
        """Set PLL state.
        Note: A modification of the PLL state modify the output frequency.
        :param state: - False  Disable PLL. (bool)
                      - True   Enable PLL.
        :returns: None
        """
        reg_value = self.read(regname_2_addr['CFR3'])
        pll_state_bit = 2
        if state is True:
            reg_value |= 1 << pll_state_bit
        else:
            reg_value &= ~(1 << pll_state_bit)
        self.write(regname_2_addr['CFR3'], reg_value)

    def get_pll_state(self):
        """Get PLL state.
        :returns: PLL state (bool)
        """
        reg_value = self.read(regname_2_addr['CFR3'])
        pll_state_bit = 2
        return self._check_bit_set(reg_value, pll_state_bit)

    def is_pll_locked(self):
        """Return the internal PLL lock (to the REF CLK input signal) state.
        :returns: True if the internal PLL is locked else return False (bool)
        """
        reg_value = self.read(regname_2_addr['USR0'])
        pll_lock_bit = 24
        return self._check_bit_set(reg_value, pll_lock_bit)

    def set_pll_divider_factor(self, value):
        """Set PLL feedback divider value.
        :param factor: factor of PLL divider (between 20 to 510) (int)
        :returns: None
        """
        if self.is_connected() is False:
            logging.error("Device is not connected.")
            return None
        if not(20 <= value <= 510):
            logging.error("PLL divider factor value out of range: %r", factor)
            value = self._bound_value(value, 20 , 510)
        cfr3 = self.read_w16(regname_2_addr['CFR3'])
        cfr3[1] = value
        self.write_w16(regname_2_addr['CFR3'], cfr3)
        logging.debug("Set PLL divider factor: %r", value)
        return value

    def get_pll_divider_factor(self):
        """Get SysClk PLL divider factor.
        Note that here we get the overall divider factor, so the prescaler
        divider by 2 in the SysClk PLL divider block is include in the
        returned factor.
        :returns: factor of PLL divider (between 4 to 66) (int)
        """
        raise NotImplemented

    def set_cp_current(self, value=0):
        """Set charge pump current value.
        :param value: charge pump current: - 0: 250 uA
                                           - 1: 375 uA
                                           - 2: off
                                           - 3: 125 uA
        :returns: None
        """
        raise NotImplemented

    def get_cp_current(self):
        """Get charge pump current configuration value.
        Charge pump current: - 0: 250 uA
                             - 1: 375 uA
                             - 2: off
                             - 3: 125 uA
        :returns: charge pump current (int)
        """
        raise NotImplemented

    def vco_calibration(self, value=None):
        """VCO calibration process.
        :param value: vco range: - 0 = low range (int)
                                 - 1 = high range
                                 - others = autorange
        :returns: None
        """
        raise NotImplemented

    @staticmethod
    def _actual_ofreq(ifreq, ftw, rsize):
        """Return the actual output frequency.
        Due to the resolution of the DDS, the actual output frequency
        may be (a bit) different than the queried.
        :param ftw: Frequency Tuning Word register value (int).
        :param rsize: Size of register (int).
        :returns: Actual output frequency (float).
        """
        return (ftw * ifreq) / (1 << rsize)

    @staticmethod
    def _actual_phy(dphy, bit):
        """Return the actual output phase.
        Due to the resolution of the DDS, the actual output phase
        may be (a bit) different than the queried.
        :param dphy: Phase register value (int).
        :param bit: Number of bits used for the phase resolution (int)
        :returns: Actual output phase offset in degree (float).
        """
        return float(360 * dphy) / (1 << bit)

    @staticmethod
    def _int_2_byte_list(value, size):
        """Take an integer and split it in a list of the corresponding
        'size' 8 bits word (byte).
        For example:
            17179869 in hexadecimal = 0x10624dd
            0x10624dd splitted in byte = [0x01, 0x06, 0x24, 0xdd]
            [0x01, 0x06, 0x24, 0xdd] in base 10 = [1, 6, 36, 221]
            => _int_2_byte_list(17179869, 4) = [1, 6, 36, 221]
        :param value: an integer to split (int)
        ;param size: sier of output list (int)
        :returns: list of byte (list of int)
        """
        value_format = '0{:d}x'.format(size * 2)
        value = format(value, value_format)
        return [int(value[i:i+2], 16) for i in range(0, size*2, 2)]

    @staticmethod
    def _bound_value(value, vmin, vmax):
        """Check that a value is included in the range [min, max], if not the value
        is bounded to the range, ie:
        - if value < min  ->  min = value
        - if value > max  ->  max = value
        :param value: Value that is checked
        :param vmin: Minimum valid value.
        :param vmax: Maximum valid value.
        :returns: Bounded value.
        """
        if value < vmin:
            logging.warning("Parameter %s out of range (%f). Set to: %f",
                            val_name, value, vmin)
            return vmin
        elif value > vmax:
            logging.warning("Parameter %s out of range (%f). Set to: %f",
                            val_name, value, vmax)
            return vmax
        else:
            return value

    @staticmethod
    def _check_bit_set(word, n):
        """Check if n-th bit of word is set or not.
        :param word: word to check (int)
        :param n: n-th bit of work to check (int)
        :returns: True is n-th bit is set else False (bool)
        """
        if word & (1 << n):
            return True
        return False

    def _io_update(self):
        """Generate IO update event: transfer written data from I/O buffer to
        the coresponding internal registers.
        :returns: None
        """
        GPIO.output(IOUPDATE_PIN, GPIO.HIGH)
        #time.sleep(0.001)
        GPIO.output(IOUPDATE_PIN, GPIO.LOW)
        logging.debug("IO update")

    def _master_reset(self):
        """Master reset: clears all memory elements and sets registers to
        default values. Required after power up.
        :returns: None
        """
        GPIO.output(RESET_PIN, GPIO.HIGH)
        time.sleep(int(1 / (1000 * SPI_CLOCK_FREQUENCY)))
        GPIO.output(RESET_PIN, GPIO.LOW)
        logging.debug("Master reset")


# =============================================================================
if __name__ == '__main__':
    # Setup basic logger
    LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s (%(lineno)d): ' \
        + '%(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

    pylogger = logging.getLogger('pyftdi')
    #pylogger.setLevel(logging.DEBUG)

    ##print("Interfaces:", Ad9915DevFtdi232HM().get_interfaces())

    OFREQ = 80000000.0
    #OFREQ = 38146.3905796
    PHY = 15
    AMP = 478
    DDS = Ad9915DevBbb()
    DDS.connect()
    #DDS.set_pll_divider_factor(250)
    #DDS.set_pll_state(True)
    #print("PLL lock:", DDS.is_pll_locked())
    #DDS._io_update()
    DDS.set_ifreq(2.5e9)
    print("CFR2:", DDS.read_w16(regname_2_addr['CFR2']))
    print(DDS.set_ofreq(OFREQ))
    print("Get output frequency")
    print("OFREQ:", DDS.get_ofreq())
    #print("Get amplitude")
    #print("AMP 1:", DDS.get_amp())
    #DDS.set_phy(PHY)
    #print("Get phase")
    #print("PHY:", DDS.get_phy())
    #DDS.set_amp(AMP)
    #print("Get amplitude")
    #print("AMP 2:", DDS.get_amp())
