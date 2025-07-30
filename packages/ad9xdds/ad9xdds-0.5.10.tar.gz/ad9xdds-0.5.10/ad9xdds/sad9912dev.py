# -*- coding: utf-8 -*-

"""package ad9xdds
author    Benoit Dubois
copyright FEMTO ENGINEERING, 2020
license   GPL v3.0+
brief     API to control AD9912 DDS development board with signals/slots
          facilities.
details   Class derived Ad9912Dev class to add signals/slots facilities
"""

import signalslot as ss
import ad9xdds.ad9912dev as ad9912dev


class SAd9912Dev(ad9912dev.Ad9912Dev):
    """Class derived from Ad9912Dev class to add signal/slot facilities.
    """

    def __init__(self, **kwargs):
        self.ifreq_updated = ss.Signal(['value'])
        self.ofreq_updated = ss.Signal(['value'])
        self.phase_updated = ss.Signal(['value'])
        self.amp_updated = ss.Signal(['value'])
        self.pll_state_updated = ss.Signal(['flag'])
        self.pll_doubler_updated = ss.Signal(['flag'])
        self.pll_factor_updated = ss.Signal(['value'])
        super().__init__(**kwargs)

    def connect(self, vendor_id=ad9912dev.VENDOR_ID,
                product_id=ad9912dev.PRODUCT_ID,
                bus=None, address=None, **kwargs):
        return super().connect(vendor_id, product_id, bus, address, **kwargs)

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

    def set_pll_state(self, flag, **kwargs):
        super().set_pll_state(flag)
        self.pll_state_updated.emit(flag=flag)

    def set_pll_doubler_state(self, flag, **kwargs):
        super().set_pll_doubler_state(flag)
        self.pll_doubler_updated.emit(flag=flag)

    def set_pll_multiplier_factor(self, value, **kwargs):
        super().set_pll_multiplier_factor(value)
        self.pll_factor_updated.emit(value=value)
