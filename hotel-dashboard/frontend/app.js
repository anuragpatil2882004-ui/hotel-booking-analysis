var summaryData = {
  cancel_by_price:[{p:"Under 2K",v:31.47},{p:"2K-4K",v:35.21},{p:"4K-6K",v:39.46},{p:"6K-8K",v:41.15},{p:"8K-10K",v:43.88},{p:"Above 10K",v:46.71}],
  lead_cancel:[{b:"0-20",v:31.4},{b:"21-40",v:39.53},{b:"41-60",v:43.47},{b:"61-80",v:35.42},{b:"81-100",v:31.16}],
  price_star:{
    labels:["Under 2K","2K-4K","4K-6K","6K-8K","8K-10K","Above 10K"],
    normal:[31.3,35.79,null,null,null,null],
    "3":[31.88,34.89,41.18,null,null,null],
    "4":[30.0,36.01,38.82,40.34,42.57,null],
    "5":[null,35.48,41.88,42.65,44.44,46.71]
  },
  price_demand:{
    labels:["Under 2K","2K-4K","4K-6K","6K-8K","8K-10K","Above 10K"],
    "Very High":[32.15,35.46,38.15,39.83,42.38,46.99],
    "High":[31.53,34.16,38.36,41.09,42.41,44.87],
    "Medium":[30.73,35.78,43.6,42.35,49.09,62.14],
    "Low":[32.77,41.19,40.51,59.38,null,null]
  },
  seasonal_demand:{
    labels:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    bookings:[4235,3936,4105,4177,4345,4243,4145,4171,4178,4261,4058,4146],
    revenue:[3.4,3.1,3.3,3.3,3.5,3.4,3.3,3.3,3.3,3.5,3.2,3.4],
    cancellation:[34.59,35.57,35.86,35.65,35.74,36.32,36.38,34.67,35.64,37.03,35.04,36.61]
  }
};

