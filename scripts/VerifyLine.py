import paramiko

def get_line_content(host, port, user, password, remote_file_path, line_number):
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    # Download the file
    local_file_path = 'local_file.txt'
    sftp.get(remote_file_path, local_file_path)

    # Read the specific line
    with open(local_file_path, 'r') as file:
        lines = file.readlines()

    line_content = lines[line_number - 1]

    sftp.close()
    transport.close()

    return line_content

# Call the function
line_content = get_line_content(
'IP da máquina', 
22, 
'stack', 
'123456', 
'/opt/stack/nova/nova/objects/block_device.py', 
90)
print(line_content)