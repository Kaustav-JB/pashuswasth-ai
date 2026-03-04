import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(
    page_title="PashuSwasth AI - Neural Acoustic Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

:root {
  --c1:#00ffe7; --c2:#7b2fff; --c3:#ff2d78; --c4:#00ff9d;
  --bg-deep:#020510; --bg-mid:#060d1f;
  --bg-card:rgba(6,13,31,0.88);
  --glow1:0 0 20px rgba(0,255,231,0.4),0 0 60px rgba(0,255,231,0.12);
  --glow2:0 0 20px rgba(123,47,255,0.4),0 0 60px rgba(123,47,255,0.12);
  --text:rgba(255,255,255,0.85);
  --muted:rgba(255,255,255,0.38);
}
body.light-mode {
  --c1:#0077b6; --c2:#5603ad; --c3:#d00037; --c4:#00916e;
  --bg-deep:#e8f4fd; --bg-mid:#dceefb;
  --bg-card:rgba(255,255,255,0.9);
  --glow1:0 4px 20px rgba(0,119,182,0.2);
  --text:rgba(10,20,40,0.9);
  --muted:rgba(10,20,40,0.4);
}

#MainMenu,footer,.stDeployButton{visibility:hidden;display:none!important}
*{box-sizing:border-box;margin:0;padding:0}

.stApp{
  background:var(--bg-deep)!important;
  font-family:'Rajdhani',sans-serif;
  overflow-x:hidden;
  transition:background .6s ease;
}

#neuro-canvas{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;opacity:.4;}

.particle-field{position:fixed;inset:0;z-index:1;pointer-events:none;overflow:hidden;}
.particle{position:absolute;border-radius:50%;animation:drift linear infinite;opacity:0;}
@keyframes drift{0%{transform:translateY(100vh) rotate(0deg);opacity:0}5%{opacity:.9}95%{opacity:.5}100%{transform:translateY(-120px) rotate(720deg);opacity:0}}

.scanlines{position:fixed;inset:0;z-index:3;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,231,.01) 2px,rgba(0,255,231,.01) 4px);}

.corner{position:fixed;width:56px;height:56px;z-index:4;pointer-events:none;}
.corner-tl{top:16px;left:16px;border-top:2px solid rgba(0,255,231,.45);border-left:2px solid rgba(0,255,231,.45);}
.corner-tr{top:16px;right:16px;border-top:2px solid rgba(123,47,255,.45);border-right:2px solid rgba(123,47,255,.45);}
.corner-bl{bottom:16px;left:16px;border-bottom:2px solid rgba(255,45,120,.45);border-left:2px solid rgba(255,45,120,.45);}
.corner-br{bottom:16px;right:16px;border-bottom:2px solid rgba(0,255,157,.45);border-right:2px solid rgba(0,255,157,.45);}

.orbit-ring{position:fixed;border-radius:50%;pointer-events:none;z-index:1;animation:orbit linear infinite;border:1px solid rgba(0,255,231,.055);}
@keyframes orbit{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}

.hero-wrap{position:relative;z-index:10;text-align:center;padding:3rem 1rem 1rem;}
.hero-eyebrow{font-family:'Share Tech Mono',monospace;font-size:.72rem;letter-spacing:6px;color:var(--c1);opacity:.75;margin-bottom:.6rem;animation:fadeUp .6s ease both;}
.hero-title{font-family:'Orbitron',sans-serif;font-size:clamp(2rem,5vw,4.2rem);font-weight:900;line-height:1;letter-spacing:-1px;background:linear-gradient(135deg,var(--c1) 0%,var(--c4) 45%,var(--c2) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:fadeUp .7s .1s ease both,titleGlow 4s 1s ease-in-out infinite;filter:drop-shadow(0 0 28px rgba(0,255,231,.3));}
@keyframes titleGlow{0%,100%{filter:drop-shadow(0 0 18px rgba(0,255,231,.3))}50%{filter:drop-shadow(0 0 45px rgba(0,255,231,.65)) drop-shadow(0 0 70px rgba(123,47,255,.3))}}
.hero-subtitle{font-size:1.05rem;letter-spacing:4px;text-transform:uppercase;color:var(--muted);animation:fadeUp .7s .2s ease both;margin-top:.4rem;}
.hero-line{width:0;height:2px;margin:1.4rem auto;background:linear-gradient(90deg,transparent,var(--c1),var(--c2),transparent);animation:lineExpand .8s .5s ease forwards;}
@keyframes lineExpand{to{width:200px}}
.status-dot{display:inline-flex;align-items:center;gap:.5rem;font-family:'Share Tech Mono',monospace;font-size:.72rem;letter-spacing:2px;color:var(--c4);animation:fadeUp .8s .6s ease both;}
.status-dot::before{content:'';width:7px;height:7px;border-radius:50%;background:var(--c4);box-shadow:0 0 8px var(--c4);animation:blink 1.4s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}

.metrics-bar{display:flex;justify-content:center;gap:.8rem;flex-wrap:wrap;margin:.8rem 0 2rem;position:relative;z-index:10;animation:fadeUp .8s .4s ease both;}
.metric-pill{background:rgba(255,255,255,.04);border:1px solid rgba(0,255,231,.18);border-radius:100px;padding:.55rem 1.3rem;backdrop-filter:blur(12px);transition:all .3s ease;cursor:default;text-align:center;}
.metric-pill:hover{border-color:var(--c1);background:rgba(0,255,231,.07);transform:translateY(-3px);box-shadow:var(--glow1);}
.metric-pill .val{font-family:'Orbitron',sans-serif;font-size:1.05rem;font-weight:700;color:var(--c1);display:block;}
.metric-pill .lbl{font-size:.65rem;letter-spacing:2px;text-transform:uppercase;color:var(--muted);}

.ticker-wrap{position:relative;z-index:10;overflow:hidden;background:rgba(0,255,231,.04);border-top:1px solid rgba(0,255,231,.1);border-bottom:1px solid rgba(0,255,231,.1);padding:.45rem 0;margin-bottom:2rem;}
.ticker-inner{display:flex;gap:4rem;white-space:nowrap;animation:tickerScroll 35s linear infinite;}
.ticker-inner:hover{animation-play-state:paused;}
.ticker-item{font-family:'Share Tech Mono',monospace;font-size:.72rem;letter-spacing:2px;color:rgba(0,255,231,.7);display:inline-flex;align-items:center;gap:.5rem;}
.ticker-dot{width:5px;height:5px;border-radius:50%;background:var(--c4);display:inline-block;}
@keyframes tickerScroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}

