""" This is the screen of the module
Copyright Nanosurf AG 2021
License - MIT
"""

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
import nanosurf as nsf
from vmf_control import vmf_module

class CaibResultTableID(nsf.gui.nsf_tables.TableEntryIDs):
    """ identifier id are used in a nsf_table widget"""
    Items = 0
    last_data = 1
    mean_value = 2

DefaultComboGapConfig = [
    nsf.gui.NSFComboEntry(0,"Gap 0"),
    nsf.gui.NSFComboEntry(1,"Gap 1"),
    nsf.gui.NSFComboEntry(2,"Gap 2"),
    nsf.gui.NSFComboEntry(3,"Gap 3"),
    nsf.gui.NSFComboEntry(4,"Gap 4"),
    nsf.gui.NSFComboEntry(5,"Gap 5"),
    nsf.gui.NSFComboEntry(6,"Gap 6"),
    nsf.gui.NSFComboEntry(7,"Gap 7"),
    nsf.gui.NSFComboEntry(8,"Gap 8"),
    nsf.gui.NSFComboEntry(9,"Gap 9"),
    nsf.gui.NSFComboEntry(10,"Gap 10"),
]

class NSFHLine(QtWidgets.QFrame):
    def __init__(self, hidden : bool = False, height: int = 1,  **kargs):
        super().__init__(*kargs)
        self.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Plain)
        self.setStyleSheet(f"background-color:#{nsf.gui.nsf_colors.NSFColorHexStr.Soft_Gray};")
        self.setFixedHeight(height)
        self.setHidden(hidden)

class NSFPressAndReleaseButton(nsf.gui.NSFPushButton):
    press_event = QtCore.Signal()
    release_event = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.installEventFilter(self)
        
    def eventFilter(self, object, event:QtCore.QEvent):
        if self.isEnabled():
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                self.press_event.emit()
                return True
            elif event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                self.release_event.emit()
                return True
        return False

""" some useful list of allowed prefixes used by nsf_sci_edit widgets"""
allowed_count_units = [nsf.sci_val.up.Prefix.base]
allowed_time_units = [nsf.sci_val.up.Prefix.base, nsf.sci_val.up.Prefix.milli]
allowed_meter_units = [nsf.sci_val.up.Prefix.milli, nsf.sci_val.up.Prefix.micro, nsf.sci_val.up.Prefix.nano]
allowed_tesla_units = [nsf.sci_val.up.Prefix.milli, nsf.sci_val.up.Prefix.micro]

