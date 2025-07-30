"""Manage the user interface for the workcell.

This class is responsible for connecting to the RoboticsUI and handling
interactions with the UI:
  - Creates buttons and console windows for launching processes
  - Submits tickets via orca
  - Sets and logs workcell status and operator events
  - Observes the status of data collection and handles login and logout timeout
"""

import datetime
import os
import pathlib
import shutil
import threading
import time

from watchdog import events
from watchdog import observers

from safari_sdk.orchestrator.helpers import orchestrator_helper
from safari_sdk.protos.ui import robotics_ui_pb2
from safari_sdk.ui import client
from safari_sdk.workcell import constants
from safari_sdk.workcell import operator_event_lib
from safari_sdk.workcell import operator_event_logger_lib
from safari_sdk.workcell import process_launcher_lib
from safari_sdk.workcell import single_instance_lib
from safari_sdk.workcell import ticket_lib


_TIMEOUT_SECONDS: float = 30 * 60
_OBSERVER_DIR: str = "/persistent/logs/robup/in/"

status_event_map = operator_event_lib.workcell_status_event_dict
workcell_status_list = [
    status.value for status in operator_event_lib.WorkcellStatus
]


class SynchronizedPair:

  def __init__(self, status: str, logout_status: str):
    self.status = status
    self.logout_status = logout_status

  def update_status_pair(self, status: str, logout_status: str) -> None:
    self.status = status
    self.logout_status = logout_status


def get_y_position(height: float, idx: int) -> float:
  return (1 - height / 2) - height * idx


