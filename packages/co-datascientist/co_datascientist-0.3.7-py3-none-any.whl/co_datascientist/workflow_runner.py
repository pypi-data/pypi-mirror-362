import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
import asyncio
from pathlib import Path
from datetime import datetime

from .models import Workflow, SystemInfo, CodeResult
from . import co_datascientist_api
from .kpi_extractor import extract_kpi_from_stdout
from .settings import settings

OUTPUT_FOLDER = "co_datascientist_output"
CHECKPOINTS_FOLDER = "co_datascientist_checkpoints"


def print_workflow_info(message: str):
    """Print workflow info with consistent formatting"""
    print(f"   {message}")


def print_workflow_step(message: str):
    """Print workflow step with consistent formatting"""
    print(f"   🔄 {message}")


def print_workflow_success(message: str):
    """Print workflow success with consistent formatting"""
    print(f"   ✅ {message}")


def print_workflow_error(message: str):
    """Print workflow error with consistent formatting"""
    print(f"   ❌ {message}")


class _WorkflowRunner:
    def __init__(self):
        self.workflow: Workflow | None = None
        self.start_timestamp = 0
        self.should_stop_workflow = False
        self.debug_mode = True
        # Track best KPI seen when polling backend
        self._checkpoint_counter: int = 0

    async def run_workflow(self, code: str, python_path: str, project_absolute_path: str, spinner=None, debug: bool = True):
        """Run a complete code evolution workflow (sequential-only)."""
        self.should_stop_workflow = False
        
        # Set debug mode for the class instance
        self.debug_mode = debug
        
        try:
            if spinner:
                spinner.text = "Waking up the Co-DataScientist"
            self.start_timestamp = time.time()
            self.should_stop_workflow = False
            self.workflow = Workflow(status_text="Workflow started", user_id="")

            system_info = get_system_info(python_path)
            logging.info(f"user system info: {system_info}")
            
            response = await co_datascientist_api.start_workflow(code, system_info)
            self.workflow = response.workflow
            if spinner:
                spinner.stop()  # stop spinner without emoji
            print("Lets start exploring your problem space!")
            print()

            await self._run_sequential_mode(response, python_path, project_absolute_path, spinner)

            if self.should_stop_workflow:
                await co_datascientist_api.stop_workflow(self.workflow.workflow_id)
                print_workflow_info("Workflow stopped by user.")
                if spinner:
                    spinner.text = "Workflow stopped"
            else:
                # Check if workflow finished due to baseline failure or successful completion
                if (hasattr(self.workflow, 'baseline_code') and 
                    self.workflow.baseline_code.result is not None and 
                    self.workflow.baseline_code.result.return_code != 0):
                    print_workflow_error("Workflow terminated due to baseline code failure!")
                    print("   📄 Review the error details above and fix your script.")
                    if spinner:
                        spinner.text = "Workflow failed"
                else:
                    print_workflow_success("Workflow completed successfully!")
                    if spinner:
                        spinner.text = "Workflow completed"
        
        except Exception as e:
            if spinner:
                spinner.stop()

            err_msg = str(e)
            # Detect user-facing validation errors coming from backend (prefixed with ❌)
            if err_msg.startswith("❌") and not self.debug_mode:
                # Show concise guidance without stack trace
                print_workflow_error(err_msg)
                return  # Do not re-raise, end gracefully

            # Otherwise, show generic workflow error and re-raise for full trace
            print_workflow_error(f"Workflow error: {err_msg}")
            raise

    async def _run_sequential_mode(self, response, python_path: str, 
                                  project_absolute_path: str, spinner=None, poll_interval: int = 1):
        """Run workflow in sequential mode (original behavior)"""
        
        iteration_count = 0

        # Ensure spinner is active throughout the loop
        if spinner:
            spinner.text = "Thinking..."
            spinner.start()

        while not self.workflow.finished and response.code_to_run is not None and not self.should_stop_workflow:
            # No minimal/best-only modes – always standard
            
            # keep spinner running; write a blank line for spacing
            if spinner:
                spinner.write("")
            else:
                print()
            
            result = _run_python_code(response.code_to_run.code, python_path)

            # Handle results based on mode
            # Log only for baseline; skip verbose output for other ideas
            if response.code_to_run.name == "baseline":
                await self._handle_baseline_result(result, response, spinner)
            # Extra space before the next spinner line
            if spinner:
                spinner.write("")
            else:
                print()
            # Restart spinner while waiting for next idea
            if spinner:
                spinner.text = "Dont worry, I'm just thinking..."
                spinner.start()

            # Prepare objects for backend
            kpi_value = extract_kpi_from_stdout(result.stdout)
            result.kpi = kpi_value
            code_version = response.code_to_run
            code_version.result = result

            response = await co_datascientist_api.finished_running_code(
                self.workflow.workflow_id,
                code_version,
                result,
                kpi_value,
            )
            self.workflow = response.workflow

            # Poll backend for best KPI every poll_interval iterations
            iteration_count += 1
            if iteration_count % poll_interval == 0:
                try:
                    best_info = await co_datascientist_api.get_workflow_population_best(self.workflow.workflow_id)
                    best_kpi = best_info.get("best_kpi") if best_info else None
                    if best_kpi is not None and spinner:
                        spinner.write(f"🚀 Current best KPI: {best_kpi}")

                    # Always save checkpoint snapshot of current best
                    best_cv = best_info.get("best_code_version") if best_info else None
                    await self._save_population_best_checkpoint(best_cv, best_kpi, project_absolute_path)
                except Exception as e:
                    # Non-fatal: just log and continue
                    logging.warning(f"Failed fetching best KPI code: {e}")

    async def _handle_baseline_result(self, result: CodeResult, response, spinner=None):
        """Handle result in standard mode (original behavior)"""
        # Check if code execution failed and provide clear feedback
        if result.return_code != 0:
            # Code failed - show error details
            print_workflow_error(f"'{response.code_to_run.name}' failed with exit code {result.return_code}")
            if result.stderr:
                print("   📄 Error details:")
                # Print each line of stderr with proper indentation
                for line in result.stderr.strip().split('\n'):
                    if spinner:
                        spinner.write(f"      {line}")
                    else:
                        print(f"      {line}")
            
            # For baseline failures, give specific guidance
            if response.code_to_run.name == "baseline":
                print("   💡 The baseline code failed to run. This will stop the workflow.")
                print("   💡 Check the error above and fix your script before running again.")
                if "ModuleNotFoundError" in (result.stderr or ""):
                    print("   💡 Missing dependencies? Try: pip install <missing-package>")
        else:
            # Code succeeded - show success message
            kpi_value = extract_kpi_from_stdout(result.stdout)
            if kpi_value is not None:
                msg = f"Completed '{response.code_to_run.name}' | KPI = {kpi_value}"
                if spinner:
                    spinner.write("   ✅ " + msg)
                else:
                    print_workflow_success(msg)
            else:
                msg = f"Completed '{response.code_to_run.name}'"
                if spinner:
                    spinner.write("   ✅ " + msg)
                else:
                    print_workflow_success(msg)

    async def _save_population_best_checkpoint(self, best_cv, best_kpi: float, project_absolute_path: str):
        """Persist best code/KPI locally whenever we see a new record."""
        try:
            if not best_cv or best_kpi is None:
                return

            # Convert best_cv to CodeVersion model if it is raw dict
            from .models import CodeVersion, CodeResult
            if isinstance(best_cv, dict):
                try:
                    # Nested result may also be dict – handle gracefully
                    if isinstance(best_cv.get("result"), dict):
                        # Ensure runtime_ms field may be missing; allow extra
                        best_cv["result"] = CodeResult.model_validate(best_cv["result"])  # type: ignore
                    best_cv = CodeVersion.model_validate(best_cv)  # type: ignore
                except Exception as e:
                    logging.warning(f"Cannot parse best_code_version payload: {e}")
                    return

            checkpoints_base = Path(project_absolute_path) / CHECKPOINTS_FOLDER
            checkpoints_base.mkdir(parents=True, exist_ok=True)

            safe_name = _make_filesystem_safe(best_cv.name or "best")
            base_filename = f"best_{self._checkpoint_counter}_{safe_name}"

            code_path = checkpoints_base / f"{base_filename}.py"
            meta_path = checkpoints_base / f"{base_filename}.json"

            code_path.write_text(best_cv.code, encoding="utf-8")

            meta = {
                "code_version_id": best_cv.code_version_id,
                "name": best_cv.name,
                "kpi": best_kpi,
                "stdout": getattr(best_cv.result, "stdout", None) if best_cv.result else None,
            }
            meta_path.write_text(json.dumps(meta, indent=4))

            self._checkpoint_counter += 1
        except Exception as e:
            logging.warning(f"Failed saving best checkpoint: {e}")


