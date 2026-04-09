
const ALL_PRICES = [{"base": 5100, "name": "Copra", "price": 10980.3}, {"base": 3500, "name": "Niger", "price": 6279.0}, {"base": 4200, "name": "Sesamum", "price": 5380.2}, {"base": 3600, "name": "Cotton", "price": 4957.2}, {"base": 4300, "name": "Urad", "price": 4751.5}, {"base": 3700, "name": "Groundnut", "price": 4229.1}, {"base": 3500, "name": "Moong", "price": 4054.75}, {"base": 3700, "name": "Sunflower", "price": 3966.4}, {"base": 2250, "name": "Sugarcane", "price": 3813.75}, {"base": 3200, "name": "Arhar", "price": 3689.6}, {"base": 2800, "name": "Gram", "price": 3480.4}, {"base": 2200, "name": "Soyabean", "price": 3465.0}, {"base": 2500, "name": "Safflower", "price": 3445.0}, {"base": 2500, "name": "Rape", "price": 3420.0}, {"base": 2800, "name": "Masoor", "price": 3376.8}, {"base": 1500, "name": "Ragi", "price": 3202.5}, {"base": 1675, "name": "Jute", "price": 2782.18}, {"base": 1350, "name": "Wheat", "price": 1906.2}, {"base": 1245.5, "name": "Paddy", "price": 1900.63}, {"base": 1520, "name": "Jowar", "price": 1795.12}, {"base": 1175, "name": "Bajra", "price": 1491.08}, {"base": 1175, "name": "Maize", "price": 1386.5}, {"base": 980, "name": "Barley", "price": 1365.63}];
const TOP5       = [["Niger", 6279.0, 5.84], ["Groundnut", 4229.1, 4.29], ["Copra", 10980.3, 2.82], ["Sunflower", 3966.4, 2.68], ["Cotton", 4957.2, 2.46]];
const BOT5       = [["Gram", 3480.4, -4.6], ["Ragi", 3202.5, -3.31], ["Sesamum", 5380.2, -1.54], ["Urad", 4751.5, -1.43], ["Arhar", 3689.6, -1.11]];

// ── Chart: Gainers vs Losers ──
const glLabels = [...TOP5.map(x=>x[0]), ...BOT5.map(x=>x[0])];
const glData   = [...TOP5.map(x=>x[2]), ...BOT5.map(x=>x[2])];
const glColors = [...TOP5.map(()=>'rgba(22,163,74,0.70)'), ...BOT5.map(()=>'rgba(217,43,43,0.70)')];
new Chart(document.getElementById('glChart'), {
  type:'bar',
  data:{labels:glLabels,datasets:[{data:glData,backgroundColor:glColors,borderRadius:8,borderSkipped:false}]},
  options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},
    tooltip:{backgroundColor:'#111',cornerRadius:10,callbacks:{label:c=>' '+c.parsed.y+'%'}}},
    scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{color:'#6b7280',font:{size:10}}},
      y:{grid:{color:'rgba(0,0,0,.04)'},ticks:{color:'#6b7280',font:{size:10},callback:v=>v+'%'}}}}
});

// ── Chart: Top 10 price distribution ──
const t10 = ALL_PRICES.slice(0,10);
new Chart(document.getElementById('distChart'), {
  type:'bar',
  data:{
    labels:t10.map(x=>x.name),
    datasets:[{data:t10.map(x=>x.price),
      backgroundColor:t10.map((_,i)=>`hsla(${0+(i*12)},75%,50%,0.7)`),
      borderRadius:6,borderSkipped:false}]
  },
  options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{backgroundColor:'#111',cornerRadius:10,
      callbacks:{label:c=>' ₹'+c.parsed.x.toLocaleString('en-IN')}}},
    scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{color:'#6b7280',font:{size:10},callback:v=>'₹'+v}},
      y:{grid:{color:'rgba(0,0,0,.04)'},ticks:{color:'#4b5563',font:{size:10}}}}}
});

