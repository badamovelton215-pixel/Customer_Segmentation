from flask import Flask, request, jsonify, render_template_string
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("customers_model.pkl")

# Cluster təsviri
CLUSTER_INFO = {
    0: {
        "ad": "Heyəcanlı Alıcılar",
        "emoji": "🛍️",
        "renk": "#f59e42",
        "qisa": "Az gəlir, çox xərcləyir",
        "qiymet": "Orta",
        "tesvir": "Bu müştərilər az qazanmalarına baxmayaraq çox xərcləyirlər. Emosional alıcılardır, endirim və kampaniyalara həssasdırlar.",
        "tovsiye": "Sadiqlik proqramları, endirim bildirişləri və fərdi kampaniyalar göndərin.",
        "ulduz": 3
    },
    1: {
        "ad": "Standart Müştərilər",
        "emoji": "📊",
        "renk": "#6366f1",
        "qisa": "Orta gəlir, orta xərc",
        "qiymet": "Orta",
        "tesvir": "Balanslaşdırılmış istehlak modeli. Nə çox israf edir, nə də həddən artıq qənaətkar davranır.",
        "tovsiye": "Premium məhsullar, üzvlük təklifləri ilə bu müştəriləri yuxarı səviyyəyə çəkə bilərsiniz.",
        "ulduz": 3
    },
    2: {
        "ad": "Diqqətli Varlılar",
        "emoji": "💎",
        "renk": "#14b8a6",
        "qisa": "Yüksək gəlir, az xərcləyir",
        "qiymet": "Yüksək",
        "tesvir": "Yüksək gəlirli, lakin qənaətkar müştərilər. Keyfiyyəti əvvəlcədən araşdırır, impulsiv almır.",
        "tovsiye": "Eksklüziv məhsullar, keyfiyyət zəmanəti, VIP xidmət ilə onları cəlb edin.",
        "ulduz": 4
    },
    3: {
        "ad": "Qənaətkar Müştərilər",
        "emoji": "🏠",
        "renk": "#94a3b8",
        "qisa": "Az gəlir, az xərcləyir",
        "qiymet": "Aşağı",
        "tesvir": "Büdcə dostu seçim edən müştərilər. Zəruri ehtiyaclar üçün alış-veriş edir, lüks məhsullara maraq az olur.",
        "tovsiye": "Ucuz paketlər, aylıq abunəlik, büdcə dostu seçimlər təklif edin.",
        "ulduz": 2
    },
    4: {
        "ad": "VIP Müştərilər",
        "emoji": "👑",
        "renk": "#f43f5e",
        "qisa": "Yüksək gəlir, çox xərcləyir",
        "qiymet": "Çox Yüksək",
        "tesvir": "Ən dəyərli müştəri seqmenti! Yüksək gəlirli və xərcləyici profil. Brendə sadiq, lüks məhsullara önəm verir.",
        "tovsiye": "VIP üzvlük, şəxsi menencer, eksklüziv koleksiyonlar, xüsusi davetlər göndərin.",
        "ulduz": 5
    }
}

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Müştəri Seqmentasiyası</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1c1c27;
    --border: #2a2a3a;
    --text: #e8e8f0;
    --muted: #6b6b8a;
    --accent: #7c6bff;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }
  .bg-orbs {
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
  }
  .orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.15;
  }
  .orb1 { width: 400px; height: 400px; background: #7c6bff; top: -100px; right: -100px; animation: float1 8s ease-in-out infinite; }
  .orb2 { width: 300px; height: 300px; background: #f43f5e; bottom: -50px; left: -50px; animation: float2 10s ease-in-out infinite; }
  .orb3 { width: 200px; height: 200px; background: #14b8a6; top: 50%; left: 40%; animation: float3 6s ease-in-out infinite; }
  @keyframes float1 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-30px,30px)} }
  @keyframes float2 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(30px,-20px)} }
  @keyframes float3 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-20px,20px)} }

  .wrapper {
    position: relative; z-index: 1;
    max-width: 720px; margin: 0 auto;
    padding: 60px 24px 80px;
  }
  header { text-align: center; margin-bottom: 56px; }
  .badge {
    display: inline-block;
    background: rgba(124,107,255,0.15);
    border: 1px solid rgba(124,107,255,0.3);
    color: #a89dff;
    font-size: 12px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase;
    padding: 6px 16px; border-radius: 100px; margin-bottom: 20px;
  }
  h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800; line-height: 1.1;
    background: linear-gradient(135deg, #fff 0%, #a89dff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 14px;
  }
  .subtitle { color: var(--muted); font-size: 16px; font-weight: 300; line-height: 1.6; }

  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
  }
  .card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700; font-size: 18px;
    margin-bottom: 28px;
    display: flex; align-items: center; gap: 10px;
    color: var(--text);
  }
  .card-title span { font-size: 20px; }

  .input-group { margin-bottom: 24px; }
  label {
    display: block;
    font-size: 13px; font-weight: 500; letter-spacing: 0.5px;
    color: var(--muted); text-transform: uppercase;
    margin-bottom: 8px;
  }
  .input-wrap {
    position: relative;
  }
  .unit {
    position: absolute; right: 16px; top: 50%; transform: translateY(-50%);
    color: var(--muted); font-size: 13px; pointer-events: none;
  }
  input[type=range] {
    width: 100%; -webkit-appearance: none;
    height: 4px; border-radius: 2px;
    background: linear-gradient(to right, var(--accent) 0%, var(--accent) var(--pct,50%), var(--border) var(--pct,50%));
    outline: none; cursor: pointer; margin-bottom: 8px;
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px; height: 20px; border-radius: 50%;
    background: var(--accent);
    border: 3px solid var(--bg);
    box-shadow: 0 0 12px rgba(124,107,255,0.5);
    cursor: pointer; transition: transform 0.2s;
  }
  input[type=range]::-webkit-slider-thumb:hover { transform: scale(1.2); }
  .range-vals {
    display: flex; justify-content: space-between;
    font-size: 12px; color: var(--muted);
  }
  .val-display {
    font-family: 'Syne', sans-serif;
    font-size: 28px; font-weight: 700;
    color: var(--text); margin-bottom: 10px;
  }
  .val-display em { font-style: normal; font-size: 14px; color: var(--muted); font-family: 'DM Sans', sans-serif; font-weight: 300; }

  .btn {
    width: 100%;
    background: linear-gradient(135deg, #7c6bff, #a855f7);
    color: #fff; border: none;
    font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700;
    letter-spacing: 0.5px;
    padding: 18px; border-radius: 14px;
    cursor: pointer;
    transition: all 0.3s;
    position: relative; overflow: hidden;
  }
  .btn::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: translateX(-100%); transition: transform 0.4s;
  }
  .btn:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(124,107,255,0.4); }
  .btn:hover::after { transform: translateX(100%); }
  .btn:active { transform: translateY(0); }

  #result {
    display: none;
    animation: slideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(30px) scale(0.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  .result-header {
    display: flex; align-items: flex-start; gap: 20px;
    margin-bottom: 28px; flex-wrap: wrap;
  }
  .result-emoji-wrap {
    width: 80px; height: 80px; border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 36px; flex-shrink: 0;
  }
  .result-name {
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: 26px; line-height: 1.2; flex: 1;
  }
  .result-tag {
    font-size: 13px; color: var(--muted); margin-top: 6px; font-weight: 300;
  }
  .stars { font-size: 18px; letter-spacing: 2px; margin-top: 8px; }

  .metrics {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 12px; margin-bottom: 24px;
  }
  .metric {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px;
  }
  .metric-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
  .metric-val { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 20px; }

  .desc-block {
    background: var(--surface2); border-left: 3px solid;
    border-radius: 0 12px 12px 0; padding: 20px;
    font-size: 15px; line-height: 1.7; color: #c8c8e0;
    margin-bottom: 16px;
  }
  .advice-block {
    display: flex; gap: 12px; align-items: flex-start;
    background: rgba(124,107,255,0.08);
    border: 1px solid rgba(124,107,255,0.2);
    border-radius: 12px; padding: 18px;
    font-size: 14px; line-height: 1.6; color: #a89dff;
  }
  .advice-icon { font-size: 20px; flex-shrink: 0; margin-top: 2px; }

  .divider {
    border: none; border-top: 1px solid var(--border);
    margin: 28px 0;
  }

  .score-bar-wrap { margin-top: 16px; }
  .score-bar-label { font-size: 12px; color: var(--muted); margin-bottom: 6px; display: flex; justify-content: space-between; }
  .score-bar-bg { background: var(--border); border-radius: 4px; height: 6px; }
  .score-bar-fill { height: 6px; border-radius: 4px; transition: width 1s cubic-bezier(0.34, 1.56, 0.64, 1); }

  footer { text-align: center; margin-top: 40px; color: var(--muted); font-size: 13px; }
</style>
</head>
<body>
<div class="bg-orbs">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
</div>

<div class="wrapper">
  <header>
    <div class="badge">🤖 ML Powered</div>
    <h1>Müştəri Seqmentasiyası</h1>
    <p class="subtitle">Gəlir və xərclərinizdən asılı olaraq hansı müştəri qrupuna aid olduğunuzu öyrənin</p>
  </header>

  <div class="card">
    <div class="card-title"><span>💸</span> Məlumatları Daxil Edin</div>

    <div class="input-group">
      <label>İllik Gəlir</label>
      <div class="val-display" id="income-display">50 <em>min $</em></div>
      <div class="input-wrap">
        <input type="range" id="income" min="1" max="150" value="50"
          oninput="updateSlider(this,'income-display','min $')">
      </div>
      <div class="range-vals"><span>1k $</span><span>150k $</span></div>
    </div>

    <div class="input-group">
      <label>Xərcləmə Skoru (0-100)</label>
      <div class="val-display" id="score-display">50 <em>/ 100</em></div>
      <div class="input-wrap">
        <input type="range" id="score" min="1" max="100" value="50"
          oninput="updateSlider(this,'score-display','/ 100')">
      </div>
      <div class="range-vals"><span>1 — Çox qənaətkar</span><span>100 — Çox xərcliyən</span></div>
    </div>

    <button class="btn" onclick="predict()">🔍 Seqmenti Müəyyən Et</button>
  </div>

  <div class="card" id="result">
    <div id="result-inner"></div>
  </div>

  <footer>KMeans Clustering · 5 Seqment · 2 Feature</footer>
</div>

<script>
function updateSlider(el, displayId, unit) {
  const min = +el.min, max = +el.max, val = +el.value;
  const pct = ((val - min) / (max - min)) * 100;
  el.style.setProperty('--pct', pct + '%');
  document.getElementById(displayId).innerHTML = val + ' <em>' + unit + '</em>';
}

// init sliders
['income','score'].forEach(id => {
  const el = document.getElementById(id);
  el.dispatchEvent(new Event('input'));
});

const CLUSTERS = """ + str({k: {
    'ad': v['ad'], 'emoji': v['emoji'], 'renk': v['renk'],
    'qisa': v['qisa'], 'qiymet': v['qiymet'], 'tesvir': v['tesvir'],
    'tovsiye': v['tovsiye'], 'ulduz': v['ulduz']
} for k, v in CLUSTER_INFO.items()}) + """;

async function predict() {
  const income = +document.getElementById('income').value;
  const score = +document.getElementById('score').value;

  const btn = document.querySelector('.btn');
  btn.textContent = '⏳ Hesablanır...';
  btn.disabled = true;

  const resp = await fetch('/predict', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({income, score})
  });
  const data = await resp.json();
  btn.textContent = '🔍 Seqmenti Müəyyən Et';
  btn.disabled = false;

  const c = CLUSTERS[data.cluster];
  const stars = '⭐'.repeat(c.ulduz) + '☆'.repeat(5-c.ulduz);

  const incomeColor = income < 40 ? '#94a3b8' : income < 80 ? '#6366f1' : '#f43f5e';
  const scoreColor = score < 35 ? '#94a3b8' : score < 65 ? '#f59e42' : '#22c55e';
  const incomeLabel = income < 40 ? '😐 Aşağı' : income < 80 ? '👍 Orta' : '🔥 Yüksək';
  const scoreLabel = score < 35 ? '💤 Aşağı' : score < 65 ? '📊 Orta' : '🛍️ Yüksək';

  document.getElementById('result-inner').innerHTML = `
    <div class="result-header">
      <div class="result-emoji-wrap" style="background:${c.renk}22; border:2px solid ${c.renk}44">
        ${c.emoji}
      </div>
      <div>
        <div class="result-name" style="color:${c.renk}">${c.ad}</div>
        <div class="result-tag">${c.qisa}</div>
        <div class="stars">${stars}</div>
      </div>
    </div>

    <div class="metrics">
      <div class="metric">
        <div class="metric-label">İllik Gəlir</div>
        <div class="metric-val" style="color:${incomeColor}">${income}k $</div>
        <div style="font-size:12px;color:var(--muted);margin-top:4px">${incomeLabel}</div>
      </div>
      <div class="metric">
        <div class="metric-label">Xərc Skoru</div>
        <div class="metric-val" style="color:${scoreColor}">${score} / 100</div>
        <div style="font-size:12px;color:var(--muted);margin-top:4px">${scoreLabel}</div>
      </div>
    </div>

    <div class="score-bar-wrap">
      <div class="score-bar-label"><span>Gəlir Səviyyəsi</span><span>${income}%</span></div>
      <div class="score-bar-bg"><div class="score-bar-fill" id="bar1" style="background:${incomeColor};width:0%"></div></div>
    </div>
    <div class="score-bar-wrap" style="margin-top:12px">
      <div class="score-bar-label"><span>Xərclər Səviyyəsi</span><span>${score}%</span></div>
      <div class="score-bar-bg"><div class="score-bar-fill" id="bar2" style="background:${scoreColor};width:0%"></div></div>
    </div>

    <hr class="divider">

    <div class="desc-block" style="border-color:${c.renk}">
      ${c.tesvir}
    </div>

    <div class="advice-block">
      <div class="advice-icon">💡</div>
      <div><strong>Marketinq Tövsiyəsi:</strong><br>${c.tovsiye}</div>
    </div>
  `;

  const resultEl = document.getElementById('result');
  resultEl.style.display = 'block';
  resultEl.style.borderColor = c.renk + '44';

  setTimeout(() => {
    const pct1 = Math.min(income / 150 * 100, 100);
    document.getElementById('bar1').style.width = pct1 + '%';
    document.getElementById('bar2').style.width = score + '%';
  }, 100);

  resultEl.scrollIntoView({behavior:'smooth', block:'start'});
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    income = float(data["income"])
    score = float(data["score"])
    X = np.array([[income, score]])
    cluster = int(model.predict(X)[0])
    info = CLUSTER_INFO[cluster]
    return jsonify({
        "cluster": cluster,
        "ad": info["ad"],
        "emoji": info["emoji"],
        "qisa": info["qisa"],
        "qiymet": info["qiymet"],
        "tesvir": info["tesvir"],
        "tovsiye": info["tovsiye"],
        "ulduz": info["ulduz"]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
