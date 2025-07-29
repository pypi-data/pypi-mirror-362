import atexit
import json
import threading
from collections.abc import Callable
from dataclasses import asdict
from queue import Queue
from sys import argv
from traceback import format_exception
from typing import Any

from blueapi.core import BlueskyContext
from bluesky.callbacks.zmq import Publisher
from bluesky.run_engine import RunEngine
from bluesky.utils import MsgGenerator
from flask import Flask, request
from flask_restful import Api, Resource
from pydantic.dataclasses import dataclass

from mx_bluesky.common.external_interaction.callbacks.common.log_uid_tag_callback import (
    LogUidTaggingCallback,
)
from mx_bluesky.common.parameters.components import MxBlueskyParameters
from mx_bluesky.common.parameters.constants import Actions, Status
from mx_bluesky.common.utils.exceptions import WarningException
from mx_bluesky.common.utils.log import (
    LOGGER,
    do_default_logging_setup,
    flush_debug_handler,
)
from mx_bluesky.common.utils.tracing import TRACER
from mx_bluesky.hyperion.experiment_plans.experiment_registry import (
    PLAN_REGISTRY,
    PlanNotFound,
)
from mx_bluesky.hyperion.external_interaction.agamemnon import (
    compare_params,
    update_params_from_agamemnon,
)
from mx_bluesky.hyperion.parameters.cli import parse_cli_args
from mx_bluesky.hyperion.parameters.constants import CONST
from mx_bluesky.hyperion.parameters.load_centre_collect import LoadCentreCollect
from mx_bluesky.hyperion.utils.context import setup_context


@dataclass
class Command:
    action: Actions
    devices: Any | None = None
    experiment: Callable[[Any, Any], MsgGenerator] | None = None
    parameters: MxBlueskyParameters | None = None


@dataclass
class StatusAndMessage:
    status: str
    message: str = ""

    def __init__(self, status: Status, message: str = "") -> None:
        self.status = status.value
        self.message = message


@dataclass
class ErrorStatusAndMessage(StatusAndMessage):
    exception_type: str = ""


def make_error_status_and_message(exception: Exception):
    return ErrorStatusAndMessage(
        status=Status.FAILED.value,
        message=repr(exception),
        exception_type=type(exception).__name__,
    )


class BlueskyRunner:
    def __init__(
        self,
        RE: RunEngine,
        context: BlueskyContext,
    ) -> None:
        self.command_queue: Queue[Command] = Queue()
        self.current_status: StatusAndMessage = StatusAndMessage(Status.IDLE)
        self.last_run_aborted: bool = False
        self.logging_uid_tag_callback = LogUidTaggingCallback()
        self.context: BlueskyContext

        self.RE = RE
        self.context = context
        RE.subscribe(self.logging_uid_tag_callback)

        LOGGER.info("Connecting to external callback ZMQ proxy...")
        self.publisher = Publisher(f"localhost:{CONST.CALLBACK_0MQ_PROXY_PORTS[0]}")
        RE.subscribe(self.publisher)

    def start(
        self,
        experiment: Callable,
        parameters: MxBlueskyParameters,
        plan_name: str,
    ) -> StatusAndMessage:
        LOGGER.info(f"Started with parameters: {parameters.model_dump_json(indent=2)}")

        devices: Any = PLAN_REGISTRY[plan_name]["setup"](self.context)

        if (
            self.current_status.status == Status.BUSY.value
            or self.current_status.status == Status.ABORTING.value
        ):
            return StatusAndMessage(Status.FAILED, "Bluesky already running")
        else:
            self.current_status = StatusAndMessage(Status.BUSY)
            self.command_queue.put(
                Command(
                    action=Actions.START,
                    devices=devices,
                    experiment=experiment,
                    parameters=parameters,
                )
            )
            return StatusAndMessage(Status.SUCCESS)

    def stopping_thread(self):
        try:
            self.RE.abort()
            self.current_status = StatusAndMessage(Status.IDLE)
        except Exception as e:
            self.current_status = make_error_status_and_message(e)

    def stop(self) -> StatusAndMessage:
        if self.current_status.status == Status.IDLE.value:
            return StatusAndMessage(Status.FAILED, "Bluesky not running")
        elif self.current_status.status == Status.ABORTING.value:
            return StatusAndMessage(Status.FAILED, "Bluesky already stopping")
        else:
            self.current_status = StatusAndMessage(Status.ABORTING)
            stopping_thread = threading.Thread(target=self.stopping_thread)
            stopping_thread.start()
            self.last_run_aborted = True
            return StatusAndMessage(Status.ABORTING)

    def shutdown(self):
        """Stops the run engine and the loop waiting for messages."""
        print("Shutting down: Stopping the run engine gracefully")
        self.stop()
        self.command_queue.put(Command(action=Actions.SHUTDOWN))

    def wait_on_queue(self):
        while True:
            command = self.command_queue.get()
            if command.action == Actions.SHUTDOWN:
                return
            elif command.action == Actions.START:
                if command.experiment is None:
                    raise ValueError("No experiment provided for START")
                try:
                    with TRACER.start_span("do_run"):
                        self.RE(command.experiment(command.devices, command.parameters))

                    self.current_status = StatusAndMessage(Status.IDLE)

                    self.last_run_aborted = False
                except WarningException as exception:
                    LOGGER.warning("Warning Exception", exc_info=True)
                    self.current_status = make_error_status_and_message(exception)
                except Exception as exception:
                    LOGGER.error("Exception on running plan", exc_info=True)

                    if self.last_run_aborted:
                        # Aborting will cause an exception here that we want to swallow
                        self.last_run_aborted = False
                    else:
                        self.current_status = make_error_status_and_message(exception)


