import napari
import numpy as np
from collections import deque
from magicgui.widgets import (
    Container,
    TextEdit,
    Checkbox,
    Table,
    PushButton,
    FileEdit
)
from datetime import datetime
from napari_builtins import io


class EventMonitor(Container):
    SCREEN_WIDTH = 600
    RECENT_LENGTH = 10
    COLUMN_WIDTHS = [100, 100, 300]
    MAX_STRING_LENGTH = 100

    def __init__(self, viewer: "napari.viewer.Viewer"):
        """
        Initializes the event monitor onto a specific viewer.

        Args:
            viewer (_type_): Attach the monitor to a specific viewer.
        """
        super().__init__(label=False)  # Initialize the Container first

        self.native.setMinimumWidth(self.SCREEN_WIDTH)
        self._viewer = viewer
        self.event_log = []
        self.recent_events = deque(maxlen=self.RECENT_LENGTH)
        self.event_attributes_list = deque(maxlen=self.RECENT_LENGTH)

        self.horizontalbox = Container(layout="horizontal")

        # Widgets
        self.tablewidget = Table(value=list(self.recent_events))
        selection_event = self.tablewidget.native.selectionModel()
        selection_event.currentChanged.connect(self._view_attributes)

        self.mouse_events_cbox = Checkbox(label="Include Mouse Events")
        self.status_events_cbox = Checkbox(label="Include Status Bar Events")
        checkboxes = [self.mouse_events_cbox, self.status_events_cbox]
        self.horizontalbox.extend(checkboxes)
        self.clearbutton = PushButton(text="Clear Event Logs")
        self.textwidget = TextEdit(value="")
        self.filechooser = FileEdit(mode="w")
        self.savebutton = PushButton(text="Save Event Reference")

        # Creating the GUI layout
        self.extend([self.tablewidget,
                     self.clearbutton,
                     self.horizontalbox,
                     self.textwidget,
                     self.filechooser,
                     self.savebutton])
        self.setup_monitoring()
        self.savebutton.clicked.connect(self.save_events)
        self.clearbutton.clicked.connect(self.clear_events)

    def setup_monitoring(self):
        # Monitor viewer events
        self._monitor_object_events(self._viewer, "viewer")
        self._monitor_object_events(self._viewer.camera, "viewer.camera")
        self._monitor_object_events(self._viewer.camera, "viewer.cursor")
        self._monitor_object_events(self._viewer.camera, "viewer.dims")
        self._monitor_object_events(self._viewer.camera, "viewer.tooltip")
        self._monitor_object_events(self._viewer.camera, "viewer.grid")

        # Monitor layer events
        self._monitor_object_events(self._viewer.layers, "layers")
        # self._check_existing_layers()

        # Monitor individual layers as they're added
        self._viewer.layers.events.inserted.connect(self._on_layer_added)

        # Monitor mouse events
        self._viewer.mouse_drag_callbacks.append(self._log_mouse_event)
        self._viewer.mouse_move_callbacks.append(self._log_mouse_event)
        self._viewer.mouse_wheel_callbacks.append(self._log_mouse_event)

    def _monitor_object_events(self, obj, event_monitor):
        """
        Cycles through an event EmitterGroup and adds an event
        to a row of the widget table.

        Parameters
        ----------
        obj : TYPE
            DESCRIPTION.
        event_monitor : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if hasattr(obj, "events"):
            for event_name in obj.events:
                event = getattr(obj.events, event_name)
                event_string = self.get_event_string(event_monitor, event_name)
                event.connect(
                    lambda e, en=event_string: self._log_event(e, en)
                )
                # getting class name - .__cls__.name

    def _check_existing_layers(self):
        for layer in self._viewer.layers:
            self._monitor_object_events(layer)

    def _log_event(self, event, event_string):
        mouse_events_disabled = not self.mouse_events_cbox.get_value()
        status_events_disabled = not self.status_events_cbox.get_value()
        if ("mouse" in event_string and mouse_events_disabled):
            return
        if ("status" in event_string and status_events_disabled):
            return
        self.record_event_data(self.event_log, event_string)
        self.record_event_data(self.recent_events, event_string, event=event)
        self.tablewidget.set_value(list(self.recent_events))

        #
        if len(self.event_log) >= self.RECENT_LENGTH:
            recent_range = range(len(self.event_log)-self.RECENT_LENGTH,
                                 len(self.event_log))
            indices = list(recent_range)
            self.tablewidget.row_headers = indices
        native_table = self.tablewidget.native

        # Dynamic TableWidget formatting
        native_table.scrollToBottom()
        native_table.setColumnWidth(0, self.COLUMN_WIDTHS[0])
        native_table.setColumnWidth(1, self.COLUMN_WIDTHS[1])
        native_table.setColumnWidth(2, self.COLUMN_WIDTHS[2])

    def _view_attributes(self, current):
        if current.isValid():
            row_index = current.row()
            self.textwidget.set_value(self.event_attributes_list[row_index])
        else:
            self.textwidget.set_value("")

    def record_event_attributes(self, event, event_string):
        event_attributes = []
        event_attributes.append(f"<b><u>{event_string}</b></u>")
        for attr in dir(event):
            if not attr.startswith("_"):
                attribute_string = f"event.{attr} = {getattr(event, attr)}"
                if len(attribute_string) > self.MAX_STRING_LENGTH:
                    attribute_string = f"event.{attr} = output too long"
                event_attributes.append(attribute_string)
        event_attributes_string = "<br>".join(event_attributes)
        self.event_attributes_list.append(event_attributes_string)

    def record_event_data(self, log, event_string, event=None):
        event_time = datetime.now().strftime(format="%H:%M:%S.%f")[:-3]
        log.append({"Event": event_string.split(".")[-1],
                    "Time": event_time,
                    "API": event_string})
        if event is not None:
            self.record_event_attributes(event, event_string)

    def get_event_string(self, event_monitor, event_name):
        return f"{event_monitor}.events.{event_name}"

    def _log_mouse_event(self, a, event):
        self._log_event(event, f"{event.type}")

    def _on_layer_added(self, event):
        layer = event.value
        self._monitor_object_events(layer, "viewer."+event.value._name)

    def save_events(self):
        list_of_events = []
        list_of_events.append(list(self.event_log[0].keys()))
        for entry in self.event_log:
            list_of_events.append(list(entry.values()))

        if self.filechooser.get_value().is_file():
            io.write_csv(self.filechooser.get_value(), list_of_events)
        else:
            self._viewer.status = "Choose a file first"

    def clear_events(self):
        self.event_log = []
        self.recent_events = deque(maxlen=self.RECENT_LENGTH)
        self.tablewidget.set_value(list(self.recent_events))


# Usage
if __name__ == "__main__":
    viewer = napari.Viewer()
    monitor = EventMonitor(viewer)
    viewer.window.add_dock_widget(monitor)

    features = {"confidence": np.array([1])}

    text = {
        "string": "Confidence is {confidence:.2f}",
        "size": 20,
        "color": "blue",
        "translation": np.array([-30, 0]),
    }

    viewer.add_image(np.random.random((100, 100)))
    viewer.add_points([0, 10], features=features, text=text)
    napari.run()
