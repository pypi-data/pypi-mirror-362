# ~/Apps/sclik/app/ipfs_setup_handler.py
import os
import sys
import time
import subprocess
import tempfile

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

    def is_api_responsive(self):
        """Check if the IPFS API is responsive without falling back to offline mode."""
        try:
            subprocess.run([self.ipfs_bin, '--api', '/ip4/127.0.0.1/tcp/5001/http', 'id'], 
                           capture_output=True, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

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

        print("Setting up IPFS as a systemd user service to ensure it keeps running.")
        self.setup_service()

        # Wait for API to become responsive
        for _ in range(60):
            if self.is_api_responsive():
                print("IPFS daemon is now running.")
                return
            time.sleep(1)

        raise RuntimeError("Failed to start IPFS daemon after setup.")

    def run(self, args, **kwargs):
        cmd = [self.ipfs_bin] + args
        return subprocess.run(cmd, **kwargs)
