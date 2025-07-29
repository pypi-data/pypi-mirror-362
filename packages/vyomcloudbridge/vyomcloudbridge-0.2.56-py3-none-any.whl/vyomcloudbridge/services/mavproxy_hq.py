from datetime import datetime
import glob
import os
import subprocess
import time

from vyomcloudbridge.utils.common import ServiceAbstract, get_mission_upload_dir


class MavproxyHq(ServiceAbstract):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.proc = None

    def start(self):
        try:
            # Step 1: Auto-detect USB device
            tty_devices = glob.glob("/dev/ttyUSB*")
            if not tty_devices:
                self.logger.error("No /dev/ttyUSB* device found. Exiting.")
                return

            tty_usb = tty_devices[0]
            uart_baud = 921600

            # Step 2: Define system/component ID
            sysid_thismav = 156
            compid_thismav = 191

            # Step 3: Prepare log directory and filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_log_dir = f"/var/log/vyomcloudbridge/mavlogs"
            log_dir = f"{base_log_dir}/{sysid_thismav}/{timestamp}/"
            log_file = f"{log_dir}mavlog_{timestamp}.tlog"

            # Step 4: Ensure log directory exists
            if not os.path.exists(log_dir):
                self.logger.info(f"Creating log directory: {log_dir}")
                os.makedirs(log_dir, exist_ok=True)
            else:
                self.logger.info(f"Log directory exists: {log_dir}")

            self.logger.info(f"Using MAVProxy device: {tty_usb}")

            # Step 5: Build MAVProxy command
            mavproxy_cmd = [
                "/vyomos/venv/bin/mavproxy.py",
                f"--master={tty_usb},{uart_baud}",
                "--daemon",
                "--out=udp:127.0.0.1:14550",
                "--out=udp:127.0.0.1:14555",
                "--out=udp:127.0.0.1:14556",
                "--out=udp:127.0.0.1:14557",
                "--out=udp:127.0.0.1:14560",
                "--out=udp:127.0.0.1:14565",
                "--out=udp:127.0.0.1:14600",
                f"--source-system={sysid_thismav}",
                f"--source-component={compid_thismav}",
                f"--logfile={log_file}",
                "--load-module=dataflash_logger",
            ]

            # Step 6: Launch MAVProxy
            with open("/tmp/mavproxy.log", "w") as log_out:
                self.proc = subprocess.Popen(
                    mavproxy_cmd, stdout=log_out, stderr=subprocess.STDOUT
                )
                self.logger.info(
                    f"MAVProxy started in background (PID: {self.proc.pid})"
                )

            # Step 7: Show log directory contents
            self.logger.info("MAVProxy log files:")
            subprocess.run(["ls", "-lh", log_dir])

        except Exception as e:
            self.logger.error(f"Error starting Mavproxy service: {str(e)}")
            self.stop()
            raise

    def stop(self):
        self.is_running = False

        if self.proc and self.proc.poll() is None:
            self.logger.info("Stopping MAVProxy process")
            self.proc.terminate()
            self.proc.wait()
        else:
            self.logger.info("No MAVProxy process to stop.")

    def cleanup(self):
        try:
            if hasattr(self, "rmq_conn") and self.rmq_conn and self.rmq_conn.is_open:
                self.rmq_conn.close()
        except Exception as e:
            self.logger.error(f"Error closing RabbitMQ connection: {str(e)}")

        try:
            self.rabbit_mq.close()
        except Exception as e:
            self.logger.error(f"Error closing RabbitMQ connection: {str(e)}")

        try:
            self.root_store.cleanup()
        except Exception as e:
            self.logger.error(f"Error closing Root store connection: {str(e)}")

    def is_healthy(self):
        """
        Check if the service is healthy.
        """
        return self.is_running

    def __del__(self):
        """Destructor called by garbage collector to ensure resources are cleaned up, when object is about to be destroyed"""
        try:
            self.logger.error(
                "Destructor called by garbage collector to cleanup MachineStats"
            )
            self.stop()
        except Exception as e:
            pass


def main():
    """Mavproxy service"""
    print("Starting Mavproxy service")

    mavproxy_service = MavproxyHq()

    try:
        # Simulate data arriving
        mavproxy_service.start()
        # Let it run for a short while
        time.sleep(20)

    finally:
        # Clean up
        mavproxy_service.stop()

    print("Completed Mavproxy service")


if __name__ == "__main__":
    main()
