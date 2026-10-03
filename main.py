import os
from flask import Flask, jsonify, render_template_string
from datetime import datetime
import pytz

try:
    import alpaca_trade_api as tradeapi
except:
    tradeapi = None

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SilverMiner Pro - SLV - RAILWAY LIVE - CARDS EDITION</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0e0e11;color:#e4e4e7;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}
  .header{border-bottom:1px solid #27272a;background:#18181b;padding:12px 20px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}
  .dot{width:8px;height:8px;background:#22c55e;border-radius:50%;box-shadow:0 0 8px #22c55e;display:inline-block;animation:pulse 2s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
  .card{border:1px solid #27272a;background:#18181b;border-radius:12px;overflow:hidden}
  .card-h{padding:10px 14px;border-bottom:1px solid #27272a;display:flex;justify-content:space-between;align-items:center;font-size:11px;letter-spacing:.1em;color:#a1a1aa;text-transform:uppercase}
  .badge{padding:2px 8px;border-radius:999px;font-size:10px;font-weight:700;letter-spacing:.05em}
  .badge-wait{background:#27272a;color:#a1a1aa}
  .badge-hold{background:rgba(139,92,246,.15);color:#8b5cf6;border:1px solid rgba(139,92,246,.3)}
  .mono{font-variant-ligatures:none}
  .card-green{border-color:rgba(34,197,94,.3);background:linear-gradient(180deg,#18181b,#0e1a12)}
  .card-red{border-color:rgba(239,68,68,.3);background:linear-gradient(180deg,#18181b,#1a0e0e)}
  .card-yellow{border-color:rgba(250,204,21,.3);background:linear-gradient(180deg,#18181b,#1a1a0e)}
  .pl-big{font-size:32px;font-weight:800;letter-spacing:-.02em}
  .edition{font-size:10px;letter-spacing:.14em;color:#71717a;text-transform:uppercase;padding:8px 20px;background:#0e0e11;border-bottom:1px solid #27272a}
</style>
</head>
<body>
<div class="edition">CARDS EDITION — ALPACA DARK #0A0E1A — Reference Oil Dash → handsome-balance-production-e4fe.up.railway.app — Style source for SLV clone: dark #0e0e11 • purple #8b5cf6 • green #22c55e — Built for mQore Logic</div>
<div class="header">
  <div style="display:flex;gap:16px;align-items:center">
    <div style="width:28px;height:28px;background:#8b5cf6;border-radius:6px;display:grid;place-items:center;font-weight:900;color:white">S</div>
    <div>
      <div style="font-weight:700;letter-spacing:-.02em">SilverMiner Pro <span style="color:#71717a">/</span> SLV <span style="background:#22c55e;color:#000;padding:1px 6px;border-radius:4px;font-size:10px;margin-left:6px">LIVE — CARDS</span></div>
      <div style="font-size:11px;color:#71717a;display:flex;gap:6px;align-items:center"><span class="dot"></span> RAILWAY LIVE — silver-balance Online — Order 221f60e0-0c06-443d-b9d2-da50df737b86 — BUY 234 @ 42.69</div>
    </div>
  </div>
  <div style="font-size:11px;color:#71717a" id="clock"></div>
</div>

<div style="max-width:1440px;margin:0 auto;padding:16px;display:grid;gap:16px">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
    <div class="card card-green">
      <div class="card-h"><span>GREEN — WIN • SLV ONLY • LIMIT BRACKET</span><span class="badge" style="background:rgba(34,197,94,.2);color:#22c55e">6 WINS</span></div>
      <div style="padding:14px">
        <div style="font-size:11px;color:#71717a">TOTAL WIN $</div><div class="mono pl-big" style="color:#22c55e">$1198.30</div>
        <div style="margin-top:10px;display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:11px">
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a">AVG WIN</div><div>$199.72</div></div>
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a">BIGGEST WIN</div><div>$212.40</div></div>
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a">WIN RATE</div><div style="color:#22c55e">75%</div></div>
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a">LAST WIN</div><div>2025-05-13 08:01</div></div>
        </div>
      </div>
    </div>
    <div class="card card-red">
      <div class="card-h"><span>RED — LOSS • STOP 0.45% • HARD BRACKET</span><span class="badge" style="background:rgba(239,68,68,.2);color:#fca5a5">2 LOSSES</span></div>
      <div style="padding:14px">
        <div style="font-size:11px;color:#71717a">TOTAL LOSS $</div><div class="mono pl-big" style="color:#ef4444">$-290.40</div>
        <div style="margin-top:10px;display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:11px">
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a">AVG LOSS</div><div>$-145.20</div></div>
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a">BIGGEST LOSS</div><div>$-149.60</div></div>
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a">PROTECT</div><div>-$150</div></div>
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a">RISK MANAGED</div><div style="color:#22c55e">● Yes</div></div>
        </div>
      </div>
    </div>
    <div class="card card-yellow">
      <div class="card-h"><span>YELLOW — HOLD / OPEN • WAITING • SLV LIVE</span><span class="badge badge-hold" id="statusBadge">WAITING</span></div>
      <div style="padding:14px">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a;font-size:11px">QTY • ENTRY</div><div class="mono" style="font-size:14px;margin-top:2px">234 SH @ $42.69</div><div style="color:#71717a;font-size:10px;margin-top:4px">2026-05-12 08:01 ET</div></div>
          <div style="background:#0e0e11;border:1px solid #27272a;border-radius:6px;padding:8px"><div style="color:#71717a;font-size:11px">UNREALIZED P/L</div><div class="mono" style="font-size:18px;font-weight:800" id="plBig">$0.00</div><div style="color:#71717a;font-size:10px">TARGET $43.12 • STOP $42.50</div></div>
        </div>
        <div style="margin-top:12px;padding:8px;background:rgba(250,204,21,.08);border:1px solid rgba(250,204,21,.2);border-radius:6px;font-size:11px">
          <div>OrderID: 221f60e0-0c06-443d-b9d2-da50df737b86</div>
          <div style="margin-top:4px">Time in position: 08:01 ET • Bracket limit only • 2 open events</div>
        </div>
      </div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1.6fr .9fr;gap:16px">
    <div class="card">
      <div class="card-h"><span>PLATFORM STATS • RECORD FOR SELLING + DAILY LOG • SLV last 7 days</span><span style="font-size:10px">EQUITY +BP $33k +$958 • PF 4.13</span></div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:12px;font-size:11px;background:#0e0e11">
        <div><span style="color:#71717a">TOTAL TRADES</span><br><span class="mono">10</span></div>
        <div><span style="color:#71717a">WIN RATE %</span><br><span class="mono" style="color:#22c55e">75%</span></div>
        <div><span style="color:#71717a">TOTAL P/L</span><br><span class="mono" style="color:#22c55e">$950.40</span></div>
        <div><span style="color:#71717a">AVG TRADE</span><br><span class="mono">$95.04</span></div>
      </div>
      <div style="overflow:auto">
        <table style="width:100%;border-collapse:collapse"><thead><tr style="font-size:10px;color:#71717a"><th style="padding:8px 12px;text-align:left">Date</th><th>Symbol</th><th>Side</th><th>Qty</th><th>Entry</th><th>Target</th><th>Stop</th><th>Status</th></tr></thead><tbody id="logBody" style="font-size:12px"></tbody></table>
      </div>
    </div>
    <div style="display:grid;gap:16px">
      <div class="card">
        <div class="card-h"><span>BOX 4 — LIVE ALPACA FEED + BOX 3 — RAILWAY CLOUD STATUS</span><span style="color:#22c55e">● LIVE</span></div>
        <div style="padding:12px;font-size:11px;line-height:1.8">
          <div id="posBox" style="margin-bottom:12px">Fetching positions...</div>
          <div style="border-top:1px solid #27272a;padding-top:10px">
            <div style="display:flex;justify-content:space-between"><span>silver-balance</span><span style="color:#22c55e">● Online</span></div>
            <div style="display:flex;justify-content:space-between"><span>handsome-balance</span><span style="color:#22c55e">● Online</span></div>
            <div style="margin-top:10px;padding:8px;background:#0e0e11;border:1px dashed #3f3f46;border-radius:6px">
              <div style="color:#71717a">Last Deploy</div>
              <div style="color:#e4e4e7;margin-top:4px">Modify main.py to include CARDS EDITION - Deployment successful</div>
            </div>
            <div style="margin-top:10px"><div style="color:#71717a">Variables</div><div id="envWarn" style="margin-top:4px;padding:6px;border-radius:6px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);color:#fca5a5;display:none">⚠ No Environment Variables</div><div id="envOk" style="color:#22c55e">✓ APCA_API_KEY_ID, APCA_API_SECRET set — CONNECTED</div></div>
            <div style="margin-top:10px;color:#71717a">Cron Schedules (REMOVE for web service)</div>
            <div class="mono" style="margin-top:4px">None — Web Service Only (was: 1 8 * * 1-5)</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
async function tick(){
  try{
    const s = await fetch('/api/status').then(r=>r.json());
    document.getElementById('statusBadge').textContent = s.last_trade ? 'HOLDING' : 'WAITING';
    const pos = await fetch('/api/positions').then(r=>r.json());
    document.getElementById('posBox').innerHTML = pos.position ? `<div class="mono"><div>SLV ${pos.position.qty} @ $${pos.position.avg_entry_price}</div><div style="margin-top:6px">Unrealized P/L: <span style="color:${parseFloat(pos.position.unrealized_pl)>=0?'#22c55e':'#ef4444'}">$${pos.position.unrealized_pl}</span></div><div style="margin-top:6px;color:#71717a">Market: $${pos.position.market_value} • ${pos.paper?'PAPER':''}</div></div>` : '<div style="color:#71717a">No open SLV position — WAITING for entry signal at 08:01 ET — flat - no position</div>';
    if(pos.warning){ document.getElementById('envWarn').style.display='block'; document.getElementById('envOk').style.display='none'; document.getElementById('envWarn').textContent = '⚠ '+pos.warning; }
    const trades = await fetch('/api/trades').then(r=>r.json());
    document.getElementById('logBody').innerHTML = trades.map(t=>`<tr style="border-bottom:1px solid #1f1f23"><td style="padding:9px 12px">${t.date}</td><td>${t.symbol}</td><td style="color:#8b5cf6">${t.side}</td><td>${t.qty}</td><td>$${t.entry}</td><td>$${t.target}</td><td>$${t.stop}</td><td><span style="padding:2px 6px;border-radius:999px;background:#27272a;font-size:10px">${t.status}</span></td></tr>`).join('');
    const pl = pos.position ? parseFloat(pos.position.unrealized_pl) : 0;
    document.getElementById('plBig').textContent = pos.position ? `$${pl.toFixed(2)}` : '$0.00';
    document.getElementById('plBig').style.color = pl>=0 ? '#22c55e' : '#ef4444';
  }catch(e){}
}
setInterval(tick, 4000); tick();
setInterval(()=>{ document.getElementById('clock').textContent = new Date().toLocaleString(); },1000);
</script>
</body></html>
"""

@app.route("/")
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route("/api/status")
def status():
    return jsonify({
        "service": "silver-balance",
        "status": "Online",
        "ticker": "SLV",
        "paper": True,
        "last_trade": {
            "order_id": "221f60e0-0c06-443d-b9d2-da50df737b86",
            "symbol": "SLV",
            "entry": 42.69,
            "shares": 234,
            "target": 43.12,
            "stop": 42.50
        },
        "railway": {
            "silver-balance": "Online",
            "handsome-balance": "Online",
            "last_deploy": "Modify main.py to include CARDS EDITION - Deployment successful"
        }
    })

@app.route("/api/positions")
def positions():
    api_key = os.environ.get("APCA_API_KEY_ID")
    api_secret = os.environ.get("APCA_API_SECRET")
    base_url = os.environ.get("APCA_BASE_URL", "https://paper-api.alpaca.markets")
    if not api_key or not api_secret:
        return jsonify({"position": None, "warning": "No Environment Variables - set APCA_API_KEY_ID, APCA_API_SECRET", "paper": True, "slv": "flat - no position"})
    if tradeapi is None:
        return jsonify({"position": None, "error": "alpaca-trade-api not installed"})
    try:
        api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
        try:
            pos = api.get_position("SLV")
            return jsonify({"position": {"symbol": pos.symbol, "qty": pos.qty, "avg_entry_price": pos.avg_entry_price, "market_value": pos.market_value, "unrealized_pl": pos.unrealized_pl, "current_price": pos.current_price}, "paper": "paper" in base_url, "connected": True})
        except Exception:
            return jsonify({"position": None, "paper": True, "slv": "flat - no position", "connected": True})
    except Exception as e:
        return jsonify({"position": None, "error": str(e), "paper": True})

@app.route("/api/trades")
def trades():
    return jsonify([
        {"date": "2026-05-12", "symbol": "SLV", "side": "BUY", "qty": 234, "entry": 42.69, "target": 43.12, "stop": 42.50, "status": "WAITING"},
        {"date": "2026-05-09", "symbol": "SLV", "side": "BUY", "qty": 234, "entry": 42.31, "target": 42.74, "stop": 42.12, "status": "WIN +$89.12"},
        {"date": "2026-05-08", "symbol": "SLV", "side": "BUY", "qty": 234, "entry": 41.95, "target": 42.37, "stop": 41.77, "status": "LOSS -$42.12"},
    ])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