class VMFScreen(nsf.frameworks.qt_app.ModuleScreen):
    def __init__(self, screen_name: str = None, **kwargs):
        super().__init__(screen_name, **kwargs)
        self.module:vmf_module.VMFModule # give pylance a type hint

    def do_setup_screen(self, module: vmf_module.VMFModule):
        """ create here your gui with all controls and their layout"""
        self.module = module

        # left layout - main controls ------------------------------------------------------------

        self.combo_holder_setup = nsf.gui.NSFComboBox(DefaultComboGapConfig,"Sample Holder setup")


        self.scival_cur_h_field = nsf.gui.NSFSciEdit("Current H-Field")
        self.scival_cur_h_field.set_allowed_prefix_ids(allowed_tesla_units)
        self.scival_cur_h_field.set_prefix_id(nsf.sci_val.up.Prefix.milli)
        self.scival_cur_h_field.set_precision(2)
        self.scival_cur_h_field.set_unit("T")
        self.scival_cur_h_field.setEnabled(False)

        self.scival_target_h_field = nsf.gui.NSFSciEdit("Target H-Field")
        self.scival_target_h_field.set_allowed_prefix_ids(allowed_tesla_units)
        self.scival_target_h_field.set_prefix_id(nsf.sci_val.up.Prefix.milli)
        self.scival_target_h_field.set_precision(2)
        self.scival_target_h_field.set_unit("T")
        self.scival_target_h_field.set_value_min_max(-1.0, 1.0)

        self.button_move_left_slow = NSFPressAndReleaseButton("<")
        self.button_move_left = NSFPressAndReleaseButton("<<")
        self.button_move_right_slow = NSFPressAndReleaseButton(">")
        self.button_move_right = NSFPressAndReleaseButton(">>")

        self.label_referenced = nsf.gui.NSFEdit("")
        self.label_referenced.setEnabled(False)
        self.label_referenced.set_value("-")

        self.button_move_to_target = nsf.gui.NSFPushButton("")
        self.button_reference_move = nsf.gui.NSFPushButton("")

        self.layout_left = QtWidgets.QVBoxLayout()
        self.layout_setup = QtWidgets.QGridLayout()
        self.layout_setup.addWidget(self.scival_cur_h_field,0,0)
        self.layout_setup.addWidget(self.combo_holder_setup,0,1)
        self.layout_setup.addWidget(self.button_reference_move, 0,2, alignment=Qt.AlignmentFlag.AlignBottom)
        self.layout_setup.addWidget(self.label_referenced,0,3)
        for col in range(4):
            self.layout_setup.setColumnStretch(col,1)
        self.layout_left.addLayout(self.layout_setup)
        self.layout_left.addSpacing(10)
        self.layout_left.addWidget(NSFHLine())
        self.layout_left.addSpacing(10)
        self.layout_position = QtWidgets.QHBoxLayout()
        self.layout_position.addStretch()
        self.layout_position.addStretch()
        self.layout_position.addStretch()
        self.layout_left.addLayout(self.layout_position)
        self.layout_move = QtWidgets.QHBoxLayout()
        self.layout_move.addWidget(self.button_move_left)
        self.layout_move.addWidget(self.button_move_left_slow)
        self.layout_move.addWidget(self.button_move_right_slow)
        self.layout_move.addWidget(self.button_move_right)
        self.layout_left.addLayout(self.layout_move)
        self.layout_left.addSpacing(10)
        self.layout_left.addWidget(NSFHLine())
        self.layout_left.addSpacing(10)
        self.layout_target_field = QtWidgets.QGridLayout()
        self.layout_target_field.addWidget(self.scival_target_h_field,0,0)
        self.layout_target_field.addWidget(self.button_move_to_target, 0,1, alignment=Qt.AlignmentFlag.AlignBottom)
        self.layout_target_field.addWidget(QtWidgets.QLabel(),0,2)
        self.layout_target_field.addWidget(QtWidgets.QLabel(),0,3)
        for col in range(4):
            self.layout_target_field.setColumnStretch(col,1)
        
        self.layout_left.addLayout(self.layout_target_field)
        self.layout_left.addStretch()

        self.layout_right= QtWidgets.QVBoxLayout()

        # set GUI controls
        self.screen_layout = QtWidgets.QHBoxLayout()
        # stretch only plot area and keep controls fix in size
        self.screen_layout.addLayout(self.layout_left, 0)
        self.screen_layout.addLayout(self.layout_right,0)
        self.setLayout(self.screen_layout)

        self.bind_gui_elements()
        self.enter_gui_state_unref()
        self.update_referenced_state()
        self.update_sample_configuration()

    def bind_gui_elements(self):
        nsf.gui.connect_to_property(self.combo_holder_setup, self.module.settings.sample_holder_config)

        self.button_reference_move.clicked_event.connect(self.on_button_reference_clicked)    
        self.button_move_to_target.clicked_event.connect(self.on_button_start_stop_clicked)    
        self.button_move_right_slow.press_event.connect(self._on_button_move_right_slow)
        self.button_move_right.press_event.connect(self._on_button_move_right)
        self.button_move_right.release_event.connect(self._on_button_move_stop)
        self.button_move_right_slow.release_event.connect(self._on_button_move_stop)
        self.button_move_left_slow.release_event.connect(self._on_button_move_stop)
        self.button_move_left.release_event.connect(self._on_button_move_stop)
        self.button_move_left.press_event.connect(self._on_button_move_left)
        self.button_move_left_slow.press_event.connect(self._on_button_move_left_slow)
        self.module.sig_target_field_started.connect(lambda : self.enter_gui_state_active(button_to_keep_active=self.button_move_to_target))
        self.module.sig_target_field_ended.connect(self.enter_gui_state_idle)
        self.module.sig_reference_move_started.connect(lambda : self.enter_gui_state_active(button_to_keep_active=self.button_reference_move))
        self.module.sig_reference_move_ended.connect(self.update_referenced_state)
        self.module.sig_h_field_available.connect(self._on_new_h_field_available)
        self.module.sig_connecting_done.connect(self._on_connecting_done)
        self.module.sig_reference_state_changed.connect(self._on_reference_state_changed)

    def on_button_connect_clicked(self):
        self.module.start_connect_to_vmf_controller()

    def on_button_start_stop_clicked(self):
        self.enter_gui_state_wait()
        if self.module.is_moving():
            self.module.stop_moving()
        else:
            self.module.start_move_to_field(self.scival_target_h_field.value())

    def on_button_reference_clicked(self):
        self.button_reference_move.setEnabled(False)
        self.enter_gui_state_wait()
        if self.module.is_moving():
            self.module.stop_moving()
        else:
            self.module.start_reference_move()

    def _on_button_move_right(self):
        self.module.start_move(direction_forward=True,speed=0.02)

    def _on_button_move_right_slow(self):
        self.module.start_move(direction_forward=True,speed=0.0005)

    def _on_button_move_left(self):
        self.module.start_move(direction_forward=False,speed=0.02)

    def _on_button_move_left_slow(self):
        self.module.start_move(direction_forward=False,speed=0.0005)

    def _on_button_move_stop(self):
        self.module.stop_moving()

    def _on_new_h_field_available(self, new_val:float):
        self.scival_cur_h_field.set_value(new_val)

    def _on_connecting_done(self):
        if self.module.is_vmf_ready():
            self.update_sample_configuration()

    def _on_reference_state_changed(self):
        self.update_referenced_state()

    def update_referenced_state(self):
        if self.module.is_referenced():
            self.update_min_max_h_field()
            self.label_referenced.set_value("Referenced")
            self.enter_gui_state_idle()
        else:
            self.label_referenced.set_value("Not referenced")
            self.enter_gui_state_unref()

    def enter_gui_state_wait(self):
        self.set_parameter_widget_enable_state(enabled=False)
        self.start_stop_button_state(wait=True)        
        self.reference_button_state(wait=True)

    def enter_gui_state_active(self, button_to_keep_active=None):
        self.set_parameter_widget_enable_state(enabled=False, active_button=button_to_keep_active)
        if button_to_keep_active is self.button_move_to_target:
            self.start_stop_button_state(wait=False, stop_state=self.module.is_moving())
        if button_to_keep_active is self.button_reference_move:
            self.reference_button_state(wait=False, stop_state=self.module.is_moving())

    def enter_gui_state_unref(self):
        self.set_parameter_widget_enable_state(enabled=False)
        self.start_stop_button_state(wait=True, stop_state=self.module.is_moving())
        self.reference_button_state(wait=False, stop_state=self.module.is_moving())
        self.combo_holder_setup.setEnabled(True)

    def enter_gui_state_idle(self):
        self.set_parameter_widget_enable_state(enabled=True)
        self.start_stop_button_state(wait=False, stop_state=self.module.is_moving())
        self.reference_button_state(wait=False, stop_state=self.module.is_moving())

    def set_parameter_widget_enable_state(self, enabled: bool = True, active_button=None):
        self.scival_target_h_field.setEnabled(enabled)
        self.combo_holder_setup.setEnabled(enabled)
        self.button_move_left.setEnabled(enabled)
        self.button_move_left_slow.setEnabled(enabled)
        self.button_move_right.setEnabled(enabled)
        self.button_move_right_slow.setEnabled(enabled)
        self.button_reference_move.setEnabled(enabled and (active_button is self.button_reference_move))
        self.button_move_to_target.setEnabled(enabled and (active_button is self.button_move_to_target))

    def reference_button_state(self, wait: bool = False, stop_state: bool = False):
        if wait:
            self.button_reference_move.setEnabled(False)
            self.button_reference_move.set_label("Wait...")
        else:
            self.button_reference_move.setEnabled(True)
            self.button_reference_move.set_label("Stop" if stop_state else "Reference")

    def start_stop_button_state(self, wait: bool = False, stop_state: bool = False):
        if wait:
            self.button_move_to_target.setEnabled(False)
            self.button_move_to_target.set_label("Wait...")
        else:
            self.button_move_to_target.setEnabled(True)
            self.button_move_to_target.set_label("Stop" if stop_state else "Move to target field")

    def update_min_max_h_field(self):
        if self.module.is_referenced():
            h_min, h_max = self.module.get_min_max_field()
            self.module.logger.info(f"New min_h_field = {h_min}, h_max_field={h_max} set to target_h_field entry field.")
            self.scival_target_h_field.set_value_min_max(h_min, h_max)
        else:
            self.module.logger.warning("Update_min_max_h_field called while not referenced.")

    def update_sample_configuration(self):
        config_list = self.module.get_sample_holder_configurations()
        new_combo_list = [ nsf.gui.NSFComboEntry(i,name) for i, name in enumerate(config_list)]
        self.combo_holder_setup.define_entries(new_combo_list)
