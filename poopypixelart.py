import streamlit as st
from streamlit.components.v1 import html

# Kanav's Pixel Art Playground
st.set_page_config(page_title="Kanav's Pixel Art Playground", layout="centered")

# Sidebar controls
with st.sidebar:
    st.header("Settings 🎨")
    grid_size = st.slider("Grid Size (NxN)", 8, 64, 16, step=8)
    cell_px   = st.slider("Pixel Size (px)", 5, 40, 20, step=5)
    theme     = st.selectbox("Theme", ["Light","Dark","Retro","Solarized","Monokai","Pastel","Neon","Cyberpunk","Forest","Ocean"])
    gif_base  = st.text_input("GIF Base Name", "animation")
    st.markdown("---")
    st.info("Draw on the canvas below. Use frame controls to animate. Export PNG/GIF on the right.")

# Theme colors mapping
theme_colors = {
    'Light':    {'bg':'#ffffff','fg':'#000000'},
    'Dark':     {'bg':'#222222','fg':'#eeeeee'},
    'Retro':    {'bg':'#f4f0e6','fg':'#333333'},
    'Solarized':{'bg':'#fdf6e3','fg':'#657b83'},
    'Monokai':  {'bg':'#272822','fg':'#f8f8f2'},
    'Pastel':   {'bg':'#ffd1dc','fg':'#355c7d'},
    'Neon':     {'bg':'#000000','fg':'#39ff14'},
    'Cyberpunk':{'bg':'#0f0f0f','fg':'#e600ff'},
    'Forest':   {'bg':'#2b580c','fg':'#e0f2e9'},
    'Ocean':    {'bg':'#023e8a','fg':'#caf0f8'}
}
colors = theme_colors[theme]
bg = colors['bg']
fg = colors['fg']

# Render the HTML/JS component
html(f"""
<style>
  body {{ background: {bg}; color: {fg}; }}
  #app {{ text-align:center; padding:10px; }}
  canvas {{ border:1px solid #444; }}
  button, input {{ margin:4px; padding:6px; background:{fg}; color:{bg}; border:none; border-radius:4px; }}
</style>
<div id="app">
  <h1>🎨 Kanav's Pixel Art Playground</h1>
  <div>
    <label>Grid: {grid_size}×{grid_size}</label>
    <label>Size: {cell_px}px</label>
    <input type="color" id="colorPicker" value="#000000">
    <button id="eraserBtn">Eraser</button>
    <button id="clearBtn">Clear</button>
    <input id="frameName" placeholder="Frame1">
    <input id="gifBase" placeholder="{gif_base}">
  </div>
  <canvas id="canvas" width="{grid_size*cell_px}" height="{grid_size*cell_px}"></canvas>
  <div>
    <button id="prev">Prev</button>
    <button id="add">Add</button>
    <button id="del">Del</button>
    <button id="next">Next</button>
    <button id="play">Play</button>
    <button id="downloadPng">PNG</button>
    <button id="downloadGif">GIF</button>
  </div>
  <div>Frame <span id="frameIdx">1</span> of <span id="frameCount">1</span></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/gif.js.optimized/dist/gif.js"></script>
<script>
(() => {{
  const gs = {grid_size}, cp = {cell_px};
  let color = '#000', eraser = false;
  let frames = [Array.from(Array(gs), () => Array(gs).fill('#FFFFFF'))];
  let frameNames = ['Frame1'], cur=0;
  const canvas = document.getElementById('canvas'), ctx = canvas.getContext('2d');
  function draw() {{
    ctx.clearRect(0,0,canvas.width,canvas.height);
    let f = frames[cur];
    for(let y=0;y<gs;y++) for(let x=0;x<gs;x++) {{
      ctx.fillStyle = f[y][x]; ctx.fillRect(x*cp,y*cp,cp,cp);
      ctx.strokeStyle = '#888'; ctx.strokeRect(x*cp,y*cp,cp,cp);
    }}
    document.getElementById('frameIdx').innerText = cur+1;
    document.getElementById('frameCount').innerText = frames.length;
    document.getElementById('frameName').value = frameNames[cur] || `Frame${{cur+1}}`;
  }}
  document.getElementById('colorPicker').oninput = e=> {{ color=e.target.value; eraser=false; }};
  document.getElementById('eraserBtn').onclick = ()=> {{ eraser=!eraser; }};
  canvas.onclick = e=> {{ let r=canvas.getBoundingClientRect(); let x=Math.floor((e.clientX-r.left)/cp), y=Math.floor((e.clientY-r.top)/cp);
    if(x>=0&&x<gs&&y>=0&&y<gs) {{ frames[cur][y][x] = eraser?'#FFFFFF':color; draw(); }} }};
  document.getElementById('clearBtn').onclick = ()=> {{ frames[cur]=Array.from(Array(gs),()=>Array(gs).fill('#FFFFFF')); draw(); }};
  document.getElementById('frameName').onchange = e=> {{ frameNames[cur]=e.target.value; }};
  document.getElementById('prev').onclick = ()=> {{ cur=Math.max(0,cur-1); draw(); }};
  document.getElementById('next').onclick = ()=> {{ cur=Math.min(frames.length-1,cur+1); draw(); }};
  document.getElementById('add').onclick = ()=> {{ frames.splice(cur+1,0,Array.from(Array(gs),()=>Array(gs).fill('#FFFFFF'))); frameNames.splice(cur+1,0,`Frame${{frames.length}}`); cur++; draw(); }};
  document.getElementById('del').onclick = ()=> {{ if(frames.length>1){{ frames.splice(cur,1); frameNames.splice(cur,1); cur=Math.max(0,cur-1); draw(); }} }};
  document.getElementById('play').onclick = ()=> {{ let i=0; let iv=setInterval(()=>{{ cur=i; draw(); i++; if(i>=frames.length) clearInterval(iv); }},300); }};
  document.getElementById('downloadPng').onclick = ()=> {{ let name=frameNames[cur]||`Frame${{cur+1}}`; let link=document.createElement('a'); link.href=canvas.toDataURL(); link.download=`${{name}}.png`; link.click(); }};
  document.getElementById('downloadGif').onclick = ()=> {{ let base=document.getElementById('gifBase').value||'{gif_base}';
    let gif=new GIF({{workers:2,quality:10}});
    frames.forEach(f=>{{ let c2=document.createElement('canvas'); c2.width=gs*cp; c2.height=gs*cp; let ct=c2.getContext('2d');
      f.forEach((r,y)=>r.forEach((col,x)=>{{ ct.fillStyle=col; ct.fillRect(x*cp,y*cp,cp,cp); }}));
      gif.addFrame(c2,{{delay:300}});
    }});
    gif.on('finished',b=>{{ let a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=`${{base}}.gif`; a.click(); }});
    gif.render();
  }};
  draw();
}})();
</script>
""", height=900)