window.onload = function () {
  document.getElementById("totalBookings").textContent = "50,000";
  document.getElementById("totalCanceled").textContent = "17,881";
  document.getElementById("cancelRate").textContent    = "35.76%";
  document.getElementById("totalRevenue").textContent  = "Rs.596.5M";
  document.getElementById("avgLead").textContent       = "50.01 days";
  document.getElementById("revenueLost").textContent     = "Rs.15.5M";

  var g = { color:"rgba(240,236,228,0.9)", grid:{color:"rgba(255,255,255,0.05)"}, ticks:{color:"rgba(160,152,128,0.9)",font:{size:11}} };

  // Chart 1 — Price range overall
  new Chart(document.getElementById("cancelByPriceChart"),{
    type:"bar",
    data:{
      labels:summaryData.cancel_by_price.map(function(r){return r.p;}),
      datasets:[{label:"Cancellation Rate (%)",data:summaryData.cancel_by_price.map(function(r){return r.v;}),
        backgroundColor:["rgba(74,222,128,0.75)","rgba(134,197,100,0.75)","rgba(212,168,67,0.75)","rgba(240,140,60,0.75)","rgba(248,113,113,0.75)","rgba(220,38,38,0.8)"],
        borderRadius:8}]
    },
    options:co("Cancellation Rate (%)",g)
  });

  // Chart 2 — Price x Star Rating (grouped bar)
  new Chart(document.getElementById("cancelPriceStarChart"),{
    type:"bar",
    data:{
      labels:summaryData.price_star.labels,
      datasets:[
        {label:"Unrated",data:summaryData.price_star.normal,backgroundColor:"rgba(160,152,128,0.75)",borderRadius:4},
        {label:"3 Star", data:summaryData.price_star["3"],  backgroundColor:"rgba(212,168,67,0.75)", borderRadius:4},
        {label:"4 Star", data:summaryData.price_star["4"],  backgroundColor:"rgba(240,201,106,0.75)",borderRadius:4},
        {label:"5 Star", data:summaryData.price_star["5"],  backgroundColor:"rgba(255,230,140,0.85)",borderRadius:4}
      ]
    },
    options:co("Cancellation Rate (%)",g)
  });

  // Chart 3 — Price x Location Demand (grouped bar)
  new Chart(document.getElementById("cancelPriceDemandChart"),{
    type:"bar",
    data:{
      labels:summaryData.price_demand.labels,
      datasets:[
        {label:"Very High Demand",data:summaryData.price_demand["Very High"],backgroundColor:"rgba(167,139,250,0.75)",borderRadius:4},
        {label:"High Demand",     data:summaryData.price_demand["High"],     backgroundColor:"rgba(74,222,128,0.75)", borderRadius:4},
        {label:"Medium Demand",   data:summaryData.price_demand["Medium"],   backgroundColor:"rgba(212,168,67,0.75)", borderRadius:4},
        {label:"Low Demand",      data:summaryData.price_demand["Low"],      backgroundColor:"rgba(248,113,113,0.75)",borderRadius:4}
      ]
    },
    options:co("Cancellation Rate (%)",g)
  });

  // Chart 4 — Lead time
  new Chart(document.getElementById("leadCancelChart"),{
    type:"line",
    data:{
      labels:summaryData.lead_cancel.map(function(r){return r.b;}),
      datasets:[{label:"Cancellation Rate (%)",data:summaryData.lead_cancel.map(function(r){return r.v;}),
        borderColor:"rgba(212,168,67,0.9)",backgroundColor:"rgba(212,168,67,0.08)",
        fill:true,tension:0.4,pointRadius:6,pointBackgroundColor:"rgba(212,168,67,1)"}]
    },
    options:co("Cancellation Rate (%)",g)
  });

  // Chart 5 — Seasonal Demand
  new Chart(document.getElementById("seasonalDemandChart"),{
    type:"bar",
    data:{
      labels:summaryData.seasonal_demand.labels,
      datasets:[
        {label:"Bookings",data:summaryData.seasonal_demand.bookings,backgroundColor:"rgba(212,168,67,0.75)",borderRadius:4},
        {type:"line",label:"Cancellation Rate (%)",data:summaryData.seasonal_demand.cancellation,borderColor:"rgba(248,113,113,0.9)",backgroundColor:"rgba(248,113,113,0.08)",fill:false,tension:0.4,pointRadius:4,pointBackgroundColor:"rgba(248,113,113,1)"}
      ]
    },
    options:{
      plugins:{legend:{labels:{color:g.color}}},
      scales:{
        x:{grid:g.grid,ticks:g.ticks},
        y:{grid:g.grid,ticks:{...g.ticks,callback:function(v){return v/1000+"K"}},title:{display:true,text:"Bookings",color:g.color}}
      }
    }
  });
};

function co(y,g){return{plugins:{legend:{labels:{color:g.color}}},scales:{x:{grid:g.grid,ticks:g.ticks},y:{grid:g.grid,ticks:g.ticks,title:{display:true,text:y,color:g.color}}}};}

