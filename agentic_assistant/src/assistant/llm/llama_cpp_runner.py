from __future__ import annotations

import subprocess
from pathlib import Path


# Sentinel value meaning "use the runner's default"
_DEFAULT = object()


class LlamaCppRunner:
    def __init__(
        self,
        executable_path: Path,
        model_path: Path,
        threads: int = 4,
        context_tokens: int = 2048,
        max_tokens: int = 256,
        temperature: float = 0.2,
        timeout_seconds: int = 120,
    ) -> None:
        self.executable_path = Path(executable_path)
        self.model_path = Path(model_path)
        self.threads = threads
        self.context_tokens = context_tokens
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds

    def _build_command(self, prompt: str, max_tokens_override: int | None = None) -> list[str]:
        n_tokens = max_tokens_override if max_tokens_override is not None else self.max_tokens
        return [
            str(self.executable_path),
            "-m",
            str(self.model_path),
            "-t",
            str(self.threads),
            "-c",
            str(self.context_tokens),
            "-n",
            str(n_tokens),
            "--temp",
            str(self.temperature),
            "-p",
            prompt,
            "-ngl",
            "0",
            "--log-disable",   # suppress llama.cpp progress/noise from stdout
            "--no-display-prompt",  # llama-cli flag to omit echoed prompt in output
        ]

    def generate(self, prompt: str, max_tokens_override: int | None = None) -> str:
        """Run inference and return the generated text only (prompt stripped).

        Args:
            prompt: The full prompt string.
            max_tokens_override: Override the default max_tokens for this call only.
                                 Useful for classification prompts that need very few tokens.
        """
        if not self.executable_path.exists():
            raise FileNotFoundError(f"llama executable not found: {self.executable_path}")
        if not self.model_path.exists():
            raise FileNotFoundError(f"model file not found: {self.model_path}")

        try:
            process = subprocess.run(
                self._build_command(prompt, max_tokens_override=max_tokens_override),
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f"llama.cpp inference timed out after {self.timeout_seconds}s"
            ) from exc

        if process.returncode != 0:
            stderr_snippet = (process.stderr or "")[:400].strip()
            raise RuntimeError(
                f"llama.cpp exited with code {process.returncode}: {stderr_snippet}"
            )

        output = process.stdout.strip()

        # --no-display-prompt suppresses prompt echo in newer llama-cli builds.
        # For older builds that still echo the prompt, strip it out manually.
        if output.startswith(prompt):
            output = output[len(prompt):].strip()

        return output

    # ------------------------------------------------------------------
    # Convenience: thin classification call (very few tokens)
    # ------------------------------------------------------------------

    def classify(self, prompt: str) -> str:
        """Run inference with max_tokens=16 for routing classification queries."""
        return self.generate(prompt, max_tokens_override=16)
