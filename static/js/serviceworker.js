// // Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py
// let staticCacheName = "django-pwa-v" + new Date().getTime();
// let filesToCache = [
//     '/',
//     '/offline/',
//     '/static/css/django-pwa-app.css',
//     '/static/images/icons/icon-72x72.png',
//     '/static/images/icons/icon-96x96.png',
//     '/static/images/icons/icon-128x128.png',
//     '/static/images/icons/icon-144x144.png',
//     '/static/images/icons/icon-152x152.png',
//     '/static/images/icons/icon-192x192.png',
//     '/static/images/icons/icon-384x384.png',
//     '/static/images/icons/icon-512x512.png',
//     '/static/images/icons/splash-640x1136.png',
//     '/static/images/icons/splash-750x1334.png',
//     '/static/images/icons/splash-1242x2208.png',
//     '/static/images/icons/splash-1125x2436.png',
//     '/static/images/icons/splash-828x1792.png',
//     '/static/images/icons/splash-1242x2688.png',
//     '/static/images/icons/splash-1536x2048.png',
//     '/static/images/icons/splash-1668x2224.png',
//     '/static/images/icons/splash-1668x2388.png',
//     '/static/images/icons/splash-2048x2732.png'
// ];

// // Cache on install
// self.addEventListener('install', event => {
//     this.skipWaiting();
//     event.waitUntil(
//         caches.open(staticCacheName)
//             .then(cache => {
//                 return cache.addAll(filesToCache);
//             })
//     )
// });

// // Clear cache on activate
// self.addEventListener('activate', event => {
//     event.waitUntil(
//         caches.keys().then(cacheNames => {
//             return Promise.all(
//                 cacheNames
//                     .filter(cacheName => (cacheName.startsWith("django-pwa-")))
//                     .filter(cacheName => (cacheName !== staticCacheName))
//                     .map(cacheName => caches.delete(cacheName))
//             );
//         })
//     );
// });

// // Serve from Cache
// self.addEventListener('fetch', event => {
//     let requestUrl = new URL(event.request.url);
// 	if (requestUrl.origin === location.origin) {
// 		if (requestUrl.pathname === '/') {
// 			event.respondWith(caches.match(''));
// 			return;
// 		}
// 	}
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 return response || fetch(event.request);
//             })
//             .catch(() => {
//                 return caches.match('/offline/');
//             })
//     )
// });


const manifest = self.__WB_MANIFEST;
if (manifest) {
  // do nothing
}

// https://web.dev/offline-fallback-page/
const CACHE_NAME = 'offline';
const FALLBACK_HTML_URL = '/offline/';
self.addEventListener('install',  (event) => {
  event.waitUntil(
    // Setting {cache: 'reload'} in the new request will ensure that the
    // response isn't fulfilled from the HTTP cache; i.e., it will be from
    // the network.
    caches.open(CACHE_NAME)
      .then((cache) => cache.add(
        new Request(FALLBACK_HTML_URL, { cache: "reload" })
      ))
  );

  // Force the waiting service worker to become the active service worker.
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  // Tell the active service worker to take control of the page immediately.
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
      .catch(() => {
        return caches.match(FALLBACK_HTML_URL);
      })
  );
});



// var staticCacheName = 'djangopwa-v1';

// var filesToCache = [
//     '/',
//     '/offline/',
// ];

// // Cache on install
// self.addEventListener("install", event => {
//     this.skipWaiting();
//     event.waitUntil(
//         caches.open(staticCacheName)
//             .then(cache => {
//                 return cache.addAll(filesToCache);
//             })
//     )
// });

// // Clear cache on activate
// self.addEventListener('activate', event => {
//     event.waitUntil(
//         caches.keys().then(cacheNames => {
//             return Promise.all(
//                 cacheNames
//                     .filter(cacheName => (cacheName.startsWith("djangopwa-v1")))
//                     .filter(cacheName => (cacheName !== staticCacheName))
//                     .map(cacheName => caches.delete(cacheName))
//             );
//         })
//     );
// });

// // Serve from Cache
// self.addEventListener("fetch", event => {
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 return response || fetch(event.request);
//             })
//             .catch(() => {
//                 return caches.match('/offline');
//             })
//     )
// });
