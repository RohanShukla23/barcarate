# BarcaRate 🔴🔵

transfer analysis tool for barça. because every culé deserves to know if that 100m signing is worth it.

## what it does

- analyzes barcelona's current squad for weaknesses
- searches la liga players with smart filtering  
- rates potential transfers with barcelona compatibility
- gives you the harsh truth about why signing another aging galáctico might not be brilliant

## quick start

```bash
git clone https://github.com/RohanShukla23/barcarate.git
cd barcarate
pip install -r requirements.txt
python app.py
```

open `http://localhost:8000` and start scouting like you're actually running the club.

## how the magic works

the transfer rating system (max 9.5, because nobody's perfect) considers:

- **player quality** - their fifa-style rating
- **age factor** - young talents get love, aging legends get reality checks
- **financial sense** - because ffp is still a thing
- **squad needs** - filling actual gaps vs collecting shiny toys
- **special factors** - signing from real madrid gets bonus points

ratings explained:
- 9.0+: dream signing
- 8.0-8.9: excellent target
- 7.0-7.9: solid addition
- 6.0-6.9: consider carefully
- below 6.0: maybe stick to fifa career mode

## current squad included

2025-26 roster with everyone from garcia to yamal. plus a database of la liga players because that's where the realistic targets are.

## tech stack

- **backend**: python + flask
- **frontend**: vanilla js with barcelona colors
- **database**: just python lists

## contributing

found the next Pedri but they're not in the database? open a pr.

## disclaimer

this is for fun and education. please don't use this to actually run fc barcelona's transfer policy.
