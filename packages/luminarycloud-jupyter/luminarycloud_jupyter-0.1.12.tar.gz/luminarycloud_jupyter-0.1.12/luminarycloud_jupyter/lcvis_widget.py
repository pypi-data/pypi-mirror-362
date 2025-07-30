import logging
import anywidget
import array
import pathlib
import traitlets
import json
import glob
import requests
from typing import Any, Optional, TYPE_CHECKING
from luminarycloud.vis.display import DisplayAttributes, ColorMap
from luminarycloud.enum.vis_enums import visquantity_text, SceneMode
from luminarycloud._proto.api.v0.luminarycloud.vis import vis_pb2

from luminarycloud_jupyter.vis_enums import (
    field_component_to_lcvis,
    representation_to_lcvis,
)

if TYPE_CHECKING:
    # We need to be careful w/ this import for typing otherwise
    # we'll introduce a circular import issue
    from luminarycloud.vis import Scene

base_path = pathlib.Path(__file__).parent / "static"


class LCVisWidget(anywidget.AnyWidget):
    _esm: pathlib.Path = base_path / "lcvis.js"

    # If the frontend widget is up and ready to receive a workspace state
    frontend_ready_for_workspace: bool = False

    # If the workspace execution is complete and the widget is ready
    # to receive other commands.
    workspace_execution_done: bool = False

    # If workspace state was set before the frontend was ready
    # we buffer the command til we get ready_for_workspace from the Wasm
    # Now we support two workspaces: one for isComparator=False, one for isComparator=True
    # TODO: If we plan to support more than 2 scenes to compare, use an index (idx) as the key here.
    buffered_workspaces: dict[bool, dict] = {}

    # Commands we need to buffer up because calls were made
    # before the widget was ready. The normal Jupyter comm stuff
    # doesn't buffer messages before the widget is up, they just get
    # discarded
    buffered_commands: list[dict] = []

    scene_mode: traitlets.Unicode = traitlets.Unicode().tag(sync=True)

    last_screenshot: Optional[bytes] = None

    camera_position: traitlets.List = traitlets.List().tag(sync=True)
    camera_look_at: traitlets.List = traitlets.List().tag(sync=True)
    camera_up: traitlets.List = traitlets.List().tag(sync=True)
    camera_pan: traitlets.List = traitlets.List().tag(sync=True)

    # TODO will: we should also expose pan as a param on the camera

    def __init__(self, scene_mode: SceneMode, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.scene_mode = scene_mode
        self.on_msg(self.receive_widget_message)

    def receive_widget_message(self, widget: Any, content: str, buffers: list[memoryview]) -> None:
        if content == "screenshot_taken":
            self.last_screenshot = buffers[0]
        elif content == "set_scene_mode":
            new_scene_mode = buffers[0].tobytes().decode("utf-8")

            self.scene_mode = new_scene_mode

        elif content == "ready_for_workspace":
            self.frontend_ready_for_workspace = True
            # Send all buffered workspaces if we have them
            if self.buffered_workspaces:
                for is_comparator, workspace in self.buffered_workspaces.items():
                    self.send(
                        {
                            "cmd": workspace["cmd"],
                            "workspaceState": workspace["workspaceState"],
                            "isComparator": is_comparator,
                        },
                        workspace["buffers"],
                    )
        elif content == "workspace_execution_done":
            self.workspace_execution_done = True
            self._send_buffered_commands()
        elif content == "load_wasm":
            # We don't know the name of the wasm file until build
            # since it comes from the npm package
            wasm_file = glob.glob("*.wasm", root_dir=base_path)
            # TODO will: We need some way to report errors back out, these just
            # get lost since its in some message handler.
            if len(wasm_file) == 0:
                raise Exception("Failed to find expected packaged Wasm file")
            wasm = (base_path / wasm_file[0]).read_bytes()
            # Note: When we merge with the buffering PR, this send
            # should not be buffered, b/c the widget is up at this point
            # and sent us this message and we need the wasm there before
            # it can complete loading LCVis and tell us its ready for buffered cmds
            self.send({"cmd": "load_wasm"}, [wasm])

    def set_workspace_state(
        self,
        scene: "Scene",
        render_data_urls: vis_pb2.GetRenderDataUrlsResponse,
        isComparator: bool,
    ) -> None:
        self.workspace_execution_done = False
        workspace_state = json.loads(render_data_urls.workspace_state)

        filter_urls = {}
        filter_data = []
        for i in range(len(render_data_urls.urls.filter_ids)):
            filter_id = render_data_urls.urls.filter_ids[i]
            url = render_data_urls.urls.data_files[i].signed_url
            # TODO: We should send back to the Python side if we're in the
            # frodo env or not, then we could skip fetching data in Python
            # and just fetch it in the FE instead to be more efficient.
            filter_urls[filter_id] = {
                "url": url,
                # What buffer index this filter's data is in
                "bufferId": i,
            }
            # For portability to standalone widget environments we download
            # the render data in Python and send it to the frontend. This
            # avoids the HTTP requests for the render data being blocked due to
            # CORS restrictions when made on the frontend
            # Track which buffer goes to which filter
            data = requests.get(url).content
            filter_data.append(data)

        workspace_state["filters_to_url"] = filter_urls

        if self.frontend_ready_for_workspace:
            self.send(
                {
                    "cmd": "set_workspace_state",
                    "workspaceState": json.dumps(workspace_state),
                    "isComparator": isComparator,
                },
                filter_data,
            )

        # when widget is re-mounted we need to send the workspace state
        self.buffered_workspaces[isComparator] = {
            "cmd": "set_workspace_state",
            "workspaceState": json.dumps(workspace_state),
            "buffers": filter_data,
            "isComparator": isComparator,
        }

    def take_screenshot(self) -> None:
        self.last_screenshot = None
        self._send_or_buffer_cmd({"cmd": "screenshot"})

    def set_surface_visibility(self, surface_id: str, visible: bool) -> None:
        self._send_or_buffer_cmd(
            {
                # TODO: put these in some shared JSON defs/constants file for cmds?
                "cmd": "set_surface_visibility",
                "surfaceId": surface_id,
                "visible": visible,
            }
        )

    def set_surface_color(self, surface_id: str, color: list[float]) -> None:
        if len(color) != 3:
            raise ValueError("Surface color must be list of 3 RGB floats, in [0, 1]")
        if any(c < 0 or c > 1 for c in color):
            raise ValueError("Surface color must be list of 3 RGB floats, in [0, 1]")
        self._send_or_buffer_cmd(
            {
                # TODO: put these in some shared JSON defs/constants file for cmds
                "cmd": "set_surface_color",
                "surfaceId": surface_id,
            },
            buffers=[array.array("f", color).tobytes()],
        )

    def set_display_attributes(self, object_id: str, attrs: DisplayAttributes) -> None:
        cmd = {
            "cmd": "set_display_attributes",
            "objectId": object_id,
            "visible": attrs.visible,
            "representation": representation_to_lcvis(attrs.representation),
        }
        if attrs.field:
            cmd["field"] = {
                "name": visquantity_text(attrs.field.quantity),
                "component": field_component_to_lcvis(attrs.field.component),
            }
        self._send_or_buffer_cmd(cmd)

    def set_color_map(self, color_map: ColorMap) -> None:
        cmd = {
            "cmd": "set_color_map",
            "field": {
                "name": visquantity_text(color_map.field.quantity),
                "component": field_component_to_lcvis(color_map.field.component),
            },
            "min": color_map.data_range.min_value,
            "max": color_map.data_range.max_value,
        }
        self._send_or_buffer_cmd(cmd)

    def reset_camera(self) -> None:
        self._send_or_buffer_cmd({"cmd": "reset_camera"})

    def set_triad_visible(self, visible: bool) -> None:
        self._send_or_buffer_cmd({"cmd": "set_triad_visible", "visible": visible})

    def _send_or_buffer_cmd(self, cmd: dict, buffers: list[bytes] | None = None) -> None:
        """
        If command-based calls are made before the widget is ready we need
        to buffer them and wait til the widget is ready to receive them. Otherwise,
        the default Jupyter comm support doesn't buffer them and the commands are
        simply discarded.
        """
        if self.workspace_execution_done:
            # If we're sending the command immediately, trigger a re-render
            cmd["rerender"] = True
            self.send(cmd, buffers)
        else:
            # If we're buffering the commands we don't want to render the partially
            # applied state, so force all to be false, we'll send a rerender command
            # at the end of the buffer
            cmd["rerender"] = False
            self.buffered_commands.append({"cmd": cmd, "buffers": buffers})

    def _send_buffered_commands(self) -> None:
        if not self.workspace_execution_done:
            logging.error("Cannot send buffered commands before frontend is ready")
            return

        for cmd in self.buffered_commands:
            self.send(cmd["cmd"], cmd["buffers"])
        # We don't re-render when running buffered commands to not show
        # the intermediate states, now that we've flushed the buffer send an
        # explicit re-render command.
        self.send({"cmd": "render_frame"})
        self.buffered_commands = []