def _make_filesystem_safe(name):
    return re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", '_', name)


def _run_python_code(code: str, python_path: str) -> CodeResult:
    import subprocess  # Ensure subprocess is imported
    start_time = time.time()
    # write the code to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name

    command = [python_path, temp_file_path]

    # run the command
    logging.info("running command: " + str(command))
    try:
        output = subprocess.run(command,
                                capture_output=True,
                                text=True,
                                input="",  # prevents it from blocking on stdin
                                timeout=settings.script_execution_timeout)  # Use centralized timeout
        return_code = output.returncode
        out = output.stdout
        err = output.stderr
    except subprocess.TimeoutExpired as e:
        # Handle timeout gracefully - mark as failed case and continue
        return_code = -9  # Standard timeout return code
        out = None
        err = f"Process timed out after {settings.script_execution_timeout} seconds"
        logging.info(f"Process timed out after {settings.script_execution_timeout} seconds")
    
    if isinstance(out, str) and out.strip() == "":
        out = None
    if isinstance(err, str) and err.strip() == "":
        err = None

    logging.info("stdout: " + str(out))
    logging.info("stderr: " + str(err))

    # delete the temporary file
    os.remove(temp_file_path)
    runtime_ms = int((time.time() - start_time) * 1000)
    return CodeResult(stdout=out, stderr=err, return_code=return_code, runtime_ms=runtime_ms)


def get_system_info(python_path: str) -> SystemInfo:
    return SystemInfo(
        python_libraries=_get_python_libraries(python_path),
        python_version=_get_python_version(python_path),
        os=sys.platform
    )


def _get_python_libraries(python_path: str) -> list[str]:
    try:
        # Use importlib.metadata to get installed packages (works in all Python 3.8+ environments)
        python_code = """
import importlib.metadata
for dist in importlib.metadata.distributions():
    print(f"{dist.metadata['Name']}=={dist.version}")
"""
        installed_libraries = subprocess.check_output(
            [python_path, "-c", python_code],
            universal_newlines=True
        ).strip()
        return [lib.strip() for lib in installed_libraries.split("\n") if lib.strip()]
    except subprocess.CalledProcessError:
        # If that fails, return empty list
        return []


def _get_python_version(python_path: str) -> str:
    return subprocess.check_output(
        [python_path, "--version"],
        universal_newlines=True
    ).strip()


workflow_runner = _WorkflowRunner()
