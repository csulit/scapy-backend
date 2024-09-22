## Installation and Running Instructions

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package installer)
- virtualenv (optional but recommended)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/ping-notifier.git
   cd ping-notifier
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

### Configuration

1. **Set up environment variables:**
   Create a `.env` file in the root directory of the project and add the following variables:
   ```env
   PUSHER_APP_ID=your_pusher_app_id
   PUSHER_KEY=your_pusher_key
   PUSHER_SECRET=your_pusher_secret
   PUSHER_CLUSTER=your_pusher_cluster
   ```

### Running the Program

1. **Run the script:**
   ```sh
   python /path/to/your/script.py
   ```

### Running as a Service

1. **Set up the systemd service:**
   Create a `ping_notifier.service` file in `/etc/systemd/system/` with the following content:
   ```ini
   [Unit]
   Description=Ping Notifier Service
   After=network.target

   [Service]
   ExecStart=sudo /path/to/your/venv/bin/python /path/to/your/script.py
   WorkingDirectory=/path/to/your/
   Restart=always
   User=root
   Environment=PYTHONUNBUFFERED=1

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start the service:**
   ```sh
   sudo systemctl enable ping_notifier.service
   sudo systemctl start ping_notifier.service
   ```

### Additional Notes

- Ensure that the `.env` file is included in your `.gitignore` to avoid committing sensitive information.
- For development and debugging, you can run the script directly without setting up the service.

For any issues or contributions, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.