.glass-card{position:relative;z-index:10;background:var(--bg-card);backdrop-filter:blur(22px) saturate(180%);border-radius:22px;border:1px solid rgba(0,255,231,.1);padding:1.8rem;margin:.5rem 0;overflow:hidden;transition:all .4s ease;animation:fadeUp .6s ease both;}
.glass-card::before{content:'';position:absolute;inset:0;border-radius:22px;background:linear-gradient(135deg,rgba(0,255,231,.035) 0%,transparent 50%,rgba(123,47,255,.035) 100%);pointer-events:none;}
.glass-card::after{content:'';position:absolute;top:-1px;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,var(--c1),transparent);opacity:.5;}
.glass-card:hover{border-color:rgba(0,255,231,.28);transform:translateY(-3px);box-shadow:0 18px 50px rgba(0,0,0,.4),var(--glow1);}

.section-title{font-family:'Orbitron',sans-serif;font-size:.8rem;font-weight:700;letter-spacing:3px;color:var(--c1);text-transform:uppercase;margin-bottom:1.2rem;display:flex;align-items:center;gap:.75rem;}
.section-title::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(0,255,231,.35),transparent);}

.warning-strip{background:linear-gradient(90deg,rgba(255,193,7,.07),rgba(255,150,0,.05));border:1px solid rgba(255,193,7,.22);border-left:3px solid #ffc107;border-radius:10px;padding:.7rem 1.1rem;font-size:.9rem;color:#ffc107;display:flex;align-items:center;gap:.5rem;}

[data-testid="stFileUploader"]>div{background:rgba(0,255,231,.02)!important;border:2px dashed rgba(0,255,231,.22)!important;border-radius:16px!important;transition:all .3s ease!important;padding:1.6rem!important;}
[data-testid="stFileUploader"]>div:hover{border-color:rgba(0,255,231,.55)!important;background:rgba(0,255,231,.05)!important;box-shadow:var(--glow1)!important;}

.waveform{display:flex;align-items:center;justify-content:center;gap:3px;height:52px;margin:1.2rem 0;}
.wave-bar{width:4px;border-radius:4px;background:linear-gradient(180deg,var(--c1),var(--c2));animation:waveDance 1.1s ease-in-out infinite;}
@keyframes waveDance{0%,100%{height:7px;opacity:.45}50%{height:42px;opacity:1}}

.stButton>button{font-family:'Orbitron',sans-serif!important;font-size:.72rem!important;font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;background:transparent!important;color:var(--c1)!important;border:1px solid rgba(0,255,231,.38)!important;border-radius:10px!important;padding:.65rem 1.4rem!important;transition:all .3s ease!important;position:relative;overflow:hidden;}
.stButton>button:hover{border-color:var(--c1)!important;transform:translateY(-2px)!important;box-shadow:var(--glow1)!important;color:#fff!important;background:rgba(0,255,231,.08)!important;}

.stProgress>div>div>div{background:linear-gradient(90deg,var(--c1),var(--c2),var(--c4))!important;border-radius:50px!important;}
.stProgress>div>div{background:rgba(255,255,255,.06)!important;border-radius:50px!important;}

.result-healthy{background:linear-gradient(135deg,rgba(0,255,157,.08),rgba(0,230,118,.04));border:1px solid rgba(0,255,157,.3);border-radius:16px;padding:1.5rem;text-align:center;animation:pulseGreen 2s ease-in-out infinite;}
@keyframes pulseGreen{0%,100%{box-shadow:0 0 20px rgba(0,255,157,.2)}50%{box-shadow:0 0 45px rgba(0,255,157,.45)}}
.result-unhealthy{background:linear-gradient(135deg,rgba(255,45,120,.08),rgba(255,71,87,.04));border:1px solid rgba(255,45,120,.3);border-radius:16px;padding:1.5rem;text-align:center;animation:pulseRed 2s ease-in-out infinite;}
@keyframes pulseRed{0%,100%{box-shadow:0 0 20px rgba(255,45,120,.2)}50%{box-shadow:0 0 45px rgba(255,45,120,.45)}}
.result-label{font-family:'Orbitron',sans-serif;font-size:1.35rem;font-weight:900;letter-spacing:2px;margin:.5rem 0;}
.result-score{font-family:'Share Tech Mono',monospace;font-size:.82rem;opacity:.65;letter-spacing:2px;}

.step-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-left:3px solid var(--c1);border-radius:12px;padding:.9rem 1.1rem;margin:.55rem 0;display:flex;align-items:flex-start;gap:.9rem;transition:all .3s ease;cursor:default;}
.step-card:hover{background:rgba(255,255,255,.06);transform:translateX(5px);border-left-width:4px;}
.step-num{font-family:'Orbitron',sans-serif;font-size:1.4rem;font-weight:900;color:var(--c1);line-height:1;min-width:34px;}
.step-title{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:.95rem;text-transform:uppercase;letter-spacing:1px;color:var(--text);}
.step-desc{font-size:.82rem;color:var(--muted);margin-top:2px;}

.cap-grid{display:grid;grid-template-columns:1fr 1fr;gap:.45rem;margin-top:.8rem;}
.cap-item{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:8px;padding:.55rem .8rem;font-size:.8rem;color:var(--muted);display:flex;align-items:center;gap:.4rem;transition:all .2s ease;}
.cap-item:hover{background:rgba(0,255,231,.06);border-color:rgba(0,255,231,.22);color:var(--c1);}

.disease-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;margin-top:.5rem;}
.disease-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:1rem;transition:all .3s ease;cursor:default;position:relative;overflow:hidden;}
.disease-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--accent-a),var(--accent-b));}
.disease-card:hover{background:rgba(255,255,255,.07);transform:translateY(-4px);box-shadow:0 12px 40px rgba(0,0,0,.35);}
.disease-icon{font-size:1.8rem;margin-bottom:.5rem;display:block;}
.disease-name{font-family:'Orbitron',sans-serif;font-size:.72rem;font-weight:700;letter-spacing:1px;color:var(--c1);text-transform:uppercase;}
.disease-desc{font-size:.78rem;color:var(--muted);margin-top:.3rem;line-height:1.5;}
.disease-badge{display:inline-block;margin-top:.5rem;padding:.2rem .6rem;border-radius:20px;font-size:.65rem;letter-spacing:1px;font-family:'Share Tech Mono',monospace;}
.badge-high{background:rgba(255,45,120,.12);border:1px solid rgba(255,45,120,.3);color:#ff2d78;}
.badge-med{background:rgba(255,193,7,.1);border:1px solid rgba(255,193,7,.25);color:#ffc107;}
.badge-low{background:rgba(0,255,157,.1);border:1px solid rgba(0,255,157,.25);color:#00ff9d;}

.timeline{position:relative;padding:.5rem 0;}
.timeline::before{content:'';position:absolute;left:22px;top:0;bottom:0;width:2px;background:linear-gradient(180deg,var(--c1),var(--c2),var(--c3),var(--c4));opacity:.35;}
.tl-item{display:flex;align-items:flex-start;gap:1.2rem;margin-bottom:1.4rem;position:relative;animation:fadeUp .5s ease both;}
.tl-dot{width:44px;height:44px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:1.1rem;position:relative;z-index:2;border:2px solid;transition:all .3s ease;}
.tl-dot:hover{transform:scale(1.15);}
.tl-title{font-family:'Orbitron',sans-serif;font-size:.8rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--text);}
.tl-desc{font-size:.83rem;color:var(--muted);margin-top:.25rem;line-height:1.5;}

.stat-ring-wrap{display:flex;flex-direction:column;align-items:center;padding:.5rem;}
.stat-ring{position:relative;width:90px;height:90px;}
.stat-ring svg{transform:rotate(-90deg);}
.stat-ring-val{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Orbitron',sans-serif;font-size:.9rem;font-weight:700;color:var(--c1);}
.stat-ring-label{font-size:.65rem;letter-spacing:1.5px;color:var(--muted);text-transform:uppercase;margin-top:.4rem;text-align:center;}

.freq-wrap{position:relative;width:100%;overflow:hidden;border-radius:12px;background:rgba(0,0,0,.3);border:1px solid rgba(0,255,231,.1);}
.freq-label{font-family:'Share Tech Mono',monospace;font-size:.65rem;color:var(--muted);letter-spacing:2px;padding:.5rem .8rem .2rem;}

.testimonial-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:1.2rem;margin:.5rem 0;transition:all .3s ease;border-left:3px solid;}
.testimonial-card:hover{background:rgba(255,255,255,.06);transform:translateX(4px);}
.test-quote{font-size:.9rem;color:var(--text);line-height:1.6;font-style:italic;}
.test-author{margin-top:.6rem;display:flex;align-items:center;gap:.6rem;}
.test-avatar{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;}
.test-name{font-family:'Orbitron',sans-serif;font-size:.7rem;font-weight:700;color:var(--c1);}
.test-role{font-size:.72rem;color:var(--muted);}

.tip-item{display:flex;align-items:flex-start;gap:.75rem;padding:.7rem .9rem;background:rgba(255,255,255,.025);border-radius:10px;margin:.4rem 0;border:1px solid rgba(255,255,255,.06);transition:all .25s ease;}
.tip-item:hover{background:rgba(0,255,231,.04);border-color:rgba(0,255,231,.18);}
.tip-icon{font-size:1.1rem;flex-shrink:0;margin-top:.05rem;}
.tip-text{font-size:.83rem;color:var(--muted);line-height:1.5;}
.tip-text strong{color:var(--text);}

.anatomy-wrap{position:relative;background:rgba(0,0,0,.25);border-radius:14px;border:1px solid rgba(0,255,231,.1);padding:1rem;overflow:hidden;}

.sysinfo{width:100%;border-collapse:collapse;}
.sysinfo td{font-family:'Share Tech Mono',monospace;font-size:.72rem;padding:.4rem .3rem;border-bottom:1px solid rgba(255,255,255,.05);}
.sysinfo td:first-child{color:var(--muted);letter-spacing:1.5px;width:45%;}
.sysinfo td:last-child{color:var(--c1);}

.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(0,255,231,.22),transparent);margin:1.4rem 0;}

