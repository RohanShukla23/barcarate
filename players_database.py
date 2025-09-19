# La Liga Players Database with updated market values from Transfermarkt (2025-2026)

# Barcelona Squad (Updated for 2025-26 season)
CURRENT_SQUAD = {
    "goalkeepers": [
        {"name": "Marc-André ter Stegen", "age": 33, "rating": 86, "value": 12000000, "position": "GK", "number": 1},
        {"name": "Joan Garcia", "age": 24, "rating": 83, "value": 25000000, "position": "GK", "number": 13},
        {"name": "Wojciech Szczęsny", "age": 35, "rating": 78, "value": 1000000, "position": "GK", "number": 25}
    ],
    "defenders": [
        {"name": "Alejandro Balde", "age": 21, "rating": 82, "value": 50000000, "position": "LB", "number": 3},
        {"name": "Ronald Araújo", "age": 26, "rating": 85, "value": 70000000, "position": "CB", "number": 4},
        {"name": "Pau Cubarsi", "age": 18, "rating": 78, "value": 25000000, "position": "CB", "number": 5},
        {"name": "Andreas Christensen", "age": 29, "rating": 80, "value": 30000000, "position": "CB", "number": 15},
        {"name": "Gerard Martín", "age": 23, "rating": 70, "value": 5000000, "position": "LB", "number": 18},
        {"name": "Jules Koundé", "age": 26, "rating": 84, "value": 55000000, "position": "RB", "number": 23},
        {"name": "Eric García", "age": 24, "rating": 75, "value": 15000000, "position": "CB", "number": 24}
    ],
    "midfielders": [
        {"name": "Gavi", "age": 21, "rating": 85, "value": 80000000, "position": "CM", "number": 6},
        {"name": "Pedri", "age": 22, "rating": 88, "value": 100000000, "position": "AM", "number": 8},
        {"name": "Fermín López", "age": 22, "rating": 78, "value": 25000000, "position": "CM", "number": 16},
        {"name": "Marc Casadó", "age": 22, "rating": 75, "value": 15000000, "position": "DM", "number": 17},
        {"name": "Dani Olmo", "age": 27, "rating": 85, "value": 60000000, "position": "AM", "number": 20},
        {"name": "Frenkie de Jong", "age": 28, "rating": 86, "value": 70000000, "position": "CM", "number": 21},
        {"name": "Marc Bernal", "age": 18, "rating": 72, "value": 8000000, "position": "DM", "number": 22}
    ],
    "forwards": [
        {"name": "Ferran Torres", "age": 25, "rating": 80, "value": 35000000, "position": "RW", "number": 7},
        {"name": "Robert Lewandowski", "age": 37, "rating": 87, "value": 15000000, "position": "ST", "number": 9},
        {"name": "Lamine Yamal", "age": 18, "rating": 85, "value": 180000000, "position": "RW", "number": 10},
        {"name": "Raphinha", "age": 28, "rating": 84, "value": 60000000, "position": "LW", "number": 11},
        {"name": "Marcus Rashford", "age": 27, "rating": 82, "value": 55000000, "position": "LW", "number": 14},
        {"name": "Roony Bardghji", "age": 19, "rating": 70, "value": 8000000, "position": "RW", "number": 28}
    ]
}