def compose_start_args(context: BlueskyContext, plan_name: str, action: Actions):
    experiment_registry_entry = PLAN_REGISTRY.get(plan_name)
    if experiment_registry_entry is None:
        raise PlanNotFound(f"Experiment plan '{plan_name}' not found in registry.")

    experiment_internal_param_type = experiment_registry_entry.get("param_type")
    plan = context.plan_functions.get(plan_name)
    if experiment_internal_param_type is None:
        raise PlanNotFound(
            f"Corresponding internal param type for '{plan_name}' not found in registry."
        )
    if plan is None:
        raise PlanNotFound(
            f"Experiment plan '{plan_name}' not found in context. Context has {context.plan_functions.keys()}"
        )
    try:
        parameters = experiment_internal_param_type(**json.loads(request.data))
        parameters = update_params_from_agamemnon(parameters)
        if isinstance(parameters, LoadCentreCollect):
            compare_params(parameters)
        if parameters.model_extra:
            raise ValueError(f"Extra fields not allowed {parameters.model_extra}")
    except Exception as e:
        raise ValueError(
            f"Supplied parameters don't match the plan for this endpoint {request.data}, for plan {plan_name}"
        ) from e
    return plan, parameters, plan_name


class RunExperiment(Resource):
    def __init__(self, runner: BlueskyRunner, context: BlueskyContext) -> None:
        super().__init__()
        self.runner = runner
        self.context = context

    def put(self, plan_name: str, action: Actions):
        status_and_message = StatusAndMessage(Status.FAILED, f"{action} not understood")
        if action == Actions.START.value:
            try:
                plan, params, plan_name = compose_start_args(
                    self.context, plan_name, action
                )
                status_and_message = self.runner.start(plan, params, plan_name)
            except Exception as e:
                status_and_message = make_error_status_and_message(e)
                LOGGER.error("".join(format_exception(e)))

        elif action == Actions.STOP.value:
            status_and_message = self.runner.stop()
        # no idea why mypy gives an attribute error here but nowhere else for this
        # exact same situation...
        return asdict(status_and_message)  # type: ignore


class StopOrStatus(Resource):
    def __init__(self, runner: BlueskyRunner) -> None:
        super().__init__()
        self.runner: BlueskyRunner = runner

    def put(self, action):
        status_and_message = StatusAndMessage(Status.FAILED, f"{action} not understood")
        if action == Actions.STOP.value:
            status_and_message = self.runner.stop()
        return asdict(status_and_message)

    def get(self, **kwargs):
        action = kwargs.get("action")
        status_and_message = StatusAndMessage(Status.FAILED, f"{action} not understood")
        if action == Actions.STATUS.value:
            LOGGER.debug(
                f"Runner received status request - state of the runner object is: {self.runner.__dict__} - state of the RE is: {self.runner.RE.__dict__}"
            )
            status_and_message = self.runner.current_status
        return asdict(status_and_message)


class FlushLogs(Resource):
    def put(self, **kwargs):
        try:
            status_and_message = StatusAndMessage(
                Status.SUCCESS, f"Flushed debug log to {flush_debug_handler()}"
            )
        except Exception as e:
            status_and_message = StatusAndMessage(
                Status.FAILED, f"Failed to flush debug log: {e}"
            )
        return asdict(status_and_message)


def create_app(
    test_config=None,
    RE: RunEngine = RunEngine({}),
    dev_mode: bool = False,
) -> tuple[Flask, BlueskyRunner]:
    context = setup_context(dev_mode=dev_mode)
    runner = BlueskyRunner(
        RE,
        context=context,
    )
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    api = Api(app)
    api.add_resource(
        RunExperiment,
        "/<string:plan_name>/<string:action>",
        resource_class_args=[runner, context],
    )
    api.add_resource(
        FlushLogs,
        "/flush_debug_log",
    )
    api.add_resource(
        StopOrStatus,
        "/<string:action>",
        resource_class_args=[runner],
    )
    return app, runner


def create_targets():
    hyperion_port = 5005
    args = parse_cli_args()
    do_default_logging_setup(
        CONST.LOG_FILE_NAME, CONST.GRAYLOG_PORT, dev_mode=args.dev_mode
    )
    LOGGER.info(f"Hyperion launched with args:{argv}")
    app, runner = create_app(dev_mode=args.dev_mode)
    return app, runner, hyperion_port, args.dev_mode


def main():
    app, runner, port, dev_mode = create_targets()
    atexit.register(runner.shutdown)
    flask_thread = threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0", port=port, debug=True, use_reloader=False
        ),
        daemon=True,
    )
    flask_thread.start()
    LOGGER.info(f"Hyperion now listening on {port} ({'IN DEV' if dev_mode else ''})")
    runner.wait_on_queue()
    flask_thread.join()


if __name__ == "__main__":
    main()
