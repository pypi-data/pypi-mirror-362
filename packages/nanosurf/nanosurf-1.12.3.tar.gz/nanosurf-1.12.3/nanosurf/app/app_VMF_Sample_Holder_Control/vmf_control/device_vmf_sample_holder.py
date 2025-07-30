""" This device controls the VMF_Sample_holder_Controller
Copyright Nanosurf AG 2023
License - MIT
"""
import enum
import time
import struct
import typing
import random
import numpy as np
import scipy.optimize as opt
from typing import Union
import nanosurf as nsf
from nanosurf.lib.spm.com_proxy import Spm
from nanosurf.lib.spm.studio import Studio
from nanosurf.lib.devices import trinamic_motor_controller as tmc_controller
from nanosurf.lib.devices import accessory_interface as ai
from nanosurf.lib.devices.i2c import chip_TMC5031 as tmc
from nanosurf.lib.devices.i2c.config_eeprom import DataSerializer, ConfigEEPROM

from . import ADCLib as adc_module

_motor_config:dict[tmc.Reg_Channel, int] = { 
    tmc.Reg_Channel.GCONF:0x08,
    tmc.Reg_Channel.X_COMPARE: 0,
    tmc.Reg_Channel.RAMPMODE: 0,
    tmc.Reg_Channel.XACTUAL: 0,
    tmc.Reg_Channel.VSTART: 0,
    tmc.Reg_Channel.A1: 32000,
    tmc.Reg_Channel.V1: 0,
    tmc.Reg_Channel.AMAX: 50000,
    tmc.Reg_Channel.VMAX: 0,
    tmc.Reg_Channel.DMAX: 65535,
    tmc.Reg_Channel.D1: 65535,
    tmc.Reg_Channel.VSTOP: 1,
    tmc.Reg_Channel.TZEROWAIT: 0,
    tmc.Reg_Channel.XTARGET: 0,
    tmc.Reg_Channel.IHOLD_IRUN: 0x1f00,
    tmc.Reg_Channel.VCOOLTHRS: 7,
    tmc.Reg_Channel.VHIGH: 30,
    tmc.Reg_Channel.SW_MODE: 0x9e0,
    tmc.Reg_Channel.MSLUT_0: 0xaaaab554,
    tmc.Reg_Channel.MSLUT_1: 0x4a9554aa,
    tmc.Reg_Channel.MSLUT_2: 0x24492929,
    tmc.Reg_Channel.MSLUT_3: 0x10104222,
    tmc.Reg_Channel.MSLUT_4: 0xf8000000,
    tmc.Reg_Channel.MSLUT_5: 0xb5bb777d,
    tmc.Reg_Channel.MSLUT_6: 0x49295556,
    tmc.Reg_Channel.MSLUT_7: 0x80404222,
    tmc.Reg_Channel.MSLUTSEL: 0xffff9a06,
    tmc.Reg_Channel.MSLUTSTART: 0x00f80001,
    tmc.Reg_Channel.CHOPCONF: 0x000101a5,
    tmc.Reg_Channel.COOLCONF: 0x00000000
}

class VMFSampleHolderConfig(ConfigEEPROM):

    def __init__(self, bus_addr:int) -> None:  
        super().__init__(bus_addr, version=1)
        self._max_string_size = 10
        self._number_of_configurations = 16
        # -----
        self.bt_number = "BT09911"    
        self.sn_number = "125-xx-xxx"  
        self.calib_offset = [0.0 for _ in range(self._number_of_configurations)]  
        self.calib_first_order = [5.0 for _ in range(self._number_of_configurations)]  
        self.calib_second_order = [0.0 for _ in range(self._number_of_configurations)]  
        self.calib_name = [f"Config_{i:02d}" for i in range(self._number_of_configurations)]  

    def serialize(self) -> bytearray:
        self._serialize_version()
        self._serialize(self.bt_number, DataSerializer.Formats.String)
        self._serialize(self.sn_number, DataSerializer.Formats.String)
        self._serialize(self.calib_offset, DataSerializer.Formats.Double, list_size=self._number_of_configurations)
        self._serialize(self.calib_first_order, DataSerializer.Formats.Double, list_size=self._number_of_configurations)
        self._serialize(self.calib_second_order, DataSerializer.Formats.Double, list_size=self._number_of_configurations)
        self._serialize(self.calib_name, DataSerializer.Formats.String, list_size=self._number_of_configurations)
        return self._write_data_bytes

    def deserialize(self, data:bytearray) -> bool:
        if self._deserialize_version(data) == 1:
            self.bt_number = self._deserialize(DataSerializer.Formats.String) 
            self.sn_number = self._deserialize(DataSerializer.Formats.String) 
            self.calib_offset = self._deserialize(DataSerializer.Formats.Double, list_size=self._number_of_configurations)
            self.calib_first_order = self._deserialize(DataSerializer.Formats.Double, list_size=self._number_of_configurations)
            self.calib_second_order = self._deserialize(DataSerializer.Formats.Double, list_size=self._number_of_configurations)
            self.calib_name = self._deserialize(DataSerializer.Formats.String, list_size=self._number_of_configurations)
        else:
            raise ValueError(f"Unknown layout version: {self._read_layout_version}")
        return True

