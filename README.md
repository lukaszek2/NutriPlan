# 🥗 NutriPlan – Lokalny serwer

Aplikacja działa jako lokalny serwer Flask.
Dane są wspólne dla wszystkich urządzeń w tej samej sieci WiFi.

---

## ⚡ Szybki start

### 1. Zainstaluj Flask (raz)
```
pip install flask
```

### 2. Uruchom serwer
```
python app.py
```

### 3. Otwórz w przeglądarce
- **Laptop:** http://localhost:5000
- **Telefon:** http://TWÓJ_IP:5000
  *(IP pojawia się w konsoli po uruchomieniu)*

---

## 📁 Struktura plików

```
nutriplan/
├── app.py              ← główny serwer Flask
├── data.json           ← Twoje dane (przepisy, plany) – tworzony automatycznie
├── requirements.txt    ← zależności Python
├── README.md           ← ten plik
└── templates/
    └── index.html      ← interfejs aplikacji
```

---

## 📱 Dostęp z telefonu

1. Laptop i telefon muszą być **w tej samej sieci WiFi**
2. Uruchom `python app.py` na laptopie
3. W konsoli zobaczysz adres, np. `http://192.168.1.42:5000`
4. Wpisz ten adres w przeglądarce telefonu
5. Możesz dodać do ekranu głównego telefonu jako skrót

---

## 💾 Dane

Wszystkie przepisy, plany i dni treningowe zapisują się w pliku `data.json`.
Możesz go skopiować jako backup lub przenieść na inny komputer.

---

## 🔧 Zmiana portu

W pliku `app.py` na końcu znajdź:
```python
app.run(host="0.0.0.0", port=5000, debug=False)
```
Zmień `5000` na dowolny inny port.
