const CACHE="yogalign-v2";
const SHELL=["./","index.html","manifest.json","icons/icon-192.png","icons/icon-512.png",
"img/Mountain_Yoga.png","img/Upward_Salute.png","img/Warior_siluet.png","img/Reverse_Warrior.png","img/Extended_Side_Angle.png",
"img/Triangle_Yoga.png","img/Goddess_Pose.png","img/Tree_Pose.png","img/Half_Moon.png","img/Standing_Side_Bend.png"];
self.addEventListener("install",e=>{
  e.waitUntil(caches.open(CACHE).then(c=>Promise.allSettled(SHELL.map(u=>c.add(u)))).then(()=>self.skipWaiting()));
});
self.addEventListener("activate",e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
/* Network-first: selalu ambil versi terbaru, pakai cache kalau offline */
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET") return;
  e.respondWith(
    fetch(e.request).then(r=>{
      if(r&&(r.ok||r.type==="opaque")){const cp=r.clone();caches.open(CACHE).then(c=>c.put(e.request,cp)).catch(()=>{});}
      return r;
    }).catch(()=>caches.match(e.request).then(m=>m||caches.match("index.html")))
  );
});
