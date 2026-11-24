# Fzt. Alparslan Erişti: Cumartesi Story Şablonu

`output/cumartesi_story.png`: 1080×1920 (9:16), her cumartesi tekrar kullanılabilecek zamansız şablon.
`output/cumartesi_story_guvenli_alan.png`: aynı tasarım, Instagram güvenli alanları (üst 250 px, alt 340 px)
ve bağlantı çıkartması için boş bırakılan alan işaretli hâli. Bu dosya yalnızca kontrol içindir, paylaşılmaz.

## Tasarım
- **Renkler:** kırık beyaz `#F3F0E8`, antrasit `#1D201E`, koyu yeşil `#2E4A3B`, yeşil `#55735F`, adaçayı `#9FB5A1`
  (gerçek kurumsal yeşil kodları `story.html` başındaki `:root` değişkenlerinden değiştirilebilir).
- **Yazı karakterleri:** Cormorant Garamond (ana başlık), Manrope (isim, alanlar, bilgiler). Fontlar `fonts/` içinde, internet gerekmez.
- **Arka plan:** sağda omurgayı ve beden çizgisini çağrıştıran, düşük opaklıkta soyut çizgiler ve yumuşak yeşil geçiş.
- **Bağlantı alanı:** Instagram kullanıcı adının altında, yaklaşık y = 1395–1560 px arası boş. Bağlantı çıkartması buraya konur.

## Yeniden üretme
```bash
node story/render.js
```
Metin veya saat değişikliği için `story.html` düzenlenip komut tekrar çalıştırılır.
