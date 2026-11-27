(function(){'use strict';
const C=window.CM_CONFIG||{},SB=(C.supabaseUrl||'').replace(/\/$/,''),KEY=C.supabaseAnonKey||'',UZAK=!!(SB&&KEY);
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)],kok=$('#kok');
const e=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const nf=n=>Number(n).toLocaleString('tr-TR');
const LS={get(k,d){try{const v=JSON.parse(localStorage.getItem(k));return v==null?d:v}catch(_){return d}},set(k,v){localStorage.setItem(k,JSON.stringify(v))},del(k){localStorage.removeItem(k)}};
const S={kat:null,grup:{},parca:{},oturum:LS.get('cm_oturum',null),profil:null,profiller:{},oneriler:[]};
let W=null,toastT;
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('acik');clearTimeout(toastT);toastT=setTimeout(()=>t.classList.remove('acik'),2200)}
function uuid(){return crypto.randomUUID?crypto.randomUUID():'y-'+Date.now()+'-'+Math.random().toString(16).slice(2)}
function renk(s){let h=0;for(const c of String(s))h=(h*31+c.charCodeAt(0))%360;return 'hsl('+h+' 62% 52%)'}
function av(id,kucuk){const p=S.profiller[id]||{ad:'?'};const ad=p.ad||'?';const bas=ad.trim().split(/\s+/).map(x=>x[0]).slice(0,2).join('').toLocaleUpperCase('tr-TR');return '<span class="av'+(kucuk?' kucuk':'')+'" style="background:'+renk(id+ad)+'" title="'+e(ad)+'">'+e(bas)+'</span>'}
const adi=id=>(S.profiller[id]||{}).ad||'Bilinmeyen';
/* ---------- Supabase (kütüphanesiz) ---------- */
async function auth(yol,govde){const r=await fetch(SB+'/auth/v1/'+yol,{method:'POST',headers:{apikey:KEY,'Content-Type':'application/json'},body:JSON.stringify(govde)});const j=await r.json().catch(()=>({}));if(!r.ok)throw new Error(j.error_description||j.msg||j.message||'Giriş başarısız');return j}
function oturumYaz(j){S.oturum={a:j.access_token,r:j.refresh_token,s:Date.now()+(j.expires_in||3600)*1000,u:{id:j.user.id,email:j.user.email}};LS.set('cm_oturum',S.oturum)}
function cikis(){S.oturum=null;S.profil=null;LS.del('cm_oturum');if(!UZAK)LS.del('cm_yerel_profil');window.onhashchange=null;history.replaceState(null,'',location.pathname);basla()}
async function jeton(){if(!S.oturum)throw new Error('Oturum yok');if(Date.now()>S.oturum.s-60000){try{oturumYaz(await auth('token?grant_type=refresh_token',{refresh_token:S.oturum.r}))}catch(x){cikis();throw x}}return S.oturum.a}
async function db(yol,opt){opt=opt||{};const t=await jeton();const r=await fetch(SB+'/rest/v1/'+yol,Object.assign({},opt,{headers:Object.assign({apikey:KEY,Authorization:'Bearer '+t,'Content-Type':'application/json',Prefer:'return=representation'},opt.headers||{})}));if(r.status===401){cikis();throw new Error('Oturum süresi doldu')}const j=await r.json().catch(()=>null);if(!r.ok)throw new Error((j&&j.message)||('Sunucu hatası '+r.status));return j}
async function profilYukle(){const rows=await db('profiller?select=*');S.profiller={};rows.forEach(p=>S.profiller[p.id]=p);S.profil=S.profiller[S.oturum.u.id]||null}
async function havuzYukle(){let tum=[],o=0;for(;;){const r=await db('oneriler?select=*&order=olusturma.asc&limit=1000&offset='+o);tum=tum.concat(r);if(r.length<1000)break;o+=1000}S.oneriler=tum}
/* ---------- açılış ---------- */
async function basla(){
  try{if(!S.kat)S.kat=await(await fetch('veri/katalog.json')).json()}catch(x){kok.innerHTML='<div class="giris"><div class="cam"><h1>Katalog bulunamadı</h1><p>veri/katalog.json okunamadı. Önce katalog aracını çalıştır.</p></div></div>';return}
  if(UZAK){if(!S.oturum)return girisCiz();try{await profilYukle()}catch(x){if(!S.oturum)return;return girisCiz(x.message)}if(!S.profil)return profilCiz();try{await havuzYukle()}catch(x){toast('Havuz okunamadı: '+x.message)}}
  else{S.profil=LS.get('cm_yerel_profil',null);if(!S.profil)return profilCiz();S.profiller={yerel:S.profil};S.oneriler=LS.get('cm_yerel_oneriler',[])}
  window.onhashchange=yon;yon()}
