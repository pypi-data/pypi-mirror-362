from flask import Flask, render_template, request, jsonify, send_file
import os, uuid
from datetime import datetime
from models import Session, BuildJob
from celery_worker import run_docker_task
from DD_Forge.ai_model_run import generate_ai_driver_remotely

app = Flask(__name__)

DOCKERFILE_TEMPLATE = "Dockerfile.template"
DOCKERFILE_FINAL = "Dockerfile"
#    return render_template("index.html")

@app.route("/")
def front():
    return render_template("index.html")

def update_dockerfile(soc, device, interface, os_choice):
    with open(DOCKERFILE_TEMPLATE, "r") as template:
        content = template.read()
    content = content.replace("{{SOC_PART}}", soc)
    content = content.replace("{{DEVICE_PART}}", device)
    content = content.replace("{{INTERFACE}}", interface)
    content = content.replace("{{OS_CHOICE}}", os_choice)
    with open(DOCKERFILE_FINAL, "w") as dockerfile:
        dockerfile.write(content)

@app.route("/form", methods=["POST","GET"])
def form():
    soc = request.form["soc"]
    device = request.form["device"]
    interface = request.form["interface"]
    os_choice = request.form["os"]
    ai = 0

    update_dockerfile(soc, device, interface, os_choice)

    job_id = str(uuid.uuid4())
    session = Session()
    job = BuildJob(
        job_id=job_id,
        soc=soc,
        device=device,
        interface=interface,
        os_type=os_choice,
        status="queued",
        progress=0,
        logs="",
        output_file=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(job)
    session.commit()
    session.close()

    run_docker_task.apply_async(args=[job_id, soc, device, interface, os_choice, ai])
    return jsonify({"status": "started", "job_id": job_id, "soc": soc, "device": device, "os": os_choice})

@app.route("/generate_ai_driver", methods=["POST","GET"])
def generate_ai_driver():
    try:
        soc = request.form.get("soc")
        device = request.form.get("device")
        interface = request.form.get("interface")
        os_choice = request.form.get("os")
        if not all([soc, device, interface, os_choice]):
            return jsonify({"status": "error", "message": "Missing required parameters"}), 400

        update_dockerfile(soc, device, interface, os_choice)
        generate_ai_driver_remotely(soc, device, interface, os_choice)

        job_id = str(uuid.uuid4())
        session = Session()
        job = BuildJob(
            job_id=job_id,
            soc=soc,
            device=device,
            interface=interface,
            os_type=os_choice,
            status="queued",
            progress=0,
            logs="",
            output_file=None,
            created_at=datetime.datetime(),
            updated_at=datetime.datetime()
        )
        session.add(job)
        session.commit()
        session.close()

        run_docker_task.apply_async(args=[job_id, soc, device, interface, os_choice, 1])
        return jsonify({"status": "success", "job_id": job_id, "soc": soc, "device": device, "os": os_choice})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/status/<job_id>")
def status(job_id):
    session = Session()
    job = session.query(BuildJob).filter_by(job_id=job_id).first()
    session.close()
    if job:
        return jsonify({
            "status": job.status,
            "progress": job.progress,
            "logs": job.logs[-100:],
            "output_file": job.output_file
        })
    return jsonify({"error": "Job not found"}), 404

@app.route("/download")
def download():
    soc = request.args.get('soc')
    os_choice = request.args.get('os')
    device = request.args.get('device')
    if not soc or not os_choice or not device:
        return "Missing required parameters!", 400

    working_dir = os.getcwd()
    output_file = os.path.join(working_dir, f"sdk_{soc}_{os_choice}_{device}.tar.gz")
    if os.path.exists(output_file):
        return send_file(output_file, as_attachment=True, download_name=f"sdk_{soc}_{os_choice}_{device}.tar.gz")
    else:
        return "Requested file not found!", 404

@app.route("/view-dockerfile")
def view_dockerfile():
    try:
        with open(DOCKERFILE_FINAL, "r") as dockerfile:
            content = dockerfile.read()
        return f"<pre>{content}</pre>"
    except FileNotFoundError:
        return "<p style='color: red;'>Dockerfile not found. Generate it first!</p>"

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run()