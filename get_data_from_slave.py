import os
import subprocess
import time

username = os.getlogin()

# chmod400 = ['icacls.exe .\\petazm42.pem /reset',
#         f'icacls.exe .\\petazm42.pem /grant:r "{username}:(r)"',
#         'icacls.exe .\\petazm42.pem /inheritance:r']

# for command in chmod400:
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()

#     if stdout:
#         print(f'Output: {stdout.decode()}')
#     if stderr:
#         print(f'Error: {stderr.decode()}')

# Iterate over each machine
import concurrent.futures
import subprocess

def run_commands_on_machine(m_name, machine):
    sshcommand = f'ssh -i ".\\petazm42.pem" {machine}'

    # Define the commands to be run
    commands = [
        f'scp -i ".\\petazm42.pem" {machine}:~/result.jpg .',
    ]

    # Run each command
    for command in commands:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Print the output of each command
        if stdout:
            print(f'Output: {stdout.decode()}')
        if stderr:
            print(command)
            print(f'Error: {stderr.decode()}')

machines = {'slave1': 'ec2-user@ec2-13-60-42-99.eu-north-1.compute.amazonaws.com',
}

if __name__ == '__main__':
    
    # Use a ThreadPoolExecutor to run the commands on each machine in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_commands_on_machine, m_name, machine): m_name for m_name, machine in machines.items()}

        for future in concurrent.futures.as_completed(futures):
            m_name = futures[future]
            try:
                future.result()
                print(f'{m_name} updated successfully')
            except Exception as exc:
                print(f'{m_name} generated an exception: {exc}')