// ── Weather icons ──
const WX={0:'☀️',1:'🌤',2:'⛅',3:'☁️',45:'🌫',51:'🌧',61:'🌧',71:'🌨',80:'🌧',95:'⛈'};
function wxi(c){for(const k of Object.keys(WX).sort((a,b)=>b-a))if(c>=+k)return WX[k];return'🌡';}
const DAYS=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

function loadWeather(lat,lon,label){
  document.getElementById('wx-loc').innerHTML='📍 <b>'+label+'</b> — Live via Open-Meteo API';
  fetch('/api/weather?lat='+lat+'&lon='+lon)
  .then(r=>r.json()).then(j=>{
    if(!j.ok)throw j.error;
    const d=j.data.daily;
    for(let i=0;i<7;i++){
      const dt=new Date(d.time[i]);
      document.getElementById('wi'+i).textContent=wxi(d.weather_code[i]);
      document.getElementById('wt'+i).textContent=Math.round(d.temperature_2m_max[i])+'°/'+Math.round(d.temperature_2m_min[i])+'°C';
      document.getElementById('wd'+i).textContent=DAYS[dt.getDay()]+' '+dt.getDate();
      document.getElementById('wr'+i).textContent=(d.precipitation_sum[i]||0).toFixed(1)+'mm';
    }
    const rain7=d.precipitation_sum.slice(0,7).reduce((a,b)=>a+b,0).toFixed(1);
    const maxT=Math.max(...d.temperature_2m_max.slice(0,7)).toFixed(0);
    const tip=document.getElementById('wx-tip');
    tip.style.display='block';
    tip.innerHTML=`<span style="color:var(--red);font-weight:700;">🤖 AI Weather Insight:</span> Next 7 days — <b>${rain7}mm</b> rainfall, peak <b>${maxT}°C</b>. `
      +(+rain7>40?'<b style="color:var(--red)">Heavy rain expected</b> — delay sowing, check drainage & fungal risk.'
      :+rain7>15?'<b style="color:var(--green)">Good soil moisture</b> — ideal window for sowing if soil is prepared.'
      :'<b style="color:var(--orange)">Dry spell</b> — activate irrigation before sowing for best germination.');
  }).catch(()=>document.getElementById('wx-loc').textContent='⚠ Weather data unavailable');
}

