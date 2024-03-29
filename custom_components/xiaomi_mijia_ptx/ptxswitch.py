import logging
from collections import defaultdict
from typing import Dict, Any, Optional
from miio.click_common import command, format_output
from miio.device import Device


_LOGGER = logging.getLogger(__name__)


MODEL_PTX_SINGLE_WALL_SWITCH = '090615.switch.switch01'

MODEL_PTX_DUAL_WALL_SWITCH = '090615.switch.switch02'

MODEL_PTX_TRIPLE_WALL_SWITCH = '090615.switch.switch03'

MODEL_PTX_HARD_SINGLE_WALL_SWITCH = '090615.switch.xswitch01'
MODEL_PTX_HARD_DUAL_WALL_SWITCH = '090615.switch.xswitch02'
MODEL_PTX_HARD_TRIPLE_WALL_SWITCH = '090615.switch.xswitch03'


AVAILABLE_PROPERTIES = {
    MODEL_PTX_SINGLE_WALL_SWITCH: [
        "is_on_1",
        "switchname1"],
    
    MODEL_PTX_HARD_SINGLE_WALL_SWITCH: [
        "is_on_1",
        "switchname1"],

    MODEL_PTX_DUAL_WALL_SWITCH: [
        "is_on_1",
        "is_on_2",
        "switchname1",
        "switchname2"],
    
      MODEL_PTX_HARD_DUAL_WALL_SWITCH: [
        "is_on_1",
        "is_on_2",
        "switchname1",
        "switchname2"],

    MODEL_PTX_TRIPLE_WALL_SWITCH: [
        "is_on_1",
        "is_on_2",
        "is_on_3",
        "switchname1",
        "switchname2",
        "switchname3"],
    
     MODEL_PTX_HARD_TRIPLE_WALL_SWITCH: [
        "is_on_1",
        "is_on_2",
        "is_on_3",
        "switchname1",
        "switchname2",
        "switchname3"],
}


class PtxSwitchStatus:
    # Container for status of PTX switch.

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def is_on_index(self, index) -> Optional[bool]:
        # True if switch {index} is on.
        k = "is_on_{}".format(index)
        if k in self.data and self.data[k] is not None:
            return self.data[k]
        return None

    @property
    def is_on(self) -> Optional[bool]:
        # True if switch 1 is on.
        return self.is_on_index(1)

    @property
    def is_on_1(self) -> Optional[bool]:
        # True if switch 1 is on.
        return self.is_on_index(1)

    @property
    def is_on_2(self) -> Optional[bool]:
        # True if switch 2 is on.
        return self.is_on_index(2)

    @property
    def is_on_3(self) -> Optional[bool]:
        # True if switch 3 is on.
        return self.is_on_index(3)

    def switch_name_index(self, index) -> Optional[str]:
        # Name of the switch button {index}
        k = "switchname{}".format(index)
        if k in self.data and self.data[k] is not None:
            return self.data[k]
        return None

    @property
    def switch_name_1(self) -> Optional[str]:
        # Name of the switch button 1
        return self.switch_name_index(1)

    @property
    def switch_name_2(self) -> Optional[str]:
        # Name of the switch button 2
        return self.switch_name_index(2)

    @property
    def switch_name_3(self) -> Optional[str]:
        # Name of the switch button 3
        return self.switch_name_index(3)

    def __repr__(self) -> str:
        s = "<PtxSwitchStatus " \
            "is_on_1=%s, " \
            "is_on_2=%s, "\
            "is_on_3=%s, " \
            "switch_name_1=%s, " \
            "switch_name_2=%s, " \
            "switch_name_3=%s>" % \
            (self.is_on_1,
             self.is_on_2,
             self.is_on_3,
             self.switch_name_1,
             self.switch_name_2,
             self.switch_name_3)
        return s

    def __json__(self):
        return self.data


