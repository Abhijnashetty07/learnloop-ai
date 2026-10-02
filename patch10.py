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
.novis{display:none !important}"""),
("""<div class="card pg2"><p class="label">YOUR RESPONSE""",
"""<div class="card pg2 novis" id="vizCard"><p class="label">VISUAL EXPLAINER</p><div class="chartwrap" style="height:250px"><canvas id="viz"></canvas></div><div class="hint" id="vizNote"></div></div>
<div class="card pg2"><p class="label">YOUR RESPONSE"""),
("""goPage(2);""", """goPage(2);showViz(current);"""),
("""function setBot(""",
"""var vizChart=null;
function rng(a,b,s){var r=[];for(var x=a;x<=b+1e-9;x+=s){r.push(+x.toFixed(2));}return r;}
function pts(xs,f){return xs.map(function(x){return {x:x,y:f(x)};});}
function ln(c,d,l,e){return Object.assign({label:l,data:d,showLine:true,borderColor:c,backgroundColor:c,pointRadius:0,tension:.35,borderWidth:3},e||{});}
var G="#f3c94b",O="#f39a2b",B="#5b9cf5",R="#ff5c7a";
var bowl=function(x){return x*x/2+1;};
var VIZ={
 loss_functions:{xt:"Model weight",yt:"Loss (error)",note:"Loss is lowest where the weight is just right. Training tries to reach the bottom of this curve.",
  ds:[ln(G,pts(rng(-4,4,.25),bowl),"Loss")]},
 gradient_descent:{xt:"Model weight",yt:"Loss (error)",note:"Each step moves downhill, like the hiker in fog. The steps shrink as the slope flattens near the bottom.",
  ds:[ln(G,pts(rng(-4,4,.25),bowl),"Loss curve"),ln(O,pts([3.5,2.6,1.8,1.2,.7,.3,.1],bowl),"Gradient descent steps",{pointRadius:6,tension:0,borderDash:[6,4]})]},
 linear_regression:{xt:"Input (e.g. house size)",yt:"Output (e.g. price)",note:"The line is fitted to stay as close as possible to all the dots, so it can predict new values.",
  ds:[{label:"Data",data:pts(rng(1,10,1),function(x){return 2*x+1+[.8,-1.2,1,-.5,1.5,-1,.6,-1.3,.9,-.4][x-1];}),backgroundColor:B,pointRadius:6},ln(G,[{x:0,y:1},{x:11,y:23}],"Best-fit line")]},
 overfitting:{xt:"Model complexity",yt:"Error",note:"Training error keeps falling, but once the model starts memorising, error on new data climbs back up.",
  ds:[ln(B,pts(rng(1,10,1),function(x){return [9,6,4.2,3,2.1,1.4,.9,.5,.25,.1][x-1];}),"Training data"),ln(R,pts(rng(1,10,1),function(x){return [9.5,6.8,5,4,3.6,3.7,4.3,5.3,6.6,8][x-1];}),"New data")]},
 activation_functions:{xt:"Input to the neuron",yt:"Output",note:"These bends are what let a network learn curved, complex patterns instead of only straight lines.",
  ds:[ln(G,pts(rng(-4,4,.25),function(x){return Math.max(0,x);}),"ReLU",{tension:0}),ln(O,pts(rng(-4,4,.25),Math.tanh),"Tanh")]}
};
function showViz(id){
  var spec=VIZ[id],card=$("vizCard");
  if(vizChart){vizChart.destroy();vizChart=null;}
  if(!spec){card.classList.add("novis");return;}
  card.classList.remove("novis");
  $("vizNote").textContent=spec.note;
  var ax=function(t){return {title:{display:true,text:t,color:"#ccc"},ticks:{color:"#ccc"},grid:{color:"#2a2a2a"}};};
  vizChart=new Chart($("viz"),{type:"scatter",data:{datasets:spec.ds},options:{maintainAspectRatio:false,animation:{duration:1400},plugins:{legend:{display:spec.ds.length>1,labels:{color:"#ccc"}}},scales:{x:ax(spec.xt),y:ax(spec.yt)}}});
}
function hideViz(){if(vizChart){vizChart.destroy();vizChart=null;}$("vizCard").classList.add("novis");}
function setBot("""),
("""Pick a concept.");goPage(1);""", """Pick a concept.");goPage(1);hideViz();"""),
])
print("Visuals patch done")
