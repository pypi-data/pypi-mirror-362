from rich.console import Console
import typer


def run(
    app_module: str = "src.main:app",
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True
):

    """
    Run Wyrmx Server.
    """
    from pathlib import Path
    import subprocess, os, sys


    projectRoot = Path.cwd()
    if not (projectRoot / "src").exists(): raise RuntimeError(f"ERROR: No `src` in {projectRoot}. Run from your project root.")

    os.chdir(projectRoot)
    sys.path.insert(0, str(projectRoot))
    
    '''subprocess.run(
        ["poetry", "run", "pyright"],
        cwd=str(projectRoot),
        check=True
    )

    subprocess.run(
        ["poetry", "run", "uvicorn", app_module, "--host", host, "--port", str(port), "--reload" if reload else "--no-reload"],
        cwd=str(projectRoot),
        check=True
    )'''


    
    with Console().status("[bold green][INFO]🔍 Running static type check with Pyright..."):
        subprocess.run(
            [
                "poetry",
                "run",
                "pyright"
            ],
            cwd=str(projectRoot),
            check=True
        )
    
    typer.secho("[INFO]✅ Type check passed. 🚀 Starting FastAPI server...", color=typer.colors.GREEN)

    subprocess.run(
        ["poetry", "run", "uvicorn", app_module, "--host", host, "--port", str(port), "--reload" if reload else "--no-reload"],
        cwd=str(projectRoot),
        check=True
    )


    