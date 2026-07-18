const C="sk-v5";
self.addEventListener("install",e=>self.skipWaiting());
self.addEventListener("activate",e=>self.clients.claim());
self.addEventListener("fetch",function(e){
  e.respondWith(fetch(e.request).then(function(r){
    try{ if(e.request.method==="GET"){ const cp=r.clone(); caches.open(C).then(c=>c.put(e.request,cp)); } }catch(_){}
    return r;
  }).catch(function(){ return caches.match(e.request); }));
});