// ── Crop DB by State ──
const CROP_DB={
  "Punjab":           {suit:["Wheat","Barley","Gram","Rape","Cotton"],avoid:["Arhar","Ragi"],desc:"Wheat heartland of India. Fertile Indo-Gangetic plains, extensive irrigation."},
  "Haryana":          {suit:["Wheat","Barley","Rape","Sugarcane","Cotton"],avoid:["Ragi","Niger"],desc:"Double-crop zone. 85% irrigated area. High mechanisation."},
  "Uttar Pradesh":    {suit:["Sugarcane","Wheat","Paddy","Arhar","Masoor"],avoid:["Sesamum","Safflower"],desc:"Largest farm state. Sugarcane belt + eastern rice zone."},
  "Bihar":            {suit:["Paddy","Wheat","Maize","Arhar","Gram"],avoid:["Cotton","Sesamum"],desc:"Fertile Gangetic alluvial plains. Flood-prone in north."},
  "West Bengal":      {suit:["Paddy","Jute","Masoor","Sesamum","Moong"],avoid:["Wheat","Cotton"],desc:"Highest rice & jute producer. Humid tropical climate."},
  "Andhra Pradesh":   {suit:["Paddy","Groundnut","Maize","Sunflower","Sesamum"],avoid:["Wheat","Barley"],desc:"Coastal & Deccan zones. Major groundnut & paddy belt."},
  "Telangana":        {suit:["Paddy","Maize","Cotton","Groundnut","Sesamum"],avoid:["Wheat","Jute"],desc:"Deccan plateau black soils. Cotton & paddy dominant crops."},
  "Karnataka":        {suit:["Ragi","Jowar","Arhar","Sunflower","Sesamum"],avoid:["Wheat","Jute"],desc:"Most diverse agro-climatic zones in India. Ragi capital."},
  "Tamil Nadu":       {suit:["Paddy","Groundnut","Sesamum","Cotton","Sugarcane"],avoid:["Wheat","Jute"],desc:"Tropical — two main seasons. Delta rice cultivation."},
  "Maharashtra":      {suit:["Cotton","Soyabean","Jowar","Sugarcane","Groundnut"],avoid:["Jute","Barley"],desc:"Largest cotton producer. Black basalt (regur) soil."},
  "Madhya Pradesh":   {suit:["Soyabean","Wheat","Gram","Sesamum","Cotton"],avoid:["Jute","Ragi"],desc:"Soyabean capital of India. Three agro-climatic sub-regions."},
  "Rajasthan":        {suit:["Wheat","Barley","Gram","Rape","Bajra"],avoid:["Paddy","Jute","Sugarcane"],desc:"Arid & semi-arid. Drought-tolerant crops essential."},
  "Gujarat":          {suit:["Cotton","Groundnut","Sesamum","Wheat","Jowar"],avoid:["Jute","Ragi"],desc:"Major cotton & groundnut exporter. Coastal + arid zones."},
  "Odisha":           {suit:["Paddy","Jute","Arhar","Sesamum","Moong"],avoid:["Wheat","Cotton"],desc:"High rainfall eastern state. Rainfed paddy dominant."},
  "Assam":            {suit:["Paddy","Jute","Maize","Sesamum","Ragi"],avoid:["Wheat","Cotton"],desc:"High humidity. Flood plains of Brahmaputra. NE India."},
  "Himachal Pradesh": {suit:["Wheat","Barley","Maize","Gram"],avoid:["Paddy","Cotton","Jute"],desc:"Hill agriculture. Temperate — apple+horticulture zone."},
  "Uttarakhand":      {suit:["Wheat","Paddy","Maize","Barley","Gram"],avoid:["Cotton","Sesamum"],desc:"Himalayan foothills. Mixed altitude subsistence+commercial."},
  "Jharkhand":        {suit:["Paddy","Arhar","Maize","Sesamum","Moong"],avoid:["Wheat","Cotton"],desc:"Rainfed tribal belt. Plateau land — mostly Kharif crops."},
  "Chhattisgarh":     {suit:["Paddy","Maize","Arhar","Sesamum","Moong"],avoid:["Wheat","Cotton"],desc:"Rice bowl of central India. High tribal small-farm density."},
  "Goa":              {suit:["Paddy","Sesamum","Ragi"],avoid:["Wheat","Cotton"],desc:"Coastal laterite soils. Heavy monsoon. Small holdings."},
  "Kerala":           {suit:["Paddy","Sesamum","Sugarcane"],avoid:["Wheat","Cotton","Jute"],desc:"Wet tropical coast. River valleys rice; spices on hills."},
};

const CROP_ICONS={Wheat:'🌾',Paddy:'🍚',Maize:'🌽',Cotton:'🌿',Soyabean:'🫘',Groundnut:'🥜',
  Sugarcane:'🎋',Gram:'🫘',Arhar:'🫘',Moong:'🫘',Masoor:'🫘',Urad:'🫘',
  Barley:'🌾',Ragi:'🌾',Jowar:'🌾',Bajra:'🌾',Jute:'🪢',Sesamum:'🌱',
  Rape:'🌼',Safflower:'🌸',Sunflower:'🌻',Copra:'🥥',Niger:'🌱'};

function stateFromCoords(lat,lon){
  lat=+lat;lon=+lon;
  if(lat>30&&lon<76)return"Punjab";
  if(lat>28&&lat<31&&lon>74&&lon<78)return"Haryana";
  if(lat>23&&lat<30&&lon>77&&lon<84)return"Uttar Pradesh";
  if(lat>24&&lat<28&&lon>83&&lon<88)return"Bihar";
  if(lat>21&&lat<27&&lon>85&&lon<89)return"West Bengal";
  if(lat>12&&lat<20&&lon>76&&lon<85)return"Andhra Pradesh";
  if(lat>17&&lat<20&&lon>77&&lon<81)return"Telangana";
  if(lat>11&&lat<18&&lon>74&&lon<78)return"Karnataka";
  if(lat>8&&lat<13&&lon>76&&lon<80)return"Tamil Nadu";
  if(lat>15&&lat<22&&lon>72&&lon<80)return"Maharashtra";
  if(lat>21&&lat<26&&lon>74&&lon<82)return"Madhya Pradesh";
  if(lat>23&&lat<30&&lon>69&&lon<78)return"Rajasthan";
  if(lat>20&&lat<24&&lon>68&&lon<74)return"Gujarat";
  if(lat>17&&lat<22&&lon>81&&lon<87)return"Odisha";
  if(lat>24&&lat<28&&lon>89&&lon<96)return"Assam";
  if(lat>30&&lon>76&&lat<34)return"Himachal Pradesh";
  if(lat>28&&lat<31&&lon>78&&lon<81)return"Uttarakhand";
  return"Madhya Pradesh";
}

