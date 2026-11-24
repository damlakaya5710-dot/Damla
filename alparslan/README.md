# Fizyoterapist Alparslan Erişti: "Ağrı burada, peki ya kaynağı?"

`output/alparslan_agri_kaynagi.mp4`: 1080×1920 (9:16, Reels/TikTok/Shorts), 30 fps, 20 sn, H.264 + AAC.

## Görsel dil
Marka afişiyle aynı estetik: krem zemin ve adaçayı yeşili kavisler, adaçayı yeşili/bej tonlarda yarı saydam kas sistemi,
sırttan seçilen omurga, beden etrafında akan ince altın hatlar ve Cormorant Garamond serif tipografi.
Beden, tek tek modellenmiş kas kitlelerinin (trapez, deltoid, latissimus, gluteus, kuadriseps vb.) yumuşak birleşimiyle
tek parça bir ağ olarak üretilir. Her kas, kendi lif yönünde dokulanır ve kas sınırları gölgelenir. İskelet, bedenin içinden görünür.

## Akış
| Süre | Görüntü | Yazı |
|---|---|---|
| 0–3 sn | Altın bir tarama çizgisi ayaktan başa kas sistemini ortaya çıkarır (arkadan 3/4 açı). Sağ omuz kırmızı nabız gibi atar. | "Ağrı burada." |
| 3–8.3 sn | Kamera omuz ile boyun arasına yaklaşır. Beden saydamlaşır, iskelet ile kas ve sinir hatları görünür. Omuz kuşağı ve üst torakal omurga vurgulanır. | "*Peki ya kaynağı?*" |
| 8.3–12.6 sn | Kamera uzaklaşır. Altın fasyal zincirler ve sarmallar tüm bedeni sarar. Leğen, sakrum, ayaklar, kafatası ve çene eklemi yanar. | "Vücudunuz *bir bütündür.* / Osteopatik bakış açısı." |
| 12.9–15.9 sn | Krem perde. | "Ağrının olduğu yer, *kaynağı olmayabilir.*" |
| 16.3–20 sn | Afiş düzeni: üstte marka, ortada altın hatlarla beden, altta iletişim satırı. | FİZYOTERAPİST · ALPARSLAN ERİŞTİ · uzmanlıklar · Ayvalık, Balıkesir, No 456 İş Merkezi, D:27 · +90 530 852 49 95 |

## Yeniden üretme
```bash
python3 audio.py output/muzik.wav                                    # fon müziği (tamamen sentez, telifsiz)
node render.js /tmp/kareler output/muzik.wav output/video.mp4        # kareler + MP4
node stills.js /tmp/kareler 2 6 10 14 18                             # seçili anların görüntüleri
```
Tarayıcıda önizleme: `node server.js`, ardından `http://127.0.0.1:8080/scene.html?play=1` adresini açın.

## Özelleştirme
- **Marka metinleri ve renkleri:** `scene.html` içindeki `BRAND` nesnesi (unvan, ad, uzmanlıklar, adres, telefon, renkler).
- **Logo:** Gerçek logoyu `overlay()` fonksiyonunun "marka" bölümünde `ctx.drawImage(...)` ile ekleyebilirsiniz.
- **Ağrı bölgesi:** `PAIN` sabiti (ör. diz için `V(.1, .5, .03)`). Bu durumda bağlantı hatlarının da yeniden düzenlenmesi gerekir.
- **Zamanlama:** Kamera için `KF` dizisi, sahne durumu için `update(t)` fonksiyonu. Müzik vuruşları `audio.py` içinde aynı saniyelere göre ayarlıdır.

## Not
Yazı tipi: Cormorant Garamond (SIL Open Font License, `fonts/`). Telefon ve konum simgeleri Material Icons'tan alındı (Apache 2.0).
