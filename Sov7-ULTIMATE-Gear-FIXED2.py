from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn, time, uuid

app = FastAPI()
users, sockets, stories = {}, {}, {}

HTML = """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>SOV7 PERFECT - No Tools Panel</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}html,body{height:100%;overflow:hidden;font-family:-apple-system,sans-serif;background:#000}
#map{height:100vh;width:100vw}.dot{width:14px;height:14px;background:#34C759;border:2px solid #fff;border-radius:50%}
.storyRing{width:36px;height:36px;border-radius:50%;background:conic-gradient(from 45deg,#feda75,#fa7e1e,#d62976,#4f5bd5,#feda75);padding:3px;display:flex;align-items:center;justify-content:center}
.storyRingInner{width:100%;height:100%;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center}
.meDot{width:20px;height:20px;background:#FF3B30;border:3px solid #fff;border-radius:50%}
#topBar{position:fixed;top:0;left:0;right:0;z-index:1000;display:flex;gap:8px;padding:10px;background:rgba(255,255,255,0.14);backdrop-filter:blur(20px)}
#addrSearch{flex:1;display:flex;background:#fff;border-radius:100px;padding:6px 6px 6px 16px}#addrSearch input{flex:1;border:none;outline:none;background:transparent;font-size:15px}
#addrSearch button{border:none;background:#000;color:#fff;padding:8px 16px;border-radius:100px;cursor:pointer;font-weight:700}
#satToggle{background:#fff;border:none;padding:8px 14px;border-radius:100px;font-weight:700;font-size:12px;cursor:pointer}
#livePanel{position:fixed;top:64px;right:10px;z-index:1200;width:86px;background:rgba(255,255,255,0.18);border-radius:22px;display:flex;flex-direction:column;max-height:72vh;border:1px solid rgba(255,255,255,0.25);backdrop-filter:blur(12px)}
#livePanel.expanded{width:300px}#liveHead{padding:13px;display:flex;justify-content:space-between;cursor:pointer;align-items:center}#liveCount{background:#34C759;color:#fff;padding:4px 9px;border-radius:100px;font-size:11px;font-weight:800}
#liveList{overflow-y:auto;padding:8px;display:flex;flex-direction:column;gap:8px}.liveCard{display:flex;gap:10px;background:rgba(255,255,255,0.42);border-radius:18px;padding:10px;cursor:pointer;border:1px solid rgba(255,255,255,0.3);transition:all .2s}
.liveCard.active{background:#000;color:#fff;border-color:#000}
.liveAv{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#34C759,#00D4FF);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;position:relative;border:2.5px solid #fff;flex-shrink:0}
.greenDot{position:absolute;bottom:-2px;right:-2px;width:12px;height:12px;background:#34C759;border:2.5px solid #fff;border-radius:50%}
#card{position:fixed;left:50%;transform:translateX(-50%) translateY(150%);z-index:1500;background:rgba(255,255,255,0.94);width:92%;max-width:380px;border-radius:26px;padding:16px;display:flex;gap:12px;transition:transform 0.5s;bottom:38vh;border:1px solid rgba(255,255,255,0.6);box-shadow:0 16px 40px rgba(0,0,0,0.18);backdrop-filter:blur(20px)}
#card.show{transform:translateX(-50%) translateY(0)}
#chat{position:fixed;bottom:0;left:50%;transform:translateX(-50%) translateY(110%);width:100%;max-width:400px;height:84vh;background:#fff;z-index:2000;border-radius:30px 30px 0 0;display:flex;flex-direction:column;transition:transform 0.5s;overflow:hidden;box-shadow:0 -12px 48px rgba(0,0,0,0.18)}
#chat.open{transform:translateX(-50%) translateY(0)}
#chatHeader{padding:12px 14px;display:flex;justify-content:space-between;align-items:center;border-bottom:0.5px solid rgba(0,0,0,0.08);background:rgba(255,255,255,0.9)}
#gearBtn{width:38px;height:38px;border-radius:50%;border:1px solid rgba(0,0,0,0.08);background:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:20px;transition:all 0.3s}#gearBtn.open{transform:rotate(90deg);background:#000;color:#fff}
.iconBtn{width:38px;height:38px;border-radius:50%;border:none;background:rgba(0,0,0,0.06);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700} 
#chatDropMenu{max-height:0;overflow:hidden;transition:max-height 0.5s;background:#f5f5f7;border-bottom:0.5px solid rgba(0,0,0,0.06)}
#chatDropMenu.open{max-height:520px;overflow-y:auto}
.dropInner{padding:14px;display:flex;flex-direction:column;gap:14px}
.noteBox{background:#fff;border-radius:22px;padding:16px;border:1px solid rgba(0,0,0,0.06);box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.noteBox textarea{width:100%;border:none;background:rgba(0,0,0,0.04);border-radius:14px;padding:12px;font-size:14px;resize:none;outline:none;min-height:84px;margin-top:8px}
.linkList{display:flex;flex-direction:column;gap:7px;max-height:180px;overflow-y:auto;margin-top:10px}
.linkCard{background:rgba(0,0,0,0.03);border-radius:14px;padding:10px 12px;cursor:pointer;border:1px solid rgba(0,0,0,0.05)}
.storyBox{background:linear-gradient(135deg,#fff,#fff8eb);border-radius:22px;padding:16px;border:1px solid rgba(0,0,0,0.06)}
#msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:6px;background:#fafafa}
.msgRow{display:flex;margin:3px 0}.msgRow.me{justify-content:flex-end}.msgRow.them{justify-content:flex-start}
.bubble{max-width:76%;padding:12px 16px;border-radius:22px;white-space:pre-wrap;word-break:break-word;font-size:15px;line-height:20px}
.bubble.me{background:#007AFF;color:#fff;border-bottom-right-radius:8px}.bubble.them{background:#e5e5ea;color:#000;border-bottom-left-radius:8px}
.bubble img{max-width:200px;border-radius:14px;margin-top:8px;display:block;cursor:pointer}.bubble video{max-width:220px;border-radius:14px;margin-top:8px;display:block}
.addrChip{background:rgba(0,0,0,0.08);padding:8px 12px;border-radius:14px;margin-top:8px;font-size:12px;cursor:pointer}
#inputWrap{padding:12px 14px calc(14px + env(safe-area-inset-bottom));border-top:0.5px solid rgba(0,0,0,0.08);display:flex;gap:8px;background:#fff;align-items:flex-end}
#inputBox{flex:1;background:#f2f2f7;border-radius:24px;padding:8px 12px;display:flex;align-items:center;min-height:42px}
#textIn{flex:1;border:none;background:transparent;outline:none;resize:none;max-height:100px;font-size:16px;padding:6px 0;font-family:inherit}
#sendBtn{width:42px;height:42px;border-radius:50%;border:none;background:#007AFF;color:#fff;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;transition:all .2s}
#sendBtn:disabled{background:#c7c7cc;cursor:not-allowed}
.mediaBtn{width:38px;height:38px;border-radius:50%;border:none;background:#f2f2f7;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.mediaBtn:active{transform:scale(0.92)}
#storyView{position:fixed;top:0;left:0;width:100vw;height:100vh;background:#000;z-index:5000;display:none;flex-direction:column}
</style>
</head>
<body>
<div id="topBar">
<div id="addrSearch"><input id="addrInput" placeholder="Search address..."><button onclick="searchAddr()">Go</button></div>
<button id="satToggle" onclick="toggleSat()">SAT</button>
<button class="iconBtn" onclick="openChat()" style="background:#fff">💬</button>
</div>
<div id="map"></div>
<div id="livePanel"><div id="liveHead" onclick="toggleLive()"><span style="font-weight:800;font-size:12px">LIVE</span><span id="liveCount">0</span></div><div id="liveList"></div></div>
<div id="card"><div style="width:42px;height:42px;border-radius:50%;background:#eee;flex-shrink:0;overflow:hidden" id="cardAv"></div><div style="flex:1"><div id="cardName" style="font-weight:800;font-size:15px">Select User</div><div id="cardSub" style="font-size:12px;opacity:.6">Tap live dot</div><div style="display:flex;gap:8px;margin-top:10px"><button onclick="openChat()" style="flex:1;padding:9px;border:none;background:#000;color:#fff;border-radius:100px;font-weight:700;cursor:pointer">Message</button><button onclick="viewStory()" style="padding:9px 14px;border:1px solid rgba(0,0,0,0.1);background:#fff;border-radius:100px;font-weight:700;cursor:pointer">Story</button></div></div></div>
<div id="chat">
<div id="chatHeader"><button id="gearBtn" onclick="toggleDrop()">⚙️</button><div style="text-align:center"><div id="chatName" style="font-weight:800;font-size:15px">No one selected</div><div id="chatStatus" style="font-size:11px;opacity:.5">Tap a user on map</div></div><button class="iconBtn" onclick="closeChat()">✕</button></div>
<div id="chatDropMenu"><div class="dropInner">
<div class="noteBox"><div style="font-weight:800;font-size:13px">📝 Private Notes</div><textarea id="noteArea" placeholder="Notes about this person..."></textarea><div style="display:flex;gap:8px;margin-top:8px"><button onclick="saveNote()" style="flex:1;padding:8px;border:none;background:#000;color:#fff;border-radius:100px;font-weight:700;cursor:pointer">Save</button></div><div class="linkList" id="noteList"></div></div>
<div class="storyBox"><div style="font-weight:800;font-size:13px">📸 Post Story (24h)</div><div id="storyDrop" style="margin-top:10px;border:2px dashed rgba(0,0,0,0.1);border-radius:18px;padding:18px;text-align:center;cursor:pointer" onclick="document.getElementById('storyFile').click()"><img id="storyDropImg" style="display:none;max-width:100%;border-radius:12px;margin-bottom:8px"><div id="storyDropText" style="font-size:13px;opacity:.6">Tap to add photo</div></div><textarea id="storyCaption" placeholder="Caption..." style="width:100%;border:none;background:rgba(0,0,0,0.04);border-radius:14px;padding:12px;font-size:14px;resize:none;outline:none;min-height:56px;margin-top:10px"></textarea><button onclick="postStory()" style="width:100%;margin-top:10px;padding:12px;border:none;background:#000;color:#fff;border-radius:100px;font-weight:800;cursor:pointer">Share Story</button></div>
</div></div>
<div id="msgs"></div>
<div id="inputWrap">
<button class="mediaBtn" onclick="document.getElementById('picIn').click()" title="Send Photo">📷</button>
<button class="mediaBtn" onclick="document.getElementById('videoIn').click()" title="Send Video">🎥</button>
<div id="inputBox"><textarea id="textIn" rows="1" placeholder="Message..."></textarea></div>
<button id="sendBtn" onclick="sendText()">↑</button>
</div>
<input type="file" id="picIn" accept="image/*" style="display:none">
<input type="file" id="videoIn" accept="video/*" style="display:none">
<input type="file" id="storyFile" accept="image/*" style="display:none">
</div>
<div id="storyView"><div style="height:4px;background:rgba(255,255,255,0.2)"><div id="storyProg" style="height:100%;background:#fff;width:0%;transition:width .05s linear"></div></div><div style="padding:14px;display:flex;justify-content:space-between;color:#fff;align-items:center"><div><div id="storyViewName" style="font-weight:800"></div><div id="storyViewTime" style="font-size:12px;opacity:.7"></div></div><button onclick="closeStoryView()" style="width:36px;height:36px;border-radius:50%;border:none;background:rgba(255,255,255,0.15);color:#fff;cursor:pointer">✕</button></div><img id="storyViewImg" style="flex:1;object-fit:contain;display:none;max-height:70vh"><div id="storyViewText" style="padding:20px;color:#fff;font-size:18px;text-align:center"></div><div style="padding:20px;display:flex;gap:10px"><button onclick="openChatFromStory()" style="flex:1;padding:14px;border:none;background:#fff;border-radius:100px;font-weight:800;cursor:pointer">Reply</button></div></div>

<script>
let map = L.map('map',{zoomControl:false}).setView([28.3,-81.7],12);
let osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let sat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
let isSat=false;
function toggleSat(){
  if(isSat){map.removeLayer(sat);map.addLayer(osm);}
  else{map.removeLayer(osm);map.addLayer(sat);}
  isSat=!isSat;
  document.getElementById('satToggle').style.background=isSat?'#000':'#fff';
  document.getElementById('satToggle').style.color=isSat?'#fff':'#000';
}
let meMarker=null,myLat=28.3,myLng=-81.7,markers={},selId=null,ws=null,progInt=null,uid='U_'+Math.random().toString(36).slice(2,6).toUpperCase();
let notes=JSON.parse(localStorage.getItem('sov7_notes')||'{}');

navigator.geolocation.watchPosition(p=>{
  myLat=p.coords.latitude;myLng=p.coords.longitude;
  if(meMarker) meMarker.setLatLng([myLat,myLng]);
  else {
    meMarker=L.marker([myLat,myLng],{icon:L.divIcon({className:'',html:'<div class=meDot></div>',iconSize:[20,20]})}).addTo(map);
  }
  map.setView([myLat,myLng],14);
  if(ws&&ws.readyState===1) ws.send(JSON.stringify({type:'move',lat:myLat,lng:myLng}));
},()=>{},{enableHighAccuracy:true});

function connectWS(){
 let proto=location.protocol==='https:'?'wss':'ws';
 ws=new WebSocket(proto+'://'+location.host+'/ws/'+uid);
 ws.onopen=()=>{
   ws.send(JSON.stringify({type:'join',lat:myLat,lng:myLng}));
   document.getElementById('chatStatus').innerText='Online - '+uid;
 };
 ws.onmessage=e=>{
   let d=JSON.parse(e.data);
   if(d.type==='users') renderUsers(d.users,d.stories);
   if(d.type==='chat'){
     addMsg(d.text,d.pic,d.vid,d.addr,'them');
     if(d.from){
       if(!selId) selectUser(d.from);
     }
   }
 };
 ws.onclose=()=>{
   setTimeout(connectWS,1500);
   document.getElementById('chatStatus').innerText='Reconnecting...';
 };
}
connectWS();

function renderUsers(usersList, storiesMap){
 let list=document.getElementById('liveList'); list.innerHTML='';
 let count=Object.keys(usersList).length;
 document.getElementById('liveCount').innerText=count;
 for(let id in usersList){
  if(id===uid) continue;
  let u=usersList[id];
  let hasStory=storiesMap&&storiesMap[id];
  let iconHtml=hasStory?'<div class=storyRing><div class=storyRingInner><div class=dot></div></div></div>':'<div class=dot></div>';
  if(markers[id]){
    markers[id].setLatLng([u.lat,u.lng]);
    markers[id].setIcon(L.divIcon({className:'',html:iconHtml,iconSize:[hasStory?36:14,hasStory?36:14]}));
  } else {
    markers[id]=L.marker([u.lat,u.lng],{icon:L.divIcon({className:'',html:iconHtml,iconSize:[hasStory?36:14,hasStory?36:14]})}).addTo(map);
    markers[id].on('click',()=>selectUser(id));
  }
  let card=document.createElement('div');
  card.className='liveCard'+(selId===id?' active':'');
  card.innerHTML='<div class=liveAv>'+id.slice(2,4)+'<div class=greenDot></div></div><div style="flex:1;overflow:hidden"><div style="font-weight:800;font-size:13px;white-space:nowrap">'+id+(hasStory?' ✨':'')+'</div><div style="font-size:11px;opacity:.7">'+u.lat.toFixed(3)+', '+u.lng.toFixed(3)+'</div></div>';
  card.onclick=()=>selectUser(id);
  list.appendChild(card);
 }
 for(let id in markers){
   if(!(id in usersList)){
     map.removeLayer(markers[id]);
     delete markers[id];
   }
 }
}

function selectUser(id){
 selId=id;
 document.getElementById('cardName').innerText=id;
 document.getElementById('cardSub').innerText='Tap Message to chat';
 document.getElementById('chatName').innerText=id;
 document.getElementById('chatStatus').innerText='Ready to message';
 document.getElementById('card').classList.add('show');
 setTimeout(()=>document.getElementById('card').classList.remove('show'),3000);
 renderNotes();
}

function toggleLive(){document.getElementById('livePanel').classList.toggle('expanded');}

async function searchAddr(){
 let q=document.getElementById('addrInput').value.trim(); if(!q) return;
 try{
   let r=await fetch('https://nominatim.openstreetmap.org/search?format=json&q='+encodeURIComponent(q));
   let j=await r.json();
   if(j[0]){
     map.setView([j[0].lat,j[0].lon],16);
     L.marker([j[0].lat,j[0].lon]).addTo(map).bindPopup(j[0].display_name).openPopup();
   } else alert('Not found');
 }catch(e){alert('Search failed');}
}
document.getElementById('addrInput').addEventListener('keydown',e=>{if(e.key==='Enter') searchAddr();});

function toggleDrop(){document.getElementById('chatDropMenu').classList.toggle('open');document.getElementById('gearBtn').classList.toggle('open');}
function saveNote(){
  let t=document.getElementById('noteArea').value.trim();
  if(!t||!selId) return;
  if(!notes[selId]) notes[selId]=[];
  notes[selId].push({text:t,ts:Date.now()});
  localStorage.setItem('sov7_notes',JSON.stringify(notes));
  document.getElementById('noteArea').value='';
  renderNotes();
}
function renderNotes(){
  let cont=document.getElementById('noteList'); cont.innerHTML='';
  if(!selId||!notes[selId]) return;
  notes[selId].slice().reverse().forEach(n=>{
    let d=document.createElement('div'); d.className='linkCard'; d.innerText=n.text; cont.appendChild(d);
  });
}

function openChat(){
  if(!selId){alert('Tap a live user dot on map or Live list first');return;}
  document.getElementById('card').classList.remove('show');
  document.getElementById('chat').classList.add('open');
  document.getElementById('textIn').focus();
}
function closeChat(){
  document.getElementById('chat').classList.remove('open');
  document.getElementById('chatDropMenu').classList.remove('open');
  document.getElementById('gearBtn').classList.remove('open');
}
function openChatFromStory(){closeStoryView();setTimeout(()=>openChat(),150);}

function addMsg(t,p,vid,addr,who){
 let msgs=document.getElementById('msgs');
 let row=document.createElement('div');row.className='msgRow '+who;
 let b=document.createElement('div');b.className='bubble '+who;
 if(t){
   let txt=document.createElement('div');txt.textContent=t;b.appendChild(txt);
   if(addr){
     let a=document.createElement('div');a.className='addrChip';a.innerText='📍 Look up: '+addr.slice(0,35);
     a.onclick=()=>{document.getElementById('addrInput').value=addr;searchAddr();closeChat();};
     b.appendChild(a);
   }
 }
 if(p){
   let img=document.createElement('img');img.src=p;img.loading='lazy';img.onclick=()=>window.open(p,'_blank');b.appendChild(img);
 }
 if(vid){
   let v=document.createElement('video');v.src=vid;v.controls=true;v.playsInline=true;v.preload='metadata';b.appendChild(v);
 }
 row.appendChild(b);msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;
}

function sendText(){
 let input=document.getElementById('textIn');
 let t=input.value.trim();
 if(!t) return;
 if(!selId){alert('No user selected - tap a person on map');return;}
 if(!ws||ws.readyState!==1){alert('Not connected yet - wait a sec');return;}
 ws.send(JSON.stringify({type:'chat',to:selId,text:t,addr:t.toLowerCase().includes('address')?t:null}));
 addMsg(t,null,null,null,'me');
 input.value=''; input.style.height='auto'; input.focus();
}
document.getElementById('textIn').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendText();}});
document.getElementById('textIn').addEventListener('input',function(){this.style.height='auto';this.style.height=Math.min(this.scrollHeight,90)+'px';});

document.getElementById('picIn').addEventListener('change',function(){
 let f=this.files[0]; if(!f) return;
 if(!selId){alert('Select user first - tap a live dot');this.value='';return;}
 if(f.size>12*1024*1024){alert('Image too big - max 12MB');this.value='';return;}
 let r=new FileReader();
 r.onload=e=>{
  if(!ws||ws.readyState!==1){alert('Not connected');return;}
  ws.send(JSON.stringify({type:'chat',to:selId,pic:e.target.result}));
  addMsg('📷 Photo',e.target.result,null,null,'me');
 };
 r.readAsDataURL(f); this.value='';
});

document.getElementById('videoIn').addEventListener('change',function(){
 let f=this.files[0]; if(!f) return;
 if(!selId){alert('Select user first');this.value='';return;}
 if(f.size>35*1024*1024){alert('Video too big max 35MB');this.value='';return;}
 let r=new FileReader();
 r.onload=e=>{
  if(!ws||ws.readyState!==1){alert('Not connected');return;}
  ws.send(JSON.stringify({type:'chat',to:selId,vid:e.target.result}));
  addMsg('🎥 Video',null,e.target.result,null,'me');
 };
 r.readAsDataURL(f); this.value='';
});

document.getElementById('storyFile').addEventListener('change',function(){
 let f=this.files[0]; if(!f) return;
 let r=new FileReader();
 r.onload=e=>{
   document.getElementById('storyDropImg').src=e.target.result;
   document.getElementById('storyDropImg').style.display='block';
   document.getElementById('storyDropText').textContent='Photo ready ✓ Tap to change';
 };
 r.readAsDataURL(f);
});

function postStory(){
 let pic=document.getElementById('storyDropImg').style.display!=='none'?document.getElementById('storyDropImg').src:'';
 let txt=document.getElementById('storyCaption').value.trim();
 if(!pic&&!txt){alert('Add photo or caption');return;}
 if(!ws||ws.readyState!==1){alert('Not connected');return;}
 ws.send(JSON.stringify({type:'story',pic:pic,text:txt}));
 document.getElementById('storyDropImg').style.display='none';
 document.getElementById('storyDropText').textContent='Tap to add photo';
 document.getElementById('storyFile').value='';
 document.getElementById('storyCaption').value='';
 toggleDrop();
 alert('Story shared! Ring active 24h');
}

function viewStory(){
 if(!selId){alert('Select person first');return;}
 fetch('/stories').then(r=>r.json()).then(all=>{
  let s=all[selId]; if(!s){alert('No story or expired');return;}
  document.getElementById('storyViewName').innerText='Person '+selId.slice(2,6);
  document.getElementById('storyViewTime').innerText=s.ts?new Date(s.ts*1000).toLocaleTimeString():'';
  if(s.pic&&s.pic.length>20){
    document.getElementById('storyViewImg').src=s.pic;
    document.getElementById('storyViewImg').style.display='block';
  } else document.getElementById('storyViewImg').style.display='none';
  document.getElementById('storyViewText').textContent=s.text||'';
  document.getElementById('storyView').style.display='flex';
  let w=0; document.getElementById('storyProg').style.width='0%'; clearInterval(progInt);
  progInt=setInterval(()=>{
    w+=0.8;document.getElementById('storyProg').style.width=w+'%';
    if(w>=100){clearInterval(progInt);closeStoryView();}
  },50);
 });
}
function closeStoryView(){document.getElementById('storyView').style.display='none';clearInterval(progInt);}
map.on('click',()=>{document.getElementById('card').classList.remove('show');});
</script>
</body></html>
"""
@app.get("/", response_class=HTMLResponse)
async def home(): return HTML
@app.get("/stories")
async def get_stories():
    now=time.time()
    for uid in list(stories.keys()):
        if now-stories[uid]['ts']>86400: stories.pop(uid,None)
    return JSONResponse(stories)
