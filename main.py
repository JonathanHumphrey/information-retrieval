import csv

#containing rank, title, year, artist and lyrics information.


def setup():
    data_dict = {}
    with open("lyrics.csv", 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            rank = int(row['Rank'])
            title = row['Song']
            year = int(row['Year'])
            artist = row['Artist']
            lyrics = row['Lyrics']
            data_dict[rank] = {'rank': rank,'title': title, 'year': year, 'artist': artist, 'lyrics': lyrics}
    return data_dict
def input(dictionary):
    keyword  = "uptown"
    matches = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            lyric_value = value.get('lyrics')
            if isinstance(lyric_value, str) and keyword in lyric_value:
                matches[key] = value
    
    return matches
data = setup()

matches = input(data)
for key, value in matches.items():
    print(f"Title: {value['title']}\nArtist: {value['artist']}")
