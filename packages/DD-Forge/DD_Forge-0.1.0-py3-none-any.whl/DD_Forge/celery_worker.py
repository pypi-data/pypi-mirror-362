import os
import re
import subprocess
import signal
from datetime import datetime
from celery import Celery
from models import Session, BuildJob
from driver_select import get_driver

celery = Celery("worker", broker="redis://localhost:6379/0")

# Global cancellation flag
terminate_requested = False

def handle_sigterm(signum, frame):
    global terminate_requested
    terminate_requested = True
    print(f"[CANCEL] Signal {signum} received. Termination requested.")

# Register signal handlers
signal.signal(signal.SIGINT, handle_sigterm)
signal.signal(signal.SIGTERM, handle_sigterm)

@celery.task(bind=True)
def run_docker_task(self, job_id, soc, device, interface, os_choice, ai):
    session = Session()
    job = session.query(BuildJob).filter_by(job_id=job_id).first()

    # Clear logs & update status
    job.logs = ""
    job.status = "running"
    job.progress = 0
    job.updated_at = datetime.utcnow()
    session.commit()

    log_file_path = f"build_logs/{job_id}.log"
    os.makedirs("build_logs", exist_ok=True)

    try:
        image_name = f"sdk_{soc}_{os_choice}"

        with open(log_file_path, "w") as logfile:
            try:
                subprocess.run(["docker", "image", "inspect", image_name],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                logfile.write(f"{image_name} already exists.\n")
            except subprocess.CalledProcessError:
                logfile.write(f"Building {image_name}...\n")
                build_proc = subprocess.Popen(
                    ["docker", "build", "--no-cache", "-t", image_name, "."],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1
                )

                for line in build_proc.stdout:
                    if terminate_requested:
                        job.status = "cancelled"
                        logfile.write("\n[CANCELLED] Build aborted by user.\n")
                        break

                    logfile.write(line)
                    match = re.search(r"\[\s*(\d+)/(\d+)\]", line)
                    if match:
                        current = int(match.group(1))
                        total = int(match.group(2))
                        job.progress = int((current / total) * 20)
                        job.updated_at = datetime.utcnow()
                        session.commit()

                build_proc.wait()

            if terminate_requested:
                job.status = "cancelled"
                job.updated_at = datetime.utcnow()
                session.commit()
                return

            # Run integration script
            urls = get_driver(soc, os_choice, device, interface)
            urls_str = " ".join(urls)
            script = "run_container_ai.sh" if ai else "run_container.sh"

            steps = ["Copying", "Pinmux", "Compiling", "Compressing", "Copying"]
            run_proc = subprocess.Popen(
                ["bash", script, urls_str, soc, os_choice, device, interface],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )

            for line in run_proc.stdout:
                if terminate_requested:
                    job.status = "cancelled"
                    logfile.write("\n[CANCELLED] Script execution aborted by user.\n")
                    break

                logfile.write(line)
                for i, step in enumerate(steps):
                    if step in line:
                        job.progress = 20 + int(((i + 1) / len(steps)) * 80)
                        break

                job.updated_at = datetime.utcnow()
                session.commit()

            run_proc.wait()

        # Store log file content in DB after all steps
        with open(log_file_path, "r") as f:
            job.logs = f.read()

        if terminate_requested:
            job.status = "cancelled"
        else:
            job.status = "done" if run_proc.returncode == 0 else "error"
            if job.status == "done":
                job.output_file = f"sdk_{soc}_{os_choice}_{device}.tar.gz"

        job.progress = 100 if job.status == "done" else job.progress
        job.updated_at = datetime.utcnow()
        session.commit()

    except Exception as e:
        job.status = "error"
        job.logs += f"\n[ERROR] {str(e)}"
        job.updated_at = datetime.utcnow()
        session.commit()

    finally:
        session.close()