function girisCiz(hata) {
  kok.innerHTML = '<div class="giris"><div class="cam"><img class="logo" src="logo.png" alt=""><h1>A-Life Lokalizasyon</h1><p>Project A-Life Türkçe yaması</p><button class="btn koyu">Google ile devam et</button><div class="hata" role="alert"></div></div></div>';
  $('.hata', kok).textContent = hata || '';
  $('button', kok).onclick = async function () {
    this.disabled = true;
    try {
      const bytes = crypto.getRandomValues(new Uint8Array(32));
      const verifier = Array.from(bytes, n => n.toString(16).padStart(2, '0')).join('');
      const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier));
      const challenge = btoa(String.fromCharCode(...new Uint8Array(digest))).replaceAll('+','-').replaceAll('/','_').replace(/=+$/, '');
      sessionStorage.setItem('cm_pkce', verifier);
      const url = new URL(SB + '/auth/v1/authorize');
      url.search = new URLSearchParams({provider:'google', redirect_to:location.origin + location.pathname, code_challenge:challenge, code_challenge_method:'s256'});
      location.assign(url);
    } catch (err) {
      $('.hata', kok).textContent = err.message;
      this.disabled = false;
    }
  };
}
async function oturumuBaslat() {
  const query = new URLSearchParams(location.search);
  const fragment = new URLSearchParams(location.hash.slice(1));
  const code = query.get('code');
  const error = query.get('error') || fragment.get('error');
  if (UZAK && (code || error)) {
    history.replaceState(null, '', location.pathname);
    const verifier = sessionStorage.getItem('cm_pkce');
    sessionStorage.removeItem('cm_pkce');
    if (error || !verifier) return girisCiz('Google ile giriş tamamlanamadı. Tekrar deneyebilirsin.');
    try {
      oturumYaz(await auth('token?grant_type=pkce', {auth_code:code, code_verifier:verifier}));
    } catch (err) {
      return girisCiz(err.message);
    }
  }
  return basla();
}
function profilCiz(){kok.innerHTML='<div class="giris"><div class="cam"><img class="logo" src="logo.png" alt=""><h1>Seni nasıl analım?</h1><p>'+(UZAK?'Önerilerinin yanında bu ad görünecek.':'Yerel mod: Supabase ayarı girilmemiş. Öneriler yalnızca bu tarayıcıda saklanır.')+'</p><form><input class="alan" name="ad" placeholder="Adın" maxlength="40" required><div class="hata"></div><button class="btn koyu">Devam et</button></form></div></div>';
  $('input',kok).focus();
  $('form',kok).onsubmit=async ev=>{ev.preventDefault();const ad=ev.target.ad.value.trim();if(!ad)return;try{if(UZAK)await db('profiller',{method:'POST',body:JSON.stringify([{id:S.oturum.u.id,ad:ad}])});else LS.set('cm_yerel_profil',{id:'yerel',ad:ad});await basla()}catch(x){$('.hata',kok).textContent=x.message}}}
/* ---------- kabuk ---------- */
function kabuk(aktif,ic){
  kok.innerHTML='<nav class="nav cam"><img class="logo" src="logo.png" alt=""><b>A-Life Lokalizasyon</b><a href="#/" class="'+(aktif==='ana'?'acik':'')+'">Sahneler</a><a href="#/havuz" class="'+(aktif==='havuz'?'acik':'')+'">Havuz'+(S.oneriler.length?' · '+nf(S.oneriler.length):'')+'</a><a href="#/kapsam" class="'+(aktif==='kapsam'?'acik':'')+'">Kapsam</a><span class="bos"></span>'+(UZAK?'':'<span class="yerel">yerel mod</span>')+'<span class="surum">'+e(S.kat.surum)+'</span><button class="ben" id="ben">'+av(S.profil.id)+e(S.profil.ad)+'</button></nav>'+ic;
  $('#ben').onclick=ev=>{ev.stopPropagation();let m=$('.menu');if(m){m.remove();return}m=document.createElement('div');m.className='menu cam';m.innerHTML='<strong>'+e(S.profil.ad)+'</strong><small>'+e(UZAK?S.oturum.u.email:'Bu tarayıcıda saklanan profil')+'</small><div>'+nf(S.oneriler.filter(o=>o.yazar===S.profil.id).length)+' önerin var</div><button class="btn kucuk" style="margin-top:12px">'+(UZAK?'Çıkış yap':'Profili sıfırla')+'</button>';$('.nav').appendChild(m);m.onclick=x=>x.stopPropagation();$('button',m).onclick=()=>cikis();document.addEventListener('click',()=>m.remove(),{once:true})}}
