# Damla Teknik Mühendislik: Isı Pompası Reels

`output/damla_isi_pompasi_reels.mp4`: 1080×1920, 30 fps, 15 sn, H.264 + AAC (Instagram Reels'e hazır).

## Akış
| Süre | Sahne | Ekrandaki yazı |
|---|---|---|
| 0–2.2 sn | Kanca: Turkuaz halka çizilir, fan karanlıktan ışıkla belirir, hava girdap gibi fana emilir | "Enerji havada." |
| 2.2–5 sn | Hızlı geri çekilen kamera ile ürünün tamamı, yörünge çekim, ürün üzerinde ışık geçişi | "ISI POMPASI" |
| 5–7.6 sn | Hızlı kamera dönüşü, ardından ısıtma: sıcak hava dalgaları ve kıvılcımlar, 5°→24° | "Isıtır." |
| 7.6–10 sn | Buz şok dalgası, ardından soğutma: kristaller ve serin sis, 24°→18° | "Soğutur." |
| 10–12 sn | Verim: tek enerji kıvılcımı girer, 4 halka çıkar, sayaç 1→4 | "enerji" / "kat konfor" |
| 12–15 sn | Kamera fanın içine dalar, parçacıklar damla logoya dönüşür | Logo + "Konforun Arkasında Tecrübe Var." |

## Yeniden üretme
```bash
python3 audio.py muzik.wav                           # müzik ve efektler (tamamen sentez, telifsiz)
node render.js /tmp/kareler muzik.wav output/video.mp4
```
Önizleme: `scene.html?play=1` adresini tarayıcıda açın.

## Not
Logo, prosedürel olarak çizilmiş geçici bir tasarımdır (damla + fan). Gerçek logo
`scene.html` içindeki `drawLogo` fonksiyonunda değiştirilebilir. Ürün de herhangi bir markaya ait
olmayan, stilize bir ısı pompası modelidir.
