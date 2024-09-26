ARBITRAGE_API_LINK = 'https://api.rr28.xyz/arbitrages/active/'
X3000_LINK = 'https://www.x3000.lv/betting?flowType=gamingOverview#sports-hub/'
TONYBET_LINK = 'https://tonybet.lv/en/'
SPELET_LINK = 'https://spelet.lv/'
TTBET_LINK = 'https://22betin.com/'
UNIBET_LINK = 'https://www.unibet.com/'

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
    "x3000": {
        "Tennis": {
            "WTA. Beijing": [
                "WTA",
                "Beijing"
            ],
            "ITF. Zlatibor": [
                "ITF Men",
                "Zlatibor"
            ],
            "ITF. Templeton": [
                "ITF Women",
                "Templeton"
            ],
            "ITF. Trnava": [  
                "ITF Men",
                "Trnava"
            ],
            "ITF. Santa Margherita di Pula": [
                "ITF Men Doubles",
                "Santa Margherita Di Pula"
            ],
            "ITF. Pilar. Women": [
                "ITF Women",
                "Pilar"
            ],
            "ITF. Santa Margherita di Pula. Women": [
                "ITF Women",
                "Santa Margherita Di Pula"
            ],
            "ITF. Asuncion": [
                "ITF Men",
                "Asuncion"
            ],
            "Challenger. Orleans": [
                "Challenger",
                "Orleans"
            ],
            "Challenger. Charleston": [
                "Challenger",
                "Charleston"
            ],
            "ITF. Templeton. Women. Qualification": [
                "ITF Women",
                "Templeton"
            ],
            "ITF. Berkeley. Women": [
                "ITF Women",
                "Berkeley"
            ],
            "ITF. Monastir. Women. Qualification": [
                "ITF Women",
                "Monastir"
            ],
            "ITF. Fuzhou": [
                "ITF Men",
                "Fuzhou"
            ],
            "WTA. Beijing. Qualification": [
                "WTA",
                "Beijing"
            ],
            "Challenger. Nonthaburi 4. Qualification": [
                "Challenger",
                "Nonthaburi"
            ],
            "Challenger. Charleston. Qualification": [
                "Challenger",
                "Charleston"
            ],
            "Challenger. Lisbon": [
                "Challenger",
                "Lisbon"
            ],
            "ITF. Pilar. Women. Qualification": [
                "ITF Women",
                "Pilar"
            ],
            "Challenger. Orleans. Qualification": [
                "Challenger",
                "Orleans"
            ],
            " ITF. Kursumlijska Banja. Women. Qualification": [
                "ITF Women",
                "Kursumlijska Banja"
            ],
            "ITF. Nanao. Women. Qualification": [
                "ITF Women",
                "Nanao"
            ],
            "Challenger. Lisbon. Qualification": [
                "Challenger",
                "Lisbon"
            ],
            "ATP. Tokyo. Qualification": [
                "ATP",
                "Tokyo"
            ],
        }   
    },
    "spelet": {
        "Tennis": {
            "WTA. Beijing": [
                "WTA",
                "WTA. Beijing"
            ],
            "Tennis | ITF. Varna. Women": [
                "ITF",
                "ITF. Varna. Women"
            ],
            "ATP. Tokyo": [
                "ATP",
                "ATP. Tokyo"
            ],
            " Challenger. Nonthaburi 4": [
                "Challenger",
                "Challenger. Nonthaburi 4"
            ],
            "ITF. Nanao. Women": [
                "ITF",
                "ITF. Nanao. Women"
            ],
            "ITF. Templeton. Women": [
                "ITF",
                "ITF. Templeton. Women"
            ],
            "ITF. Berkeley. Women": [
                "ITF",
                "ITF. Berkeley. Women"
            ],
            "Challenger. Orleans": [
                "Challenger",
                "Challenger. Orleans"
            ],
            "Challenger. Charleston": [
                "Challenger",
                "Challenger. Charleston"
            ],
            "ITF. Asuncion": [
                "ITF",
                "ITF. Asuncion"
            ],
            "ITF. Pilar. Women": [
                "ITF",
                "ITF. Pilar. Women"
            ],
            "ITF. Santa Margherita di Pula": [
                "ITF",
                "ITF. Santa Margherita di Pula"
            ],
            "ITF. Trnava": [
                "ITF",
                "ITF. Trnava"
            ],
            "ITF. Zlatibor": [
                "ITF",
                "ITF. Zlatibor"
            ],
            "ITF. Falun": [
                "ITF",
                "ITF. Falun"
            ],
            "ATP. Chengdu": [
                "ATP",
                "ATP. Chengdu"
            ],
            " ITF. Kursumlijska Banja. Women": [
                "ITF",
                " ITF. Kursumlijska Banja. Women"
            ],
            " ITF. Kigali": [
                "ITF",
                " ITF. Kigali"
            ],
            "ITF. Targu Mures": [
                "ITF",
                "ITF. Targu Mures"
            ],
            "UTR Pro Tennis Series. Tigre": [
                "UTR",
                "UTR Pro Tennis Series. Tigre"
            ],
            "ITF. Yeongwol. Women": [
                "ITF",
                "ITF. Yeongwol. Women"
            ],
            "ATP. Chengdu. Doubles": [
                "ATP",
                "ATP. Chengdu. Doubles"
            ],
            "Challenger. Antofagasta": [
                "Challenger",
                "Challenger. Antofagasta"
            ],
            "Challenger. Lisbon": [
                "Challenger",
                "Challenger. Lisbon"
            ],
            " Challenger. Columbus": [
                "Challenger",
                "Challenger. Columbus"
            ],
        }
    }
}