function yon(){const h=location.hash.replace(/^#\/?/,'').split('/');window.scrollTo(0,0);
  if(h[0]==='g'&&h[1])return calisma(h[1],parseInt(h[2]||'0',10)||0,h[3]?decodeURIComponent(h[3]):null);
  W=null;if(h[0]==='havuz'){if(UZAK)return havuzYukle().then(()=>{if(location.hash==='#/havuz')havuz()}).catch(x=>toast(x.message));return havuz()}if(h[0]==='kapsam')return kapsam();ana()}
function guvenBar(d,t){const p=k=>((d[k]||0)/t*100).toFixed(2);return '<div class="guven" title="Bağlam güveni"><i class="l2" style="width:'+p('2')+'%"></i><i class="l1" style="width:'+p('1')+'%"></i><i class="l0" style="width:'+p('0')+'%"></i></div>'}
function ana(){const son=LS.get('cm_son',null);
  let ic='<main class="sayfa"><div class="selam">Merhaba, '+e(S.profil.ad)+'</div><h1 class="dev">Bugün hangi <em>sahneye</em> bakıyoruz?</h1><p class="alt-yazi">Bir bölüm seç, sahneyi aç, Türkçeyi yerinde düzelt. Onaylı çeviri değişmez; önerin havuza düşer.</p>';
  if(son)ic+='<a class="devam cam" href="#/g/'+e(son.g)+'/'+son.i+'"><div><span>Kaldığın yer</span><br><strong>'+e(son.ad)+'</strong> · '+e(son.b)+'</div><span class="btn koyu kucuk" style="display:inline-grid;place-items:center">Devam et</span></a>';
  S.kat.bolumler.forEach(b=>{ic+='<div class="bolum-ad">'+e(b.ad)+'</div><div class="izgara">'+b.gruplar.map(g=>'<a class="kart cam" href="#/g/'+g.id+'/0"><div class="sayi">'+nf(g.satir)+'<small>satır</small></div><h3>'+e(g.ad)+'</h3><p>'+e(g.aciklama)+'</p>'+guvenBar(g.duzey,g.satir)+'</a>').join('')+'</div>'});
  ic+='<div class="lejant"><span><i class="nokta2"></i>Bağlam kaynakta kayıtlı</span><span><i class="nokta1"></i>Dolaylı (ortak ya da başka paketin notu, paket başlığı, anahtar öneki)</span><span><i class="nokta0"></i>Bağlam kaydı yok</span></div></main>';
  kabuk('ana',ic)}
/* ---------- veri ---------- */
async function grupAl(id){if(!S.grup[id])S.grup[id]=await(await fetch('veri/g/'+id+'.json')).json();return S.grup[id]}
async function parcaAl(id,c){const k=id+'-'+c;if(!S.parca[k])S.parca[k]=await(await fetch('veri/s/'+k+'.json')).json();return S.parca[k]}
const ETIKET={reg:'karakter grubu',role:'rol',st:'tutum',tmp:'deneyim',mood:'ruh hali',day:'gün',hour:'saat',world:'ortam',r1:'1. konuşan',r2:'2. konuşan',out:'çıkış',faction:'fraksiyon','güven':'güven'};
function kosulParca(c){return String(c||'').split('|').map(x=>x.trim()).filter(Boolean).map(x=>{const i=x.indexOf('=');return i<0?['',x]:[ETIKET[x.slice(0,i)]||x.slice(0,i),x.slice(i+1).replace(/,/g,', ')]})}
function duzeyYazi(g,c){const l=c[3];
  if(g.tur==='npc'){if(l===2)return['Sahne notu kayıtlı','Açıklama, bu satırların çevrildiği paketin sahne notundan ('+c[4]+') geliyor.'];if(l===1&&String(c[4]).charAt(0)==='+')return['Paketin genel notu','Bu sahneye özel not yok. Yalnızca çevrildiği paketin ('+String(c[4]).slice(1)+') genel notu kayıtlı.'];if(l===1)return String(c[4]).charAt(0)==='~'?['Başka paketin notu','Not, aynı olay adını taşıyan başka bir paket ('+String(c[4]).slice(1)+') için yazılmış. Bu satırlar için doğrulanmadı.']:['Ortak olay notu','Not, olay adına göre ortak listeden geldi. Bu satırlar için ayrıca doğrulanmadı.'];return['Sahne notu yok','Yalnızca olay adı ve koşul etiketleri kayıtlı. Sahneyi kaynakta doğrulayamadım.']}
  if(g.tur==='ui'){if(l===2)return['Dosya ve satır kayıtlı','Yalnızca metnin hangi Lua dosyasında ve satırında geçtiği kayıtlı. Ekrandaki yeri doğrulanmadı.'];if(l===1)return['Paket başlığına göre','Bu satır, çevrildiği paketin başlığına ('+c[4]+') göre gruplandı. Ekrandaki yeri kayıtlı değil.'];return['Bağlam kaydı yok','Bu satırın nerede göründüğü kaynakta kayıtlı değil. Sıra, dosyadaki sıradır.']}
  if(g.tur==='sandbox')return['Anahtar önekine göre','Ayarlar yalnızca anahtar adına göre gruplandı; seçenek, açıklaması ve değerleri aynı kartta durur.'];
  return['Bağlam kaydı yok','Bu dosya için bağlam kaydı tutulmuyor.']}
const YT=/\{[^{}]*\}|%\d*\$?[sdif]|<[A-Z][A-Z0-9_]*(?::[^>]*)?>|\\n|\[img[^\]]*\]/g;
function ytFark(a,b){const say=s=>{const m={};(String(s||'').match(YT)||[]).forEach(x=>m[x]=(m[x]||0)+1);return m};const x=say(a),y=say(b),f=[];Object.keys(Object.assign({},x,y)).forEach(k=>{if((x[k]||0)!==(y[k]||0))f.push(k)});return f}
const onerilerOf=k=>S.oneriler.filter(o=>o.anahtar===k&&o.hedef===W.g.hedef);
/* ---------- çalışma ekranı ---------- */
async function calisma(gid,i,odakKey){
  let g;try{g=await grupAl(gid)}catch(x){location.hash='#/';return}
  i=Math.max(0,Math.min(i,g.sahneler.length-1));const sh=g.sahneler[i];const p=(await parcaAl(gid,sh[2]))[String(i)];
  const taslak=LS.get('cm_taslak',{});
  W={gid:gid,g:g,i:i,sh:sh,c:p.c,r:p.r,goster:60,ara:'',sara:(W&&W.gid===gid?W.sara:''),odak:null,taslak:taslak};
  LS.set('cm_son',{g:gid,i:i,ad:g.ad,b:sh[0]});
  const lv=[...new Set(p.c.map(c=>c[3]))].sort().reverse();
  kabuk('ana','<div class="duzen"><aside class="yan cam"><header><a href="#/">‹ Bölümler</a><h2>'+e(g.ad)+'</h2><input class="alan" id="sara" placeholder="'+nf(g.sahneler.length)+' sahnede ara" value="'+e(W.sara)+'"></header><div class="liste" id="liste"></div></aside><main class="orta"><div class="iz">'+e(g.ad)+' · '+e(g.hedef)+'.json</div><h1>'+e(sh[0])+'</h1><div class="ust">'+lv.map(l=>'<span class="rozet l'+l+'">'+e(duzeyYazi(g,p.c.find(c=>c[3]===l))[0])+'</span>').join('')+'<span>'+nf(p.r.length)+' satır</span></div><p class="ipucu">'+e(g.iliski==='rastgele'?'Aynı koşul başlığı altındaki satırlar, o durumda rastgele seçilen ayrı sözlerdir. Birbirinin devamı gibi okuma.':g.tur==='npc'?'Bu satırların birbirini izleyip izlemediği kaynakta kayıtlı değil. Sıra, dosyadaki sıradır; konuşma sırası olarak doğrulanmadı.':'Satırlar dosyadaki sırayla listelenir.')+'</p><div class="arac"><input class="alan" id="ara" placeholder="Bu sahnede ara"><span><kbd>Ctrl</kbd> <kbd>Enter</kbd> kaydet ve ilerle · <kbd>Alt</kbd> <kbd>↓</kbd><kbd>↑</kbd> satır değiştir</span></div><div id="satirlar"></div></main><aside class="bag cam" id="bag"></aside></div>');
  $('#sara').oninput=ev=>{W.sara=ev.target.value;listeCiz()};$('#ara').oninput=ev=>{W.ara=ev.target.value;W.goster=60;satirCiz()};
  listeCiz();if(odakKey){const ix=p.r.findIndex(r=>r[0]===odakKey);if(ix>=W.goster)W.goster=ix+20}satirCiz(odakKey)}
