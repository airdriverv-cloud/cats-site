(function(){'use strict';
var B=document.body,P=window.PHOTOS,A=window.ARTICLES;
function url(k,t){var h=P[k][0],o=BASE+h+'.jpg';return t?BASE.replace('/upload/','/upload/t_thumbnail_512/')+h+'.jpg':o}
function img(k,c,w,h){var i=new Image();i.className=c||'';i.alt=P[k][1];i.width=w;i.height=h;i.loading='lazy';i.decoding='async';i.src=url(k,1);i.onerror=function(){i.onerror=null;i.src=url(k,0)};return i}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x)e.textContent=x;return e}
function link(href,x,c){var a=el('a',c,x);a.href=href;return a}
function ext(a){a.target='_blank';a.rel='noopener noreferrer';return a}
function href(a,pre){return a.legacy?pre+'articles/'+a.slug+'.html':pre+'article.html?a='+a.slug}
function card(a,pre){var c=link(href(a,pre),'','card');c.dataset.cat=a.cat;c.dataset.s=(a.title+' '+a.desc).toLowerCase().replace(/ё/g,'е');c.appendChild(img(a.photo,'',512,300));var b=el('div','cb');b.appendChild(el('span','m',a.cat));b.appendChild(el('h3','',a.title));b.appendChild(el('p','',a.desc));c.appendChild(b);return c}
function credit(k){var p=el('p','cap','Фото: ');var a=ext(link(P[k][2]||'https://www.pexels.com/','Pexels'));p.appendChild(a);return p}
var menu=document.getElementById('menu');
var list=document.getElementById('cards');
if(list){A.forEach(function(a){list.appendChild(card(a,''))});
var hero=document.getElementById('hero-img');hero.appendChild(img('bed','',1200,923));hero.appendChild(credit('bed'));
var q=document.getElementById('q'),cat='Все',cnt=document.getElementById('cnt'),em=document.getElementById('empty');
var fb=document.querySelectorAll('[data-f]');
function upd(){var s=q.value.toLowerCase().replace(/ё/g,'е').trim(),n=0;[].forEach.call(list.children,function(c){var ok=(cat==='Все'||c.dataset.cat===cat)&&c.dataset.s.indexOf(s)>-1;c.hidden=!ok;if(ok)n++});cnt.textContent='Найдено: '+n+' из '+A.length;em.hidden=n>0;[].forEach.call(fb,function(b){b.setAttribute('aria-pressed',String(b.dataset.f===cat))})}
q.addEventListener('input',upd);[].forEach.call(fb,function(b){b.addEventListener('click',function(){cat=b.dataset.f;upd()})});
document.getElementById('reset').addEventListener('click',function(){q.value='';cat='Все';upd()});upd();
var cr=document.getElementById('credits');if(cr){Object.keys(P).forEach(function(k){if(P[k][2]){var li=el('li');li.appendChild(ext(link(P[k][2],P[k][1]+' — Pexels')));cr.appendChild(li)}})}}
var root=document.getElementById('article');
if(root){var slug=new URLSearchParams(location.search).get('a'),a=A.filter(function(x){return x.slug===slug&&!x.legacy})[0];
if(!a){root.appendChild(el('h1','','Статья не найдена'));root.appendChild(link('index.html#articles','← Все статьи'))}else{document.title=a.title+' — Мир кошек';
root.appendChild(el('p','eyebrow',a.cat));root.appendChild(el('h1','',a.title));root.appendChild(img(a.photo,'cover',1200,600));root.appendChild(credit(a.photo));
var pr=el('div','prose');a.s.forEach(function(s){pr.appendChild(el('h2','',s[0]));pr.appendChild(el('p','',s[1]))});
var sr=el('div','src');sr.appendChild(el('h2','','Подробнее у специалистов'));a.src.forEach(function(s){var p=el('p');p.appendChild(ext(link(s[1],s[0]+' ↗')));sr.appendChild(p)});pr.appendChild(sr);root.appendChild(pr);
var rel=document.getElementById('related');rel.appendChild(el('h2','','Ещё по теме'));var g=el('div','cards');A.filter(function(x){return x.slug!==a.slug&&x.cat===a.cat}).slice(0,2).forEach(function(x){g.appendChild(card(x,''))});rel.appendChild(g)}}
})();
