# Alparslan: "Ağrı burada, peki ya kaynağı?"

`output/alparslan_agri_kaynagi.mp4`: 1080×1920 (9:16, Reels/TikTok/Shorts), 30 fps, 19 sn, H.264 + AAC.

## Akış
| Süre | Görüntü | Yazı |
|---|---|---|
| 0–3 sn | Karanlıktan yarı saydam 3B beden ve iskelet belirir. Sağ omuz kırmızı ışıkla nabız gibi atar. | "Ağrı burada." |
| 3–8.3 sn | Kamera omuz ile boyun arasına yaklaşır ve arkaya doğru döner. Kas lifleri (trapez, levator, rhomboid, göğüs, deltoid) ile sinir yolları (brakiyal pleksus) tek tek çizilir. Bağlantılar yalnızca boyuna değil sırta, göğse ve kola da eşit ağırlıkla uzanır. | "Peki ya kaynağı?" |
| 8.3–12.6 sn | Kamera yavaşça uzaklaşıp bedenin etrafında döner. Omuzdan tüm bedene miyofasyal zincirler açılır: sırt, bel, karşı kalça, diz, ayak, çene ve karşı kol. Bedenin pek çok noktasında olası kaynak ışıkları yanar, sinyaller her yerden omuza doğru akar. Kırmızı ağrı, ağın bir parçasına dönüşür. | — |
| 12.9–16.1 sn | Sahne kararır. | "Ağrının olduğu yer, **kaynağı olmayabilir.**" |
| 16.5–19 sn | Beden silikleşir, marka belirir. | **ALPARSLAN** + slogan |

Boyun yalnızca örnek olarak kullanılır. Hiçbir aşamada tek kaynak gibi vurgulanmaz: yakın planda bile sırt, göğüs ve kol bağlantıları aynı anda açılır. Geniş planda boyundaki nokta, diğer on bir noktadan farksızdır.

## Yeniden üretme
```bash
python3 audio.py output/muzik.wav                                    # fon müziği (tamamen sentez, telifsiz)
node render.js /tmp/kareler output/muzik.wav output/video.mp4        # kareler + MP4
node stills.js /tmp/kareler 2 6 10 14 18                             # seçili anların görüntüleri
```
Tarayıcıda önizleme: `node server.js`, ardından `http://127.0.0.1:8080/scene.html?play=1` adresini açın.

## Özelleştirme
- **Marka adı / slogan / hesap adı:** `scene.html` içindeki `BRAND` nesnesi. Slogan şu an geçici bir metin: `BÜTÜNCÜL BAKIŞ · KALICI ÇÖZÜM`.
- **Logo:** Gerçek logoyu `overlay()` fonksiyonunun "marka" bölümünde `ctx.drawImage(...)` ile ekleyebilirsiniz.
- **Ağrı bölgesi:** `PAIN` sabiti (ör. diz için `V(.1, .5, .03)`). Bu durumda bağlantı hatlarının da yeniden düzenlenmesi gerekir.
- **Zamanlama:** Kamera için `KF` dizisi, sahne durumu için `update(t)` fonksiyonu. Müzik vuruşları `audio.py` içinde aynı saniyelere göre ayarlıdır.

## Not
Anatomi prosedürel ve stilize bir modeldir (yarı saydam "x-ray" estetiği). Fotogerçekçi bir anatomi için lisanslı bir GLB modeli
(ör. Zygote, TurboSquid) `GLTFLoader` ile sahneye yüklenebilir. Kamera, ışık, bağlantı hatları ve yazı katmanı olduğu gibi kullanılmaya devam eder.
