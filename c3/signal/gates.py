import copy
import hjson
import numpy as np
from c3.c3objs import C3obj


class Instruction:
    """
    Collection of components making up the control signal for a line.

    Parameters
    ----------
    t_start : np.float64
        Start of the signal.
    t_end : np.float64
        End of the signal.
    channels : list
        List of channel names (strings)


    Attributes
    ----------
    comps : dict
        Nested dictionary with lines and components as keys

    Example:
    comps = {
             'channel_1' : {
                            'envelope1': envelope1,
                            'envelope2': envelope2,
                            'carrier': carrier
                            }
             }

    """

    def __init__(
        self,
        name: str = " ",
        channels: list = [],
        t_start: np.float64 = 0.0,
        t_end: np.float64 = 0.0,
    ):
        self.name = name
        self.t_start = t_start
        self.t_end = t_end
        self.comps = {}  # type: ignore
        for chan in channels:
            self.comps[chan] = {}
        # TODO remove redundancy of channels in instruction

    def asdict(self) -> dict:
        components = {}  # type:ignore
        for chan, item in self.comps.items():
            components[chan] = {}
            for key, comp in item.items():
                components[chan][key] = comp.asdict()
        return {"gate_length": self.t_end - self.t_start, "drive_channels": components}

    def __str__(self) -> str:
        return hjson.dumps(self.asdict())

    def add_component(self, comp: C3obj, chan: str):
        """
        Add one component, e.g. an envelope, local oscillator, to a channel.

        Parameters
        ----------
        comp : C3obj
            Component to be added.
        chan : str
            Identifier for the target channel

        """
        self.comps[chan][comp.name] = comp