var locations={City:[{name:"Mumbai",demand:"Very High",pop:"20.7M"},{name:"Delhi",demand:"Very High",pop:"32.9M"},{name:"Bengaluru",demand:"Very High",pop:"13.2M"},{name:"Hyderabad",demand:"High",pop:"10.5M"},{name:"Chennai",demand:"High",pop:"11.5M"},{name:"Kolkata",demand:"High",pop:"14.9M"},{name:"Pune",demand:"High",pop:"7.4M"},{name:"Ahmedabad",demand:"Medium",pop:"8.4M"},{name:"Jaipur",demand:"Medium",pop:"3.9M"},{name:"Surat",demand:"Medium",pop:"7.8M"},{name:"Lucknow",demand:"Medium",pop:"3.7M"},{name:"Chandigarh",demand:"Medium",pop:"1.2M"},{name:"Kochi",demand:"Medium",pop:"2.1M"},{name:"Indore",demand:"Low",pop:"3.3M"},{name:"Bhopal",demand:"Low",pop:"2.4M"}],Resort:[{name:"Goa",demand:"Very High",pop:"1.5M"},{name:"Shimla",demand:"Very High",pop:"0.17M"},{name:"Manali",demand:"Very High",pop:"0.08M"},{name:"Udaipur",demand:"Very High",pop:"0.65M"},{name:"Ooty",demand:"High",pop:"0.09M"},{name:"Munnar",demand:"High",pop:"0.05M"},{name:"Coorg",demand:"High",pop:"0.27M"},{name:"Rishikesh",demand:"High",pop:"0.10M"},{name:"Darjeeling",demand:"High",pop:"0.13M"},{name:"Andaman Islands",demand:"High",pop:"0.43M"},{name:"Mussoorie",demand:"Medium",pop:"0.03M"},{name:"Kasauli",demand:"Medium",pop:"0.01M"},{name:"Lonavala",demand:"Medium",pop:"0.07M"},{name:"Mahabaleshwar",demand:"Medium",pop:"0.01M"},{name:"Kodaikanal",demand:"Low",pop:"0.04M"}]};
var bpm={normal:{ac:[1800,1200,800,500],nonac:[1200,800,500,350]},"3":{ac:[3500,2800,2000,1400],nonac:[2500,2000,1400,900]},"4":{ac:[7000,5500,4000,2800],nonac:[5000,4000,2800,2000]},"5":{ac:[15000,11000,8000,5500],nonac:[11000,8000,5500,4000]}};
var di={"Very High":0,"High":1,"Medium":2,"Low":3};
function gmp(star,ac,demand){return bpm[star][ac][di[demand]!=null?di[demand]:2];}
function normText(v){return (v||"").toLowerCase().replace(/[^a-z0-9]/g,"");}
function levDist(a,b){
  var m=a.length,n=b.length;
  var dp=new Array(m+1);
  for(var i=0;i<=m;i++){dp[i]=new Array(n+1);}
  for(var i=0;i<=m;i++)dp[i][0]=i;
  for(var j=0;j<=n;j++)dp[0][j]=j;
  for(var i=1;i<=m;i++){
    for(var j=1;j<=n;j++){
      var c=a[i-1]===b[j-1]?0:1;
      dp[i][j]=Math.min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+c);
    }
  }
  return dp[m][n];
}
function pickLocation(arr,rawLocation,hotelType){
  var q=normText(rawLocation);
  if(!q){
    for(var i=0;i<arr.length;i++){if(arr[i].demand==="Medium"){return arr[i];}}
    return {name:hotelType,demand:"Medium",pop:"--"};
  }
  for(var i=0;i<arr.length;i++){
    if(normText(arr[i].name)===q){return arr[i];}
  }
  var best=null,bestScore=1e9;
  for(var i=0;i<arr.length;i++){
    var n=normText(arr[i].name);
    var d=levDist(q,n);
    if(n.indexOf(q)>=0||q.indexOf(n)>=0){d=Math.min(d,1);}
    if(d<bestScore){best=arr[i];bestScore=d;}
  }
  var threshold=Math.max(2,Math.floor(q.length*0.35));
  if(best&&bestScore<=threshold){return best;}
  // Keep user's original location if we cannot confidently map it.
  return {name:rawLocation,demand:"Medium",pop:"--"};
}

