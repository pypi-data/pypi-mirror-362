# -*- coding: utf-8 -*-

"""package ad9xdds
author    Benoit Dubois
copyright FEMTO ENGINEERING, 2021
license   GPL v3.0+
brief     Add signal/slot facility to Ad9915DevUmr232Hm class.
details   Class derived from Ad9915DevUmr232Hm to add signal/slot facilities.
          Signal/slot facilities use signalslot package.
          Ad9915DevUmr232Hm class allow handling of AD9915 development board
          through USB to SPI adapter.
"""

import signalslot as ss
import ad9xdds.ad9915dev_umr232hm as ad9915dev_umr232hm


class SAd9915Dev(ad9915dev_umr232hm.Ad9915Dev):
    """Class derived from Ad9915Dev class to add signal/slot facilities.
    """

    def __init__(self, **kwargs):
        self.ifreq_updated = ss.Signal(['value'])
        self.ofreq_updated = ss.Signal(['value'])
        self.phase_updated = ss.Signal(['value'])
        self.amp_updated = ss.Signal(['value'])
        super().__init__(**kwargs)

    def connect(self, url, **kwargs):
        return super().connect(url, **kwargs)

    def set_ifreq(self, value, **kwargs):
        super().set_ifreq(value)
        self.ifreq_updated.emit(value=value)

    def set_ofreq(self, value, **kwargs):
        aofreq = super().set_ofreq(value)
        self.ofreq_updated.emit(value=aofreq)
        return aofreq

    def set_phy(self, value, **kwargs):
        aphy = super().set_phy(value)
        self.phase_updated.emit(value=aphy)
        return aphy

    def set_amp(self, value, **kwargs):
        aamp = super().set_amp(value)
        self.amp_updated.emit(value=aamp)
        return aamp