class PtxSwitch(Device):
    # Main class representing the PTX switch

    def __init__(self, ip: str = None, token: str = None, start_id: int = 0,
                 debug: int = 0, lazy_discover: bool = True,
                 model: str = MODEL_PTX_TRIPLE_WALL_SWITCH) -> None:
        super().__init__(ip, token, start_id, debug, lazy_discover)

        if model in AVAILABLE_PROPERTIES:
            self.model = model
        else:
            self.model = MODEL_PTX_TRIPLE_WALL_SWITCH

    @command(
        default_output=format_output(
            "",
            "Switch 1 Status: {result.is_on_1}\n"
            "Switch 2 Status: {result.is_on_2}\n"
            "Switch 2 Status: {result.is_on_3}\n"
            "Switch 1 Name: {result.switch_name_1}\n"
            "Switch 2 Name: {result.switch_name_2}\n"
            "Switch 3 Name: {result.switch_name_3}\n")
    )
    def status(self) -> PtxSwitchStatus:
        """
        PTX Triple wall switch payload dump:

        # Query all 3 Switches status
        ->  {Mi Home App} data= {"id":2468,"method":"get_prop","params":[0,0,0]}

        # Returns On, Off, Off
        <-  {PTX Switch}  data= {"result":[1,0,0,1],"id":2468}

        # Query Switch Name 3
        ->  {Mi Home App} data= {"id":2471,"method":"get_prop","params":["switchname3"]}

        # Returns Switch Name 3
        <-  {PTX Switch}  data= {"result":["switch3"],"id":2471}

        # Set switch name 1 to 'test name 1'
        ->  {Mi Home App} data= {"id":2472,"method":"SetSwtichname1","params":["test name 1"]}

        # Didn't firgure out meaning of this return data.
        # Switches status were On, Off, Off at this moment
        <-  {PTX Switch}  data= {"result":[0],"id":2472}

        # Turn on switch 1
        ->  {Mi Home App} data= {"id":2473,"method":"SetSwitch1","params":[1]}

        # Returns status On
        <-  {PTX Switch}  data= {"result":[1],"id":2473}

        # Turn Off switch 1
        ->  {Mi Home App} data= {"id":2474,"method":"SetSwitch1","params":[0]}

        # Returns status Off
        <-  {PTX Switch}  data= {"result":[0],"id":2474}

        # Turn on all switches
        ->  {Mi Home App} data= {"id":3381,"method":"SetSwitchAll","params":[1,1,1]}

        # Returns On, On, On
        <-  {PTX Switch}  data= {"result":[1,1,1],"id":3381}

        # Turn off all switches
        ->  {Mi Home App} data= {"id":3382,"method":"SetSwitchAll","params":[0,0,0]}

        # Returns off, off, off
        <-  {PTX Switch}  data= {"result":[0,0,0],"id":3382}

        """
        # Retrieve properties.
        properties = AVAILABLE_PROPERTIES[self.model].copy()

        # Querying switch status require [0,0,0] as the request
        # params. Querying other property require property name
        # (eg. 'switchname1') as the request param.

        # params for querying status of the switches
        params_switch_status = list()

        # params for querying other properties
        params_other = list()

        # Query every switch status

        for k in properties:
            if k[:5] == "is_on":
                params_switch_status.append(0)
            else:
                params_other.append(k)

        result_1 = self.send(
            "get_prop",
            params_switch_status
        )

        param_count = len(params_switch_status)
        values_count = len(result_1)
        if values_count >= param_count:
            # return values always have one more than requested.
            # get return values only we want
            result_1 = result_1[:param_count]
        else:
            result_1 = [None, None, None]
            _LOGGER.debug(
                "Count (%s) of requested params does not match the "
                "count (%s) of received values.",
                param_count, values_count)

        # Query other params
        # A single request is limited to 1 properties. Therefore the
        # properties are divided into multiple requests

        result_2 = list()
        for param in params_other:
            value = self.send(
                "get_prop",
                [param]
            )
            if len(value) >= 1:
                v = value[0]
                if param[:10] == "switchname":
                    if isinstance(v, str):
                        result_2.append(v)
                    else:
                        _LOGGER.debug("Unexpected type of switchname")
                        result_2.append(None)

                else:
                    result_2.append(v)

            else:
                result_2.append(None)
                _LOGGER.debug("Property %s returns None.", param)

        result = PtxSwitchStatus(
            defaultdict(lambda: None,
                        zip(properties,
                            result_1 + result_2)))
        return result

    def turn_switch(self, index: int, switch_state: int) -> bool:
        """
        Turn a switch channel on/off.
        index: switch channel index, start from 1.
        switch_state: 0 means on, 1 means off.
        """
        properties = AVAILABLE_PROPERTIES[self.model]
        key = "is_on_{}".format(index)
        if key not in properties:
            _LOGGER.debug("switch index (%s) not supported.", index)
            return False

        result = self.send(
            "SetSwitch{}".format(index),
            [switch_state]
        )
        if result[:1] == [0] or result[:1] == [1]:
            return True
        else:
            _LOGGER.debug("Toogle switch {} failed.".format(index))
            return False

    def turn_on_switch(self, index: int) -> object:
        return self.turn_switch(index, 1)

    def turn_off_switch(self, index: int) -> bool:
        return self.turn_switch(index, 0)

    def set_switch_name(self, index: int, name: str) -> bool:
        """
        Set new name for a switch channel.
        index: switch channel index, start from 1.
        name: new name.
        """
        properties = AVAILABLE_PROPERTIES[self.model]
        key = "switchname{}".format(index)
        if key not in properties:
            _LOGGER.debug("switch index (%s) not supported.", index)
            return False

        result = self.send(
            "SetSwtichname{}".format(index),
            [name]
        )

        if result[:1] == 0 or result[:1] == 1:
            return True
        else:
            _LOGGER.debug(
                "Set name of switch {} failed.".format(index)
            )
            return False