function calcRisk(ht,lt,sd,pp,sr,at,li){
  var s=0;
  if(lt>=41&&lt<=60)s+=6;else if(lt>=21&&lt<=40)s+=4;else if(lt>=61&&lt<=80)s+=2;else if(lt>80)s+=1;
  if(sd===7)s+=4;else if(sd<=2)s+=3;else if(sd<=4)s+=2;else if(sd>=8)s+=1;
  var mp=gmp(sr,at,li.demand),pr=pp/mp,dm={"Very High":0.6,"High":0.8,"Medium":1.0,"Low":1.6}[li.demand]||1.0;
  if(pr>2.0)s+=Math.round(10*dm);else if(pr>1.5)s+=Math.round(7*dm);else if(pr>1.2)s+=Math.round(4*dm);else if(pr>1.0)s+=Math.round(2*dm);else if(pr<0.5)s+=3;else if(pr<0.7)s+=1;
  if(sr==="5")s+=3;else if(sr==="4")s+=2;else if(sr==="3")s+=1;
  if(at==="ac")s+=1;if(ht==="City")s+=1;
  if(li.demand==="Very High")s+=2;else if(li.demand==="High")s+=1;else if(li.demand==="Low")s-=1;
  return s>=14?"high":s>=8?"medium":"low";
}

document.addEventListener("DOMContentLoaded",function(){
   document.getElementById("addBookingBtn").addEventListener("click",function(){
     var lt=parseInt(document.getElementById("leadTime").value);
     var sd=parseInt(document.getElementById("stayDuration").value);
     var pp=parseInt(document.getElementById("pricePerNight").value);
     var rt=document.getElementById("roomType").value;
     var analysisLocation=(document.getElementById("analysisLocation").value||"").trim();
     var box=document.getElementById("predictionResult");
     if(!lt||!sd||!pp){box.className="prediction-box medium";box.innerHTML="Please fill in all fields.";return;}
     var u=JSON.parse(localStorage.getItem("hd_user")||"{}");
     var ht=u.hotelType||"City";
     var rl=analysisLocation||u.hotelLocation||"";
     var sr=u.starRating||"normal";
     var at=rt;
    var arr=locations[ht]||[];
    var li=pickLocation(arr,rl,ht);
    var tc=pp*sd,r=calcRisk(ht,lt,sd,pp,sr,at,li);
    var sl={normal:"Normal","3":"3 Star","4":"4 Star","5":"5 Star"}[sr];
    var al=at==="ac"?"AC":"Non-AC";
    var rl2={low:"Low Risk",medium:"Medium Risk",high:"High Risk"}[r];
    var adv={low:"This booking looks stable. Low chance of cancellation.",medium:"Moderate risk. Consider sending a reminder closer to check-in.",high:"High risk. Recommend requiring a non-refundable deposit."}[r];
    var ps="";
    if(r==="medium"||r==="high"){
      var mp=gmp(sr,at,li.demand),rec=Math.round(mp*0.9);
      if(pp>rec)ps='<div style="margin-top:12px;padding:10px 14px;background:rgba(255,255,255,0.05);border-radius:4px;font-size:0.85rem;">Suggestion: Lowering to Rs.'+rec.toLocaleString()+'/night may reduce cancellation risk.</div>';
      else if(pp<Math.round(mp*0.6))ps='<div style="margin-top:12px;padding:10px 14px;background:rgba(255,255,255,0.05);border-radius:4px;font-size:0.85rem;">Note: Price is below market (typical: Rs.'+mp.toLocaleString()+'/night).</div>';
    }
    box.className="prediction-box "+r;
    box.innerHTML='<strong>Cancellation Risk: <span class="risk-badge">'+rl2+'</span></strong><br/><span style="opacity:0.85">'+adv+'</span><br/><br/>Hotel: <strong>'+ht+'</strong> - <strong>'+li.name+'</strong> ('+li.demand+' demand)<br/>Room: <strong>'+sl+'</strong> | <strong>'+al+'</strong> | Rs.'+pp.toLocaleString()+'/night | <strong>'+sd+' nights</strong> | Lead: <strong>'+lt+' days</strong><br/><strong>Total: Rs.'+tc.toLocaleString()+'</strong>'+ps;
    var prev=window._ub||[];prev.push({tc:tc});window._ub=prev;
    document.getElementById("totalBookings").textContent=(50000+prev.length).toLocaleString();
    document.getElementById("totalRevenue").textContent="Rs."+((592735959+prev.reduce(function(s,b){return s+b.tc;},0))/1e6).toFixed(2)+"M";
  });
});