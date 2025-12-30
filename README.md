# Olist CEO Request Dashboard (Dash)

Bu proje, **Olist e-commerce platformu** için CEO seviyesinde karar destek sunmayı amaçlayan,  
**Dash (Plotly + Bootstrap)** ile geliştirilmiş çok sayfalı bir **analitik dashboard** çalışmasıdır.

Çalışmanın odağı, **satıcı (seller) kârlılığı**, **maliyet yapısı** ve  
**negatif etkili satıcıların platformdan çıkarılmasının finansal sonuçlarıdır**.

---

## 🎯 Amaç

Bu dashboard’un amacı:
- Teknik süreçleri değil, **iş içgörülerini** ön plana çıkarmak
- CEO / üst yönetim için **“hangi kararı almalıyız?”** sorusuna görsel destek sunmak
- Satıcı bazlı kârlılık analizinden **aksiyon alınabilir sonuçlar** üretmek

---

## 🧠 Hedef Kitle

Bu çalışma özellikle:
- **CEO**
- **CFO**
- Üst düzey karar vericiler

için tasarlanmıştır.  
Bu nedenle model detayları yerine **sonuçlar ve etkiler** görselleştirilmiştir.

---

## 📊 Dashboard İçeriği

Dashboard çok sayfalı (`Dash Pages`) yapı ile hazırlanmıştır.

### 🏠 Home (CEO Summary)
- Toplam gelir, maliyet ve net kâr KPI’ları
- Subscription, satış komisyonu, review maliyeti ve IT maliyetlerini içeren **P&L Waterfall**
- Platformun mevcut finansal fotoğrafı

### 📈 Seller Impact Analysis
- Satıcıların kârlılığa göre sıralanması
- En kötü performanslı satıcıların çıkarılması durumunda:
  - Kümülatif kâr değişimi
  - IT maliyeti dahil / hariç senaryolar
- Slider ile **“kaç satıcı çıkarılırsa en optimal kâr elde edilir?”** sorusuna yanıt

### ℹ️ About
- CEO’ya sunulacak temel çıkarımlar
- Karar önerilerinin kısa özeti

---

## 🛠️ Kullanılan Teknolojiler

- **Python**
- **Dash**
- **Plotly**
- **Dash Bootstrap Components**