function listeCiz(){const q=W.sara.toLocaleLowerCase('tr-TR'),out=[];let n=0,top=0;
  W.g.sahneler.forEach((s,i)=>{if(q&&s[0].toLocaleLowerCase('tr-TR').indexOf(q)<0)return;top++;if(n<250||i===W.i){n++;out.push('<a href="#/g/'+W.gid+'/'+i+'" class="'+(i===W.i?'acik':'')+'"><i class="nokta'+s[4]+'"></i><span>'+e(s[0])+'</span><em>'+nf(s[1])+'</em></a>')}});
  if(top>n)out.push('<div class="not">'+nf(top-n)+' sahne daha var. Daraltmak için yukarıdan ara.</div>');if(!top)out.push('<div class="not">Eşleşen sahne yok.</div>');
  const l=$('#liste');l.innerHTML=out.join('');const a=$('a.acik',l);if(a)a.scrollIntoView({block:'nearest'})}
function gorunen(){const q=W.ara.toLocaleLowerCase('tr-TR');return W.r.map((r,ix)=>ix).filter(ix=>!q||((W.r[ix][1]||'')+' '+W.r[ix][2]).toLocaleLowerCase('tr-TR').indexOf(q)>=0)}
function satirCiz(odakKey){const ixs=gorunen(),out=[];let onceki=-1;
  ixs.slice(0,W.goster).forEach(ix=>{const r=W.r[ix],c=W.c[r[3]];
    if(r[3]!==onceki&&W.c.length>1){onceki=r[3];const kp=kosulParca(c[1]);out.push('<div class="kosul">'+(kp.length?kp.map(k=>'<span class="chip">'+(k[0]?e(k[0])+': ':'')+'<b>'+e(k[1])+'</b></span>').join(''):'<span class="chip">koşul etiketi yok</span>')+(W.g.tur==='npc'&&c[0]?'<span class="chip">'+e(c[0])+'</span>':'')+'</div>')}
    const t=W.taslak[W.g.hedef+'|'+r[0]],os=onerilerOf(r[0]);
    const own=os.filter(o=>o.yazar===S.profil.id && o.gorulen_tr===r[2]).at(-1);
    out.push('<div class="satir'+(t!=null&&t!==r[2]?' degisti':'')+'" data-ix="'+ix+'"><div class="izler">'+[...new Set(os.map(o=>o.yazar))].map(y=>av(y,1)).join('')+'</div><div class="en'+(r[1]==null?' yok':'')+'">'+(r[1]==null?'İngilizce kaynağı yok':e(r[1]))+'</div><textarea rows="1" spellcheck="false" aria-label="Türkçe">'+e(t ?? own?.onerilen_tr ?? r[2])+'</textarea><small class="kayit-durumu" role="status">'+(own?'Havuzda kayıtlı önerin':'')+'</small><div class="alt"><input class="alan" placeholder="Gerekçe (isteğe bağlı)" maxlength="300"><button class="btn koyu" data-is="kaydet">Öneriyi kaydet</button><button class="btn" data-is="geri">Geri al</button><div class="uyari"></div></div></div>')});
  if(ixs.length>W.goster)out.push('<button class="btn daha" id="daha">'+nf(ixs.length-W.goster)+' satır daha göster</button>');if(!ixs.length)out.push('<p class="bos-not" style="padding:30px 20px">Eşleşen satır yok.</p>');
  const kap=$('#satirlar');kap.innerHTML=out.join('');$$('textarea',kap).forEach(boy);
  const d=$('#daha');if(d)d.onclick=()=>{W.goster+=120;const k=W.odak!=null?W.r[W.odak][0]:null;satirCiz(k)};
  kap.onpointerdown=ev=>{
    if(ev.pointerType!=='mouse'||ev.button!==0||ev.target.closest('input,button,textarea'))return;
    const row=ev.target.closest('.satir');
    if(row){ev.preventDefault();$('textarea',row).focus({preventScroll:true})}
  };
  kap.addEventListener('focusin',satiraOdaklan);
  kap.onclick=ev=>{const s=ev.target.closest('.satir');if(!s)return;const is=ev.target.dataset&&ev.target.dataset.is;if(is==='kaydet')kaydet(+s.dataset.ix);else if(is==='geri')geriAl(+s.dataset.ix);else if(!ev.target.closest('.alt')&&ev.target.tagName!=='TEXTAREA')$('textarea',s).focus()};
  kap.oninput=ev=>{if(ev.target.tagName!=='TEXTAREA')return;boy(ev.target);const s=ev.target.closest('.satir'),r=W.r[+s.dataset.ix],k=W.g.hedef+'|'+r[0];if(ev.target.value===r[2])delete W.taslak[k];else W.taslak[k]=ev.target.value;LS.set('cm_taslak',W.taslak);s.classList.toggle('degisti',ev.target.value!==r[2]);uyar(s,r)};
  kap.onkeydown=ev=>{const s=ev.target.closest('.satir');if(!s)return;if((ev.ctrlKey||ev.metaKey)&&ev.key==='Enter'){ev.preventDefault();kaydet(+s.dataset.ix)}else if(ev.altKey&&(ev.key==='ArrowDown'||ev.key==='ArrowUp')){ev.preventDefault();komsu(s,ev.key==='ArrowDown'?1:-1)}};
  let hedef=odakKey?$$('.satir',kap).find(s=>W.r[+s.dataset.ix][0]===odakKey):null;hedef=hedef||$('.satir',kap);
  if(hedef){odakla(+hedef.dataset.ix);if(odakKey){$('textarea',hedef).focus({preventScroll:true});hedef.scrollIntoView({block:'center'})}}else $('#bag').innerHTML='<p class="bos-not">Satır seçilmedi.</p>'}
