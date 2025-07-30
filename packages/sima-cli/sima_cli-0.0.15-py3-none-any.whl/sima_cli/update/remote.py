import paramiko
import os
import click
import time
import socket
import itertools
import threading
import sys
import select
from typing import Tuple

DEFAULT_USER = "sima"
DEFAULT_PASSWORD = "edgeai"

def _wait_for_ssh(ip: str, timeout: int = 120):
    """
    Show an animated spinner while waiting for SSH on the target IP to become available.

    Args:
        ip (str): IP address of the target board.
        timeout (int): Maximum seconds to wait.
    """
    spinner = itertools.cycle(['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'])
    stop_event = threading.Event()

    def animate():
        while not stop_event.is_set():
            sys.stdout.write(f"\r🔁 Waiting for board to reboot {next(spinner)} ")
            sys.stdout.flush()
            time.sleep(0.1)

    thread = threading.Thread(target=animate)
    thread.start()

    start_time = time.time()
    success = False
    while time.time() - start_time < timeout:
        try:
            sock = socket.create_connection((ip, 22), timeout=3)
            sock.close()
            success = True
            break
        except (socket.error, paramiko.ssh_exception.SSHException):
            time.sleep(2)  # wait and retry

    stop_event.set()
    thread.join()

    if not success:
        print(f"❌ Timeout: SSH did not become available on {ip} within {timeout} seconds.")
    else:
        print("\r✅ Board is online!           \n")

def get_remote_board_info(ip: str, passwd: str = DEFAULT_PASSWORD) -> Tuple[str, str]:
    """
    Connect to the remote board and retrieve board type and build version.

    Args:
        ip (str): IP address of the board.
        timeout (int): SSH timeout in seconds.

    Returns:
        (board_type, build_version): Tuple of strings, or ('', '') on failure.
    """
    board_type = ""
    build_version = ""

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=DEFAULT_USER, password=passwd, timeout=10)

        stdin, stdout, stderr = ssh.exec_command("cat /etc/build")
        output = stdout.read().decode()
        ssh.close()

        for line in output.splitlines():
            line = line.strip()
            if line.startswith("MACHINE"):
                board_type = line.split("=")[-1].strip()
            elif line.startswith("SIMA_BUILD_VERSION"):
                build_version = line.split("=")[-1].strip()

        return board_type, build_version

    except Exception:
        return "", ""


def _scp_file(sftp, local_path: str, remote_path: str):
    """Upload file via SFTP and report."""
    filename = os.path.basename(local_path)
    click.echo(f"📤 Uploading {filename} → {remote_path}")
    sftp.put(local_path, remote_path)
    click.echo("✅ Upload complete")

def _run_remote_command(ssh, command: str, password: str = DEFAULT_PASSWORD):
    """
    Run a remote command over SSH and stream its output live to the console.
    If the command starts with 'sudo', pipe in the password.

    Args:
        ssh (paramiko.SSHClient): Active SSH connection.
        command (str): The command to run on the remote host.
        password (str): Password to use if the command requires sudo.
    """
    click.echo(f"🚀 Running on remote: {command}")

    needs_sudo = command.strip().startswith("sudo")
    if needs_sudo:
        # Use -S to allow password from stdin
        command = f"sudo -S {command[len('sudo '):]}"

    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

    if needs_sudo:
        # Send password immediately, followed by newline
        stdin.write(password + "\n")
        stdin.flush()

    while not stdout.channel.exit_status_ready():
        rl, _, _ = select.select([stdout.channel], [], [], 0.5)
        if rl:
            if stdout.channel.recv_ready():
                output = stdout.channel.recv(4096).decode("utf-8", errors="replace")
                for line in output.splitlines():
                    click.echo(f"📄 {line}")
            if stdout.channel.recv_stderr_ready():
                err_output = stdout.channel.recv_stderr(4096).decode("utf-8", errors="replace")
                for line in err_output.splitlines():
                    click.echo(f"⚠️ {line}")

    # Final remaining output
    remaining = stdout.read().decode("utf-8", errors="replace")
    for line in remaining.splitlines():
        click.echo(f"📄 {line}")

    remaining_err = stderr.read().decode("utf-8", errors="replace")
    for line in remaining_err.splitlines():
        click.echo(f"⚠️ {line}")

def reboot_remote_board(ip: str, passwd: str):
    """
    Reboot remote board by sending SSH command
    """    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ip, username=DEFAULT_USER, password=passwd, timeout=10)

        _run_remote_command(ssh, "sudo systemctl stop watchdog", password=passwd)
        _run_remote_command(ssh, "sudo bash -c 'echo b > /proc/sysrq-trigger'", password=passwd)

    except Exception as reboot_err:
        click.echo(f"⚠️  Unable to connect to the remote board")

def push_and_update_remote_board(ip: str, troot_path: str, palette_path: str, passwd: str, reboot_and_wait: bool):
    """
    Upload and install firmware images to remote board over SSH.
    Assumes default credentials: sima / edgeai.
    Includes reboot and SSH wait after each step.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, username=DEFAULT_USER, password=passwd, timeout=10)
        sftp = ssh.open_sftp()
        remote_dir = "/tmp"

        # Upload tRoot image
        troot_name = os.path.basename(troot_path)
        palette_name = os.path.basename(palette_path)
        _scp_file(sftp, troot_path, os.path.join(remote_dir, troot_name))
        click.echo("🚀 Uploaded tRoot image.")

        # Run tRoot update
        _run_remote_command(
            ssh,
            f"sudo swupdate -H simaai-image-troot:1.0 -i /tmp/{troot_name}", password=passwd
        )
        click.echo("✅ tRoot update complete.")

        # Upload Palette image
        _scp_file(sftp, palette_path, os.path.join(remote_dir, palette_name))
        click.echo("🚀 Uploaded system image.")

        # Run Palette update
        _run_remote_command(
            ssh,
            f"sudo swupdate -H simaai-image-palette:1.0 -i /tmp/{palette_name}",
            password=passwd
        )
        click.echo("✅ Board image update complete.")

        # In the case of PCIe system, we don't need to reboot the card, instead, we will let it finish then update the PCIe driver in the host
        # After that we can reboot the whole system.
        if reboot_and_wait:
            # Reboot and expect disconnect
            click.echo("🔁 Rebooting board after update. Waiting for reconnection...")

            try:
                _run_remote_command(ssh, "sudo systemctl stop watchdog", password=passwd)
                _run_remote_command(ssh, "sudo bash -c 'echo b > /proc/sysrq-trigger'", password=passwd)

            except Exception as reboot_err:
                click.echo(f"⚠️  SSH connection lost due to reboot (expected): {reboot_err}, please powercycle the device...")

            try:
                ssh.close()
            except Exception:
                pass

            # Wait for board to come back
            time.sleep(5)
            _wait_for_ssh(ip, timeout=120)

            # Reconnect and verify version
            try:
                click.echo("🔍 Reconnecting to verify build version...")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=DEFAULT_USER, password=passwd, timeout=10)

                _run_remote_command(ssh, "cat /etc/build | grep SIMA_BUILD_VERSION", password=passwd)
                ssh.close()
            except Exception as e:
                click.echo(f"❌ Unable to validate the version: {e}")

        click.echo("✅ Firmware update process complete.")

    except Exception as e:
        click.echo(f"❌ Remote update failed: {e}")


if __name__ == "__main__":
    _wait_for_ssh("192.168.2.20", timeout=60)
    print(get_remote_board_info("192.168.2.20"))