class WorkcellManager:
  """Manage starting and stopping of processes."""
  _timeout_thread: threading.Thread = None
  _timeout_stop_event: threading.Event = None
  _timeout_start_time: float = 0
  _login_time: float = 0
  _accumulated_successful_episode_time: float = 0
  _accumulated_total_episode_time: float = 0
  _login_thread: threading.Thread = None
  _observer: observers.Observer = None
  workcell_status_pair = SynchronizedPair(
      status="Task Setup/Change", logout_status="Available"
  )
  _robotics_platform: str = "NotSpecified"
  # Preferred method of get/set current operator ID.
  _orca_helper: orchestrator_helper.OrchestratorHelper | None
  _check_disk_space_thread: threading.Thread = None
  _total_space_gb: float = 0
  process_launcher: process_launcher_lib.ProcessLauncher | None = None

  def __init__(
      self,
      robotics_platform: str,
      project_id: str,
      robot_id: str,
      hostname: str,
      port: int,
      event_logger: operator_event_logger_lib.OperatorEventLogger,
      use_singleton_lock: bool = False,
  ):
    self.hostname: str = hostname
    self._port = port
    lock_file = pathlib.Path(constants.SINGLE_INSTANCE_LOCK_FILE)
    self.use_singleton_lock = use_singleton_lock
    self.single_instance = single_instance_lib.SingleInstance(
        lock_file, self.use_singleton_lock
    )
    self.ui_exists: bool = False
    self.ui: client.Framework = client.Framework(
        callbacks=self.UiCallbacks(self),
    )
    self.ui.connect(host=self.hostname, port=self._port)
    self.ui.register_client_name("workcell_manager")
    self.dropdown_value: str = None
    self.login_user: str = None
    self._robotics_platform = robotics_platform
    print(f"robotics_platform: {robotics_platform}")
    self.project_id = project_id
    print(f"project_id: {self.project_id}")
    self.robot_id = robot_id
    print(f"robot_id: {self.robot_id}")
    self.event_logger = event_logger
    self.restore_operator_status()
    self.update_timeout_process()
    self.start_orca_connection()

    # Get the total disk space.
    try:
      disk_usage = shutil.disk_usage("/isodevice")
      self._total_space_gb = disk_usage.total / constants.SIZE_OF_GB
      if self._total_space_gb == 0:
        raise OSError("Total disk space is 0, aborting.")
    except OSError as e:
      print(f"Error checking disk space: {e}.")

  def start_orca_connection(self) -> None:
    """Starts the orca process."""
    self._orca_helper = orchestrator_helper.OrchestratorHelper(
        robot_id=self.robot_id,
        job_type=orchestrator_helper.JOB_TYPE.ALL,
        raise_error=False,
    )
    response = self._orca_helper.connect()
    if response.success:
      response = self._orca_helper.get_current_connection()
      orca_service = response.server_connection
      self.orca_client = ticket_lib.get_ticket_cli(
          project_id=self.project_id,
          orca_service=orca_service,
      )
      print(f"Created orca client for project: {self.project_id}")
      self.ui.create_button_spec(
          constants.CREATE_TICKET_BUTTON_ID,
          constants.CREATE_TICKET_BUTTON_LABEL,
          spec=constants.create_ticket_button_spec,
      )
    else:
      self._orca_helper = None
      self.orca_client = ticket_lib.DummyTicketCli()
      print(
          f"Failed to connect to Orchestrator Service: {response.error_message}"
      )

  def restore_operator_status(self) -> None:
    """Restores the operator status from the status file."""
    op_status_file = pathlib.Path(constants.OPERATOR_EVENT_STATUS_FILE)
    if op_status_file.is_file():
      op_status_txt = op_status_file.read_text()
      if not op_status_txt or op_status_txt not in status_event_map:
        last_status = operator_event_lib.WorkcellStatus.AVAILABLE.value
        logout_status = status_event_map[last_status].logout_status.value
        print(
            "Operator status file found but was empty or had invalid content:"
            f" '{op_status_txt}'. Using default status: {last_status}"
        )
      else:
        last_status = op_status_txt
        print(f"Operator status file found: {op_status_txt}")
        logout_status = status_event_map[last_status].logout_status.value
      self.workcell_status_pair.update_status_pair(
          status=last_status, logout_status=logout_status
      )
    else:
      last_status = operator_event_lib.WorkcellStatus.AVAILABLE.value
      logout_status = status_event_map[last_status].logout_status.value
      print(
          f"Operator status file not found. Using default status: {last_status}"
      )
      self.workcell_status_pair.update_status_pair(
          status=last_status, logout_status=logout_status
      )

  def get_robotics_platform(self) -> str:
    return self._robotics_platform

  class UiCallbacks(client.UiCallbacks):
    """Callbacks for the project."""

    def __init__(self, script: "WorkcellManager"):
      """Stores a reference to the outer script."""
      self.script = script
      self.troubleshooting_choices: list[str] = [
          "Hardware Failure",
          "Unexpected Software Behavior",
          "Unexpected Robot Behavior",
          "Waiting for Eval Fix",
          "Calibration",
          "Task Feasibiity",
      ]
      self.troubleshooting_hardware_failure_choices: list[str] = [
          "Finger",
          "Hand",
          "Wrist",
          "Wrist Camera",
          "Head Camera",
          "Other",
      ]

    def init_screen(self, ui: client.Framework):
      """Called when the connection is made."""
      self.script.ui = ui
      print("I connected to the RoboticsUI!")
      self.script.create_operator_event_gui_elements()
      self.script.ui_exists = True
      self.script.ui.register_remote_command(
          "enable-dropdown-shortcuts",
          "Enable keyboard shortcuts for the workcell status dropdown."
      )
      self.script.ui.register_remote_command(
          "disable-dropdown-shortcuts",
          "Disable keyboard shortcuts for the workcell status dropdown."
      )

    def console_data_received(self, command: str):
      match command.strip():
        case "enable-dropdown-shortcuts":
          self.script.set_dropdown_shortcuts(True)
        case "disable-dropdown-shortcuts":
          self.script.set_dropdown_shortcuts(False)
        case _:
          pass

    def teleop_received(
        self, teleop_message: robotics_ui_pb2.TeleopMessage
    ) -> None:
      """Prevent teleop broadcast from spamming the terminal."""
      return

    def button_pressed(self, button_id: str) -> None:
      """Called when a button is pressed."""
      if self.script.process_launcher is not None:
        self.script.process_launcher.button_pressed(button_id)
      if button_id == constants.OPERATOR_LOGOUT_BUTTON_ID:
        self.script.logout()
        return
      if button_id == constants.CREATE_TICKET_BUTTON_ID:
        ticket_lib.fill_ticket_form(
            self.script.ui, self.script.robot_id
        )
        print("done with  action change")

    def dialog_pressed(self, dialog_id: str, choice: str) -> None:
      """Called when a dialog is submitted."""
      if self.script.process_launcher is not None:
        self.script.process_launcher.dialog_pressed(dialog_id, choice)

    def dropdown_pressed(
        self,
        dropdown_id: str,
        choice: str | list[str],
    ) -> None:
      """Called when one of the dropdown option is submitted."""
      # Execute below dropdown process only if the call originates from
      # the operator event dropdown
      if dropdown_id == constants.OPERATOR_EVENT_DROPDOWN_ID:
        print(f"Submission received for {dropdown_id}: {choice}")
        logout_status = status_event_map[choice].logout_status.value
        self.script.workcell_status_pair.update_status_pair(
            status=choice,
            logout_status=logout_status,
        )
        # Long term: workcell_status_pair should take a function object to set
        # the definition of update_status_pair, so update_timeout_process gets
        # called automatically whenever update_status_pair is.
        self.script.update_timeout_process()
        self.script.update_dropdown_value(choice)
        if (
            choice
            == operator_event_lib.WorkcellStatus.TROUBLESHOOTING_TESTING.value
        ):
          self.script.ui.create_dropdown(
              dropdown_id=constants.TROUBLESHOOTING_DROPDOWN_ID,
              title="Selection",
              msg="Please select a troubleshooting item:",
              choices=self.troubleshooting_choices,
              submit_label="Submit",
              spec=robotics_ui_pb2.UISpec(width=0.3, height=0.3, x=0.5, y=0.5),
          )
        else:
          self.script.event_logger.create_workcell_status_event(
              event=choice, event_data="ops status"
          )
          self.script.event_logger.write_event()
          print("done with non-troubleshooting dropdown action change")
      elif dropdown_id == constants.TROUBLESHOOTING_DROPDOWN_ID:
        if choice == "Hardware Failure":
          self.script.ui.create_dropdown(
              dropdown_id=constants.TROUBLESHOOTING_HARDWARE_FAILURE_DROPDOWN_ID,
              title="Selection",
              msg="Please select a hardware failure item:",
              choices=self.troubleshooting_hardware_failure_choices,
              submit_label="Submit",
              spec=robotics_ui_pb2.UISpec(width=0.3, height=0.3, x=0.5, y=0.5),
          )
        else:
          ops_event_data = choice
          self.script.event_logger.create_workcell_status_event(
              event=operator_event_lib.WorkcellStatus.TROUBLESHOOTING_TESTING.value,
              event_data=ops_event_data,
          )
          self.script.event_logger.write_event()
          print("done with troubleshooting dropdown action change")
      elif (
          dropdown_id == constants.TROUBLESHOOTING_HARDWARE_FAILURE_DROPDOWN_ID
      ):
        ops_event_data = choice
        self.script.event_logger.create_workcell_status_event(
            event=operator_event_lib.WorkcellStatus.TROUBLESHOOTING_TESTING.value,
            event_data=ops_event_data,
        )
        self.script.event_logger.write_event()
        print(
            "done with troubleshooting hardware failure dropdown action change"
        )
      else:
        print(f"Unsupported dropdown choice: {dropdown_id}")

    def prompt_pressed(self, prompt_id: str, data: str) -> None:
      """Called when one of the prompt option is submitted."""
      print(f"\n\nSubmission received for {prompt_id}: {data}")

      if prompt_id == constants.OPERATOR_NOTES_PROMPT_ID:
        self.script.event_logger.create_ui_event(
            event=operator_event_lib.UIEvent.OTHER_EVENT.value,
            event_data=data,
        )
        self.script.event_logger.write_event()
        print("done with prompt action change")
      elif prompt_id == constants.OPERATOR_LOGIN_BUTTON_ID:
        self.script.login_with_user_id(data)

    def form_pressed(self, form_id: str, results: str):
      """Called when a form is submitted."""
      if form_id == "ticket_form":
        self.script.ui.create_chat(
            chat_id="create_ticket_window",
            title="Ticket Status",
            submit_label="",
            spec=robotics_ui_pb2.UISpec(
                x=0.4,
                y=0.7,
                width=0.4,
                height=0.4,
                disabled=True,
            ),
        )
        ticket_valid, ticket_error_message = ticket_lib.is_valid_ticket_form(
            results
        )
        if not ticket_valid:
          self.script.ui.add_chat_line(
              chat_id="create_ticket_window",
              text=ticket_error_message,
          )
          return

        results = ticket_lib.prepare_ticket_form_for_user(
            results, login_user=self.script.login_user
        )
        try:
          ticket_submission_instant = datetime.datetime.now()
          formatted_ticket_submission_instant = (
              ticket_submission_instant.strftime("%Y-%m-%d %H:%M:%S")
          )
          ticket_id = self.script.orca_client.submit_ticket(results)
          self.script.ui.add_chat_line(
              chat_id="create_ticket_window",
              text=(
                  f"{formatted_ticket_submission_instant}: Submitted ticket"
                  f" with id: {ticket_id}\n"
              ),
          )
          print("done with ticket submission action change")
        except NotImplementedError as e:
          self.script.ui.add_chat_line(
              chat_id="create_ticket_window",
              text=f"Failed to submit ticket: {e}",
          )

    def ui_connection_died(self) -> None:
      print("Lost UI connection.")
      time.sleep(5)
      print("Shutting down process launcher.")
      self.script.ui_exists = False

  def stop(self) -> None:
    """Stops the process."""
    if self.process_launcher is not None:
      self.process_launcher.stop()
    self.ui.shutdown()
    self.stop_disk_space_check_thread()
    self.stop_timeout_thread()
    self.stop_login_thread()
    self.stop_observer()
    print("Stopping workcell manager.")

  def create_operator_event_gui_elements(self) -> None:
    """Creates workcell and operator event logging GUI elements."""
    # read the status from possible filepaths.
    initial_value = operator_event_lib.WorkcellStatus.AVAILABLE.value
    for filename in constants.OPERATOR_EVENT_FILEPATHS:
      op_status = pathlib.Path(os.path.expanduser(filename))
      if op_status.is_file():
        op_status_txt = op_status.read_text()
        print(f"Found op status file: {filename} op status: {op_status_txt}")
        initial_value = op_status_txt
        break
      else:
        print(f"No op status file found: {filename}")

    self.ui.create_dropdown(
        dropdown_id=constants.OPERATOR_EVENT_DROPDOWN_ID,
        title="Status Options",
        msg="Select Event Type",
        choices=workcell_status_list,
        submit_label="Submit",
        spec=constants.STATUS_DROPDOWN_SPEC,
        initial_value=initial_value
    )
    self.dropdown_value = initial_value
    self.create_dropdown_display_text(initial_value)
    self.ui.setup_header(
        height=0.2,
        visible=True,
        collapsible=False,
        expandable=False,
        screen_scaling=True,
    )

  def create_dropdown_display_text(self, choice: str) -> None:
    """Called when one of the dropdown option is submitted."""
    if choice in status_event_map:
      color = status_event_map[choice].background_color
    else:
      print("Unsupported dropdown choice.")
      color = robotics_ui_pb2.Color(red=1.0, green=1.0, blue=1.0, alpha=1.0)
    self.ui.create_or_update_text(
        text_id="Status",
        text=("<size=80em>" + choice + "</size>"),
        spec=robotics_ui_pb2.UISpec(
            width=0.5,
            height=0.7,
            background_color=color,
            x=0.5,
            y=0.5,
            mode=robotics_ui_pb2.UIMode.UIMODE_HEADER,
        ),
    )

  def update_dropdown_value(self, data: str) -> None:
    """Called when one of the dropdown option is submitted."""
    result: str | None = None
    for filename in constants.OPERATOR_EVENT_FILEPATHS:
      try:
        file = pathlib.Path(os.path.expanduser(filename))
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(data)
        print(f"Saving file in '{filename}'")
        result = filename
        break
      except OSError as e:
        print(f"Error creating file in '{filename}': {e}")
    if result:
      print(f"File '{result}' written successfully.")
    else:
      print("Failed to write file. Operator event status will not be saved.")

    self.dropdown_value = data
    self.create_dropdown_display_text(data)

  def login_with_user_id(self, user_id: str) -> None:
    """Logs in with the given user id and sends a login event."""
    # If the user is already logged in, log them out first.
    if self.login_user:
      self.logout()
    print(f"Logging in with user: {user_id}")
    self.login_user = user_id
    self.event_logger.set_ldap(user_id)
    self.event_logger.create_ui_event(
        event=operator_event_lib.UIEvent.LOGIN.value
    )
    self.event_logger.write_event()
    self._login_time = time.time()
    if self._orca_helper is not None:
      self._orca_helper.set_current_robot_operator_id(operator_id=user_id)
    self.update_login_process(login_time=self._login_time)
    print("Calling start_disk_space_check_thread")
    self.start_disk_space_check_thread()

  def logout(self) -> None:
    """Set the login user to None and send a logout event."""
    if not self.login_user:
      print("No user to log out of.")
      return
    print(f"Logging out of current user: {self.login_user}")
    self.login_user = None
    self.event_logger.create_ui_event(
        event=operator_event_lib.UIEvent.LOGOUT.value
    )
    self.ui.send_dropdown_pressed_event(
        constants.OPERATOR_EVENT_DROPDOWN_ID,
        self.workcell_status_pair.logout_status,
    )
    self.event_logger.write_event()
    self.event_logger.clear_ldap()
    self.event_logger.clear_reporting_ldap()
    self._login_time = 0
    if self._orca_helper is not None:
      self._orca_helper.set_current_robot_operator_id(operator_id="")
    self.update_login_process()

  def update_login_process(self, login_time: float = 0) -> None:
    """Called when login or logout button is pressed."""
    self._login_time = login_time
    if self._login_time != 0:
      self.start_login_thread()
    elif self._login_time == 0:
      self.stop_login_thread()
    else:
      print("No login or logout button pressed")

  def update_timeout_process(self) -> None:
    """Start or stop the timeout process when the workcell status is updated."""
    if not os.path.isdir(os.path.expanduser(_OBSERVER_DIR)):
      print(
          f"Logs directory '{_OBSERVER_DIR}' does not exist to be observed."
          " Auto-logout timer disabled."
      )
      return

    # Start timeout process only if the operator is in operation.
    if (
        self.workcell_status_pair.status
        == operator_event_lib.WorkcellStatus.IN_OPERATION.value
    ):
      self.start_timeout_thread()
      self.start_observer()
    else:
      self.stop_timeout_thread()
      self.stop_observer()

  def start_observer(self) -> None:
    """Start observer to watch for changes in the logs directory."""
    if self._observer is not None:
      return

    class ObserverHandler(events.FileSystemEventHandler):
      """Handler for file system events.

      This handler resets the timeout when a new file is created in the
      persistent logs directory.
      """

      _handler: WorkcellManager

      def __init__(self, handler: WorkcellManager):
        self._handler = handler

      def on_created(self, event):
        self._handler.reset_timeout()

    event_handler = ObserverHandler(self)
    self._observer = observers.Observer()
    self._observer.daemon = True
    self._observer.schedule(
        event_handler, os.path.expanduser(_OBSERVER_DIR), recursive=True
    )
    self._observer.start()
    print("Observer started...")

  def stop_observer(self) -> None:
    """Stops the observer."""
    if self._observer is None:
      return
    self._observer.stop()
    self._observer.join()
    self._observer = None
    print("Observer stopped...")

  def start_login_thread(self) -> None:
    """Starts the login thread."""
    if self._login_thread is not None:
      return
    self._login_thread = threading.Timer(
        interval=1.0, function=self._update_total_time
    )
    self._login_thread.start()
    print("Login Thread started...")
    threading.Timer(interval=1.0, function=self._display_bash_text).start()
    print("Bash text display thread started...")

  def start_disk_space_check_thread(self) -> None:
    """Starts the disk space check thread."""
    print("Disk Space Check Thread attempt...")
    if self._check_disk_space_thread is not None:
      return
    print("Disk Space Check Thread starting...")
    self._check_disk_space_thread = threading.Timer(
        interval=1800.0, function=self._check_disk_space_percentage
    )
    self._check_disk_space_thread.start()

  def _update_total_time(self) -> None:
    """Updates the total time."""
    if self._login_thread is None:
      return
    self.accumulate_episode_time()
    threading.Timer(interval=1.0, function=self._update_total_time).start()

  def stop_login_thread(self) -> None:
    """Stops the login thread."""
    if self._login_thread is not None:
      self._login_thread = None
    print("Login Thread stopped...")

  def stop_disk_space_check_thread(self) -> None:
    """Stops the disk space check thread."""
    if self._check_disk_space_thread is not None:
      self._check_disk_space_thread = None
    print("Disk Space Check Thread stopped...")

  def display_message(
      self,
      message: str = "",
      text_id: str = "",
      timeout: str = "10",
      window: str = "",
  ) -> None:
    """Displays a message for timeout seconds."""
    print(
        f"Message displayed: {message},\n"
        f"Id displayed: {id},\n"
        f"Timeout: {timeout},\n"
        f"window displayed: {window}"
    )
    win_w, win_h, win_x, win_y = window.split(",")
    win_w = float(win_w)
    win_h = float(win_h)
    win_x = float(win_x)
    win_y = float(win_y)
    color = robotics_ui_pb2.Color(red=1.0, green=0.0, blue=1.0, alpha=1.0)
    self.ui.create_or_update_text(
        text_id=text_id,
        text=message,
        spec=robotics_ui_pb2.UISpec(
            width=win_w,
            height=win_h,
            x=win_x,
            y=win_y,
            mode=robotics_ui_pb2.UIMode.UIMODE_HEADER,
            background_color=color,
        ),
    )
    time.sleep(int(timeout))
    print("Message display complete.")
    self.ui.remove_element(text_id)

  def _display_bash_text(self) -> None:
    """Displays messages coming from bash script."""
    if os.path.exists(constants.UITEXT_FILE_PATH):
      with open(constants.UITEXT_FILE_PATH, "r") as f:
        lines = f.readlines()
      ## delete the file after reading.
      os.remove(constants.UITEXT_FILE_PATH)
      msg, text_id, timeout, window = lines[1].strip().split(":")

      display_thread = threading.Thread(
          target=self.display_message, args=(msg, text_id, timeout, window)
      )
      display_thread.start()
    threading.Timer(interval=2.0, function=self._display_bash_text).start()

  def accumulate_episode_time(self) -> None:
    """Accumulates the total episode time(success & fail)."""

    self._accumulated_total_episode_time = 0
    self._accumulated_successful_episode_time = 0
    if os.path.exists(constants.EPISODE_TIME_FILE_PATH):
      with open(constants.EPISODE_TIME_FILE_PATH, "r") as f:
        for line in f:
          if len(line.strip().split()) != 3:
            continue
          episode_start_time, episode_end_time, result = line.strip().split()
          episode_start_time = float(episode_start_time)
          episode_end_time = float(episode_end_time)
          if episode_start_time < self._login_time:
            continue
          self._accumulated_total_episode_time += (
              episode_end_time - episode_start_time
          )
          if result == "success":
            self._accumulated_successful_episode_time += (
                episode_end_time - episode_start_time
            )

    def format_time(seconds: float) -> str:
      seconds = round(seconds)
      hours = seconds // 3600
      seconds = seconds % 3600
      minutes = seconds // 60
      seconds = seconds % 60
      return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    if os.path.exists(constants.EPISODE_TIME_FILE_PATH):
      self.ui.create_or_update_text(
          text_id="total_episode",
          text=(
              "<color=white>hours collected: <color=green>"
              f"{format_time(self._accumulated_successful_episode_time)}"
              " (success)</color> / "
              f"{format_time(self._accumulated_total_episode_time)} (all) |"
              " login timer :"
              f" {format_time(time.time() - self._login_time)}</color>"
          ),
          spec=robotics_ui_pb2.UISpec(
              width=0.5,
              height=0.15,
              x=0.5,
              y=0.075,
              mode=robotics_ui_pb2.UIMode.UIMODE_HEADER,
              background_color=robotics_ui_pb2.Color(alpha=0),
          ),
      )
    else:
      self.ui.create_or_update_text(
          text_id="total_episode",
          text=(
              "<color=green> login timer : "
              f" {format_time(time.time() - self._login_time)}</color>"
          ),
          spec=robotics_ui_pb2.UISpec(
              width=0.5,
              height=0.15,
              x=0.5,
              y=0.075,
              mode=robotics_ui_pb2.UIMode.UIMODE_HEADER,
              background_color=robotics_ui_pb2.Color(alpha=0),
          ),
      )

  def start_timeout_thread(self) -> None:
    """Starts the timeout thread."""
    if self._timeout_thread is not None:
      return
    self._timeout_start_time = time.time()
    self._timeout_stop_event = threading.Event()
    self._timeout_thread = threading.Thread(target=self._update_timeout_thread)
    self._timeout_thread.start()
    print("Timeout started...")

  def stop_timeout_thread(self) -> None:
    """Stops the timeout thread."""
    if (
        self._timeout_stop_event is not None
        and not self._timeout_stop_event.is_set()
    ):
      self._timeout_stop_event.set()
      print("Timeout stopped...")
    if self._timeout_thread is not None:
      self._timeout_thread = None

  def reset_timeout(self) -> None:
    """Resets the timeout."""
    self._timeout_start_time = time.time()

  def set_dropdown_shortcuts(self, enabled: bool) -> None:
    """Whether to enable keyboard shortcuts for the workcell status dropdown."""
    shortcuts = operator_event_lib.workcell_shortcut_dict if enabled else None
    self.ui.create_dropdown(
        dropdown_id=constants.OPERATOR_EVENT_DROPDOWN_ID,
        title="Status Options",
        msg="Select Event Type",
        choices=workcell_status_list,
        submit_label="Submit",
        spec=constants.STATUS_DROPDOWN_SPEC,
        shortcuts=shortcuts,
        initial_value=self.dropdown_value,
    )
    print(
        f"{'Enable' if enabled else 'Disable'} keyboard shortcuts for the"
        " workcell status dropdown."
    )

  def _update_timeout_thread(self) -> None:
    """Updates the timeout thread and exit when timeout is reached."""
    while not self._timeout_stop_event.is_set():
      remaining = _TIMEOUT_SECONDS - (time.time() - self._timeout_start_time)
      if remaining <= 0:
        self.stop_timeout_thread()
        self.stop_observer()
        self.ui.send_button_pressed_event(constants.OPERATOR_LOGOUT_BUTTON_ID)
        print("Timeout...")
        break
      time.sleep(0.1)

  def _check_disk_space_percentage(self) -> None:
    """Checks for low disk space and alerts the user if needed."""
    print("Checking disk space percentage...")
    try:
      disk_usage = shutil.disk_usage("/isodevice")
      free_space_gb = disk_usage.free / constants.SIZE_OF_GB
      free_space_percentage = (free_space_gb / self._total_space_gb) * 100
      print(f"Total disk space: {self._total_space_gb:.2f} GB.")
      print(f"Free disk space: {free_space_gb:.2f} GB.")
      print(f"Free disk space percentage: {free_space_percentage:.2f} %.")
      if free_space_percentage < constants.LOW_DISK_SPACE_THRESHOLD_PERCENTAGE:
        self.ui.create_dialog(
            dialog_id="low_disk_space_alert",
            title="Low Disk Space",
            msg=(
                f"Low disk space! Available: {free_space_percentage:.2f} %."
                "Please free up some space."
            ),
            buttons=["OK"],
            spec=robotics_ui_pb2.UISpec(width=0.4, height=0.2, x=0.5, y=0.5),
        )
      threading.Timer(
          interval=1800.0, function=self._check_disk_space_percentage
      ).start()
    except OSError as e:
      print(f"Error checking disk space: {e}")
    except ZeroDivisionError as e:
      print(f"Error checking disk space: {e}. Total disk space is zero.")
      raise