@app.websocket("/ws/{user_id}")
async def ws_handler(websocket: WebSocket, user_id: str):
    await websocket.accept()
    sockets[user_id]=websocket
    try:
        while True:
            d=await websocket.receive_json()
            if d.get('type')=='join': users[user_id]={'lat':d['lat'],'lng':d['lng']}
            elif d.get('type')=='move':
                if user_id in users: users[user_id]['lat']=d['lat']; users[user_id]['lng']=d['lng']
            elif d.get('type')=='chat':
                to_id=d.get('to')
                if to_id in sockets:
                    try: await sockets[to_id].send_json({'type':'chat','from':user_id,'text':d.get('text',''),'pic':d.get('pic'),'vid':d.get('vid'),'addr':d.get('addr')})
                    except: pass
            elif d.get('type')=='story':
                stories[user_id]={'id':str(uuid.uuid4())[:8],'pic':d.get('pic',''),'text':d.get('text',''),'ts':time.time()}
            payload={'type':'users','users':users,'stories':{uid:{'id':v['id']} for uid,v in stories.items() if time.time()-v['ts']<=86400}}
            for s in list(sockets.values()):
                try: await s.send_json(payload)
                except: pass
    except: pass
    finally: users.pop(user_id,None); sockets.pop(user_id,None)

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