function boy(t){t.style.height='auto';t.style.height=t.scrollHeight+'px'}
function satiraOdaklan(ev){
  const row=ev.target.closest('.satir');
  if(row)odakla(Number(row.dataset.ix));
}
function uyar(s,r){const f=ytFark(r[1]!=null?r[1]:r[2],$('textarea',s).value);$('.uyari',s).textContent=f.length?'Yer tutucu farkı: '+f.join('  ')+' (İngilizcedeki sayıyla uyuşmuyor)':''}
function komsu(s,yon){let n=s;do{n=yon>0?n.nextElementSibling:n.previousElementSibling}while(n&&!n.classList.contains('satir'));if(n){$('textarea',n).focus({preventScroll:true});n.scrollIntoView({block:'center',behavior:'smooth'})}return !!n}
function odakla(ix){if(W.odak===ix&&$('.satir.odak'))return;W.odak=ix;$$('.satir.odak').forEach(x=>x.classList.remove('odak'));const s=$('.satir[data-ix="'+ix+'"]');if(s){s.classList.add('odak');boy($('textarea',s));uyar(s,W.r[ix])}bagCiz(ix)}
function bagCiz(ix){const r=W.r[ix],c=W.c[r[3]],g=W.g,dy=duzeyYazi(g,c),kp=kosulParca(c[1]);
  let h='<section><h4>Bağlam</h4><span class="rozet l'+c[3]+'">'+e(dy[0])+'</span>'+(c[2]?'<p>'+e(c[2])+'</p>':'')+'<p class="'+(c[3]<2?'uy':'')+'" style="font-size:13px">'+e(dy[1])+'</p>';
  const pk=g.paketler&&g.paketler[c[4]];if(pk&&pk[1])h+='<details style="margin-top:10px"'+(String(c[4]).charAt(0)==='+'?' open':'')+'><summary>Paketin genel notu</summary><p>'+e(pk[1])+'</p></details>';h+='</section>';
  if(kp.length)h+='<section><h4>'+(g.tur==='npc'?'Kim, hangi koşulda':'Kayıt')+'</h4><dl>'+kp.map(k=>'<dt>'+e(k[0]||'etiket')+'</dt><dd>'+e(k[1])+'</dd>').join('')+'</dl></section>';
  if(g.tur==='npc'){const kd=W.r.filter(x=>x[3]===r[3]&&x!==r);
    if(g.iliski==='rastgele')h+='<section><h4>Bu durumda duyulabilecek diğer sözler</h4>'+(kd.length?kd.slice(0,5).map(x=>'<p>'+e(x[2])+'</p>').join('')+(kd.length>5?'<p class="bos-not">ve '+nf(kd.length-5)+' söz daha</p>':''):'<p class="bos-not">Bu koşulda başka söz kayıtlı değil.</p>')+'</section>';
    else h+='<section><h4>Aynı koşul kaydındaki satırlar</h4><p class="bos-not">'+nf(kd.length)+' satır daha aynı dosya ve koşulu paylaşıyor. Konuşma sırası kaynakta kayıtlı değil.</p></section>'}
  h+='<section><h4>Adres</h4><dl><dt>hedef</dt><dd><code>onayli/'+e(g.hedef)+'.json</code></dd><dt>anahtar</dt><dd><code>'+e(r[0])+'</code></dd>'+(c[0]?'<dt>kaynak</dt><dd><code>'+e(c[0])+'</code></dd>':'')+'<dt>katalog</dt><dd><code>'+e(S.kat.surum)+'</code></dd></dl></section>';
  const os=onerilerOf(r[0]);h+='<section><h4>Bu satıra gelen öneriler</h4>'+(os.length?os.map(o=>'<div class="oneri"><header>'+av(o.yazar,1)+'<b>'+e(adi(o.yazar))+'</b><span>'+new Date(o.olusturma).toLocaleDateString('tr-TR')+'</span></header>'+e(o.onerilen_tr)+(o.gerekce?'<q>'+e(o.gerekce)+'</q>':'')+(o.gorulen_tr!==r[2]?'<q style="color:var(--amber)">Bu öneri yazılırken Türkçe farklıydı: '+e(o.gorulen_tr)+'</q>':'')+'</div>').join(''):'<p class="bos-not">Henüz öneri yok.</p>')+'</section>';
  $('#bag').innerHTML=h}
