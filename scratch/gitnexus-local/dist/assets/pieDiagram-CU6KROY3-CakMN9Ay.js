import{t as e}from"./chunk-AQ6EADP3-BpMj3rQl.js";import{Ct as t,D as n,Mt as r,N as i,Pt as a,Qt as o,W as s,dt as c,ft as l,gt as u,lt as d,nt as f,pt as p,tn as m,vt as h,wt as g,xt as _}from"./index-Bpj1wmP0.js";import"./chunk-4R4BOZG6-D3gm7tYj.js";import"./chunk-RERM46MO-Betu1cSy.js";import{t as v}from"./chunk-JQRUD6KW-DElaNjc0.js";import{t as y}from"./chunk-2T2R6R2M-CwRZR2tj.js";import"./chunk-UP6H54XL-0YWa0NDg.js";import"./chunk-UXSXWOXI-CSz0OXpz.js";import"./chunk-C62D2QBJ-CvFF2PnB.js";import"./chunk-CEXFNPSA-DdNtJtrF.js";import"./chunk-J5EP6P6S-DtcVaAJI.js";import"./chunk-RLI5ZMPA-BFUxCvX2.js";import"./chunk-2UTLFMKG-CpoohCFN.js";import"./chunk-RKZBBQEN-Cutpza0t.js";import"./chunk-KGYTTC2M-D0K5or7e.js";var b=d.pie,x={sections:new Map,showData:!1,config:b},S=x.sections,C=x.showData,w=structuredClone(b),T={getConfig:e(()=>structuredClone(w),`getConfig`),clear:e(()=>{S=new Map,C=x.showData,_()},`clear`),setDiagramTitle:l,getDiagramTitle:h,setAccTitle:c,getAccTitle:g,setAccDescription:u,getAccDescription:f,addSection:e(({label:e,value:t})=>{if(t<0)throw Error(`"${e}" has invalid value: ${t}. Negative values are not allowed in pie charts. All slice values must be >= 0.`);S.has(e)||(S.set(e,t),m.debug(`added new section: ${e}, with value: ${t}`))},`addSection`),getSections:e(()=>S,`getSections`),setShowData:e(e=>{C=e},`setShowData`),getShowData:e(()=>C,`getShowData`)},E=e((e,t)=>{v(e,t),t.setShowData(e.showData),e.sections.map(t.addSection)},`populateDb`),D={parse:e(async e=>{let t=await y(`pie`,e);m.debug(t),E(t,T)},`parse`)},O=e(e=>`
  .pieCircle{
    stroke: ${e.pieStrokeColor};
    stroke-width : ${e.pieStrokeWidth};
    opacity : ${e.pieOpacity};
  }
  .pieOuterCircle{
    stroke: ${e.pieOuterStrokeColor};
    stroke-width: ${e.pieOuterStrokeWidth};
    fill: none;
  }
  .pieTitleText {
    text-anchor: middle;
    font-size: ${e.pieTitleTextSize};
    fill: ${e.pieTitleTextColor};
    font-family: ${e.fontFamily};
  }
  .slice {
    font-family: ${e.fontFamily};
    fill: ${e.pieSectionTextColor};
    font-size:${e.pieSectionTextSize};
    // fill: white;
  }
  .legend text {
    fill: ${e.pieLegendTextColor};
    font-family: ${e.fontFamily};
    font-size: ${e.pieLegendTextSize};
  }
`,`getStyles`),k=e(e=>{let t=[...e.values()].reduce((e,t)=>e+t,0),n=[...e.entries()].map(([e,t])=>({label:e,value:t})).filter(e=>e.value/t*100>=1);return r().value(e=>e.value).sort(null)(n)},`createPieArcs`),A={parser:D,db:T,renderer:{draw:e((e,r,c,l)=>{m.debug(`rendering pie chart
`+e);let u=l.db,d=t(),f=n(u.getConfig(),d.pie),h=s(r),g=h.append(`g`);g.attr(`transform`,`translate(225,225)`);let{themeVariables:_}=d,[v]=i(_.pieOuterStrokeWidth);v??=2;let y=f.textPosition,b=o().innerRadius(0).outerRadius(185),x=o().innerRadius(185*y).outerRadius(185*y);g.append(`circle`).attr(`cx`,0).attr(`cy`,0).attr(`r`,185+v/2).attr(`class`,`pieOuterCircle`);let S=u.getSections(),C=k(S),w=[_.pie1,_.pie2,_.pie3,_.pie4,_.pie5,_.pie6,_.pie7,_.pie8,_.pie9,_.pie10,_.pie11,_.pie12],T=0;S.forEach(e=>{T+=e});let E=C.filter(e=>(e.data.value/T*100).toFixed(0)!==`0`),D=a(w).domain([...S.keys()]);g.selectAll(`mySlices`).data(E).enter().append(`path`).attr(`d`,b).attr(`fill`,e=>D(e.data.label)).attr(`class`,`pieCircle`),g.selectAll(`mySlices`).data(E).enter().append(`text`).text(e=>(e.data.value/T*100).toFixed(0)+`%`).attr(`transform`,e=>`translate(`+x.centroid(e)+`)`).style(`text-anchor`,`middle`).attr(`class`,`slice`);let O=g.append(`text`).text(u.getDiagramTitle()).attr(`x`,0).attr(`y`,-400/2).attr(`class`,`pieTitleText`),A=[...S.entries()].map(([e,t])=>({label:e,value:t})),j=g.selectAll(`.legend`).data(A).enter().append(`g`).attr(`class`,`legend`).attr(`transform`,(e,t)=>{let n=22*A.length/2;return`translate(216,`+(t*22-n)+`)`});j.append(`rect`).attr(`width`,18).attr(`height`,18).style(`fill`,e=>D(e.label)).style(`stroke`,e=>D(e.label)),j.append(`text`).attr(`x`,22).attr(`y`,14).text(e=>u.getShowData()?`${e.label} [${e.value}]`:e.label);let M=512+Math.max(...j.selectAll(`text`).nodes().map(e=>e?.getBoundingClientRect().width??0)),N=O.node()?.getBoundingClientRect().width??0,P=450/2-N/2,F=450/2+N/2,I=Math.min(0,P),L=Math.max(M,F)-I;h.attr(`viewBox`,`${I} 0 ${L} 450`),p(h,450,L,f.useMaxWidth)},`draw`)},styles:O};export{A as diagram};