function getGPS(){
  const btn=document.getElementById('btn-gps');
  const st=document.getElementById('loc-status');
  if(!navigator.geolocation){st.innerHTML='<span style="color:var(--red)">❌ Geolocation not supported by this browser.</span>';return;}
  btn.disabled=true;
  btn.innerHTML='<span class="spin"></span> Detecting location…';
  st.innerHTML='<span class="spin"></span> Requesting GPS access — please click Allow…';

  navigator.geolocation.getCurrentPosition(pos=>{
    const {latitude:lat,longitude:lon,accuracy}=pos.coords;
    st.innerHTML=`<span style="color:var(--green)">✅ GPS acquired — accuracy ±${Math.round(accuracy)}m. Fetching address…</span>`;
    btn.innerHTML='✅ Location Acquired';

    // Call Nominatim reverse geocode for village/taluk/district
    fetch('/api/geocode?lat='+lat+'&lon='+lon)
    .then(r=>r.json())
    .then(j=>{
      if(j.ok){
        const d=j.data;
        const state=d.state || stateFromCoords(lat,lon);
        document.getElementById('b-village').textContent  = d.village  || 'Not detected';
        document.getElementById('b-taluk').textContent    = d.taluk    || 'Not detected';
        document.getElementById('b-district').textContent = d.district || 'Not detected';
        document.getElementById('b-state').textContent    = state + (d.pincode?' · '+d.pincode:'');
        document.getElementById('location-banner').style.display='block';
        const locLabel=(d.village||d.district||state)+', '+state;
        loadWeather(lat,lon,locLabel);
        runAI(state,lat,lon,d);
      } else {
        const state=stateFromCoords(lat,lon);
        document.getElementById('b-state').textContent=state;
        document.getElementById('b-village').textContent='GPS accuracy: ±'+Math.round(accuracy)+'m';
        document.getElementById('location-banner').style.display='block';
        loadWeather(lat,lon,state+' (GPS)');
        runAI(state,lat,lon,{});
      }
      st.innerHTML='<span style="color:var(--green)">✅ Location analysis complete.</span>';
    }).catch(()=>{
      const state=stateFromCoords(lat,lon);
      loadWeather(lat,lon,state);
      runAI(state,lat,lon,{});
      document.getElementById('b-state').textContent=state;
      document.getElementById('location-banner').style.display='block';
    });
  }, err=>{
    btn.disabled=false;
    btn.innerHTML='📡 Detect My Exact Location';
    const msgs={1:'❌ Permission denied — please allow location in browser settings.',
                 2:'❌ Position unavailable — check device GPS.',
                 3:'❌ Timed out — try again or use manual input.'};
    st.innerHTML='<span style="color:var(--red)">'+(msgs[err.code]||'❌ GPS error')+'</span>';
    document.getElementById('man-wrap').style.display='block';
  }, {enableHighAccuracy:true,timeout:15000,maximumAge:0});
}

function analyseState(){
  const s=document.getElementById('state-sel').value;
  if(!s){alert('Please select a state.');return;}
  document.getElementById('b-state').textContent=s;
  document.getElementById('b-village').textContent='—';
  document.getElementById('b-taluk').textContent='—';
  document.getElementById('b-district').textContent='—';
  document.getElementById('location-banner').style.display='block';
  loadWeather(22.5,78.9,s+' (Manual)');
  runAI(s,null,null,{});
}