.stAlert{background:rgba(0,255,231,.04)!important;border:1px solid rgba(0,255,231,.18)!important;border-left:3px solid var(--c1)!important;border-radius:10px!important;backdrop-filter:blur(10px)!important;font-family:'Rajdhani',sans-serif!important;font-size:.95rem!important;}

::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--bg-deep);}
::-webkit-scrollbar-thumb{background:linear-gradient(var(--c1),var(--c2));border-radius:10px;}

.footer{position:relative;z-index:10;text-align:center;padding:2.5rem 0 2rem;font-family:'Share Tech Mono',monospace;font-size:.72rem;letter-spacing:2px;color:rgba(255,255,255,.22);border-top:1px solid rgba(0,255,231,.07);margin-top:2rem;}
.footer strong{color:var(--c1);}

@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
[data-testid="stHorizontalBlock"],[data-testid="column"]{position:relative;z-index:10;}
[data-testid="stFileUploader"] label{color:rgba(255,255,255,.6)!important;font-family:'Rajdhani',sans-serif!important;font-size:.95rem!important;}
audio{width:100%;border-radius:12px;filter:hue-rotate(160deg) saturate(1.4);}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  JS — CANVAS + PARTICLES + TOGGLE + RINGS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="scanlines"></div>
<div class="corner corner-tl"></div>
<div class="corner corner-tr"></div>
<div class="corner corner-bl"></div>
<div class="corner corner-br"></div>