function geriAl(ix){const s=$('.satir[data-ix="'+ix+'"]'),r=W.r[ix],t=$('textarea',s);t.value=r[2];delete W.taslak[W.g.hedef+'|'+r[0]];LS.set('cm_taslak',W.taslak);s.classList.remove('degisti');boy(t);uyar(s,r);t.focus()}
async function kaydet(ix){const s=$('.satir[data-ix="'+ix+'"]'),r=W.r[ix],c=W.c[r[3]],val=$('textarea',s).value,ger=$('.alt input',s).value.trim();
  const onceki=onerilerOf(r[0]).filter(o=>o.yazar===S.profil.id && o.gorulen_tr===r[2]).at(-1);
  if(val===(onceki?.onerilen_tr ?? r[2]) && !ger){toast(onceki?'Bu önerin zaten havuzda':'Öneri için Türkçeyi düzenle veya gerekçe yaz');return}
  if(!val.trim()){toast('Boş öneri kaydedilmez');return}
  const kayit={yazar:S.profil.id,hedef:W.g.hedef,anahtar:r[0],katalog_surumu:S.kat.surum,en:r[1],gorulen_tr:r[2],onerilen_tr:val,gerekce:ger||null,baglam:{grup:W.gid,sahne:W.sh[0],kaynak:c[0]||null,kosul:c[1]||null,baglam_duzeyi:c[3]}};
  const b=$('[data-is=kaydet]',s);if(b.disabled)return; b.disabled=true;
  try{let tam;if(UZAK){tam=(await db('oneriler',{method:'POST',body:JSON.stringify([kayit])}))[0]}else{tam=Object.assign({id:uuid(),olusturma:new Date().toISOString(),yazar:S.profil.id},kayit)}
    S.oneriler.push(tam);if(!UZAK)LS.set('cm_yerel_oneriler',S.oneriler);
    delete W.taslak[W.g.hedef+'|'+r[0]];LS.set('cm_taslak',W.taslak);s.classList.add('tamam');$('.izler',s).innerHTML=[...new Set(onerilerOf(r[0]).map(o=>o.yazar))].map(y=>av(y,1)).join('');
    if(!s.isConnected)return; $('.kayit-durumu',s).textContent='Havuzda kayıtlı önerin'; $('.alt input',s).value='';
    const nl=$('.nav a[href="#/havuz"]');if(nl)nl.textContent='Havuz · '+nf(S.oneriler.length);toast('Öneri havuza eklendi');W.odak=null;if(!komsu(s,1))odakla(ix)}
  catch(x){$('.uyari',s).textContent='Kaydedilemedi: '+x.message;toast('Öneri kaydedilemedi')}b.disabled=false}