class VMFControllerConfig(ConfigEEPROM):

    def __init__(self, bus_addr:int) -> None:  
        super().__init__(bus_addr, version=1)
        self.bt_number = "BT09912"    
        self.sn_number = "124-xx-xxx"  

    def serialize(self) -> bytearray:
        self._serialize_version()
        self._serialize(self.bt_number, DataSerializer.Formats.String)
        self._serialize(self.sn_number, DataSerializer.Formats.String)
        return self._write_data_bytes

    def deserialize(self, data:bytearray) -> bool:
        if self._deserialize_version(data) == 1:
            self.bt_number = self._deserialize(DataSerializer.Formats.String) 
            self.sn_number = self._deserialize(DataSerializer.Formats.String) 
        else:
            raise ValueError(f"Unknown layout version: {self._read_layout_version}")
        return True


class VMFSampleHolderController():

    class VMFReferenceData():
        def __init__(self) -> None:
            self.reference_field_pos : list[float] = []
            self.reference_motor_pos : list[int] = []
            self.full_turn_steps = 5050000        
            self.is_reference_move_done = False
            self.field_min = 0.0
            self.field_max = 0.0

    class VMFConfiguration():
        def __init__(self) -> None:
            self.name = ""
            self.cal_values:typing.List[float] = []

    def __init__(self, simulation:bool = False) -> None:
        self._is_in_simulation_mode = simulation
        self._is_moving = False
        self._connected = False
        self._sample_holder_connected = False
        self._spm: nsf.SPMApp
        self._bus_master:ai.AccessoryInterface = None 
        self._motor_controller : tmc_controller.TrinamicMotorController = None
        self._adc_module : adc_module.ADC_Module = None
        self._chip_config_vmf_controller: VMFControllerConfig = None
        self._chip_config_sample_holder: VMFSampleHolderConfig = None
        self._scale_v_adc_to_tesla_offset = 0.0
        self._scale_v_adc_to_tesla_gain = 3.8
        self._scale_v_adc_to_tesla_square = 0.0
        self.speed_max = 0.08
        self.speed_min = 1e-6
        self._move_hook = self._default_move_hook
        self._message_hook = self._default_message_hook
        self._last_msg = ""
        self.reference_data = self.VMFReferenceData()
        self.configurations:typing.List[VMFSampleHolderController.VMFConfiguration] = []
        self._active_configuration = -1

    def _default_move_hook(self, current_field:float) -> bool:
        " This function is called during move action. If the hook returns False, the move is aborted"
        return self._is_moving
            
    def _default_message_hook(self, msg:str, error_type:bool=False) -> bool:
        " This function is called if an action has to report an status. "
        if error_type:
            print(f"Error: {msg}")        
        else:
            print(f"{msg}")
        return 
            
    def connect(self, spm:Union[Studio, Spm], serial_no:str = "", ai_port:int = -1, auto_setup:bool = True)-> bool:
        """ Connect to the VMFSampleHolderController Box and initializes all chips
            If serial_no is not provided it searches for any controller found on any AI-Port.
            If auto_setup is True, the setup() is called after successful connection
        """
        if self._is_in_simulation_mode:
            self._connected = True
            self._chip_config_vmf_controller = VMFControllerConfig(bus_addr=0x57)
            self._chip_config_sample_holder = VMFSampleHolderConfig(bus_addr=0x56)
            self._copy_configuration_from_sample_holder()
            if auto_setup:
                self.setup()
        else:
            self._connected = False
            try:
                self._bus_master = ai.AccessoryInterface(spm)
                self._connected = self._search_for_vmf_controller(serial_no, ai_port)
                if self._connected:
                    self._chip_config_vmf_controller = VMFControllerConfig(bus_addr=0x57)
                    self._chip_config_sample_holder = VMFSampleHolderConfig(bus_addr=0x56)
                    self._motor_controller = tmc_controller.TrinamicMotorController(bus_addr=0x2B, name="Magnet rotation motor", motors=1)
                    self._adc_module = adc_module.ADC_Module(bus_addr=0x2C)
                    self._bus_master.assign_chip(self._chip_config_vmf_controller)
                    self._bus_master.assign_chip(self._chip_config_sample_holder)
                    self._bus_master.assign_chip(self._motor_controller)
                    
                    if not self._chip_config_vmf_controller.load_config():
                        self._connected = False
                        raise IOError("Could not load configuration of vmf-controller from EEPROM!")
                    
                    if auto_setup:
                        self.setup()

                    self._active_configuration = 0
                    if self.is_sample_holder_connected():
                        if not self._load_calibrations_from_sample_holder():
                            raise IOError("Could not load configuration of vmf-sample-holder from EEPROM!")


                    self._last_msg = f"Connected to {self._chip_config_vmf_controller.sn_number} and sample holder {self._chip_config_sample_holder.sn_number}"
                else:
                    self._last_msg = " Could not find VMF-Controller. Check proper connection and power supply."

            except Exception as e:
                self._last_msg = f"{e}"
                
        return self._connected
    
    def is_connected(self) -> bool:
        return self._connected
    
    def get_message(self) -> str:
        return self._last_msg

    def get_serial_no(self) -> str:
        if self._connected:
            return self._chip_config_vmf_controller.sn_number
        return ""

    def is_sample_holder_connected(self):
        if self._connected:
            if self._is_in_simulation_mode:
                self._sample_holder_connected = True
            else:
                self._sample_holder_connected = self._chip_config_sample_holder.is_connected()
        return self._sample_holder_connected

    def get_sample_holder_serial_no(self) -> str:
        if self._sample_holder_connected:
            return self._chip_config_sample_holder.sn_number
        return ""

    def setup(self):
        if self._connected:
            if not self._is_in_simulation_mode:
                self._motor_controller.init_board(auto_config=False)
                self._motor_controller.write_config(0, _motor_config)
                self._motor_controller.set_current_position(self.reference_data.full_turn_steps / 4)
                self._motor_controller.motor_driver_enable(0, enable=True)

                self._adc_module.connect(self._bus_master, differential=True)
                self._adc_module.active_channel(0)
        else:
            raise IOError("Not connected.")
        
    def _load_calibrations_from_sample_holder(self) -> bool:
        done = False

        if self.is_sample_holder_connected():
            done = self._chip_config_sample_holder.load_config()
        else:
            default_config = VMFSampleHolderConfig(bus_addr=None)
            self._chip_config_sample_holder.calib_name = default_config.calib_name
            self._chip_config_sample_holder.calib_offset = default_config.calib_offset
            self._chip_config_sample_holder.calib_first_order = default_config.calib_first_order
            self._chip_config_sample_holder.calib_second_order = default_config.calib_second_order

        self._copy_configuration_from_sample_holder()
        self.configuration_select(self._active_configuration)        
        return done

    def get_current_h_field(self) -> float:
        if self._is_in_simulation_mode:
            return random.random()  
        adc_val = self._adc_module.read_multiple_channel(0)
        a = self._scale_v_adc_to_tesla_offset   
        b = self._scale_v_adc_to_tesla_gain 
        c = self._scale_v_adc_to_tesla_square
        if self._scale_v_adc_to_tesla_square == 0.0:
            current_field =  (adc_val - a) / b 
        else:
            current_field = (np.sqrt(4.0*c*(adc_val - a) + b*b)-b)/(2.0*c)
        return current_field
    
    def get_current_motor_pos_normalized(self) -> float:
        if self.reference_data.is_reference_move_done:
            max_pos_motor = self.reference_data.full_turn_steps / 4
            zero_pos_motor = self.reference_data.full_turn_steps / 4
            current_pos_motor = self._motor_controller.get_current_position()
            return (current_pos_motor - zero_pos_motor) / max_pos_motor 
        else:
            return 0.0

    def get_current_motor_pos(self) -> int:
        return self._motor_controller.get_current_position()

    def stop_moving(self):
        self._is_moving = False
        self._motor_controller.motor_stop() 
        self._motor_controller.motor_driver_enable(motor = 0, enable = False)

    def is_moving(self) -> bool:
        return self._is_moving
    
    def is_referenced(self) -> bool:
        return self.reference_data.is_reference_move_done
    
    def clear_referenced(self):
        self.reference_data.is_reference_move_done = False
    
    def register_move_hook(self, func):
        self._move_hook = func if func is not None else self._default_move_hook

    def register_message_hook(self, func):
        self._message_hook = func if func is not None else self._default_message_hook

    def move(self, direction_forward: bool, speed:float):
        if self._is_in_simulation_mode:
            return
        self._is_moving = True

        if self.reference_data.is_reference_move_done:
            direction = self.reference_data.full_turn_steps / 2 if direction_forward else 0
        else:
            direction = +10000000 if direction_forward else -10000000

        self._motor_controller.motor_driver_enable(motor = 0, enable = True)
        if self.reference_data.is_reference_move_done:
            self._motor_controller.start_move_to_absolute(int(direction),tmc_controller.from_normalized_speed(speed))
        else:
            self._motor_controller.start_move_relative(int(direction),tmc_controller.from_normalized_speed(speed))

        measuredField = self.get_current_h_field()
        while self._move_hook(measuredField) :
            # time.sleep(0.1)
            measuredField = self.get_current_h_field()

        self._motor_controller.motor_stop() 
        self._motor_controller.motor_driver_enable(motor = 0, enable = False)
        return True
    
    def reference_move(self) -> bool:
        if self._is_in_simulation_mode:
            self.reference_data.is_reference_move_done = True
            self.reference_data.field_min = -200.0e-3
            self.reference_data.field_max = +190.0e-3
            self._last_msg = f"Min field= {nsf.SciVal(self.reference_data.field_min, 'T')}, max field= {nsf.SciVal(self.reference_data.field_max, 'T')}"
            return self.reference_data.is_reference_move_done
        self._is_moving = True

        self.reference_data.reference_field_pos = []
        self.reference_data.reference_motor_pos = []
        
        self._message_hook("Reading min/max field range", False)
        # drive one round to measure the highest and the lowest field
        self._motor_controller.set_current_position(0)
        self._motor_controller.motor_driver_enable(motor = 0, enable = True)
        self._motor_controller.start_move_relative(int(self.reference_data.full_turn_steps*1.1),tmc_controller.from_normalized_speed(self.speed_max)) 
        keep_running = True
        while self._motor_controller.is_motor_moving() and keep_running:
            measurement = self.get_current_h_field()
            pos = self._motor_controller.get_current_position()
            keep_running = self._move_hook(measurement)
            self.reference_data.reference_field_pos.append(measurement)
            self.reference_data.reference_motor_pos.append(pos)
        self.reference_data.field_min = min(self.reference_data.reference_field_pos)
        self.reference_data.field_max = max(self.reference_data.reference_field_pos)
        self._last_msg = f"Min field= {nsf.SciVal(self.reference_data.field_min, 'T')}, max field= {nsf.SciVal(self.reference_data.field_max, 'T')}"
        # print(f"{self._last_msg=}")
        if keep_running:
            self._message_hook("Coarse move to zero field position", False)
            zero_motor_pos = self._find_zero_position()
            if zero_motor_pos >= 0: 
                self._motor_controller.start_move_to_absolute(int(zero_motor_pos),tmc_controller.from_normalized_speed(0.1)) 
                keep_running = True
                while self._motor_controller.is_motor_moving() and keep_running:
                    measurement = self.get_current_h_field()
                    pos = self._motor_controller.get_current_position()
                    keep_running = self._move_hook(measurement)
                self.reference_data.is_reference_move_done = True

                self._message_hook("Fine move to zero field position", False)
                self.reference_data.is_reference_move_done &= self.move_to_field(0.0)

                self._motor_controller.set_current_position(self.reference_data.full_turn_steps / 4)
            else:
                self._message_hook("Fine move to zero field position", True)
                self._last_msg = "Could not find zero crossing"

        self._motor_controller.motor_driver_enable(motor = 0, enable = False)
        
        if not keep_running:
            self._last_msg = "User abort"
            self.reference_data.is_reference_move_done = False

        if self.reference_data.is_reference_move_done:
            self._last_msg = f"Referenced. Min field= {nsf.SciVal(self.reference_data.field_min, 'T')}, max field= {nsf.SciVal(self.reference_data.field_max, 'T')}"
        return self.reference_data.is_reference_move_done

    def move_to_field(self, target_field:float) -> bool:
        if self._is_in_simulation_mode:
            return True
        self._is_moving = True
        self._adc_module.active_channel(0)

        # print(f"target Field = {nsf.SciVal(target_field, 'T')}")
        # print(f"measuredField = {(nsf.SciVal(self.get_current_h_field(), 'T'))}")

        self._motor_controller.motor_driver_enable(motor = 0, enable = True)

        if not self.reference_data.is_reference_move_done:
            # detect slope on sine wave
            measurement1 = self.get_current_h_field()
            self._motor_controller.start_move_relative(+20000,tmc_controller.from_normalized_speed(0.04))
            while self._motor_controller.is_motor_moving():
                pass
            measurement2 = self.get_current_h_field()

            if measurement2 == measurement1:
                slope_sign = 0
            else: 
                slope_sign = 1 if measurement2 > measurement1 else -1
            # print(f"measurement 1 = {(nsf.SciVal(measurement1, 'T'))}")
            # print(f"measurement 2 = {(nsf.SciVal(measurement2, 'T'))}")
            # print(f"{slope_sign=}")
        else:
            slope_sign = 1.0
            if target_field > self.reference_data.field_max or target_field < self.reference_data.field_min:
                self._last_msg =f"Error: target field out of possible field range. min={nsf.SciVal(self.reference_data.field_min, 'T')}, max={nsf.SciVal(self.reference_data.field_max, 'T')}"
                return False

        if slope_sign != 0.0:
            
            print("\nchange magnetic field...\n")

            if self.reference_data.is_reference_move_done:
                ref_i_gain = 0.1 
                ref_h_field = 0.7 #[T]
                i_gain = ref_i_gain*ref_h_field/self.reference_data.field_max
            else:
                i_gain = 0.1 

            keep_running = True
            current_field = self.get_current_h_field()
            while keep_running:
                current_field = self.get_current_h_field()
                keep_running = self._move_hook(current_field)    
    
                field_error = target_field - current_field

                # slow down if field is near to target
                if abs(field_error) <= 5e-3: 
                    i_gain_slowdown = 0.5
                else:
                    i_gain_slowdown = 1.0

                if abs(field_error) <= 0.1e-3: 
                    break

                speed = field_error*i_gain*i_gain_slowdown 

                # limit speed and convert to absolute value
                motor_speed = min(max(self.speed_min, abs(speed)), self.speed_max) 
                                
                # prepare moving direction
                direction = self.reference_data.full_turn_steps if field_error > 0.0 else -self.reference_data.full_turn_steps
                #print(f"{current_field=}, {field_error=}, {motor_speed=}, {direction=}, {i_gain=}, {i_gain_slowdown=}")
                
                # set output
                self._motor_controller.start_move_relative(int(direction*slope_sign), tmc_controller.from_normalized_speed(motor_speed))            

            self._motor_controller.motor_stop() 
            self._motor_controller.motor_driver_enable(motor = 0, enable = False)

            if keep_running:
                self._last_msg = "Target field reached"
            else:
                self._last_msg = "Adjusting aborted"
            return keep_running
        else:
            self._last_msg ="Error: Could not find moving direction"
            return False
    
    def move_to_pos(self, target_pos:float, speed:float) -> bool:
        """ Move motor to specified position. works only if referenced.
        
        Parameters
        ----------
            target_pos: float:
                position is relative to range: -1.0 is at minimum field, pos 1.0 at maximum field, 0.0 at zero field
            speed: float:
                moving speed. 1.0 means full speed
        """
        # print(f"target pos = {target_pos}")

        if self._is_in_simulation_mode:
            return True
        self._is_moving = True

        if self.reference_data.is_reference_move_done:

            max_pos_motor = self.reference_data.full_turn_steps / 4
            zero_pos_motor = self.reference_data.full_turn_steps / 4

            motor_speed = min(max(self.speed_min, abs(speed*self.speed_max)), self.speed_max) 
            motor_target_pos = min(max(0.0, zero_pos_motor + max_pos_motor*target_pos), zero_pos_motor + max_pos_motor) 
            # print(f"{motor_target_pos=}")
            self._motor_controller.motor_driver_enable(motor = 0, enable = True)
            self._motor_controller.start_move_to_absolute(motor_target_pos,tmc_controller.from_normalized_speed(motor_speed))

            keep_running = True
            while keep_running & self._motor_controller.is_motor_moving():
                current_field = self.get_current_h_field()
                keep_running = self._move_hook(current_field)    
    
            self._motor_controller.motor_stop() 
            self._motor_controller.motor_driver_enable(motor = 0, enable = False)

            if keep_running:
                self._last_msg = "Target position reached"
            else:
                self._last_msg = "Adjusting aborted"

            # print(f"{self._last_msg}")
            return keep_running

        else:
            self._last_msg ="Error: Motor not referenced"
            print(f"{self._last_msg}")
            return False
    
    def configuration_select(self, index:int):
        if index < 0 or index >= len(self.configurations):
            raise IndexError("Parameter 'index' is out of range")
        self._active_configuration = index
        self._scale_v_adc_to_tesla_square = self.configurations[self._active_configuration].cal_values[2]
        self._scale_v_adc_to_tesla_gain = self.configurations[self._active_configuration].cal_values[1]
        self._scale_v_adc_to_tesla_offset = self.configurations[self._active_configuration].cal_values[0]
    
    def configuration_selected(self) -> int:
        return self._active_configuration

    def configuration_load(self) -> bool:
        self._load_calibrations_from_sample_holder()
        if self._active_configuration >= len(self.configurations):
            self._active_configuration = -1

    def configuration_list(self) -> typing.List[str,]:
        return self.configurations
    
    def _get_active_config(self) -> VMFConfiguration:
        return self.configurations[self._active_configuration]

    def _set_active_config(self, config:VMFConfiguration):
        self.configurations[self._active_configuration] = config
        self.configuration_select(self._active_configuration)

    def _copy_configuration_from_sample_holder(self):
        self.configurations.clear()
        for index in range(len(self._chip_config_sample_holder.calib_name)):
            self.configurations.append(self.VMFConfiguration())
            self.configurations[index].name = self._chip_config_sample_holder.calib_name[index]
            self.configurations[index].cal_values.append(self._chip_config_sample_holder.calib_offset[index])
            self.configurations[index].cal_values.append(self._chip_config_sample_holder.calib_first_order[index])
            self.configurations[index].cal_values.append(self._chip_config_sample_holder.calib_second_order[index])
    
    def _load_calibrations_from_sample_holder(self) -> bool:
        self.configurations.clear()
        if self.is_sample_holder_connected():
            loaded = False
            if self._is_in_simulation_mode:
                self._chip_config_sample_holder.calib_name = ["Config_0","Config_1","Config_2","Config_3"]
                self._chip_config_sample_holder.calib_offset = [0.0, 0.1, 0.2, 0.3]
                self._chip_config_sample_holder.calib_first_order = [3.8, 3.8/2, 3.8/4, 3.8/8]
                self._chip_config_sample_holder.calib_second_order = [0.0, 0.0, 0.0, 0.0]
                self._chip_config_sample_holder.name = ["Sim0","Sim1","Sim2","Sim3"]
                loaded = True
            else:
                loaded = self._chip_config_sample_holder.load_config()
            self._copy_configuration_from_sample_holder()
            return loaded
        return False

    def _save_calibrations_to_sample_holder(self) -> bool:
        if self.is_sample_holder_connected():
            try:
                for index in range(len(self.configurations)):
                    cal_index = self._chip_config_sample_holder.calib_name.index(self.configurations[index].name) 
                    self._chip_config_sample_holder.calib_offset[cal_index] = self.configurations[index].cal_values[0]
                    self._chip_config_sample_holder.calib_first_order[cal_index] = self.configurations[index].cal_values[1]
                    self._chip_config_sample_holder.calib_second_order[cal_index] = self.configurations[index].cal_values[2]
                                   
                done = self._chip_config_sample_holder.store_config()    
                if done:
                    self._last_msg = "Done."
                else:
                    self._last_msg = "Error: Could not save calibration. Unknown low level chip access problem."
                return done
            except ValueError as e:
                self._last_msg = f"Error: Could not save calibration. Reason: {e}"
        else:
            self._last_msg = "Sample holder not connected"
        return False

    def _initialize_controller_eeprom(self, serial_no:str = "") -> bool:
        done = False
        chip_config_vmf_controller = VMFControllerConfig(bus_addr=0x57)
        if serial_no != "":
            chip_config_vmf_controller.sn_number = serial_no
        self._bus_master.assign_chip(chip_config_vmf_controller)
        if chip_config_vmf_controller.is_connected():
            done = chip_config_vmf_controller.store_config()
            if done:
                self._last_msg = "Successfully initialized VMF-Controller EEPROM"
            else:
                self._last_msg = "Error: Could not initialize VMF-Controller EEPROM"
        else:
            self._last_msg = "Error: Could not find VMF-Controller EEPROM"
        return done
    
    def _initialize_sample_holder_eeprom(self, serial_no:str = "") -> bool:
        done = False
        chip_config_vmf_holder = VMFSampleHolderConfig(bus_addr=0x56)
        if serial_no != "":
            chip_config_vmf_holder.sn_number = serial_no
        self._bus_master.assign_chip(chip_config_vmf_holder)
        if chip_config_vmf_holder.is_connected():
            done = chip_config_vmf_holder.store_config()
            if done:
                self._last_msg = "Successfully initialized VMF-Sample-Holder EEPROM"
            else:
                self._last_msg = "Error: Could not initialize VMF-Sample-Holder EEPROM"
        else:
            self._last_msg = "Error: Could not find VMF-Sample-Holder EEPROM"
        return done
    
    def _search_for_vmf_controller(self, serial_no:str, port_no:int) -> int:
        """ if serial_no is '' then device is searched and first found will be used
            if port_no is > 0  then the device has to be on specified port, otherwise it is searched on all ports and first device found will be used, 
        """
        available_masters = self._bus_master.get_list_of_available_interfaces()
        if len(available_masters) > 0:
            print("Found Accessory Interface. Searching VMF-Controller...")
            for ai_index in available_masters:
                if self._bus_master.connect(ai_index):
                    if port_no > 0:
                        self._bus_master.select_port(port_no)
                        return self._bus_master.is_slave_device_connected()
                    elif serial_no != "": # try to find specific device
                        return self._bus_master.select_port_with_slave(serial_no)
                    else: # or try to find any vmf-controller device connected
                        for port_no in range(1, self._bus_master.get_port_count()+1):
                            self._bus_master.select_port(port_no)
                            if self._bus_master.is_slave_device_connected():
                                try:
                                    slave_id = self._bus_master.get_slave_device_id()
                                    if "124" == slave_id.get_serial_number()[:3]:
                                        return True                  
                                except Exception as e:
                                    print(e)
                                    return False
        return False
    
    def _find_zero_position(self) -> int:
        """ Calculates the motor position where the field has its zero field cross with positive slope
            Returns
            -------
            motor_pos_of_zero_field: float
                position is negativ if zero field position could not be detected 
                otherwise it returns the motor position with zero field value
        """
        positive_zero_cross_position = -1
        amp_guess = abs(self.reference_data.field_max - self.reference_data.field_min) / 2.0
        offset_guess = (self.reference_data.field_max + self.reference_data.field_min) / 2.0
        frq_guess = 1.0 / abs(max(self.reference_data.reference_motor_pos) - min(self.reference_data.reference_motor_pos))
        p0 = np.array([amp_guess, frq_guess, 0, offset_guess])
        try:
            p_opt, *_ = opt.curve_fit(sine_fit, self.reference_data.reference_motor_pos, self.reference_data.reference_field_pos, p0)
            amp, freq, phase, _offset = p_opt
            # sometimes fit algorithm returns a negativ amplitude 
            if amp < 0.0:
                phase += np.pi
            
            # calc zero transition by derivative of sine wave     
            positive_zero_cross_position = -phase/2.0/np.pi/freq
            # depending on calculated phase the zero pos is negative, in this case we rotate one turn until we get positive values
            while positive_zero_cross_position < 0.0:
                positive_zero_cross_position += 1/freq
        except Exception:
            pass
        # print(f"{positive_zero_cross_position=}")
        return int(positive_zero_cross_position)

def sine_fit(t,a,f,p,o) -> float:
    return a*np.sin(2*np.pi*t*f+p)+o

