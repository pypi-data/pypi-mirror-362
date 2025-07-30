#!/usr/bin/env python3
"""simulate.py - Launch a RemoteRL simulator process (environment host)

This module starts a RemoteRL **simulator** instance, which registers with the RemoteRL 
service and hosts environments for remote trainers. It should be run on a machine where 
the environments (simulators or robots) reside **before** starting any trainer. Once launched, 
it will block indefinitely, waiting for trainers to connect and issue environment commands.

Key behavior:
- Resolves the RemoteRL API key from configuration (no direct CLI args). If the API key is not 
  provided, it looks for it in:
  1. The environment variable `REMOTERL_API_KEY`.
  2. The user config file (e.g. `~/.config/remoterl/config.json` or path specified by 
     `REMOTERL_CONFIG_PATH`).
  If no API key is found, the simulator will exit with an instructive error (prompting you to set 
  up the API key via `remoterl register` or environment variable).
- Calls `remoterl.init(api_key, role="simulator")` to connect to the RemoteRL cloud gateway. On 
  successful connection, this process is marked as a simulator and begins waiting for work.
- Runs indefinitely until interrupted (Ctrl+C), at which point it will shut down gracefully.

**Usage:** Typically invoked through the CLI as `remoterl simulate`. On startup, it prints a 
confirmation message (including a short form of the API key) indicating the simulator is running. 
From that point, any remote trainer using the same API key can request environments and steps, 
which this process will handle internally. Use Ctrl+C to terminate the simulator when done.
"""
from __future__ import annotations
import typer
from typing import List, Dict, Any
from .helpers import parse_cli_tail
import remoterl   # pip install remoterl
from remoterl.config import resolve_api_key

def simulate(params: List[str] | Dict[str, Any] | None = None) -> None:
    """Dispatch to the selected *RL framework* with the parsed configuration."""
    # ------------------------------------------------------------------
    # Parameter normalisation
    # ------------------------------------------------------------------
    if params is None:
        params = {}
    if isinstance(params, list):  # raw CLI tail → parse
        params = parse_cli_tail(params)
    if not isinstance(params, dict):
        typer.secho("*params* must be a dict or list of tokens.", fg="red", bold=True)
        raise typer.Exit(code=1)
    
    max_env_runners = params.get("max_env_runners", 32) 
    
    api_key = resolve_api_key()
    if not api_key:
        typer.secho(
            "Error: No RemoteRL API key found.\n"
            "Set the REMOTERL_API_KEY env var or run `remoterl register` first.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    typer.echo(f"**RemoteRL Simulator Started** (API key: {api_key[:8]}...)\n")

    try:
        remoterl.init(
            api_key,
            role="simulator",
            max_env_runners=max_env_runners,
        )
    except KeyboardInterrupt:
        typer.echo("Simulation aborted by user.", err=True)
        raise typer.Exit(code=1)


# input *args, **kwargs to allow for future extensions
if __name__ == "__main__":
    simulate()
