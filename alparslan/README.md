# Fizyoterapist Alparslan Erişti: "Ağrı burada, peki ya kaynağı?"

`output/alparslan_agri_kaynagi.mp4`: 1080×1920 (9:16, Reels/TikTok/Shorts), 30 fps, 19 sn, H.264 + AAC.

## Akış
| Süre | Görüntü | Yazı |
|---|---|---|
| 0–3 sn | Ayaktan başa yükselen bir tarama çizgisi anatomik iskeleti ve yarı saydam bedeni ortaya çıkarır. Kaburga kafesi nefes alır. Sağ omuz kırmızı ışıkla nabız gibi atar, baş ağrıdan hafifçe uzaklaşır. | "Ağrı burada." |
| 3–8.3 sn | Kamera omuz ile boyun arasına yaklaşır ve arkaya döner. Kas lifleri ve sinir yolları çizilir. Omuz kuşağı (köprücük, kürek kemiği, ilk kaburgalar) ile üst torakal omurga sıcak bir ışıkla vurgulanır. | "Peki ya kaynağı?" |
| 8.3–12.6 sn | Kamera uzaklaşıp bedenin etrafında döner. Miyofasyal zincirler tüm bedene açılır, sinyaller her yerden omuza akar. **Osteopatik vurgu:** leğen, sakrum, sakroiliak eklem, kalçalar, ayaklar, kafatası ve çene eklemi yanar. | "OSTEOPATİK BAKIŞ · Beden bir bütündür." |
| 12.9–15.9 sn | Sahne kararır. | "Ağrının olduğu yer, **kaynağı olmayabilir.**" |
| 16.2–19 sn | Bedenden yayılan ışık, marka kimliğindeki krem/adaçayı yeşili karta dönüşür. | FİZYOTERAPİST · **ALPARSLAN ERİŞTİ** · **Osteopati** \| Manuel Terapi · Psikonöroimmünoloji \| Klinik Pilates |

Boyun yalnızca örnek olarak kullanılır. Hiçbir aşamada tek kaynak gibi vurgulanmaz: yakın planda sırt, göğüs, kol ve torakal omurga da aynı anda öne çıkar. Geniş planda ise vurgu bedenin bütününe yayılır.

## İskelet
Kafatası (göz çukurları, elmacık kemiği, dişler, alt çene, çene eklemi), 24 omur ve diskleri (gövde, arka kemer, çıkıntılar), 12 çift kaburga, kıkırdak ve sternum,
köprücük kemiği, spinalı kürek kemiği, epifizli uzun kemikler (humerus, radius/ulna, femur, tibia/fibula), leğen kemiği (iliak kanatlar, sakrum, pubis/iskium), el ve ayak kemikleri.

## Yeniden üretme
```bash
python3 audio.py output/muzik.wav                                    # fon müziği (tamamen sentez, telifsiz)
node render.js /tmp/kareler output/muzik.wav output/video.mp4        # kareler + MP4
node stills.js /tmp/kareler 2 6 10 14 18                             # seçili anların görüntüleri
```
Tarayıcıda önizleme: `node server.js`, ardından `http://127.0.0.1:8080/scene.html?play=1` adresini açın.

## Özelleştirme
- **Marka metinleri ve renkleri:** `scene.html` içindeki `BRAND` nesnesi (unvan, ad, uzmanlık satırları, hesap adı, krem/yeşil tonları).
- **Logo:** Gerçek logoyu `overlay()` fonksiyonunun "marka" bölümünde `ctx.drawImage(...)` ile ekleyebilirsiniz.
- **Ağrı bölgesi:** `PAIN` sabiti (ör. diz için `V(.1, .5, .03)`). Bu durumda bağlantı hatlarının da yeniden düzenlenmesi gerekir.
- **Zamanlama:** Kamera için `KF` dizisi, sahne durumu için `update(t)` fonksiyonu. Müzik vuruşları `audio.py` içinde aynı saniyelere göre ayarlıdır.

## Not
Anatomi prosedürel ve stilize bir modeldir (yarı saydam "x-ray" estetiği). Fotogerçekçi bir anatomi için lisanslı bir GLB modeli
(ör. Zygote, TurboSquid) `GLTFLoader` ile sahneye yüklenebilir. Kamera, ışık, bağlantı hatları ve yazı katmanı olduğu gibi kullanılmaya devam eder.
