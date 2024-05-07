# -*- coding: utf-8 -*-


import MySQLdb
import dotenv

#  dotenv.set_key('.env', 'MySQL_password', <PASSWORD>)

mysql_config = dotenv.dotenv_values('.env')
mysql_config['MySQL_password'] = mysql_config['MySQL_password'].replace('"', '')
mysql_args = (mysql_config['MySQL_host'], mysql_config['MySQL_user'], mysql_config['MySQL_password'], mysql_config['MySQL_db'])


def dump_table(table_name):
    command = f"Select * from {table_name}"
    db = MySQLdb.connect(*mysql_args)
    with db:
        cur = db.cursor()
        cur.execute(command)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        db.commit()
    print(f'{command=} executed.')
    return rows


def init_db():
    db = MySQLdb.connect(*mysql_args)
    with db:
        cur = db.cursor()
        # TABLE contestant
        cur.execute('CREATE TABLE IF NOT EXISTS contestant (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), nationality VARCHAR(255))')
        # TABLE picture
        cur.execute('CREATE TABLE IF NOT EXISTS picture (contestant_id INT AUTO_INCREMENT PRIMARY KEY, picture_path TEXT)')
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
    table_name: str, name of table to be appended
    values:   tuple, values corresponding to column, respectively
    
    Insert into TABLE Values (val1, val2, val3, ...)
    '''
    command = f"Insert into {table_name} Values {values}"
    print(f'try execute {command=}.')
    db = MySQLdb.connect(*mysql_args)
    with db:
        cur = db.cursor()
        cur.execute(command)
        db.commit()
    print(f'{command=} executed.')

def update_db(table_name, set_clause, where_clause):
    '''
    table_name:    str, name of table to be updated
    select_clause: str, column of result that will be modified
    where_clause:  str, condition result must achieve
    
    Update TABLE set SET_CLAUSE where WHERE_CLAUSE
    '''
    command = f"Update {table_name} set {set_clause} where {where_clause}"
    db = MySQLdb.connect(*mysql_args)
    with db:
        cur = db.cursor()
        cur.execute(command)
        db.commit()
    print(f'{command=} executed.')
    
def select_db(table_name, select_clause, where_clause='1'):
    '''
    table_name:    str, name of table to be searched
    select_clause: str, column of result that returned
    where_clause:  str, condition result must achieve
    
    Select SELECT_CLAUSE from TABLE where WHERE_CLAUSE
    '''
    if where_clause == '':
        command = f"Select {select_clause} from {table_name}"
    else:
        command = f"Select {select_clause} from {table_name} where {where_clause}"
    db = MySQLdb.connect(*mysql_args)
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
    # push2

