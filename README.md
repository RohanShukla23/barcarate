# BarcaRate 🔴🔵

transfer analysis for barca. because every culé deserves to know if that 100m signing is worth it.

## what it does

- analyzes barcelona's current squad for weaknesses
- searches la liga players with smart filtering  
- rates potential transfers with barcelona dna compatibility (yes, that's a real thing)
- gives you the harsh truth about why signing another aging galáctico might not be brilliant

## quick start

```bash
git clone https://github.com/yourusername/barca-rate.git
cd barca-rate
pip install -r requirements.txt
python app.py
```

open `http://localhost:8000` and start scouting like you're actually running the club.

## how the magic works

the transfer rating system (max 9.5, because nobody's perfect) considers:

- **player quality** - their fifa-style rating
- **age factor** - young talents get love, aging legends get reality checks
- **financial sense** - because ffp is still a thing
- **squad needs** - filling actual gaps vs collecting shinny toys
- **special factors** - signing from real madrid gets bonus points obviously

ratings explained:
- 9.0+: dream signing (messi returning vibes)
- 8.0-8.9: excellent target
- 7.0-7.9: solid addition
- 6.0-6.9: consider carefully
- below 6.0: maybe stick to fifa career mode

## current squad included

2024-25 roster with everyone from ter stegen to yamal. plus a database of la liga players because that's where the realistic targets are.

## tech stack

- **backend**: python + flask (keeping it simple)
- **frontend**: vanilla js with barcelona colors (of course)
- **database**: just python lists (we're not storing the next galáctico's contract here)

## contributing

found the next pedri but they're not in the database? open a pr. think the analysis is too harsh on your favorite player? that's the point.

## disclaimer

this is for fun and education. please don't use this to actually run fc barcelona's transfer policy. though honestly, it might not be worse than some recent decisions.

*més que un club, més que a tool*