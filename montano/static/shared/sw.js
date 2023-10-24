self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open('my-cache-name').then(function(cache) {
        return cache.addAll([
          '/',
          // '/static/images/icon.png', // Add all the files you want to cache
          // Add other assets that need to be cached
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
  });