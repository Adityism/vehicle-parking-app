self.addEventListener('install', event => {
 event.waitUntil(
   caches.open('static-v1').then(cache => {
     return cache.addAll([
       '/',
       '/index.html',
       '/favicon.ico',
       '/manifest.json',
       '/src/assets/main.css',
       '/src/assets/base.css',
     ])
   })
 )
})

self.addEventListener('fetch', (event) => {
 if (event.request.url.includes('/api/') || event.request.url.includes('localhost:5009')) {
   return;
 }
 
 event.respondWith(
   caches.match(event.request).then(response => {
     return response || fetch(event.request)
   })
 );
})