# Comprehensive La Liga Database
LA_LIGA_PLAYERS = [
    # FC Barcelona (Updated for 2025-26)
    {"name": "Marc-André ter Stegen", "age": 33, "rating": 86, "value": 12000000, "position": "GK", "team": "FC Barcelona"},
    {"name": "Joan Garcia", "age": 24, "rating": 83, "value": 25000000, "position": "GK", "team": "FC Barcelona"},
    {"name": "Wojciech Szczęsny", "age": 35, "rating": 78, "value": 1000000, "position": "GK", "team": "FC Barcelona"},
    {"name": "Alejandro Balde", "age": 21, "rating": 82, "value": 50000000, "position": "LB", "team": "FC Barcelona"},
    {"name": "Ronald Araújo", "age": 26, "rating": 85, "value": 70000000, "position": "CB", "team": "FC Barcelona"},
    {"name": "Pau Cubarsi", "age": 18, "rating": 78, "value": 25000000, "position": "CB", "team": "FC Barcelona"},
    {"name": "Andreas Christensen", "age": 29, "rating": 80, "value": 30000000, "position": "CB", "team": "FC Barcelona"},
    {"name": "Gerard Martín", "age": 23, "rating": 70, "value": 5000000, "position": "LB", "team": "FC Barcelona"},
    {"name": "Jules Koundé", "age": 26, "rating": 84, "value": 55000000, "position": "RB", "team": "FC Barcelona"},
    {"name": "Eric García", "age": 24, "rating": 75, "value": 15000000, "position": "CB", "team": "FC Barcelona"},
    {"name": "Gavi", "age": 21, "rating": 85, "value": 80000000, "position": "CM", "team": "FC Barcelona"},
    {"name": "Pedri", "age": 22, "rating": 88, "value": 100000000, "position": "AM", "team": "FC Barcelona"},
    {"name": "Fermín López", "age": 22, "rating": 78, "value": 25000000, "position": "CM", "team": "FC Barcelona"},
    {"name": "Marc Casadó", "age": 22, "rating": 75, "value": 15000000, "position": "DM", "team": "FC Barcelona"},
    {"name": "Dani Olmo", "age": 27, "rating": 85, "value": 60000000, "position": "AM", "team": "FC Barcelona"},
    {"name": "Frenkie de Jong", "age": 28, "rating": 86, "value": 70000000, "position": "CM", "team": "FC Barcelona"},
    {"name": "Marc Bernal", "age": 18, "rating": 72, "value": 8000000, "position": "DM", "team": "FC Barcelona"},
    {"name": "Ferran Torres", "age": 25, "rating": 80, "value": 35000000, "position": "RW", "team": "FC Barcelona"},
    {"name": "Robert Lewandowski", "age": 37, "rating": 87, "value": 15000000, "position": "ST", "team": "FC Barcelona"},
    {"name": "Lamine Yamal", "age": 18, "rating": 85, "value": 180000000, "position": "RW", "team": "FC Barcelona"},
    {"name": "Raphinha", "age": 28, "rating": 84, "value": 60000000, "position": "LW", "team": "FC Barcelona"},
    {"name": "Marcus Rashford", "age": 27, "rating": 82, "value": 55000000, "position": "LW", "team": "FC Barcelona"},
    {"name": "Roony Bardghji", "age": 19, "rating": 70, "value": 8000000, "position": "RW", "team": "FC Barcelona"},
    
    # Real Madrid CF
    {"name": "Kylian Mbappé", "age": 26, "rating": 91, "value": 180000000, "position": "ST", "team": "Real Madrid CF"},
    {"name": "Vinícius Jr.", "age": 24, "rating": 89, "value": 150000000, "position": "LW", "team": "Real Madrid CF"},
    {"name": "Jude Bellingham", "age": 21, "rating": 87, "value": 120000000, "position": "CM", "team": "Real Madrid CF"},
    {"name": "Rodrygo", "age": 24, "rating": 85, "value": 80000000, "position": "RW", "team": "Real Madrid CF"},
    {"name": "Federico Valverde", "age": 26, "rating": 86, "value": 100000000, "position": "CM", "team": "Real Madrid CF"},
    {"name": "Eduardo Camavinga", "age": 22, "rating": 84, "value": 80000000, "position": "CM", "team": "Real Madrid CF"},
    {"name": "Aurélien Tchouaméni", "age": 25, "rating": 85, "value": 80000000, "position": "DM", "team": "Real Madrid CF"},
    {"name": "Antonio Rüdiger", "age": 31, "rating": 84, "value": 25000000, "position": "CB", "team": "Real Madrid CF"},
    {"name": "Éder Militão", "age": 26, "rating": 83, "value": 50000000, "position": "CB", "team": "Real Madrid CF"},
    {"name": "Thibaut Courtois", "age": 32, "rating": 89, "value": 35000000, "position": "GK", "team": "Real Madrid CF"},
    {"name": "Dani Carvajal", "age": 33, "rating": 82, "value": 10000000, "position": "RB", "team": "Real Madrid CF"},
    {"name": "Ferland Mendy", "age": 29, "rating": 79, "value": 20000000, "position": "LB", "team": "Real Madrid CF"},
    {"name": "Lucas Vázquez", "age": 33, "rating": 77, "value": 8000000, "position": "RB", "team": "Real Madrid CF"},
    {"name": "Luka Modrić", "age": 39, "rating": 83, "value": 5000000, "position": "CM", "team": "Real Madrid CF"},
    {"name": "Brahim Díaz", "age": 25, "rating": 78, "value": 25000000, "position": "AM", "team": "Real Madrid CF"},
    
    # Atlético Madrid
    {"name": "Antoine Griezmann", "age": 33, "rating": 85, "value": 15000000, "position": "AM", "team": "Atlético Madrid"},
    {"name": "Álvaro Morata", "age": 32, "rating": 82, "value": 12000000, "position": "ST", "team": "Atlético Madrid"},
    {"name": "Julián Álvarez", "age": 25, "rating": 84, "value": 90000000, "position": "ST", "team": "Atlético Madrid"},
    {"name": "João Félix", "age": 25, "rating": 83, "value": 60000000, "position": "AM", "team": "Atlético Madrid"},
    {"name": "Koke", "age": 32, "rating": 83, "value": 8000000, "position": "CM", "team": "Atlético Madrid"},
    {"name": "Rodrigo de Paul", "age": 30, "rating": 81, "value": 25000000, "position": "CM", "team": "Atlético Madrid"},
    {"name": "José Giménez", "age": 29, "rating": 82, "value": 20000000, "position": "CB", "team": "Atlético Madrid"},
    {"name": "Stefan Savić", "age": 33, "rating": 80, "value": 8000000, "position": "CB", "team": "Atlético Madrid"},
    {"name": "Jan Oblak", "age": 31, "rating": 87, "value": 45000000, "position": "GK", "team": "Atlético Madrid"},
    {"name": "Nahuel Molina", "age": 26, "rating": 79, "value": 20000000, "position": "RB", "team": "Atlético Madrid"},
    {"name": "Reinildo", "age": 30, "rating": 78, "value": 15000000, "position": "LB", "team": "Atlético Madrid"},
    {"name": "Pablo Barrios", "age": 21, "rating": 76, "value": 30000000, "position": "CM", "team": "Atlético Madrid"},
    
    # Real Sociedad
    {"name": "Mikel Oyarzabal", "age": 27, "rating": 83, "value": 40000000, "position": "LW", "team": "Real Sociedad"},
    {"name": "Alexander Sørloth", "age": 29, "rating": 80, "value": 25000000, "position": "ST", "team": "Real Sociedad"},
    {"name": "Takefusa Kubo", "age": 23, "rating": 82, "value": 60000000, "position": "RW", "team": "Real Sociedad"},
    {"name": "Martín Zubimendi", "age": 25, "rating": 84, "value": 60000000, "position": "DM", "team": "Real Sociedad"},
    {"name": "Mikel Merino", "age": 28, "rating": 82, "value": 25000000, "position": "CM", "team": "Real Sociedad"},
    {"name": "Robin Le Normand", "age": 27, "rating": 80, "value": 30000000, "position": "CB", "team": "Real Sociedad"},
    {"name": "Igor Zubeldia", "age": 27, "rating": 79, "value": 25000000, "position": "CB", "team": "Real Sociedad"},
    {"name": "Álex Remiro", "age": 29, "rating": 79, "value": 15000000, "position": "GK", "team": "Real Sociedad"},
    {"name": "Aihen Muñoz", "age": 27, "rating": 77, "value": 12000000, "position": "LB", "team": "Real Sociedad"},
    
    # Athletic Bilbao
    {"name": "Nico Williams", "age": 22, "rating": 84, "value": 70000000, "position": "LW", "team": "Athletic Bilbao"},
    {"name": "Iñaki Williams", "age": 30, "rating": 81, "value": 20000000, "position": "ST", "team": "Athletic Bilbao"},
    {"name": "Oihan Sancet", "age": 24, "rating": 81, "value": 40000000, "position": "AM", "team": "Athletic Bilbao"},
    {"name": "Ander Herrera", "age": 35, "rating": 79, "value": 3000000, "position": "CM", "team": "Athletic Bilbao"},
    {"name": "Dani Vivian", "age": 25, "rating": 78, "value": 25000000, "position": "CB", "team": "Athletic Bilbao"},
    {"name": "Aitor Paredes", "age": 25, "rating": 76, "value": 18000000, "position": "CB", "team": "Athletic Bilbao"},
    {"name": "Unai Simón", "age": 27, "rating": 82, "value": 30000000, "position": "GK", "team": "Athletic Bilbao"},
    {"name": "Óscar de Marcos", "age": 35, "rating": 76, "value": 2000000, "position": "RB", "team": "Athletic Bilbao"},
    
    # Villarreal CF
    {"name": "Gerard Moreno", "age": 32, "rating": 82, "value": 15000000, "position": "ST", "team": "Villarreal CF"},
    {"name": "Yeremy Pino", "age": 22, "rating": 80, "value": 40000000, "position": "RW", "team": "Villarreal CF"},
    {"name": "Álex Baena", "age": 23, "rating": 81, "value": 50000000, "position": "LW", "team": "Villarreal CF"},
    {"name": "Dani Parejo", "age": 35, "rating": 81, "value": 3000000, "position": "CM", "team": "Villarreal CF"},
    {"name": "Pau Torres", "age": 27, "rating": 83, "value": 35000000, "position": "CB", "team": "Villarreal CF"},
    {"name": "Raúl Albiol", "age": 39, "rating": 79, "value": 1000000, "position": "CB", "team": "Villarreal CF"},
    {"name": "Filip Jörgensen", "age": 22, "rating": 76, "value": 15000000, "position": "GK", "team": "Villarreal CF"},
    {"name": "Alfonso Pedraza", "age": 28, "rating": 77, "value": 12000000, "position": "LB", "team": "Villarreal CF"},
    
    # Real Betis
    {"name": "Isco", "age": 32, "rating": 80, "value": 8000000, "position": "AM", "team": "Real Betis"},
    {"name": "Nabil Fekir", "age": 31, "rating": 81, "value": 15000000, "position": "AM", "team": "Real Betis"},
    {"name": "Giovani Lo Celso", "age": 28, "rating": 80, "value": 18000000, "position": "CM", "team": "Real Betis"},
    {"name": "Guido Rodríguez", "age": 30, "rating": 78, "value": 12000000, "position": "DM", "team": "Real Betis"},
    {"name": "Marc Roca", "age": 28, "rating": 77, "value": 10000000, "position": "CM", "team": "Real Betis"},
    {"name": "Germán Pezzella", "age": 33, "rating": 78, "value": 4000000, "position": "CB", "team": "Real Betis"},
    {"name": "Chadi Riad", "age": 21, "rating": 74, "value": 8000000, "position": "CB", "team": "Real Betis"},
    {"name": "Claudio Bravo", "age": 41, "rating": 76, "value": 500000, "position": "GK", "team": "Real Betis"},
    {"name": "Juan Miranda", "age": 24, "rating": 75, "value": 8000000, "position": "LB", "team": "Real Betis"},
    {"name": "Héctor Bellerín", "age": 29, "rating": 76, "value": 8000000, "position": "RB", "team": "Real Betis"},

    # Sevilla FC
    {"name": "Youssef En-Nesyri", "age": 27, "rating": 79, "value": 15000000, "position": "ST", "team": "Sevilla FC"},
    {"name": "Dodi Lukébakio", "age": 27, "rating": 78, "value": 18000000, "position": "RW", "team": "Sevilla FC"},
    {"name": "Suso", "age": 31, "rating": 77, "value": 8000000, "position": "RW", "team": "Sevilla FC"},
    {"name": "Boubakary Soumaré", "age": 25, "rating": 76, "value": 15000000, "position": "CM", "team": "Sevilla FC"},
    {"name": "Nemanja Gudelj", "age": 33, "rating": 76, "value": 3000000, "position": "DM", "team": "Sevilla FC"},
    {"name": "Loïc Badé", "age": 24, "rating": 77, "value": 20000000, "position": "CB", "team": "Sevilla FC"},
    {"name": "Sergio Ramos", "age": 38, "rating": 80, "value": 2000000, "position": "CB", "team": "Sevilla FC"},
    {"name": "Ørjan Nyland", "age": 34, "rating": 74, "value": 2000000, "position": "GK", "team": "Sevilla FC"},
    {"name": "Marcos Acuña", "age": 33, "rating": 78, "value": 8000000, "position": "LB", "team": "Sevilla FC"},

    # Valencia CF
    {"name": "Hugo Duro", "age": 25, "rating": 76, "value": 12000000, "position": "ST", "team": "Valencia CF"},
    {"name": "Diego López", "age": 22, "rating": 75, "value": 15000000, "position": "LW", "team": "Valencia CF"},
    {"name": "Pepelu", "age": 26, "rating": 76, "value": 12000000, "position": "CM", "team": "Valencia CF"},
    {"name": "André Almeida", "age": 24, "rating": 74, "value": 8000000, "position": "CM", "team": "Valencia CF"},
    {"name": "Cristhian Mosquera", "age": 20, "rating": 73, "value": 8000000, "position": "CB", "team": "Valencia CF"},
    {"name": "Cenk Özkacar", "age": 23, "rating": 72, "value": 6000000, "position": "LB", "team": "Valencia CF"},
    {"name": "Giorgi Mamardashvili", "age": 24, "rating": 78, "value": 25000000, "position": "GK", "team": "Valencia CF"},
    {"name": "Thierry Correia", "age": 25, "rating": 74, "value": 8000000, "position": "RB", "team": "Valencia CF"},

    # Celta Vigo
    {"name": "Iago Aspas", "age": 37, "rating": 81, "value": 4000000, "position": "ST", "team": "Celta Vigo"},
    {"name": "Borja Iglesias", "age": 31, "rating": 77, "value": 8000000, "position": "ST", "team": "Celta Vigo"},
    {"name": "Óscar Mingueza", "age": 25, "rating": 76, "value": 12000000, "position": "RB", "team": "Celta Vigo"},
    {"name": "Fran Beltrán", "age": 25, "rating": 75, "value": 8000000, "position": "CM", "team": "Celta Vigo"},
    {"name": "Hugo Sotelo", "age": 21, "rating": 72, "value": 5000000, "position": "CM", "team": "Celta Vigo"},
    {"name": "Carl Starfelt", "age": 29, "rating": 74, "value": 6000000, "position": "CB", "team": "Celta Vigo"},
    {"name": "Vicente Guaita", "age": 37, "rating": 76, "value": 1000000, "position": "GK", "team": "Celta Vigo"},

    # Getafe CF
    {"name": "Borja Mayoral", "age": 27, "rating": 76, "value": 10000000, "position": "ST", "team": "Getafe CF"},
    {"name": "Mason Greenwood", "age": 23, "rating": 82, "value": 50000000, "position": "RW", "team": "Getafe CF"},
    {"name": "Nemanja Maksimović", "age": 29, "rating": 76, "value": 8000000, "position": "CM", "team": "Getafe CF"},
    {"name": "Luis Milla", "age": 28, "rating": 75, "value": 8000000, "position": "CM", "team": "Getafe CF"},
    {"name": "Omar Alderete", "age": 27, "rating": 76, "value": 10000000, "position": "CB", "team": "Getafe CF"},
    {"name": "Djené Dakonam", "age": 32, "rating": 77, "value": 5000000, "position": "CB", "team": "Getafe CF"},
    {"name": "David Soria", "age": 31, "rating": 77, "value": 8000000, "position": "GK", "team": "Getafe CF"},

    # Osasuna
    {"name": "Ante Budimir", "age": 33, "rating": 76, "value": 3000000, "position": "ST", "team": "CA Osasuna"},
    {"name": "Rubén García", "age": 31, "rating": 75, "value": 4000000, "position": "RW", "team": "CA Osasuna"},
    {"name": "Jon Moncayola", "age": 26, "rating": 74, "value": 8000000, "position": "CM", "team": "CA Osasuna"},
    {"name": "Lucas Torró", "age": 30, "rating": 75, "value": 6000000, "position": "DM", "team": "CA Osasuna"},
    {"name": "Alejandro Catena", "age": 29, "rating": 74, "value": 4000000, "position": "CB", "team": "CA Osasuna"},
    {"name": "David García", "age": 30, "rating": 73, "value": 3000000, "position": "CB", "team": "CA Osasuna"},
    {"name": "Sergio Herrera", "age": 31, "rating": 75, "value": 3000000, "position": "GK", "team": "CA Osasuna"},

    # Las Palmas
    {"name": "Sandro Ramírez", "age": 29, "rating": 75, "value": 6000000, "position": "ST", "team": "UD Las Palmas"},
    {"name": "Alberto Moleiro", "age": 21, "rating": 74, "value": 12000000, "position": "LW", "team": "UD Las Palmas"},
    {"name": "Javi Muñoz", "age": 25, "rating": 73, "value": 5000000, "position": "CM", "team": "UD Las Palmas"},
    {"name": "Kirian Rodríguez", "age": 28, "rating": 74, "value": 4000000, "position": "CM", "team": "UD Las Palmas"},
    {"name": "Mika Mármol", "age": 23, "rating": 72, "value": 4000000, "position": "CB", "team": "UD Las Palmas"},
    {"name": "Álvaro Vallés", "age": 27, "rating": 75, "value": 8000000, "position": "GK", "team": "UD Las Palmas"},

    # Rayo Vallecano
    {"name": "Sergio Camello", "age": 24, "rating": 74, "value": 8000000, "position": "ST", "team": "Rayo Vallecano"},
    {"name": "Isi Palazón", "age": 29, "rating": 76, "value": 8000000, "position": "RW", "team": "Rayo Vallecano"},
    {"name": "Jorge de Frutos", "age": 27, "rating": 74, "value": 6000000, "position": "RW", "team": "Rayo Vallecano"},
    {"name": "Óscar Valentín", "age": 29, "rating": 74, "value": 4000000, "position": "DM", "team": "Rayo Vallecano"},
    {"name": "Florian Lejeune", "age": 33, "rating": 76, "value": 3000000, "position": "CB", "team": "Rayo Vallecano"},
    {"name": "Stole Dimitrievski", "age": 30, "rating": 74, "value": 4000000, "position": "GK", "team": "Rayo Vallecano"},

    # Mallorca
    {"name": "Cyle Larin", "age": 29, "rating": 75, "value": 6000000, "position": "ST", "team": "RCD Mallorca"},
    {"name": "Dani Rodríguez", "age": 37, "rating": 74, "value": 1000000, "position": "AM", "team": "RCD Mallorca"},
    {"name": "Samú Costa", "age": 24, "rating": 74, "value": 8000000, "position": "CM", "team": "RCD Mallorca"},
    {"name": "Antonio Raíllo", "age": 33, "rating": 74, "value": 2000000, "position": "CB", "team": "RCD Mallorca"},
    {"name": "Martin Valjent", "age": 28, "rating": 75, "value": 6000000, "position": "CB", "team": "RCD Mallorca"},
    {"name": "Predrag Rajković", "age": 29, "rating": 76, "value": 5000000, "position": "GK", "team": "RCD Mallorca"},

    # Girona FC
    {"name": "Artem Dovbyk", "age": 27, "rating": 79, "value": 30000000, "position": "ST", "team": "Girona FC"},
    {"name": "Viktor Tsygankov", "age": 27, "rating": 78, "value": 20000000, "position": "RW", "team": "Girona FC"},
    {"name": "Savinho", "age": 20, "rating": 76, "value": 25000000, "position": "LW", "team": "Girona FC"},
    {"name": "Aleix García", "age": 27, "rating": 77, "value": 15000000, "position": "CM", "team": "Girona FC"},
    {"name": "Yangel Herrera", "age": 26, "rating": 76, "value": 12000000, "position": "CM", "team": "Girona FC"},
    {"name": "Daley Blind", "age": 34, "rating": 77, "value": 3000000, "position": "CB", "team": "Girona FC"},
    {"name": "Paulo Gazzaniga", "age": 32, "rating": 75, "value": 3000000, "position": "GK", "team": "Girona FC"},

    # Alavés
    {"name": "Kike García", "age": 34, "rating": 74, "value": 2000000, "position": "ST", "team": "Deportivo Alavés"},
    {"name": "Luis Rioja", "age": 31, "rating": 74, "value": 3000000, "position": "LW", "team": "Deportivo Alavés"},
    {"name": "Jon Guridi", "age": 27, "rating": 73, "value": 4000000, "position": "CM", "team": "Deportivo Alavés"},
    {"name": "Antonio Blanco", "age": 24, "rating": 72, "value": 5000000, "position": "DM", "team": "Deportivo Alavés"},
    {"name": "Abdel Abqar", "age": 25, "rating": 73, "value": 5000000, "position": "CB", "team": "Deportivo Alavés"},
    {"name": "Antonio Sivera", "age": 27, "rating": 72, "value": 3000000, "position": "GK", "team": "Deportivo Alavés"},

    # Espanyol
    {"name": "Javi Puado", "age": 26, "rating": 74, "value": 8000000, "position": "ST", "team": "RCD Espanyol"},
    {"name": "Alejo Véliz", "age": 21, "rating": 72, "value": 6000000, "position": "ST", "team": "RCD Espanyol"},
    {"name": "Jofre Carreras", "age": 20, "rating": 70, "value": 4000000, "position": "RW", "team": "RCD Espanyol"},
    {"name": "José Gragera", "age": 26, "rating": 72, "value": 4000000, "position": "DM", "team": "RCD Espanyol"},
    {"name": "Leandro Cabrera", "age": 33, "rating": 73, "value": 2000000, "position": "CB", "team": "RCD Espanyol"},
    {"name": "Joan García", "age": 23, "rating": 75, "value": 15000000, "position": "GK", "team": "RCD Espanyol"},

    # Leganés
    {"name": "Miguel de la Fuente", "age": 25, "rating": 71, "value": 3000000, "position": "ST", "team": "CD Leganés"},
    {"name": "Seydouba Cissé", "age": 24, "rating": 70, "value": 2000000, "position": "CM", "team": "CD Leganés"},
    {"name": "Yvan Neyou", "age": 27, "rating": 71, "value": 2000000, "position": "DM", "team": "CD Leganés"},
    {"name": "Sergio González", "age": 31, "rating": 72, "value": 1500000, "position": "CB", "team": "CD Leganés"},
    {"name": "Matija Nastasić", "age": 31, "rating": 73, "value": 2000000, "position": "CB", "team": "CD Leganés"},
    {"name": "Marko Dmitrović", "age": 32, "rating": 74, "value": 3000000, "position": "GK", "team": "CD Leganés"},

    # Valladolid
    {"name": "Raúl Moro", "age": 22, "rating": 71, "value": 4000000, "position": "LW", "team": "Real Valladolid"},
    {"name": "Mamadou Sylla", "age": 25, "rating": 70, "value": 3000000, "position": "ST", "team": "Real Valladolid"},
    {"name": "Stanko Juric", "age": 21, "rating": 69, "value": 2000000, "position": "CM", "team": "Real Valladolid"},
    {"name": "Eray Cömert", "age": 26, "rating": 72, "value": 4000000, "position": "CB", "team": "Real Valladolid"},
    {"name": "Javi Sánchez", "age": 27, "rating": 71, "value": 3000000, "position": "CB", "team": "Real Valladolid"},
    {"name": "Karl Hein", "age": 22, "rating": 68, "value": 2000000, "position": "GK", "team": "Real Valladolid"}
]

def get_players_by_team(team_name: str):
    """Get all players from a specific team"""
    return [player for player in LA_LIGA_PLAYERS if player["team"].lower() == team_name.lower()]

def get_teams():
    """Get list of all teams"""
    return list(set(player["team"] for player in LA_LIGA_PLAYERS))