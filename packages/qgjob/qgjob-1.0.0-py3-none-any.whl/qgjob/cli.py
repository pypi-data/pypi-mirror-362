import typer
from qgjob.client import submit_job, get_status

app = typer.Typer(help="Submit and monitor AppWright test jobs.")

@app.command()
def submit(
    org_id: str = typer.Option(..., help="Organization ID"),
    app_version_id: str = typer.Option(..., help="App version identifier"),
    test: str = typer.Option(..., help="Path to the AppWright test script"),
    priority: int = typer.Option(5, help="Job priority (lower is higher)"),
    target: str = typer.Option("emulator", help="Target: emulator, device, browserstack")
):
    """Submit a new test job."""
    result = submit_job(org_id, app_version_id, test, priority, target)
    typer.echo(result)

@app.command()
def status(
    job_id: str = typer.Option(..., help="Job ID to check status for"),
    poll: bool = typer.Option(False, "--poll", help="Poll until job completes or fails"),
):
    """Check the status of a job."""
    from time import sleep
    import sys

    while True:
        result = get_status(job_id)

        if isinstance(result, str):
            typer.secho(result, fg=typer.colors.RED)
            sys.exit(1)

        typer.echo(f"Job {job_id} → {result['status']}")

        if not poll or result["status"] in ("completed", "failed"):
            sys.exit(1 if result["status"] == "failed" else 0)

        sleep(3)