/* ---------- havuz ---------- */
function cakisma(){const m={};S.oneriler.forEach(o=>{const k=o.hedef+'|'+o.anahtar;m[k]=(m[k]||0)+1});return m}
function disaAktar(){const ck=cakisma();return{bicim:'ceviri-masasi/oneriler@2',indirme:new Date().toISOString(),sitedeki_katalog_surumu:S.kat.surum,ozet:{oneri:S.oneriler.length,satir:Object.keys(ck).length,birden_fazla_oneri_alan_satir:Object.values(ck).filter(n=>n>1).length},oneriler:S.oneriler.map(o=>({id:o.id,hedef:o.hedef,anahtar:o.anahtar,katalog_surumu:o.katalog_surumu,en:o.en,gorulen_tr:o.gorulen_tr,onerilen_tr:o.onerilen_tr,gerekce:o.gerekce||null,yazar:{id:o.yazar,ad:adi(o.yazar)},olusturma:o.olusturma,ayni_satira_oneri_sayisi:ck[o.hedef+'|'+o.anahtar],baglam:o.baglam||null}))}}
window.CM={disaAktar:disaAktar,durum:S};
let HF='hepsi';
function havuz(){const ck=cakisma();let l=S.oneriler.slice().reverse();if(HF==='cakisan')l=l.filter(o=>ck[o.hedef+'|'+o.anahtar]>1);else if(HF!=='hepsi')l=l.filter(o=>o.yazar===HF);
  const yazarlar=[...new Set(S.oneriler.map(o=>o.yazar))];
  let ic='<main class="sayfa" style="max-width:920px"><div class="baslik-satir"><h1>Öneri havuzu</h1><button class="btn" id="yenile">Yenile</button><button class="btn koyu" id="indir"'+(S.oneriler.length?'':' disabled')+'>JSON indir</button></div><div class="suz"><button data-f="hepsi" class="'+(HF==='hepsi'?'acik':'')+'">Hepsi · '+nf(S.oneriler.length)+'</button>'+yazarlar.map(y=>'<button data-f="'+e(y)+'" class="'+(HF===y?'acik':'')+'">'+av(y,1)+e(adi(y))+' · '+nf(S.oneriler.filter(o=>o.yazar===y).length)+'</button>').join('')+'<button data-f="cakisan" class="'+(HF==='cakisan'?'acik':'')+'">Aynı satıra birden fazla öneri · '+nf(Object.values(ck).filter(n=>n>1).length)+'</button></div>';
  ic+=l.length?l.slice(0,300).map(o=>'<article class="hk cam"><div class="en">'+(o.en==null?'<i>İngilizce kaynağı yok</i>':e(o.en))+'</div><div class="eski">'+e(o.gorulen_tr)+'</div><div class="oneri" style="background:none;padding:0">'+e(o.onerilen_tr)+'</div>'+(o.gerekce?'<p style="margin:8px 0 0;color:var(--ink2);font-size:14px">'+e(o.gerekce)+'</p>':'')+'<footer>'+av(o.yazar,1)+'<span style="font-size:13.5px;font-weight:600">'+e(adi(o.yazar))+'</span><span class="kod">'+e(o.hedef)+' · '+e(o.anahtar)+'</span><span style="flex:1"></span>'+(ck[o.hedef+'|'+o.anahtar]>1?'<span class="rozet l1">bu satıra '+ck[o.hedef+'|'+o.anahtar]+' öneri</span>':'')+(o.katalog_surumu!==S.kat.surum?'<span class="rozet uy">başka katalog sürümü: '+e(o.katalog_surumu)+'</span>':'')+(o.baglam&&o.baglam.grup?'<button class="btn kucuk" data-git="'+e(o.id)+'">Sahneye git</button>':'')+'</footer></article>').join('')+(l.length>300?'<p class="bos-not">İlk 300 öneri gösteriliyor. Tamamı JSON dosyasında.</p>':''):'<div class="hk cam bos-not">Burada henüz öneri yok.</div>';
  kabuk('havuz',ic+'</main>');
  $$('.suz button').forEach(b=>b.onclick=()=>{HF=b.dataset.f;havuz()});
  $('#indir').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(disaAktar(),null,1)],{type:'application/json'}));a.download='oneriler-'+S.kat.surum+'-'+new Date().toISOString().slice(0,10)+'.json';a.click();toast('JSON indirildi')};
  $('#yenile').onclick=async()=>{if(UZAK){try{await profilYukle();await havuzYukle();toast('Havuz güncellendi')}catch(x){toast(x.message)}}havuz()};
  $$('[data-git]').forEach(b=>b.onclick=async()=>{const o=S.oneriler.find(x=>x.id===b.dataset.git),g=await grupAl(o.baglam.grup),i=g.sahneler.findIndex(s=>s[0]===o.baglam.sahne);if(i<0){toast('Bu sahne güncel katalogda yok');return}location.hash='#/g/'+o.baglam.grup+'/'+i+'/'+encodeURIComponent(o.anahtar)})}
