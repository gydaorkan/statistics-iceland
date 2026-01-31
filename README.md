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
# Statistics Iceland - Data Viewer

Vefforrit til að sækja og sýna gögn frá Hagstofu Íslands (Statistics Iceland) í gegnum vefþjónustu.

## Lýsing

Þetta verkefni veitir einfalt vefviðmót til að fá aðgang að tölfræðigögnum frá Hagstofu Íslands í gegnum PX-Web API. Verkefnið inniheldur:

- **Data Fetcher Module** - Python módúl til að sækja gögn frá Hagstofu API
- **Vefforrit** - Flask-byggð vefsíða til að skoða og leita í gögnum
- **REST API** - Einfaldar API endastöðvar til að nálgast gögnin

## Uppsetning

### Kröfur

- Python 3.7 eða nýrra
- pip (Python package installer)

### Uppsetning

1. Klónaðu þetta gagnasafn:
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
2. Settu upp nauðsynlega pakka:
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
### Keyra vefforritið

```bash
python app.py
```

Opnaðu síðan vafra á: `http://localhost:5000`

### Nota Python módúlinn beint

```python
from data_fetcher import StatisticsIcelandAPI

# Búa til API client
api = StatisticsIcelandAPI(language="is")

# Sækja lista af töflum
tables = api.get_tables()

# Sækja metadata fyrir töflu
metadata = api.get_table_metadata("table_id_here")

# Sækja gögn úr töflu
data = api.get_table_data("table_id_here")
```

### Keyra dæmi

```bash
python example.py
```

## API Endastöðvar

Vefforritið býður upp á eftirfarandi API endastöðvar:

- `GET /api/tables` - Sækir lista af tiltækum töflum
- `GET /api/table/<table_id>` - Sækir metadata fyrir tiltekna töflu
- `POST /api/table/<table_id>/data` - Sækir gögn úr töflu
- `GET /api/search?q=keyword` - Leitar að töflum

## Um Hagstofu Íslands API

Þetta verkefni notar opinbert PX-Web API frá Hagstofu Íslands:
- Base URL: `https://px.hagstofa.is/pxis/api/v1/`
- Engin auðkenning er nauðsynleg
- Gögnin eru aðgengileg á íslensku og ensku

Fyrir frekari upplýsingar um API, sjá: https://dataportal.is/utgafur/leidbeiningar/talnagrunnur/um-api/

## Framtíðaruppfærslur

Möguleikar á frekari þróun:

- Stuðningur við fleiri opnar gagnaheimildir
- Betri gagnasjónræn birting (töflur, gröf)
- Export virkni (CSV, Excel, JSON)
- Geymsla gagna í gagnagrunni
- Aukin leitarvirkni

## Höfundarréttur

Gögn eru frá Hagstofu Íslands og falla undir [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) leyfi.
