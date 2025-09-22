const CACHE_NAME = 'daily-arxiv-v1';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/css/styles.css',
  '/css/settings.css',
  '/css/statistic.css',
  '/js/app.js',
  '/assets/logo2-removebg-preview.png',
  '/assets/logo2-white.png',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/settings.html',
  '/statistic.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => {
          return cacheName.startsWith('daily-arxiv-') &&
                 cacheName !== CACHE_NAME;
        }).map(cacheName => caches.delete(cacheName))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    // Navigation requests: network-first strategy
    event.respondWith(
      fetch(event.request)
        .catch(() => caches.match(event.request))
        .catch(() => caches.match('/'))
    );
  } else {
    // Other requests: cache-first strategy
    event.respondWith(
      caches.match(event.request)
        .then(response => response || fetch(event.request))
    );
  }
});
