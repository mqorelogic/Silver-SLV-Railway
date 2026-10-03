from flask import Flask, jsonify, render_template_string
import os, requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html><head><title>SilverMiner Pro - SLV</title>
<style>
body{background:#0e0e11;color:#e5e7eb;font-family:monospace;padding:20px}
.card{background:#1a1a23;border:1px solid #2d2d3a;border-radius:12px;padding:16px;margin:12px 0}
.online{color:#22c55e} .dot{width:10px;height:10px;background:#22c55e;border-radius:50%;display:inline-block}
h1{color:#c0c0c0} .silver{color:#c0c0c0} .box1{border:2px solid #c0c0c0;font-size:24px;text-align:center}
</style></head><body>
<h1>🥈 SilverMiner Pro - SLV <span class="dot"></span> <span class="online">Online</span></h1>
<div class="card box1" id="box1">LOADING SLV - WAITING...</div>
<div class="card"><b>Railway:</b> silver-balance <span class="online">Online</span> | handsome-balance <span class="online">Online</span><br>
<b>Last Deploy:</b> Modify main.py to include a wait loop - Deployment successful<br>
<b>Cron:</b> 1 8 * * 1-5 python slv_cloud.py | 58 15 * * 1-5 python slv_cloud.py</div>
<div class="card" id="pos">Checking Alpaca SLV position...</div>
<div class="card"><b>Last Order:</b> 221f60e0-0c06-443d-b9d2-da50df737b86<br>BUY 234 @ 42.69 Target 43.12 Stop 42.50</div>
<script>
fetch('/api/status').then(r=>r.json()).then(d=>{document.getElementById('box1').innerText=d.ticker+' - '+d.status+' - Order '+d.last_trade.order_id});
fetch('/api/positions').then(r=>r.json()).then(d=>{document.getElementById('pos').innerText=JSON.stringify(d)});
</script>
</body></html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/status")
def status():
    return jsonify({"service":"silver-balance","status":"Online","ticker":"SLV","last_trade":{"order_id":"221f60e0-0c06-443d-b9d2-da50df737b86","symbol":"SLV","entry":42.69,"shares":234}})

@app.route("/api/positions")
def pos():
    key=os.getenv("APCA_API_KEY_ID"); sec=os.getenv("APCA_API_SECRET")
    if not key: return jsonify({"error":"No Environment Variables - add keys from handsome-balance"})
    import requests
    base=os.getenv("APCA_BASE_URL","https://paper-api.alpaca.markets")
    r=requests.get(f"{base}/v2/positions/SLV",headers={"APCA-API-KEY-ID":key,"APCA-API-SECRET-KEY":sec})
    return (r.json(), r.status_code) if r.status_code==200 else jsonify({"SLV":"flat - no position"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT",8080)))
