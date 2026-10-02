def edit(path, pairs):
    t = open(path, encoding="utf-8-sig").read()
    for old, new in pairs:
        if old in t:
            t = t.replace(old, new, 1)
        else:
            print("SKIPPED (not found):", old[:50])
    open(path, "w", encoding="utf-8").write(t)

edit("templates/index.html", [
(""".chartwrap{height:300px;position:relative}""",
""".chartwrap{height:300px;position:relative}
header{flex-wrap:wrap;gap:10px}
main{grid-template-columns:1fr;max-width:760px}
.card.pg1,.card.pg2,.card.pg3{display:none}
body[data-pg="1"] .card.pg1,body[data-pg="2"] .card.pg2,body[data-pg="3"] .card.pg3{display:block}
#pgnav{display:flex;gap:8px;justify-content:center;padding:14px 28px 0;flex-wrap:wrap}
#pgnav button,#pager button{background:#1d1d1d;color:var(--text);border:1px solid var(--line);border-radius:999px;padding:9px 18px;font-size:14px;cursor:pointer}
#pgnav button.on,#pager button:hover:not(:disabled){border-color:var(--gold);color:var(--gold)}
#pager{display:flex;justify-content:space-between;max-width:760px;margin:0 auto;padding:0 28px 30px}
#pager button:disabled{opacity:.35;cursor:not-allowed}"""),
("""<body>""", """<body data-pg="1">"""),
("""</header>""",
"""</header>
<nav id="pgnav"><button data-pg="1">1. Topics</button><button data-pg="2">2. Learn &amp; answer</button><button data-pg="3">3. Progress</button></nav>"""),
("""<div class="card"><p class="label">CONCEPT TRACKER</p>""", """<div class="card pg1"><p class="label">CONCEPT TRACKER</p>"""),
("""<div class="card"><div class="botrow">""", """<div class="card pg2"><div class="botrow">"""),
("""<div class="card"><p class="label">YOUR RESPONSE""", """<div class="card pg2"><p class="label">YOUR RESPONSE"""),
("""<div class="card"><p class="label">SESSION MASTERY GROWTH""", """<div class="card pg3"><p class="label">SESSION MASTERY GROWTH"""),
("""<div class="card"><div class="state""", """<div class="card pg3"><div class="state"""),
("""</main>""",
"""</main>
<div id="pager"><button id="pgBack">&larr; Back</button><button id="pgNext">Next &rarr;</button></div>"""),
("""<span class="pill" id="voiceBtn""",
"""<select class="nameinp" id="voiceSel" title="Loopy voice"></select><span class="pill" id="voiceBtn"""),
("""$("answer").disabled=false;$("submit").disabled=false;""",
"""$("answer").disabled=false;$("submit").disabled=false;goPage(2);"""),
("""setBot("idle","Fresh start! Pick a concept.");""",
"""setBot("idle","Fresh start! Pick a concept.");goPage(1);"""),
("""function setBot(""",
"""var PG=1, sayId=0;
function goPage(n){
  PG=Math.max(1,Math.min(3,n));
  document.body.setAttribute("data-pg",PG);
  document.querySelectorAll("#pgnav button").forEach(function(b){b.classList.toggle("on",+b.dataset.pg===PG);});
  $("pgBack").disabled=(PG===1);$("pgNext").disabled=(PG===3);
  window.scrollTo(0,0);
  if(PG===3&&chart){setTimeout(function(){chart.resize();},60);}
}
document.querySelectorAll("#pgnav button").forEach(function(b){b.onclick=function(){goPage(+b.dataset.pg);};});
$("pgBack").onclick=function(){goPage(PG-1);};
$("pgNext").onclick=function(){goPage(PG+1);};
function pickVoice(){
  var vs=speechSynthesis.getVoices().filter(function(v){return /^en/i.test(v.lang);});
  function score(v){var s=0;if(/natural|neural/i.test(v.name))s+=6;if(/online|google/i.test(v.name))s+=3;if(/en-IN/i.test(v.lang))s+=2;if(/neerja|heera|aria|jenny|zira|samantha/i.test(v.name))s+=1;return s;}
  vs.sort(function(a,b){return score(b)-score(a);});
  var sel=$("voiceSel"),keep=sel.value;
  sel.innerHTML=vs.map(function(v,i){return '<option value="'+i+'">'+esc(v.name)+'</option>';}).join("");
  window._vs=vs;voice=vs[0]||null;
  if(keep!==""&&vs[keep]){sel.value=keep;voice=vs[keep];}
}
function say(text){
  if(!voiceOn||!window.speechSynthesis||!text){return;}
  speechSynthesis.cancel();
  var id=++sayId,bot=$("bot");
  var parts=String(text).replace(/\s+/g," ").match(/[^.!?]+[.!?]*/g)||[String(text)];
  parts.forEach(function(t,i){
    var u=new SpeechSynthesisUtterance(t.trim());
    if(voice){u.voice=voice;u.lang=voice.lang;}
    u.rate=0.95;u.pitch=1;
    if(i===0){u.onstart=function(){if(id===sayId){bot.classList.add("talking");}};}
    if(i===parts.length-1){u.onend=function(){if(id===sayId){bot.classList.remove("talking");}};u.onerror=u.onend;}
    speechSynthesis.speak(u);
  });
}
$("voiceSel").onchange=function(){voice=(window._vs||[])[this.value]||voice;say("Hi, this is how I sound.");};
if(!window.speechSynthesis){$("voiceSel").style.display="none";}
goPage(1);
function setBot("""),
])
print("Pages and voice patch done")
