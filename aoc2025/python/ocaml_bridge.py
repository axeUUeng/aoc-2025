import subprocess
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def run_ocaml(day, level, input_str):
    exe_name = f"day{int(day):02d}.exe"
    cmd = ["dune", "exec", f"bin/{exe_name}", "--", str(level)]

    try:
        result = subprocess.run(
            cmd,
            input=input_str,
            capture_output=True,
            text=True,
            check=True,
            cwd=ROOT,  # ensure dune runs from project root
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else ""
        stdout = exc.stdout.strip() if exc.stdout else ""
        details = "\n".join(part for part in [stdout, stderr] if part)
        raise RuntimeError(f"OCaml execution failed for {' '.join(cmd)}\n{details}") from exc

    return result.stdout.strip()
