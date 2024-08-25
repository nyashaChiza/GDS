const CACHE_NAME = 'gds-pwa-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/styles.css',
  '/static/js/main.js',
  '/static/images/favicon.png',
  '/static/images/logo-dark-small2x.png',
];

// Install Event
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(urlsToCache.map((url) => new Request(url, { cache: "reload" })));
      })
      .catch((error) => {
        console.error('Failed to cache resources during installation:', error);
        // Log each URL that fails to cache
        urlsToCache.forEach((url) => {
          fetch(url).catch((fetchError) => {
            console.error(`Failed to fetch ${url}:`, fetchError);
          });
        });
      })
  );
});

// Fetch Event
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response; // Return cached resource
        }
        return fetch(event.request).then((networkResponse) => {
          // Cache the new resource and return it
          return caches.open(CACHE_NAME).then((cache) => {
            if (event.request.url.startsWith('http')) {
              cache.put(event.request, networkResponse.clone());
            }
            return networkResponse;
          });
        });
      }).catch((error) => {
        console.error('Failed to fetch resource:', error);
        // Optionally, return a fallback page or resource here
      })
  );
});

// Activate Event
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log(`Deleting old cache: ${cacheName}`);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
