import paramiko
import tempfile

def change_line_content(host, port, user, password, remote_file_path, line_number, new_content):
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    # Download the file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    local_file_path = temp_file.name
    sftp.get(remote_file_path, local_file_path)

    # Read the file and change the specific line
    with open(local_file_path, "r") as file:
        lines = file.readlines()
    old_content = lines[line_number - 1]
    lines[line_number - 1] = new_content + "\n"

    # Write the changed content back to the file
    with open(local_file_path, "w") as file:
        file.writelines(lines)

    # Upload the file back to the remote machine
    sftp.put(local_file_path, remote_file_path)

     # Log the mutation
    with open("mutations.log", "a") as log_file:
        log_file.write(f"Mutated file {remote_file_path} on {host} at line {line_number} from '{old_content.strip()}' to '{new_content}'\n")

     # Restart the service on the remote machine
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user, password)
    # stdin, stdout, stderr = ssh.exec_command(f"reboot")
    # print(stdout.read().decode())
    # print(stderr.read().decode())

    sftp.close()
    transport.close()
    ssh.close()

# Call the function
change_line_content(
'IP da máquina', 
22, 
'stack', 
'123456', 
'/opt/stack/nova/nova/objects/block_device.py', 
90,
"        'volume_size': fields.IntegerField(nullable=True),")
