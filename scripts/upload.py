import json
import psycopg2

def clean_data(data):
    '''Cleans the json data'''
    for record in data:
        if type(record['Yds']) is str and ',' in record['Yds']:
            record['Yds'] = record['Yds'].replace(',', '')
        record['Yds'] = int(record['Yds'])

        if type(record['Lng']) is str and 'T' in record['Lng']:
            record['Lng'] = record['Lng'].replace('T', '')
        record['Lng'] = int(record['Lng'])

def value_string(column_names):
    columns = column_names.split(',')
    values = ''
    for column_name in columns:
        if column_name != 'fum':
            values += "%(" + column_name + ')s,'
        else:
            values += '%(' + column_name + ')s'
    return values

def mappings(record):
    mappings = {}
    mappings['player'] = record['Player']
    mappings['team'] = record['Team']
    mappings['pos'] = record['Pos']
    mappings['att'] = record['Att']
    mappings['att_g'] = record['Att/G']
    mappings['yds'] = record['Yds']
    mappings['avg'] = record['Avg']
    mappings['yds_g'] = record['Yds/G']
    mappings['td'] = record['TD']
    mappings['lng'] = record['Lng']
    mappings['first'] = record['1st']
    mappings['first_percentage'] = record['1st%']
    mappings['twenty_plus'] = record['20+']
    mappings['forty_plus'] = record['40+']
    mappings['fum'] = record['FUM']

    return mappings


if __name__ == '__main__':
    # Connect to db
    connection = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='db', port='5432')
    table_name = 'app_rushingstatistic'
    cursor = connection.cursor()
    cursor.execute("SELECT * from " + table_name)
    result = cursor.fetchall()

    if len(result) == 0:
        print('No entries in table.')
        # Open json file containing rushing stats
        stats = open('/code/rushing.json')
        data = json.load(stats)
        clean_data(data)

        column_names = 'player,team,pos,att,att_g,yds,avg,yds_g,td,lng,first,first_percentage,twenty_plus,forty_plus,fum'

        insert_query = "INSERT INTO " + table_name + '(' + column_names + ') VALUES(' + value_string(column_names) + ')'

        print('Inserting json entries into db...')
        for record in data:
            cursor.execute(insert_query, mappings(record))

        connection.commit()
    

