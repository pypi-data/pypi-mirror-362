import subprocess
from dataclasses import dataclass

from akride import logger
from akride._utils.catalog.string_utils import decode_bytes


@dataclass
class SubprocessResult:
    stdout: str
    stderr: str
    ret_code: int

    def has_failed(self):
        return self.ret_code != 0


def run_subprocess(script_path: str, *args) -> SubprocessResult:
    try:
        args = [str(arg) for arg in args]

        # Execute the shell script
        result = subprocess.run(
            [script_path] + args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return SubprocessResult(
            stdout=decode_bytes(bytes_data=result.stdout),
            stderr=decode_bytes(bytes_data=result.stderr),
            ret_code=result.returncode,
        )
    except subprocess.CalledProcessError as ex:
        logger.exception(f"Failed to run script {script_path}")
        return SubprocessResult(
            stdout=decode_bytes(ex.stdout),
            stderr=decode_bytes(ex.stderr),
            ret_code=ex.returncode,
        )
