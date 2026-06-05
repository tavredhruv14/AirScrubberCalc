import os
import threading
import time
from urllib.request import urlopen
from flask import Flask, request, jsonify, render_template
from air_scrubber_calc import calculate_scrubber

app = Flask(__name__)

def start_auto_ping():
    app_url = os.environ.get('AUTO_PING_URL') or os.environ.get('RENDER_EXTERNAL_URL')
    if not app_url:
        return

    interval_seconds = int(os.environ.get('AUTO_PING_INTERVAL_SECONDS', '240'))
    ping_url = app_url.rstrip('/') + '/ping'

    def ping_loop():
        while True:
            time.sleep(interval_seconds)
            try:
                with urlopen(ping_url, timeout=10) as response:
                    response.read(1)
            except Exception:
                pass

    threading.Thread(target=ping_loop, name='auto-ping', daemon=True).start()

start_auto_ping()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return jsonify({"status": "awake"})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    try:
        results = calculate_scrubber(data)
        return jsonify({"success": True, "data": results})
    except Exception as e:
        import traceback
        return jsonify({"success": False, "error": str(e), "trace": traceback.format_exc()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