function runAI(state,lat,lon,geo){
  const db=CROP_DB[state]||{suit:["Wheat","Paddy","Maize","Gram","Arhar"],avoid:[],desc:'Diverse agricultural area.'};
  const pm={};
  ALL_PRICES.forEach(p=>{pm[p.name]=p.price;});

  // Verdict
  document.getElementById('ai-result').style.display='block';
  setTimeout(()=>window.scrollTo({top:document.getElementById('ai-result').offsetTop-80,behavior:'smooth'}),200);

  const topPriced=db.suit.map(c=>({c,p:pm[c]||0})).sort((a,b)=>b.p-a.p);
  document.getElementById('verdict-title').textContent=`🤖 AI Analysis — ${state}`;
  document.getElementById('verdict-sub').innerHTML=
    `<b style="color:rgba(255,255,255,.9)">${state}</b>: ${db.desc}<br><br>`+
    `✅ <span style="color:#fbbf24;font-weight:700;">Best crops:</span> ${db.suit.join(', ')}`+
    (db.avoid.length?`<br>⚠ <span style="color:#fca5a5;">Avoid in this region:</span> ${db.avoid.join(', ')}`:'');

  // Crop cards
  const rg=document.getElementById('rec-grid');
  rg.innerHTML='';
  db.suit.forEach(crop=>{
    const price=pm[crop];
    const icon=CROP_ICONS[crop]||'🌿';
    const sig=price>3000?'🔥 High Value':price>1500?'⚡ Good Return':'📊 Stable';
    const el=document.createElement('a');
    el.href='/commodity/'+crop.toLowerCase();
    el.className='rec';
    el.innerHTML=`<div class="rec-ico">${icon}</div>
      <div class="rec-name">${crop}</div>
      <div class="rec-price">₹${price?price.toLocaleString('en-IN'):'—'}/Qtl</div>
      <div class="rec-sig">${sig}</div>`;
    rg.appendChild(el);
  });

  // AI Tips
  const month=new Date().getMonth();
  const season=month>=5&&month<=9?'🌧 Kharif (Monsoon)':month>=10||month<=1?'❄️ Rabi (Winter)':'☀️ Zaid (Summer)';
  const top1=topPriced[0];
  const tips=[
    {ic:'🌱',t:`<b>Current Season:</b> You are in the <b>${season}</b> growing season. Align sowing with seasonal calendar for the best yield.`},
    {ic:'💰',t:`<b>Highest-Value Crop for ${state}:</b> <b>${top1?.c||db.suit[0]}</b> — current AI-predicted price <b>₹${(top1?.p||0).toLocaleString('en-IN')}/Qtl</b>.`},
    {ic:'📦',t:`<b>Storage Strategy:</b> Buy when prices are low (see 6-month forecast below) and sell at peak. Use eNAM portal or gramin bhandaran warehouses.`},
    {ic:'🔬',t:`<b>Soil Testing:</b> Get free soil testing at your nearest Krishi Vigyan Kendra (KVK). Check pH, NPK, and micronutrients before ${db.suit[0]||'crop'} sowing.`},
    {ic:'🌧',t:`<b>Irrigation Tip:</b> ${month>=5&&month<=9?state+' receives monsoon rains now — monitor waterlogging risks in low-lying fields.':'Dry season in your region — ensure drip/sprinkler irrigation is active before sowing.'}`},
    {ic:'📈',t:`<b>Market Timing:</b> Check the 6-month outlook table below. Register on <b>eNAM</b> (e-National Agricultural Market) for direct, better-price buyers.`},
    {ic:'🤖',t:`<b>About These Predictions:</b> Prices are computed by a <b>Decision Tree ML model</b> trained on WPI (Wholesale Price Index) data 2019–2024, with monthly rainfall seasonality.`},
  ];
  const tl=document.getElementById('tips-list');
  tl.innerHTML=tips.map(t=>`<div class="tip"><div class="tip-i">${t.ic}</div><div class="tip-t">${t.t}</div></div>`).join('');
}
