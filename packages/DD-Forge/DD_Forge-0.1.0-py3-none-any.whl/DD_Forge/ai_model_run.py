import subprocess
import os

def generate_ai_driver_remotely(soc, device, interface, os_choice):
    remote_user = "shabari"
    remote_host = "192.168.13.189"
    remote_script = "/media/ava/Data_CI/workspace/shabari/Gladson/DD_Forge_AI/run_ai_model.sh"
    remote_output = f"/media/ava/Data_CI/workspace/shabari/Gladson/DD_Forge_AI/output/{soc}_{os_choice}_{interface}_{device}"
    print(f"In AI_Model_Run SOC:{soc} OS:{os_choice} Interface:{interface} Device:{device}\n")
    # Run the script remotely via SSH
    ssh_cmd = f"ssh {remote_user}@{remote_host} 'bash {remote_script} {soc} {device} {interface} {os_choice}'"
    subprocess.run(ssh_cmd, shell=True, check=True)

    # Create local destination
    local_dir = os.path.join("/home/mcw/Desktop/DD_Forge/DD/DD_Forge_AI_Drivers", f"{soc}_{os_choice}_{device}_{interface}")
    if not os.path.exists(local_dir):
        os.makedirs(local_dir, exist_ok=True)

    # Fetch generated files (.c and .h)
    scp_cmd = f"scp {remote_user}@{remote_host}:{remote_output}/* {local_dir}/"
    subprocess.run(scp_cmd, shell=True, check=True)

    #return os.path.join(local_dir, f"{device}.h"), os.path.join(local_dir, f"{device}.c")
