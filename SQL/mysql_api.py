# -*- coding: utf-8 -*-


import MySQLdb


def dump_table(table_name):
    command = f"Select * from {table_name}"
    db = MySQLdb.connect(host="localhost", user="root", db="taekwondo") #, password="NCUCSIE"
    with db:
        cur = db.cursor()
        cur.execute(command)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        db.commit()
    print(f'{command=} executed.')


'''
CREATE TABLE IF NOT EXISTS contestant (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nationality VARCHAR(255));
CREATE TABLE IF NOT EXISTS comp_stats(contestant_id INT, contest_num INT, contest_tot_secs INT, 
                    wins INT, win_rounds INT, lose_rounds INT, 
                    punches INT, kicks INT, suc_punches INT, suc_kicks INT, 
                    pts INT, vios INT, vio_lost_pts INT);
CREATE TABLE IF NOT EXISTS technique_stats(contestant_id INT, 
                    360RoundHouseKickLeft INT, 360RoundHouseKickRight INT, AxeKickLeft INT, AxeKickRight INT, 
                    BackHookKickLeft INT, BackHookKickRight INT, BackKickLeft INT, BackKickRight INT, 
                    FrontKickLeft INT, FrontKickRight INT, RoundHouseKickLeft INT, RoundHouseKickRight INT,
                    SideKickLeft INT, SideKickRight INT, 
                    PunchLeft INT, PunchRight INT);
CREATE TABLE IF NOT EXISTS body_stats(contestant_id INT, 
                    height FLOAT, weight FLOAT);
CREATE TABLE IF NOT EXISTS competition (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), date DATE, location VARCHAR(255), log LONGTEXT, 
                    red_contestant_id INT, blue_contestant_id INT, winner_id INT, 
                    red_points INT, blue_points INT);

'''
def init_db():
    db = MySQLdb.connect(host="localhost", user="root", password="NCUCSIE", db="taekwondo")
    with db:
        cur = db.cursor()
        # TABLE contestant
        cur.execute('CREATE TABLE IF NOT EXISTS contestant (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nationality VARCHAR(255))')
        # TABLE comp_stats
        cur.execute('CREATE TABLE IF NOT EXISTS comp_stats(contestant_id INT, contest_num INT, contest_tot_secs INT, \
                    wins INT, win_rounds INT, lose_rounds INT, \
                    punches INT, kicks INT, suc_punches INT, suc_kicks INT, \
                    pts INT, vios INT, vio_lost_pts INT)')
        # TABLE technique_stats
        cur.execute('CREATE TABLE IF NOT EXISTS technique_stats(contestant_id INT, \
                    360RoundHouseKickLeft INT, 360RoundHouseKickRight INT, AxeKickLeft INT, AxeKickRight INT, \
                    BackHookKickLeft INT, BackHookKickRight INT, BackKickLeft INT, BackKickRight INT, \
                    FrontKickLeft INT, FrontKickRight INT, RoundHouseKickLeft INT, RoundHouseKickRight INT, \
                    SideKickLeft INT, SideKickRight INT, \
                    PunchLeft INT, PunchRight INT)')
        # TABLE body_stats
        cur.execute('CREATE TABLE IF NOT EXISTS body_stats(contestant_id INT, \
                    height FLOAT, weight FLOAT)')
        # TABLE competition
        cur.execute('CREATE TABLE IF NOT EXISTS competition (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), date DATE, location VARCHAR(255), log LONGTEXT, \
                    red_contestant_id INT, blue_contestant_id INT, winner_id INT, \
                    red_points INT, blue_points INT, \
                    red_contestant_id INT, blue_contestant_id INT, winner_id INT)')
        db.commit()
    # db.close()
    print('Database initialized.')
    
def insert_db(table_name, values):
    '''
    table_name: str
    values: tuple
    
    Insert into TABLE Values (val1, val2, val3, ...)
    '''
    command = f"Insert into {table_name} Values {values}"
    db = MySQLdb.connect(host="localhost", user="root", db="taekwondo") #, password="NCUCSIE"
    with db:
        cur = db.cursor()
        cur.execute(command)
        db.commit()
    print(f'{command=} executed.')

def update_db(table_name, set_clause, where_clause):
    '''
    table_name: str
    set_clause: str
    where_clause: str
    
    Update TABLE set SET_CLAUSE where WHERE_CLAUSE
    '''
    command = f"Update {table_name} set {set_clause} where {where_clause}"
    db = MySQLdb.connect(host='localhost', user='root', db='taekwondo') #, password='NCUCSIE'
    with db:
        cur = db.cursor()
        cur.execute(command)
        db.commit()
    print(f'{command=} executed.')
    
def select_db(table_name, select_clause, where_clause):
    '''
    table_name: str
    select_clause: str
    where_clause: str
    
    Select SELECT_CLAUSE from TABLE where WHERE_CLAUSE
    '''
    command = f"Select {select_clause} from {table_name} where {where_clause}"
    db = MySQLdb.connect(host='localhost', user='root', db='taekwondo') # , password='NCUCSIE'
    with db:
        cur = db.cursor()
        cur.execute(command)
        rows = cur.fetchall()
        db.commit()
    print(f'{command=} executed.')
    return rows

if __name__ == '__main__':
    # init_db()
    
    competition_values = (1, 'competition1', '2021-10-16', 'NCU', 'log', 0, 0, 1, 2, 1)
    insert_db('competition', competition_values)
    
    # pass

