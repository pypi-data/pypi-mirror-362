# ~/Apps/sclik/app/ipfs_setup_handler.py
import os
import sys
import time
import subprocess
import tempfile
import socket
import json

class IpfsSetupHandler:
    def __init__(self):
        self.ipfs_bin = os.path.join(os.path.expanduser('~'), '.local', 'bin', 'ipfs')
        self.ipfs_home = os.path.expanduser('~/.ipfs')
        self.service_name = 'ipfs.service'
        self.service_dir = os.path.join(os.path.expanduser('~'), '.config', 'systemd', 'user')
        os.makedirs(os.path.dirname(self.ipfs_bin), exist_ok=True)

    def install_ipfs(self):
        url = "https://dist.ipfs.tech/kubo/v0.35.0/kubo_v0.35.0_linux-amd64.tar.gz"
        with tempfile.TemporaryDirectory() as temp_dir:
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            try:
                subprocess.run(['wget', url], check=True)
                file_name = os.path.basename(url)
                subprocess.run(['tar', '-xvzf', file_name], check=True)
                subprocess.run(['cp', 'kubo/ipfs', self.ipfs_bin], check=True)
                os.chmod(self.ipfs_bin, 0o755)  # Ensure executable
            except subprocess.CalledProcessError as e:
                print(f"Error during IPFS installation: {e}")
                sys.exit(1)
            finally:
                os.chdir(original_dir)

    def init_ipfs(self):
        if not os.path.exists(self.ipfs_home):
            try:
                subprocess.run([self.ipfs_bin, 'init'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to initialize IPFS: {e}")
                sys.exit(1)

    def setup_service(self):
        service_path = os.path.join(self.service_dir, self.service_name)
        os.makedirs(self.service_dir, exist_ok=True)

        service_content = f"""[Unit]
Description=IPFS Daemon

[Service]
ExecStart={self.ipfs_bin} daemon
Restart=always

[Install]
WantedBy=default.target
"""

        with open(service_path, 'w') as f:
            f.write(service_content)

        try:
            subprocess.run(['systemctl', '--user', 'daemon-reload'], check=True)
            subprocess.run(['systemctl', '--user', 'enable', '--now', self.service_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to set up IPFS service: {e}")
            print("Note: This setup assumes systemd with user services support. If your system doesn't support this, please run IPFS manually.")
            sys.exit(1)

    def get_current_api_port(self):
        config_path = os.path.join(self.ipfs_home, 'config')
        if not os.path.exists(config_path):
            return 5001
        with open(config_path, 'r') as f:
            config = json.load(f)
        api_addr = config.get('Addresses', {}).get('API', '/ip4/0.0.0.0/tcp/5001')
        parts = api_addr.split('/')
        return int(parts[-1])

    def is_api_responsive(self):
        """Check if the IPFS API is responsive without falling back to offline mode."""
        api_port = self.get_current_api_port()
        try:
            subprocess.run([self.ipfs_bin, '--api', f'/ip4/127.0.0.1/tcp/{api_port}/http', 'id'], 
                           capture_output=True, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def is_port_free(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            try:
                s.bind((host, port))
                return True
            except OSError:
                return False

    def find_available_port(self, host, start_port):
        for port in range(start_port, start_port + 100):
            if self.is_port_free(host, port):
                return port
        raise RuntimeError(f"No available port found starting from {start_port} on {host}")

    def configure_ports(self):
        # API port
        default_api_port = 5001
        api_host = '127.0.0.1'
        if not self.is_port_free(api_host, default_api_port):
            api_port = self.find_available_port(api_host, 5002)
            self.run(['config', 'Addresses.API', f'/ip4/{api_host}/tcp/{api_port}'])
            print(f"Changed API port to {api_port} due to conflict.")

        # Gateway port
        default_gateway_port = 8080
        gateway_host = '127.0.0.1'
        if not self.is_port_free(gateway_host, default_gateway_port):
            gateway_port = self.find_available_port(gateway_host, 5002)
            self.run(['config', 'Addresses.Gateway', f'/ip4/{gateway_host}/tcp/{gateway_port}'])
            print(f"Changed Gateway port to {gateway_port} due to conflict.")

        # Swarm ports (TCP and UDP, but check TCP)
        default_swarm_port = 4001
        swarm_host = '0.0.0.0'
        if not self.is_port_free(swarm_host, default_swarm_port):
            swarm_port = self.find_available_port(swarm_host, 5002)
            swarm_addrs = [
                f"/ip4/0.0.0.0/tcp/{swarm_port}",
                f"/ip6/::/tcp/{swarm_port}",
                f"/ip4/0.0.0.0/udp/{swarm_port}/quic-v1",
                f"/ip6/::/udp/{swarm_port}/quic-v1",
            ]
            self.run(['config', '--json', 'Addresses.Swarm', json.dumps(swarm_addrs)])
            print(f"Changed Swarm port to {swarm_port} due to conflict.")

    def fix_stale_lock(self):
        lock_path = os.path.join(self.ipfs_home, 'repo.lock')
        if not os.path.exists(lock_path):
            return

        try:
            result = subprocess.run(['fuser', lock_path], capture_output=True, text=True, check=False)
            if result.returncode == 1 and not result.stdout.strip():  # No process holding the lock
                print("Removing stale lock file...")
                os.remove(lock_path)
        except FileNotFoundError:  # fuser not available
            print("fuser not found; attempting to remove potential stale lock...")
            os.remove(lock_path)

    def ensure_running(self):
        if self.is_api_responsive():
            return

        print("IPFS daemon not responsive, attempting fix...")
        self.fix_stale_lock()

        if self.is_api_responsive():
            return

        # Stop service if exists
        try:
            subprocess.run(['systemctl', '--user', 'stop', self.service_name], check=False)
        except FileNotFoundError:
            pass  # No systemctl

        # Clean up lock and api files
        lock_path = os.path.join(self.ipfs_home, 'repo.lock')
        api_path = os.path.join(self.ipfs_home, 'api')
        if os.path.exists(lock_path):
            os.remove(lock_path)
        if os.path.exists(api_path):
            os.remove(api_path)

        self.init_ipfs()
        self.configure_ports()

        print("Setting up IPFS as a systemd user service to ensure it keeps running.")
        self.setup_service()

        # Wait for API to become responsive
        for _ in range(60):
            if self.is_api_responsive():
                print("IPFS daemon is now running.")
                return
            time.sleep(1)

        # Diagnostic output before raising error
        try:
            status_result = subprocess.run(['systemctl', '--user', 'status', self.service_name], capture_output=True, text=True, check=False)
            print("IPFS service status:\n" + status_result.stdout)
            if status_result.stderr:
                print("Status error:\n" + status_result.stderr)

            logs_result = subprocess.run(['journalctl', '--user', '-u', self.service_name, '-n', '30', '--no-pager'], capture_output=True, text=True, check=False)
            print("Last 30 journalctl lines for ipfs.service:\n" + logs_result.stdout)
            if logs_result.stderr:
                print("Journalctl error:\n" + logs_result.stderr)
        except Exception as e:
            print(f"Failed to retrieve service status or logs: {e}")

        raise RuntimeError("Failed to start IPFS daemon after setup. Check above logs for details.")

    def run(self, args, **kwargs):
        cmd = [self.ipfs_bin] + args
        return subprocess.run(cmd, **kwargs)
