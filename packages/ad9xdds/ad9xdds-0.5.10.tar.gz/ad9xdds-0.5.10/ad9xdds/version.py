# -*- coding: utf-8 -*-

""" ad9xdds/version.py """
__version__ = "0.5.10"

# 0.5.10 (2025/07/17): Fix rounding error with low resolution ofreq value:
#                      Use decimal.Decimal fixed point for arithmetic.
# 0.5.9  (02/04/2025): Correct set_ifreq() return value in AD9915Dev class.
# 0.5.8  (21/03/2025): AD9915: bugs correction.
# 0.5.7  (20/03/2025): AD9915: update fine output frequency setting capability.
#                      AD9912, minor: correct IFMAX and OFMAX values to avoid type
#                      checking error.
# 0.5.6  (27/02/2024): Minor: correct returned value of dds_emul.set_freq().
# 0.5.5  (24/08/2023): Enhance reliability of Ad9912Dev get/set parameters.
# 0.5.4  (23/08/2023): Handle R/W exception of FX2 device.
# 0.5.3  (04/05/2022): Correct fine tuning capability.
# 0.5.2  (08/09/2021): Add fine tuning of output frequency capability to
#                      AD9915 class and script. Enhance reliability of
#                      writing methods.
# 0.5.1  (06/09/2021): Add cli script to handle AD9915 dev board.
#                      Add explicit type conversion of ifreq, ofreq and
#                      amplitude setter method of Ad9915Dev class.
# 0.5.0  (01/09/2021): Change/Simplify name of Ad9915Dev_Umr232h to Ad9915.
#                      Enhance write method of classes Ad9912 et Ad9915.
#                      Change method name of register setter/getter of Ad9915
#                      class. Some others corrections.
# 0.4.5  (11/05/2021): Correct initialisation of ad9915dev_umr232h.
#                      Update firm_manager. Some other minor corrections.
# 0.4.4  (31/03/2021): Add emulated AD9915 development board.
# 0.4.3  (07/01/2021): Add support of AD9915 development board.
# 0.4.2  (02/07/2020): Correct import error in ad9912dev module.
# 0.4.1  (02/07/2020): Add selection of DDS device through usb bus and
#                      usb address in addition to vid and pid parameters.
# 0.4.0  (13/12/2019): Add support of signal/slot facilities in pure python
#                      using signalslot package.
# 0.3.2  (27/09/2019): Update support of pyusb to v1.0.2 instead of v1.0.0a3.
# 0.3.1  (27/06/2019): Update package name (dds -> ad9xdds).
# 0.3.0  (19/06/2019): move to PyQt5.
