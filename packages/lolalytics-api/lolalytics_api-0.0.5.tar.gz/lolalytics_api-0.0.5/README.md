# Unofficial Lolalytics scraper  
[TBA] a lot of things

## Installation  
```bash
pip install lolalytics-api
```

## Functions  
### `get_tierlist`
- `def get_tierlist(n: int = 10, lane: str = '', rank: str = '')`  
*Empty rank is set by default to Emerald+  
*Empty lane is set by default to all lanes  
```json
{
  "0": {
      "rank": "1",
      "champion": "Ahri",
      "tier": "S+",
      "winrate": "52.73"
    },
  "1": {
      "rank": "2",
      "champion": "Yone",
      "tier": "S",
      "winrate": "50.92"
    }
}
```

### `get_counters`
- `def get_counters(n: int = 10, champion: str = '', rank: str = '')`  
*Empty rank is set by default to Emerald+
```json
{
  "0": {
      "champion": "Akali",
      "winrate": "47.91"
    }
}
```

### `display_ranks`
- `def display_ranks(display: bool = True)`  
Display all available ranks and their shortcuts.  
If display is True (default), prints the ranks to the console.  
Otherwise, returns a dict.

### `display_lanes`
- `def display_lanes(display: bool = True)`  
Same as above, but for lanes.

### `get_champion_data`  
- `def get_champion_data(champion: str, lane: str = '', rank: str = '')`  
Returns detailed info about a certain champion.  
```json
{
    "winrate": "51.7%",
    "wr_delta": "0.93%",
    "game_avg_wr": "50.77%",
    "pickrate": "7.46%",
    "tier": "S+",
    "rank": "1 / 99",
    "banrate": "10.27%",
    "games": "67,380"
}
```

### `matchup`
- `def matchup(champion1: str, champion2: str, lane: str = '', rank: str = '')`  
Returns winrate and number of games played in a matchup between two champions.  
```json
{
    "winrate": "49.8%",
    "number_of_games": "1,000"
}
```

### `patch_notes`
- `def patch_notes(rank: str = '')`  
It does NOT show detailed patch notes.  
Nevertheless, it shows which champions were buffed/nerfed/adjusted, also with the winrate/pickrate/banrate changes for each of them.  
```json
{
    "buffed": {
        "0": {
            "champion": "Fiddlesticks",
            "winrate": "52.48% (+0.80%)",
            "pickrate": "2.88 (+0.55)",
            "banrate": "3.12 (+0.47)"
        }
    },
    "nerfed": {
        "0": {
            "champion": "Ryze",
            "winrate": "49.03% (-0.67%)",
            "pickrate": "3.45 (-0.07)",
            "banrate": "0.68 (-0.10)"
        }
    },
    "adjusted": {
        "0": {
            "champion": "Briar",
            "winrate": "52.66% (+0.61%)",
            "pickrate": "3.70 (+0.63)",
            "banrate": "5.14 (+1.53)"
        }
    }
}
```
