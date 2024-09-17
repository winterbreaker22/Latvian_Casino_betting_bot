ARBITRAGE_API_LINK = 'https://api.rr28.xyz/arbitrages/active/'
X3000_LINK = 'https://www.x3000.lv/betting?flowType=gamingOverview#sports-hub/'
TONYBET_LINK = 'https://tonybet.lv/en/'
SPELET_LINK = 'https://spelet.lv/'
TTBET_LINK = 'https://22betin.com/'

WAGER = 100

COMPETITION_TRANS: dict = {
    "Tennis": "Teniss",
    "Football": "Futbols",
    "Baseball": "Beisbols",

    "Grand Slam": "Grand Slam",
    "ATP": "ATP",
    "WTA": "WTA",
    "Challenger": "Challenger",
    "Challenger Doubles": "Challenger dubultspēles",
    "ATP Doubles": "ATP Doubles",
    "ITF Men": "ITF Vīriešu Vienspēles",
    "ITF Men Doubles": "ITF Vīriešu Dubultspēles",
    "ITF Men Qual.": "ITF Viriešu Kvalifikācijas Turnīrs",
    "ITF Women": "ITF Sieviešu Vienspēles",
    "WTA Doubles": "WTA dubultspēles",

    "Madrid": "Madrid",
    "Genoa": "Dženova",
}

COMPETITION_PARSE: dict = {
    "X3000": {
        "Tennis": {
            "ITF. Madrid": [
                "ITF Men",
                "Madrid",
            ],
            "Challenger. Genoa": [
                "Challenger",
                "Genoa",
            ],
            "ITF. Leiria. Women": [
                "ITF Women",
                "Leiria",
            ],
            "Challenger. Cassis": [
                "Challenger Doubles",
                "Cassis",
            ],
            "ITF. Kursumlijska Banja": [
                "ITF Women",
                "Kursumlijska Banja",
            ],
            "ITF. Tehran": [
                "ITF Men",
                "Tehran",
            ],
        },
    },
}