/* ---------- kapsam ---------- */
function kapsam(){const k=S.kat,es=k.eslesmeyen;
  let ic='<main class="sayfa" style="max-width:1000px"><div class="baslik-satir"><h1>Kapsam</h1><span class="kod">katalog '+e(k.surum)+' · '+e(k.uretim)+'</span></div><div class="tablo cam"><h3>Hedef dosyalar</h3><p>Onaylı çevirideki her kayıt kataloğa girdi mi?</p><table><tr><th>Hedef dosya</th><th>Onaylı</th><th>Katalogda</th><th>Dışarıda</th><th>İngilizcesi yok</th><th>Türkçesi yok</th></tr>'+k.kapsam.map(r=>'<tr><td><code>onayli/'+e(r.hedef)+'.json</code></td><td>'+nf(r.onayli)+'</td><td>'+nf(r.katalogda)+'</td><td>'+nf(r.disarida)+'</td><td>'+nf(r.en_yok)+'</td><td>'+nf(r.tr_yok)+'</td></tr>').join('')+'</table></div>';
  ic+='<div class="tablo cam"><h3>Bağlam güveni</h3><p>Her bölümde kaç satırın bağlamı hangi kesinlikte.</p><table><tr><th>Bölüm</th><th>Satır</th><th>Kaynakta kayıtlı</th><th>Dolaylı</th><th>Kayıt yok</th></tr>'+k.bolumler.map(b=>b.gruplar.map(g=>'<tr><td>'+e(g.ad)+'</td><td>'+nf(g.satir)+'</td><td>'+nf(g.duzey['2']||0)+'</td><td>'+nf(g.duzey['1']||0)+'</td><td>'+nf(g.duzey['0']||0)+'</td></tr>').join('')).join('')+'</table></div>';
  const a=Object.keys(es.en_var_tr_yok||{}),b=Object.keys(es.tr_var_en_yok||{});
  ic+='<div class="tablo cam"><h3>Eşleşmeyenler</h3>'+(a.length?a.map(h=>'<p><b>'+e(h)+'</b>: İngilizcesi olup onaylı Türkçesi olmayan '+es.en_var_tr_yok[h].length+' anahtar. '+es.en_var_tr_yok[h].slice(0,12).map(x=>'<code>'+e(x[1])+'</code>').join(', ')+'</p>').join(''):'')+(b.length?b.map(h=>'<p><b>'+e(h)+'</b>: İngilizce kaynağı olmayan '+es.tr_var_en_yok[h].length+' onaylı satır. Katalogda yalnızca Türkçesiyle duruyor.</p>').join(''):'')+(!a.length&&!b.length?'<p>Eşleşmeyen kayıt yok.</p>':'')+'</div></main>';
  kabuk('kapsam',ic)}
oturumuBaslat();
})();
