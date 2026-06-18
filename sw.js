// Service Worker 廃止 — 古いキャッシュを全削除して自分を解除
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.clients.matchAll({type:'window'}))
      .then(clients => clients.forEach(c => c.navigate(c.url)))
  );
});
