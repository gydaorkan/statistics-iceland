# Statistics Iceland Web Application

Vefforrit sem sýnir áhugaverða tölfræði frá Hagstofu Íslands.

## Lýsing

Þetta forrit sækir gögn frá opinni gagnaþjónustu Hagstofu Íslands (Statistics Iceland API) og birtir þau á fallegu vefviðmóti. Forritið notar Flask vefumgjörð til að búa til vef sem birtir tölfræðigögn á aðgengilegan og skýran hátt.

## Eiginleikar

- 📊 Sækir gögn beint frá Hagstofu Íslands
- 🎨 Falleg og móðurleg hönnun
- 📱 Virkar á öllum tækjum (responsive)
- 🔄 Uppfærist sjálfkrafa með nýjustu gögnum
- 🌐 API endpoint fyrir forritara

## Uppsetning

1. Klónaðu repository:
```bash
git clone https://github.com/gydaorkan/statistics-iceland.git
cd statistics-iceland
```

2. Settu upp virtual environment (optional en mælt með):
```bash
python3 -m venv venv
source venv/bin/activate  # Á Windows: venv\Scripts\activate
```

3. Settu upp dependencies:
```bash
pip install -r requirements.txt
```

## Notkun

1. Keyrðu forritið:
```bash
python3 app.py
```

2. Opnaðu vafra og farðu á:
```
http://localhost:5000
```

### Þróunarhamur (Development Mode)

Til að keyra í þróunarham með debug mode:
```bash
export FLASK_DEBUG=true  # Á Windows: set FLASK_DEBUG=true
python3 app.py
```

**Athugið:** Debug mode ætti **aldrei** að vera virkur í framleiðslu (production) vegna öryggisáhættu.

## API Endpoints

- `GET /` - Aðalsíða með tölfræðigögnum
- `GET /api/data` - JSON endpoint fyrir hrágögn

## Tækni

- **Python 3.12+**
- **Flask** - Vefumgjörð
- **Requests** - HTTP library fyrir API köll
- **Statistics Iceland API** - Gagnagjafi

## Heimild

Öll gögn koma frá [Hagstofu Íslands](https://hagstofa.is) og eru opin gögn undir Creative Commons Attribution 4.0 leyfi.

## License

MIT License
