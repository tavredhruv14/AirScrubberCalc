import os
import sys
from flask import Flask, request, jsonify, render_template

# Use the native Python calculator module instead of Excel COM
from air_scrubber_calc import calculate_scrubber

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    # run natively
    app.run(host='0.0.0.0', port=5000, debug=False)