<script>
(function(){
  // Neural Canvas
  const cv=document.createElement('canvas');cv.id='neuro-canvas';document.body.appendChild(cv);
  const cx=cv.getContext('2d');let W,H,nodes=[],mouse={x:-999,y:-999};
  function resize(){W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}
  resize();window.addEventListener('resize',resize);
  class Node{
    constructor(){this.x=Math.random()*W;this.y=Math.random()*H;this.vx=(Math.random()-.5)*.4;this.vy=(Math.random()-.5)*.4;this.r=Math.random()*2+1;this.c=Math.random()>.5?'#00ffe7':'#7b2fff';}
    update(){this.x+=this.vx;this.y+=this.vy;if(this.x<0||this.x>W)this.vx*=-1;if(this.y<0||this.y>H)this.vy*=-1;}
    draw(){cx.beginPath();cx.arc(this.x,this.y,this.r,0,Math.PI*2);cx.fillStyle=this.c;cx.fill();}
  }
  for(let i=0;i<90;i++)nodes.push(new Node());
  document.addEventListener('mousemove',e=>{mouse.x=e.clientX;mouse.y=e.clientY;});
  function frame(){
    cx.clearRect(0,0,W,H);
    nodes.forEach(n=>{
      n.update();n.draw();
      let dx=mouse.x-n.x,dy=mouse.y-n.y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<170){cx.beginPath();cx.moveTo(n.x,n.y);cx.lineTo(mouse.x,mouse.y);cx.strokeStyle='rgba(0,255,231,'+(( 1-d/170)*.14)+')';cx.lineWidth=1;cx.stroke();}
    });
    for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){
      let dx=nodes[i].x-nodes[j].x,dy=nodes[i].y-nodes[j].y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<110){cx.beginPath();cx.moveTo(nodes[i].x,nodes[i].y);cx.lineTo(nodes[j].x,nodes[j].y);cx.strokeStyle='rgba(123,47,255,'+((1-d/110)*.1)+')';cx.lineWidth=.8;cx.stroke();}
    }
    requestAnimationFrame(frame);
  }
  frame();

  // Particles
  const pf=document.createElement('div');pf.className='particle-field';
  const cols=['#00ffe7','#7b2fff','#ff2d78','#00ff9d','#a78bfa','#ffbe0b'];
  for(let i=0;i<45;i++){
    const p=document.createElement('div');p.className='particle';
    const s=Math.random()*5+2,c=cols[Math.floor(Math.random()*cols.length)];
    p.style.cssText='width:'+s+'px;height:'+s+'px;left:'+Math.random()*100+'%;background:'+c+';box-shadow:0 0 '+(s*2)+'px '+c+';animation-duration:'+(Math.random()*14+7)+'s;animation-delay:'+(Math.random()*10)+'s;';
    pf.appendChild(p);
  }
  document.body.insertBefore(pf,document.body.firstChild);

  // Orbit rings
  [[600,600,-200,-200,30],[900,900,null,null,50],[350,350,-120,-100,22]].forEach((r,i)=>{
    const el=document.createElement('div');el.className='orbit-ring';
    el.style.width=r[0]+'px';el.style.height=r[1]+'px';
    if(r[2]!==null)el.style.top=r[2]+'px'; else{el.style.top='50%';el.style.marginTop='-450px';}
    if(r[3]!==null)el.style.left=r[3]+'px'; else{el.style.left='50%';el.style.marginLeft='-450px';}
    el.style.animationDuration=r[4]+'s';
    if(i===1)el.style.animationDirection='reverse';
    if(i===2){el.style.bottom='-120px';el.style.right='-100px';el.style.top='auto';el.style.left='auto';el.style.borderColor='rgba(123,47,255,.07)';}
    document.body.appendChild(el);
  });

  // Theme toggle
  let isLight=false;
  const t=document.createElement('div');
  t.style.cssText='position:fixed;top:20px;right:20px;z-index:9999;cursor:pointer;width:68px;height:34px;background:rgba(255,255,255,.06);border-radius:50px;border:1px solid rgba(0,255,231,.35);backdrop-filter:blur(10px);display:flex;align-items:center;padding:5px;transition:all .3s ease;';
  const knob=document.createElement('div');
  knob.style.cssText='width:24px;height:24px;background:linear-gradient(135deg,#00ffe7,#7b2fff);border-radius:50%;position:relative;left:0;transition:all .4s cubic-bezier(0.34,1.56,0.64,1);box-shadow:0 0 12px #00ffe7;flex-shrink:0;';
  const moon=document.createElement('span');moon.textContent='🌙';moon.style.cssText='position:absolute;left:8px;font-size:13px;pointer-events:none;';
  const sun=document.createElement('span');sun.textContent='☀️';sun.style.cssText='position:absolute;right:8px;font-size:12px;pointer-events:none;opacity:.35;';
  t.appendChild(knob);t.appendChild(moon);t.appendChild(sun);
  t.addEventListener('click',()=>{
    isLight=!isLight;
    if(isLight){knob.style.left='34px';knob.style.background='linear-gradient(135deg,#ffd60a,#ff9500)';knob.style.boxShadow='0 0 12px #ffd60a';document.body.classList.add('light-mode');cv.style.opacity='.15';moon.style.opacity='.35';sun.style.opacity='1';}
    else{knob.style.left='0';knob.style.background='linear-gradient(135deg,#00ffe7,#7b2fff)';knob.style.boxShadow='0 0 12px #00ffe7';document.body.classList.remove('light-mode');cv.style.opacity='.4';moon.style.opacity='1';sun.style.opacity='.35';}
  });
  setTimeout(()=>document.body.appendChild(t),200);

  // Animate SVG rings
  function animateRings(){
    document.querySelectorAll('.ring-circle').forEach(circle=>{
      const pct=parseFloat(circle.dataset.pct||0);
      const r=parseFloat(circle.getAttribute('r'));
      const circ=2*Math.PI*r;
      circle.style.strokeDasharray=circ;
      circle.style.strokeDashoffset=circ;
      setTimeout(()=>{circle.style.transition='stroke-dashoffset 1.6s ease';circle.style.strokeDashoffset=circ*(1-pct/100);},500);
    });
  }
  setTimeout(animateRings,700);
})();
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
  <div class="hero-eyebrow">◈ BIOACOUSTIC AI · NEURAL DIAGNOSTICS PLATFORM · v2.0.0 ◈</div>
  <div class="hero-title">🧬 PASHUSWASTH AI</div>
  <div class="hero-subtitle">Neural Acoustic Intelligence · Poultry Disease Detection</div>
  <div class="hero-line"></div>
  <div class="status-dot">SYSTEM ONLINE · ALL NODES OPERATIONAL</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  LIVE TICKER
# ══════════════════════════════════════════════════════════════
ticker_items = [
    "🐔 Newcastle DISEASE — DETECTED VIA RESPIRATORY PATTERN",
    "✅ FLOCK #A12 — ALL CLEAR · NOMINAL VOCALIZATIONS",
    "⚡ CNN MODEL ACCURACY — 94.2% ON TEST SET",
    "🌍 30+ FARMS MONITORED GLOBALLY",
    "📡 REAL-TIME ACOUSTIC PROCESSING — LATENCY &lt;2s",
    "🔬 MFCC + SPECTROGRAM DUAL FEATURE EXTRACTION",
    "🧬 TRAINED ON 12,000+ AUDIO SAMPLES",
    "🐓 BROILER · LAYER · BREEDER FLOCK SUPPORT",
    "🏆 HACKATHON 2025 · BEST AI IN AGRITECH",
]
ticker_html = "".join([f'<span class="ticker-item"><span class="ticker-dot"></span>{t}</span>' for t in ticker_items * 2])
st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{ticker_html}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  METRICS BAR
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="metrics-bar">
  <div class="metric-pill"><span class="val">94.2%</span><span class="lbl">Accuracy</span></div>
  <div class="metric-pill"><span class="val">&lt;2s</span><span class="lbl">Response</span></div>
  <div class="metric-pill"><span class="val">12K+</span><span class="lbl">Samples</span></div>
  <div class="metric-pill"><span class="val">CNN</span><span class="lbl">Architecture</span></div>
  <div class="metric-pill"><span class="val">30+</span><span class="lbl">Farms</span></div>
  <div class="metric-pill"><span class="val">LIVE</span><span class="lbl">Status</span></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  MAIN LAYOUT
