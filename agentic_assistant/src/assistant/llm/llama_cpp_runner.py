from __future__ import annotations

import subprocess
from pathlib import Path


class LlamaCppRunner:
    def __init__(
        self,
        executable_path: Path,
        model_path: Path,
        threads: int = 4,
        context_tokens: int = 2048,
        max_tokens: int = 256,
        temperature: float = 0.2,
    ) -> None:
        self.executable_path = Path(executable_path)
        self.model_path = Path(model_path)
        self.threads = threads
        self.context_tokens = context_tokens
        self.max_tokens = max_tokens
        self.temperature = temperature

    def _build_command(self, prompt: str) -> list[str]:
        return [
            str(self.executable_path),
            "-m",
            str(self.model_path),
            "-t",
            str(self.threads),
            "-c",
            str(self.context_tokens),
            "-n",
            str(self.max_tokens),
            "--temp",
            str(self.temperature),
            "-p",
            prompt,
            "-ngl",
            "0",
        ]

    def generate(self, prompt: str) -> str:
        if not self.executable_path.exists():
            raise FileNotFoundError(f"llama executable not found: {self.executable_path}")
        if not self.model_path.exists():
            raise FileNotFoundError(f"model file not found: {self.model_path}")

        process = subprocess.run(
            self._build_command(prompt),
            check=True,
            text=True,
            capture_output=True,
        )
        output = process.stdout.strip()

        if prompt in output:
            output = output.split(prompt, 1)[-1].strip()
        return output
