#!/usr/bin/env python3
# filepath: ps_console/src/ps_console.py
"""
Interactive console program for controlling Hanmatek HM310T power supply.
Cross-platform compatible (Windows and macOS).
"""

import argparse
import sys
import time
import select
from pyHM310T import PowerSupply, PowerSupplyCommunicationError


class PowerSupplyConsole:
    """Interactive console for power supply control."""

    def __init__(self, port, baudrate=9600, slave=1):
        """Initialize the power supply connection."""
        self.port = port
        self.baudrate = baudrate
        self.slave = slave
        self.ps = None


    def connect(self):
        """Connect to the power supply."""

        try:
            print(f"Connecting to power supply on {self.port}...")
            self.ps = PowerSupply(
                port=self.port,
                baudrate=self.baudrate,
                slave=self.slave
            )
            print("Connected successfully!")
            return True

        except PowerSupplyCommunicationError as e:
            print(f"Error: Failed to connect to power supply - {e}")
            return False

        except Exception as e:
            print(f"Error: {e}")
            return False


    def disconnect(self):
        """Disconnect from the power supply."""
        if self.ps:
            self.ps.close()
            print("Disconnected from power supply.")


    def cmd_help(self, args=None):
        """Display help information."""
        help_text = """
Available commands (short/long):
  sv / set_voltage <value>  - Set output voltage (0-30V)
  gv / get_voltage          - Get current voltage setting
  ra / ramp <v1> <v2> <sec> - Ramp voltage from v1 to v2 over time (10-360 sec)

  sc / set_current <value>  - Set output current (0-10A)
  gc / get_current          - Get current current setting

  en / enable               - Enable power output
  dis / disable             - Disable power output

  st / status               - Show power supply status
  disp / display            - Show output display values (actual V/A/W)

  ovp [value]               - Get/Set Over Voltage Protection
  ocp [value]               - Get/Set Over Current Protection
  opp [value]               - Get/Set Over Power Protection
  prot / protection         - Show protection status

  h / help                  - Show this help message
  q / quit / exit           - Exit the program
"""
        print(help_text)


    def cmd_set_voltage(self, args):
        """Set the output voltage."""
        if not args:
            print("Error: Voltage value required. Usage: set_voltage <value>")
            return

        try:
            voltage = float(args[0])
            self.ps.set_voltage(voltage)
            print(f"Voltage set to {voltage}V")

        except ValueError:
            print("Error: Invalid voltage value. Must be a number.")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_get_voltage(self, args=None):
        """Get the current voltage setting."""

        try:
            voltage = self.ps.get_voltage()
            print(f"Set voltage: {voltage}V")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_set_current(self, args):
        """Set the output current."""
        if not args:
            print("Error: Current value required. Usage: set_current <value>")
            return

        try:
            current = float(args[0])
            self.ps.set_current(current)
            print(f"Current set to {current}A")

        except ValueError:
            print("Error: Invalid current value. Must be a number.")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_get_current(self, args=None):
        """Get the current current setting."""

        try:
            current = self.ps.get_current()
            print(f"Set current: {current}A")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_enable(self, args=None):
        """Enable the power output."""

        try:
            self.ps.enable_output()
            print("Power output enabled")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_disable(self, args=None):
        """Disable the power output."""

        try:
            self.ps.disable_output()
            print("Power output disabled")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_status(self, args=None):
        """Display the current power supply status."""

        try:
            enabled = self.ps.is_output_enabled()
            voltage = self.ps.get_voltage()
            current = self.ps.get_current()

            print("\n=== Power Supply Status ===")
            print(f"Output: {'ENABLED' if enabled else 'DISABLED'}")
            print(f"Set Voltage: {voltage}V")
            print(f"Set Current: {current}A")
            print("===========================\n")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_display(self, args=None):
        """Display the actual output values."""

        try:
            voltage = self.ps.get_voltage_display()
            current = self.ps.get_current_display()
            power = self.ps.get_power_display()

            print("\n=== Output Display ===")
            print(f"Voltage: {voltage}V")
            print(f"Current: {current}A")
            print(f"Power: {power}W")
            print("======================\n")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_ovp(self, args):
        """Get or set Over Voltage Protection."""

        try:
            if args:
                value = float(args[0])
                self.ps.set_ovp(value)
                print(f"OVP set to {value}V")
            else:
                value = self.ps.get_ovp()
                print(f"OVP: {value}V")

        except ValueError:
            print("Error: Invalid OVP value. Must be a number.")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_ocp(self, args):
        """Get or set Over Current Protection."""

        try:
            if args:
                value = float(args[0])
                self.ps.set_ocp(value)
                print(f"OCP set to {value}A")
            else:
                value = self.ps.get_ocp()
                print(f"OCP: {value}A")

        except ValueError:
            print("Error: Invalid OCP value. Must be a number.")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_opp(self, args):
        """Get or set Over Power Protection."""

        try:
            if args:
                value = float(args[0])
                self.ps.set_opp(value)
                print(f"OPP set to {value}W")
            else:
                value = self.ps.get_opp()
                print(f"OPP: {value}W")

        except ValueError:
            print("Error: Invalid OPP value. Must be a number.")

        except Exception as e:
            print(f"Error: {e}")


    def cmd_protection(self, args=None):
        """Display protection status."""

        try:
            status = self.ps.get_protection_status()
            print("\n=== Protection Status ===")
            print(f"Over Voltage (OVP): {'TRIGGERED' if status['isOVP'] else 'OK'}")
            print(f"Over Current (OCP): {'TRIGGERED' if status['isOCP'] else 'OK'}")
            print(f"Over Power (OPP): {'TRIGGERED' if status['isOPP'] else 'OK'}")
            print(f"Over Temperature (OTP): {'TRIGGERED' if status['isOTP'] else 'OK'}")
            print(f"Short Circuit (SCP): {'TRIGGERED' if status['isSCP'] else 'OK'}")
            print("=========================\n")

        except Exception as e:
            print(f"Error: {e}")


    def _check_keypress(self):
        """Check if a key has been pressed (cross-platform)."""
        if sys.platform == 'win32':
            import msvcrt
            return msvcrt.kbhit()
        else:
            # Unix/macOS
            return select.select([sys.stdin], [], [], 0)[0] != []


    def cmd_ramp(self, args):
        """Ramp voltage from start to end over specified time."""
        if len(args) < 3:
            print("Error: Usage: ramp <start_voltage> <end_voltage> <time_seconds>")
            return

        try:
            start_voltage = float(args[0])
            end_voltage = float(args[1])
            time_span = float(args[2])

            # Validate time span
            if time_span < 10 or time_span > 360:
                print("Error: Time span must be between 10 and 360 seconds")
                return

            # Calculate step parameters
            update_interval = 0.5  # Update every half second
            num_steps = int(time_span / update_interval)
            voltage_step = (end_voltage - start_voltage) / num_steps

            print(f"\nRamping voltage from {start_voltage}V to {end_voltage}V over {time_span} seconds")
            print("Press any key to stop ramping...\n")

            # Save terminal settings on Unix/macOS for non-blocking input
            if sys.platform != 'win32':
                import tty
                import termios
                old_settings = termios.tcgetattr(sys.stdin)

                try:
                    tty.setcbreak(sys.stdin.fileno())

                    current_voltage = start_voltage
                    for step in range(num_steps + 1):
                        # Check for keypress to stop
                        if self._check_keypress():
                            if sys.platform == 'win32':
                                import msvcrt
                                msvcrt.getch()  # Clear the key buffer
                            else:
                                sys.stdin.read(1)  # Clear the key buffer
                            print("\nRamping stopped by user")
                            break

                        # Set voltage
                        self.ps.set_voltage(current_voltage)

                        # Display progress
                        elapsed = step * update_interval
                        progress = (step / num_steps) * 100 if num_steps > 0 else 100
                        print(f"Time: {elapsed:.1f}s / {time_span}s | Voltage: {current_voltage:.2f}V | Progress: {progress:.1f}%", end='\r')

                        # Break if we've reached the end
                        if step >= num_steps:
                            break

                        # Wait for next update
                        time.sleep(update_interval)
                        current_voltage += voltage_step

                    # Ensure final voltage is set
                    self.ps.set_voltage(end_voltage)
                    print(f"\nRamping complete! Final voltage: {end_voltage}V" + " " * 20)

                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

            else:
                # Windows implementation
                import msvcrt
                current_voltage = start_voltage
                for step in range(num_steps + 1):
                    # Check for keypress to stop
                    if self._check_keypress():
                        msvcrt.getch()  # Clear the key buffer
                        print("\nRamping stopped by user")
                        break

                    # Set voltage
                    self.ps.set_voltage(current_voltage)

                    # Display progress
                    elapsed = step * update_interval
                    progress = (step / num_steps) * 100 if num_steps > 0 else 100
                    print(f"Time: {elapsed:.1f}s / {time_span}s | Voltage: {current_voltage:.2f}V | Progress: {progress:.1f}%", end='\r')

                    # Break if we've reached the end
                    if step >= num_steps:
                        break

                    # Wait for next update
                    time.sleep(update_interval)
                    current_voltage += voltage_step

                # Ensure final voltage is set
                self.ps.set_voltage(end_voltage)
                print(f"\nRamping complete! Final voltage: {end_voltage}V" + " " * 20)

        except ValueError:
            print("Error: Invalid parameter. All values must be numbers.")

        except Exception as e:
            print(f"Error: {e}")


    def run(self):
        """Run the interactive console."""
        if not self.connect():
            return 1

        print("\nPower Supply Interactive Console")
        print("Type 'help' for available commands, 'quit' to exit\n")

        # Command mapping (both short and long versions)
        commands = {
            # Voltage commands
            'set_voltage': self.cmd_set_voltage,
            'sv': self.cmd_set_voltage,
            'get_voltage': self.cmd_get_voltage,
            'gv': self.cmd_get_voltage,
            'ramp': self.cmd_ramp,
            'ra': self.cmd_ramp,
            # Current commands
            'set_current': self.cmd_set_current,
            'sc': self.cmd_set_current,
            'get_current': self.cmd_get_current,
            'gc': self.cmd_get_current,
            # Output control
            'enable': self.cmd_enable,
            'en': self.cmd_enable,
            'disable': self.cmd_disable,
            'dis': self.cmd_disable,
            # Status and display
            'status': self.cmd_status,
            'st': self.cmd_status,
            'display': self.cmd_display,
            'disp': self.cmd_display,
            # Protection settings
            'ovp': self.cmd_ovp,
            'ocp': self.cmd_ocp,
            'opp': self.cmd_opp,
            'protection': self.cmd_protection,
            'prot': self.cmd_protection,
            # Help
            'help': self.cmd_help,
            'h': self.cmd_help,
        }

        self.cmd_help()

        try:
            while True:

                try:
                    # Get user input
                    user_input = input("PS> ").strip()

                    if not user_input:
                        continue

                    # Parse command and arguments
                    parts = user_input.split()
                    command = parts[0].lower()
                    args = parts[1:] if len(parts) > 1 else []

                    # Check for exit commands
                    if command in ['quit', 'exit', 'q']:
                        # Ask if user wants to disable output before exiting
                        if self.ps.is_output_enabled():
                            response = input("Output is enabled. Disable before exiting? (y/n): ")
                            if response.lower() in ['y', 'yes']:
                                self.ps.disable_output()
                                print("Output disabled.")
                        print("Goodbye!")
                        break

                    # Execute command
                    if command in commands:
                        commands[command](args)
                    else:
                        print(f"Unknown command: {command}. Type 'help' for available commands.")

                except KeyboardInterrupt:
                    print("\nUse 'quit' or 'exit' to leave the program.")

                except EOFError:
                    print("\nGoodbye!")
                    break

        finally:
            self.disconnect()

        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Interactive console for Hanmatek HM310T power supply control',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  Windows:  python interactive_console.py COM3
  macOS:    python interactive_console.py /dev/ttyUSB0
  Linux:    python interactive_console.py /dev/ttyUSB0

  With custom baudrate:
            python interactive_console.py COM3 --baudrate 115200
        """
    )

    parser.add_argument(
        'port',
        nargs='?',
        help='Serial port (e.g., COM3 on Windows, /dev/ttyUSB0 on macOS/Linux)'
    )
    parser.add_argument(
        '--baudrate', '-b',
        type=int,
        default=9600,
        help='Baudrate for serial communication (default: 9600)'
    )
    parser.add_argument(
        '--slave', '-s',
        type=int,
        default=1,
        help='Modbus slave address (default: 1)'
    )

    args = parser.parse_args()

    # If port was not provided on the command line, prompt the user for it
    if not args.port:
        try:
            user_port = input("Enter serial port (e.g., COM3 or /dev/ttyUSB0): ").strip()
        except EOFError:
            print("Error: No port provided.")
            parser.print_help()
            return 2

        if not user_port:
            print("Error: No port provided.")
            parser.print_help()
            return 2

        args.port = user_port

    # Create and run console
    console = PowerSupplyConsole(
        port=args.port,
        baudrate=args.baudrate,
        slave=args.slave
    )

    return console.run()


if __name__ == '__main__':
    sys.exit(main())