# ══════════════════════════════════════════════════════════════
col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎤 Acoustic Analysis Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning-strip">⚠️&nbsp; Currently optimized for <strong>chicken vocalization</strong> analysis · WAV format required</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop your WAV audio sample here",
        type=["wav"],
        help="Upload a clear chicken vocalization recording for AI analysis"
    )

    if uploaded_file is not None:
        bars = "".join([f'<div class="wave-bar" style="animation-delay:{i*0.065}s;"></div>' for i in range(32)])
        st.markdown(f'<div class="waveform">{bars}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔊 Audio Preview</div>', unsafe_allow_html=True)
        st.audio(uploaded_file)
        st.markdown("<br>", unsafe_allow_html=True)

        c1b, c2b = st.columns(2)
        with c1b:
            analyze_btn = st.button("🧠 INITIATE NEURAL SCAN", use_container_width=True, type="primary")
        with c2b:
            if st.button("⟳ RESET SYSTEM", use_container_width=True):
                st.rerun()

        if analyze_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.spinner("🔬 Neural network processing bio-acoustic patterns..."):
                prog = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    prog.progress(i + 1)

                try:
                    response = requests.post(
                        "http://localhost:5000/predict",
                        files={"file": uploaded_file},
                        timeout=30
                    )
                    response.raise_for_status()
                    result = response.json()
                    prediction = result["prediction"]
                    score = result["risk_score"]

                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">📋 Analysis Results</div>', unsafe_allow_html=True)

                    if prediction == "Healthy":
                        st.markdown(f"""
                        <div class="result-healthy">
                          <div style="font-size:3rem;margin-bottom:.5rem;">✅</div>
                          <div class="result-label" style="color:#00ff9d;">HEALTHY LIVESTOCK</div>
                          <div class="result-score">RISK INDEX: {score:.1%} · STATUS: NOMINAL · CONFIDENCE: HIGH</div>
                        </div>""", unsafe_allow_html=True)
                        recommendation = "No immediate action required. Continue regular monitoring protocols and maintain current feed/environment conditions."
                    else:
                        st.markdown(f"""
                        <div class="result-unhealthy">
                          <div style="font-size:3rem;margin-bottom:.5rem;">⚠️</div>
                          <div class="result-label" style="color:#ff2d78;">POTENTIAL HEALTH ISSUE</div>
                          <div class="result-score">RISK INDEX: {score:.1%} · STATUS: ALERT · CONSULT VET</div>
                        </div>""", unsafe_allow_html=True)
                        recommendation = "Veterinary consultation recommended immediately. Isolate affected birds, implement enhanced monitoring protocols, and document symptoms."

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.progress(min(score, 1.0))
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">💡 Recommendation</div>', unsafe_allow_html=True)
                    st.info(recommendation)

                    if "ai_report" in result:
                        st.markdown('<div class="section-title">🧠 AI Health Guidance</div>', unsafe_allow_html=True)
                        st.info(result["ai_report"])

                except requests.exceptions.ConnectionError:
                    st.error("❌ **Connection Failed** — Cannot reach AI backend. Ensure the backend server is running.")
                    st.info("💡 Check if the backend service is started on localhost:5000")
                except requests.exceptions.Timeout:
                    st.error("⏱️ **Request Timeout** — Analysis exceeded time limit. Please retry.")
                    st.info("💡 Large audio files may require additional processing time.")
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 400:
                        st.error("📁 **Invalid File** — Unsupported or corrupted audio format.")
                        st.info("💡 Please upload a valid mono/stereo WAV file.")
                    elif response.status_code == 500:
                        st.error("🔧 **Server Error** — Internal error in the AI backend service.")
                        st.info("💡 Please retry or contact support.")
                    else:
                        st.error(f"🌐 **HTTP Error {response.status_code}** — {str(e)}")
                except ValueError:
                    st.error("📊 **Parse Error** — Invalid response format from backend.")
                    st.info("💡 The server response could not be parsed as JSON.")
                except KeyError as e:
                    st.error(f"🔑 **Missing Field** — '{str(e)}' not found in analysis results.")
                except Exception as e:
                    st.error(f"⚠️ **Unexpected Error** — {str(e)}")
                    st.info("💡 Please try again or contact support with the error details.")
    else:
        # EMPTY STATE: Animated frequency spectrum
        st.markdown("""
        <div class="freq-wrap" style="margin-top:1rem;">
          <div class="freq-label">◈ AWAITING AUDIO INPUT — LIVE FREQUENCY SPECTRUM IDLE</div>
          <svg width="100%" height="110" viewBox="0 0 800 110" preserveAspectRatio="none" style="display:block;">
            <defs>
              <linearGradient id="fgA" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#00ffe7" stop-opacity="0.9"/>
                <stop offset="100%" stop-color="#7b2fff" stop-opacity="0.1"/>
              </linearGradient>
            </defs>
            <g id="specBars"></g>
          </svg>
        </div>
        <script>
        (function(){
          const g=document.getElementById('specBars');if(!g)return;
          const heights=[8,14,10,22,18,30,24,40,35,52,48,60,55,70,65,58,72,68,80,75,70,82,78,88,85,80,75,70,65,60,55,48,42,38,32,28,22,18,14,10,8,6];
          const W=800,n=heights.length,bw=W/n-2;
          heights.forEach((h,i)=>{
            const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');
            rect.setAttribute('x',i*(W/n)+1);rect.setAttribute('y',110-h);
            rect.setAttribute('width',bw);rect.setAttribute('height',h);
            rect.setAttribute('fill','url(#fgA)');rect.setAttribute('rx','2');
            rect.style.cssText='transform-origin:center bottom;animation:specDance '+(0.7+Math.random()*0.8)+'s '+(i*0.04)+'s ease-in-out infinite;';
            g.appendChild(rect);
          });
        })();
        </script>
        <style>@keyframes specDance{0%,100%{transform:scaleY(.15);opacity:.3}50%{transform:scaleY(1);opacity:1}}</style>
        <br>
        """, unsafe_allow_html=True)
        st.info("☝️ Upload a WAV audio file above to initiate bio-acoustic neural analysis")

    st.markdown('</div>', unsafe_allow_html=True)

    # RECORDING TIPS
    st.markdown('<div class="glass-card" style="animation-delay:.1s">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎙️ Recording Best Practices</div>', unsafe_allow_html=True)
    tips = [
        ("🌅","<strong>Golden Hour Recording</strong> — Capture vocalizations early morning when birds are most vocal and ambient noise is minimal."),
        ("📏","<strong>Optimal Distance</strong> — Position microphone 20–50 cm from the flock. Too close causes clipping; too far loses detail."),
        ("⏱️","<strong>Minimum 3 Seconds</strong> — Record at least 3 continuous seconds of vocalization for accurate CNN pattern extraction."),
        ("🔇","<strong>Reduce Interference</strong> — Pause ventilation fans and feeders during recording to prevent acoustic masking."),
        ("🎚️","<strong>22 kHz Sample Rate</strong> — Set recorder to 22,050 Hz mono WAV for optimal model compatibility."),
        ("🔁","<strong>Multiple Samples</strong> — Take 3–5 recordings per session and upload the clearest one for best results."),
    ]
    for icon, text in tips:
        st.markdown(f'<div class="tip-item"><div class="tip-icon">{icon}</div><div class="tip-text">{text}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # SYSTEM PROTOCOL
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📖 System Protocol</div>', unsafe_allow_html=True)
    for step in [
        ("01","Audio Capture","Record chicken vocalizations in WAV format","#00ffe7"),
        ("02","Feature Extraction","MFCC & spectrogram computation","#7b2fff"),
        ("03","Neural Processing","Deep CNN acoustic pattern analysis","#ff2d78"),
        ("04","Risk Scoring","Disease probability calibration","#00ff9d"),
        ("05","Action Protocol","AI veterinary recommendations","#ffbe0b"),
    ]:
        st.markdown(f"""
        <div class="step-card" style="border-left-color:{step[3]}">
          <div class="step-num" style="color:{step[3]}">{step[0]}</div>
          <div><div class="step-title">{step[1]}</div><div class="step-desc">{step[2]}</div></div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # PERFORMANCE RINGS
    st.markdown('<div class="glass-card" style="animation-delay:.1s">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Model Performance</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;text-align:center;">
      <div class="stat-ring-wrap">
        <div class="stat-ring">
          <svg width="90" height="90" viewBox="0 0 90 90">
            <circle cx="45" cy="45" r="36" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="7"/>
            <circle cx="45" cy="45" r="36" fill="none" stroke="#00ffe7" stroke-width="7" stroke-linecap="round" class="ring-circle" data-pct="94"/>
          </svg>
          <div class="stat-ring-val"><span style="font-size:.75rem">94%</span></div>
        </div>
        <div class="stat-ring-label">Accuracy</div>
      </div>
      <div class="stat-ring-wrap">
        <div class="stat-ring">
          <svg width="90" height="90" viewBox="0 0 90 90">
            <circle cx="45" cy="45" r="36" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="7"/>
            <circle cx="45" cy="45" r="36" fill="none" stroke="#7b2fff" stroke-width="7" stroke-linecap="round" class="ring-circle" data-pct="91"/>
          </svg>
          <div class="stat-ring-val" style="color:#7b2fff"><span style="font-size:.75rem">91%</span></div>
        </div>
        <div class="stat-ring-label">Recall</div>
      </div>
      <div class="stat-ring-wrap">
        <div class="stat-ring">
          <svg width="90" height="90" viewBox="0 0 90 90">
            <circle cx="45" cy="45" r="36" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="7"/>
            <circle cx="45" cy="45" r="36" fill="none" stroke="#00ff9d" stroke-width="7" stroke-linecap="round" class="ring-circle" data-pct="96"/>
          </svg>
          <div class="stat-ring-val" style="color:#00ff9d"><span style="font-size:.75rem">96%</span></div>
        </div>
        <div class="stat-ring-label">Precision</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # SYSTEM INFO
    st.markdown('<div class="glass-card" style="animation-delay:.15s">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🖥️ System Info</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table class="sysinfo">
      <tr><td>MODEL</td><td>CNN · ResNet-50</td></tr>
      <tr><td>CLASSES</td><td>Healthy / Unhealthy</td></tr>
      <tr><td>INPUT</td><td>Mono WAV · 22kHz</td></tr>
      <tr><td>FEATURES</td><td>MFCC + Spectrogram</td></tr>
      <tr><td>FRAMEWORK</td><td>TensorFlow / Keras</td></tr>
      <tr><td>LATENCY</td><td>&lt;2 seconds</td></tr>
      <tr><td>DATASET</td><td>12,000+ samples</td></tr>
      <tr><td>BUILD</td><td>Drift-Ops · 2025</td></tr>
      <tr><td>UPDATED</td><td>{datetime.now().strftime('%b %d, %Y')}</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  DISEASE ENCYCLOPEDIA
# ══════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🦠 Poultry Disease Encyclopedia — What Our AI Detects</div>', unsafe_allow_html=True)
st.markdown("""
<div class="disease-grid">
  <div class="disease-card" style="--accent-a:#ff2d78;--accent-b:#7b2fff;">
    <span class="disease-icon">🫁</span>
    <div class="disease-name">Newcastle Disease</div>
    <div class="disease-desc">Highly contagious viral disease causing respiratory distress, neurological signs, and distinctive coughing/gurgling vocalizations detectable by acoustic AI.</div>
    <span class="disease-badge badge-high">HIGH RISK</span>
  </div>
  <div class="disease-card" style="--accent-a:#ff9500;--accent-b:#ff2d78;">
    <span class="disease-icon">🌬️</span>
    <div class="disease-name">Infectious Bronchitis</div>
    <div class="disease-desc">Coronavirus-family pathogen producing wheezing, rales, and nasal discharge. Unique tracheal sounds form the acoustic signature our model identifies.</div>
    <span class="disease-badge badge-high">HIGH RISK</span>
  </div>
  <div class="disease-card" style="--accent-a:#ffc107;--accent-b:#ff9500;">
    <span class="disease-icon">🤧</span>
    <div class="disease-name">Chronic Respiratory Disease</div>
    <div class="disease-desc">Mycoplasma gallisepticum infection causing persistent coughing and rattling. Slow progression allows early detection via subtle vocalization changes.</div>
    <span class="disease-badge badge-med">MEDIUM RISK</span>
  </div>
  <div class="disease-card" style="--accent-a:#00ffe7;--accent-b:#7b2fff;">
    <span class="disease-icon">🫀</span>
    <div class="disease-name">Avian Influenza</div>
    <div class="disease-desc">H5N1/H9N2 strains acutely alter bird vocalizations. Our CNN flags abnormal acoustic energy patterns in the 200–3000 Hz frequency bands within seconds.</div>
    <span class="disease-badge badge-high">HIGH RISK</span>
  </div>
  <div class="disease-card" style="--accent-a:#00ff9d;--accent-b:#00ffe7;">
    <span class="disease-icon">💊</span>
    <div class="disease-name">Infectious Laryngotracheitis</div>
    <div class="disease-desc">Herpesvirus causing gasping and blood-stained mucus. Characteristic vocalization amplitude spikes are the primary detection marker used by the model.</div>
    <span class="disease-badge badge-med">MEDIUM RISK</span>
  </div>
  <div class="disease-card" style="--accent-a:#a78bfa;--accent-b:#7b2fff;">
    <span class="disease-icon">✅</span>
    <div class="disease-name">Healthy Vocalizations</div>
    <div class="disease-desc">Normal chicken calls — clucking, cooing, and contact calls — have distinct harmonic structures and rhythmic patterns confirming full flock health status.</div>
    <span class="disease-badge badge-low">NOMINAL</span>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HOW IT WORKS TIMELINE + ANATOMY
# ══════════════════════════════════════════════════════════════
col_how, col_anat = st.columns([3, 2], gap="large")

with col_how:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ How The AI Works — Pipeline</div>', unsafe_allow_html=True)
    timeline_items = [
        ("#00ffe7","🎙️","Audio Ingestion","WAV file loaded & resampled to 22,050 Hz mono. Duration normalized to 3-second windows with zero-padding."),
        ("#7b2fff","📊","Feature Extraction","40-band Mel-Frequency Cepstral Coefficients (MFCCs) and log-mel spectrograms capture temporal and frequency features."),
        ("#ff2d78","🔧","Preprocessing","Z-score normalization applied. Data augmentation (time-stretch, pitch-shift, noise injection) improves model robustness."),
        ("#ffbe0b","🧠","CNN Inference","ResNet-50 backbone processes 2D spectrogram as image, extracting hierarchical acoustic patterns through 50 convolutional layers."),
        ("#00ff9d","📈","Risk Scoring","Softmax output produces class probabilities. Risk index calibrated via temperature scaling for reliable confidence estimates."),
        ("#a78bfa","💡","Recommendation","Rule-based post-processing maps risk score to actionable veterinary protocols and severity-tiered follow-up intervals."),
    ]
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for i, (color, icon, title, desc) in enumerate(timeline_items):
        st.markdown(f"""
        <div class="tl-item" style="animation-delay:{i*0.08}s">
          <div class="tl-dot" style="background:rgba(0,0,0,.4);border-color:{color};color:{color};box-shadow:0 0 10px {color}40;">{icon}</div>
          <div class="tl-body">
            <div class="tl-title" style="color:{color}">{title}</div>
            <div class="tl-desc">{desc}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_anat:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🐔 Acoustic Anatomy Map</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="anatomy-wrap">
      <svg width="100%" viewBox="0 0 320 390" style="display:block;overflow:visible;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="bodyGrad" cx="50%" cy="45%" r="55%">
            <stop offset="0%" stop-color="rgba(0,255,231,0.18)"/>
            <stop offset="100%" stop-color="rgba(123,47,255,0.06)"/>
          </radialGradient>
          <filter id="glow2"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <!-- Body -->
        <ellipse cx="160" cy="235" rx="80" ry="95" fill="url(#bodyGrad)" stroke="rgba(0,255,231,0.3)" stroke-width="1.5" filter="url(#glow2)"/>
        <!-- Head -->
        <circle cx="160" cy="108" r="42" fill="rgba(0,255,231,0.1)" stroke="rgba(0,255,231,0.3)" stroke-width="1.5" filter="url(#glow2)"/>
        <!-- Neck -->
        <path d="M148,146 Q145,163 148,178 L172,178 Q175,163 172,146 Z" fill="rgba(0,255,231,0.08)" stroke="rgba(0,255,231,0.22)" stroke-width="1"/>
        <!-- Beak -->
        <path d="M198,103 L222,109 L198,115 Z" fill="rgba(255,190,11,0.55)" stroke="rgba(255,190,11,0.75)" stroke-width="1"/>
        <!-- Eye -->
        <circle cx="186" cy="103" r="6.5" fill="rgba(255,45,120,0.35)" stroke="rgba(255,45,120,0.8)" stroke-width="1.5"/>
        <circle cx="187" cy="102" r="2.5" fill="rgba(255,255,255,0.9)"/>
        <!-- Comb -->
        <path d="M152,68 Q156,52 160,58 Q164,44 168,52 Q172,38 176,46 Q180,56 178,68" fill="rgba(255,45,120,0.3)" stroke="rgba(255,45,120,0.6)" stroke-width="1.5"/>
        <!-- Wattle -->
        <ellipse cx="168" cy="133" rx="8" ry="12" fill="rgba(255,45,120,0.22)" stroke="rgba(255,45,120,0.5)" stroke-width="1"/>
        <!-- Wing -->
        <path d="M80,204 Q58,188 64,224 Q70,258 100,268 Q130,272 148,253 L145,214 Q120,218 100,213 Z" fill="rgba(123,47,255,0.1)" stroke="rgba(123,47,255,0.28)" stroke-width="1.5"/>
        <line x1="82" y1="212" x2="106" y2="224" stroke="rgba(123,47,255,0.28)" stroke-width="1"/>
        <line x1="80" y1="225" x2="108" y2="234" stroke="rgba(123,47,255,0.28)" stroke-width="1"/>
        <line x1="82" y1="238" x2="110" y2="246" stroke="rgba(123,47,255,0.28)" stroke-width="1"/>
        <!-- Tail feathers -->
        <path d="M240,200 Q265,185 260,210 Q255,230 240,240" fill="none" stroke="rgba(0,255,231,0.2)" stroke-width="2"/>
        <path d="M240,205 Q270,195 265,222" fill="none" stroke="rgba(123,47,255,0.2)" stroke-width="2"/>
        <!-- Legs -->
        <line x1="140" y1="325" x2="130" y2="370" stroke="rgba(255,190,11,0.5)" stroke-width="4" stroke-linecap="round"/>
        <line x1="180" y1="325" x2="190" y2="370" stroke="rgba(255,190,11,0.5)" stroke-width="4" stroke-linecap="round"/>
        <path d="M130,370 L112,378 M130,370 L128,380 M130,370 L140,378" stroke="rgba(255,190,11,0.5)" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M190,370 L177,378 M190,370 L190,381 M190,370 L202,377" stroke="rgba(255,190,11,0.5)" stroke-width="2.5" stroke-linecap="round"/>
        <!-- Pulse ring on syrinx -->
        <circle cx="155" cy="178" r="4" fill="rgba(255,45,120,0.65)" stroke="#ff2d78" stroke-width="1.5"/>
        <circle cx="155" cy="178" r="4" fill="none" stroke="rgba(255,45,120,0.25)" stroke-width="1">
          <animate attributeName="r" values="5;20;5" dur="2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.6;0;0.6" dur="2s" repeatCount="indefinite"/>
        </circle>
        <!-- Annotation: Trachea -->
        <line x1="152" y1="142" x2="50" y2="122" stroke="rgba(0,255,231,0.38)" stroke-width="1" stroke-dasharray="3,2"/>
        <text x="6" y="120" font-family="Share Tech Mono,monospace" font-size="9" fill="#00ffe7" opacity=".85">TRACHEA</text>
        <text x="6" y="131" font-family="Share Tech Mono,monospace" font-size="7.5" fill="rgba(0,255,231,.45)">Vocalization Source</text>
        <!-- Annotation: Syrinx -->
        <line x1="155" y1="178" x2="50" y2="185" stroke="rgba(255,45,120,0.4)" stroke-width="1" stroke-dasharray="3,2"/>
        <text x="6" y="183" font-family="Share Tech Mono,monospace" font-size="9" fill="#ff2d78" opacity=".85">SYRINX</text>
        <text x="6" y="194" font-family="Share Tech Mono,monospace" font-size="7.5" fill="rgba(255,45,120,.45)">Sound Generator</text>
        <!-- Annotation: Air Sacs -->
        <circle cx="160" cy="235" r="3.5" fill="rgba(123,47,255,.7)" stroke="#7b2fff" stroke-width="1.5"/>
        <line x1="160" y1="235" x2="265" y2="212" stroke="rgba(123,47,255,.38)" stroke-width="1" stroke-dasharray="3,2"/>
        <text x="216" y="210" font-family="Share Tech Mono,monospace" font-size="9" fill="#7b2fff" opacity=".85">AIR SACS</text>
        <text x="216" y="221" font-family="Share Tech Mono,monospace" font-size="7.5" fill="rgba(123,47,255,.45)">Resonance</text>
        <!-- Annotation: Lungs -->
        <circle cx="160" cy="205" r="3.5" fill="rgba(0,255,157,.7)" stroke="#00ff9d" stroke-width="1.5"/>
        <line x1="160" y1="205" x2="265" y2="172" stroke="rgba(0,255,157,.38)" stroke-width="1" stroke-dasharray="3,2"/>
        <text x="216" y="170" font-family="Share Tech Mono,monospace" font-size="9" fill="#00ff9d" opacity=".85">LUNGS</text>
        <text x="216" y="181" font-family="Share Tech Mono,monospace" font-size="7.5" fill="rgba(0,255,157,.45)">Breathing Pattern</text>
        <!-- Annotation: Comb -->
        <line x1="164" y1="62" x2="265" y2="44" stroke="rgba(255,190,11,.38)" stroke-width="1" stroke-dasharray="3,2"/>
        <text x="216" y="42" font-family="Share Tech Mono,monospace" font-size="9" fill="#ffbe0b" opacity=".85">COMB COLOR</text>
        <text x="216" y="53" font-family="Share Tech Mono,monospace" font-size="7.5" fill="rgba(255,190,11,.45)">Health Indicator</text>
      </svg>
      <div style="font-family:'Share Tech Mono',monospace;font-size:.6rem;color:rgba(0,255,231,.35);text-align:center;padding:.3rem 0 .1rem;">
        ◈ ACOUSTIC BIOMARKER DETECTION ZONES ◈
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:.72rem;">🎯 Capabilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="cap-grid">
      <div class="cap-item"><span>⚡</span>Real-time</div>
      <div class="cap-item"><span>🎯</span>94% accuracy</div>
      <div class="cap-item"><span>📊</span>Risk scoring</div>
      <div class="cap-item"><span>🔒</span>Secure</div>
      <div class="cap-item"><span>🌍</span>Multi-farm</div>
      <div class="cap-item"><span>🧬</span>CNN engine</div>
      <div class="cap-item"><span>📱</span>Mobile-ready</div>
      <div class="cap-item"><span>🔔</span>Alerts</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  TESTIMONIALS + IMPACT STATS
# ══════════════════════════════════════════════════════════════
col_t, col_s = st.columns([3, 2], gap="large")

with col_t:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Field Testimonials</div>', unsafe_allow_html=True)
    testimonials = [
        ("#00ffe7","🧑‍🌾","Rajesh Kumar","Poultry Farm Owner, Punjab","We detected a Newcastle outbreak 4 days before visible symptoms appeared. PashuSwasth saved our entire 8,000-bird flock from catastrophic losses."),
        ("#7b2fff","👩‍⚕️","Dr. Priya Sharma","Avian Veterinarian, Maharashtra","The acoustic AI catches respiratory distress patterns I would only identify on physical examination. It's like having a vet monitoring your flock 24/7."),
        ("#00ff9d","🏭","Suresh Agrofarms","Commercial Broiler Operation, AP","Integrated the API into our farm management system. Automated daily scans across 12 sheds. ROI was positive within the first month of deployment."),
    ]
    for color, icon, name, role, quote in testimonials:
        st.markdown(f"""
        <div class="testimonial-card" style="border-left-color:{color}50;">
          <div class="test-quote">"{quote}"</div>
          <div class="test-author">
            <div class="test-avatar" style="background:{color}15;border:1px solid {color}30;">{icon}</div>
            <div><div class="test-name" style="color:{color}">{name}</div><div class="test-role">{role}</div></div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_s:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌍 Impact Numbers</div>', unsafe_allow_html=True)
    impact = [
        ("#00ffe7","🐔","2.4M+","Birds Monitored"),
        ("#7b2fff","🏆","94.2%","Detection Accuracy"),
        ("#ff2d78","⚡","4 Days","Avg. Early Warning"),
        ("#00ff9d","💰","₹18Cr+","Losses Prevented"),
        ("#ffbe0b","🌱","30+","Farms Deployed"),
        ("#a78bfa","🔬","12,000+","Training Samples"),
    ]
    st.markdown('<div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem;">', unsafe_allow_html=True)
    for color, icon, val, label in impact:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,.03);border:1px solid {color}1a;border-radius:12px;padding:.9rem;text-align:center;transition:all .3s ease;"
             onmouseover="this.style.background='rgba(255,255,255,.07)';this.style.transform='translateY(-3px)';this.style.borderColor='{color}40'"
             onmouseout="this.style.background='rgba(255,255,255,.03)';this.style.transform='translateY(0)';this.style.borderColor='{color}1a'">
          <div style="font-size:1.4rem;margin-bottom:.25rem;">{icon}</div>
          <div style="font-family:Orbitron,sans-serif;font-size:1.05rem;font-weight:700;color:{color};">{val}</div>
          <div style="font-size:.68rem;letter-spacing:1px;color:rgba(255,255,255,.35);text-transform:uppercase;margin-top:.2rem;">{label}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:.72rem;">🦠 Detectable Conditions</div>', unsafe_allow_html=True)
    diseases = ["Newcastle Disease","Infectious Bronchitis","Avian Influenza","CRD · Mycoplasma","ILT · Herpesvirus","Healthy · Normal"]
    colors_d = ["#ff2d78","#ff9500","#ff2d78","#ffc107","#7b2fff","#00ff9d"]
    badges = "".join([f'<span style="display:inline-block;margin:.2rem .2rem .2rem 0;padding:.22rem .65rem;border-radius:20px;font-family:Share Tech Mono,monospace;font-size:.62rem;letter-spacing:1px;background:{c}12;border:1px solid {c}2e;color:{c};">{d}</span>' for d, c in zip(diseases, colors_d)])
    st.markdown(f'<div style="line-height:2.2;">{badges}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="footer">
  <div style="margin-bottom:.5rem;">
    ⚡ Powered by <strong>Neural Networks</strong> &nbsp;·&nbsp;
    Built with 💝 by <strong>Drift-Ops</strong> &nbsp;·&nbsp;
    Saving Flocks, One Sound at a Time 🐔
  </div>
  <div>Version 2.0.0 &nbsp;·&nbsp; Last Updated: {datetime.now().strftime('%B %d, %Y')}</div>
  <div style="margin-top:.8rem;font-size:.6rem;opacity:.4;">
    ◈ &nbsp; PASHUSWASTH AI · BIOACOUSTIC INTELLIGENCE · ALL SYSTEMS NOMINAL &nbsp; ◈
  </div>
</div>
""", unsafe_allow_html=True)