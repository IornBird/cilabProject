from mysql_api import insert_db, update_db, select_db


def insert_contestant(ContestantInsertValues):
    '''
    ContestantInsertValues: tuple (id, name, nationality)
    TABLE: 
      contestant: 
        id INT AUTO_INCREMENT PRIMARY KEY
        name VARCHAR(255)
        nationality VARCHAR(255)
      comp_stats: 
        contestant_id INT
        contest_num INT 比賽總場數
        contest_tot_secs INT 比賽總秒數
        wins INT 勝場數
        win_rounds INT 總勝回合數
        lose_rounds INT 總敗回合數
        punches INT 正拳次數
        kicks INT 踢擊次數
        suc_punches INT 正拳成功次數
        suc_kicks INT 踢擊成功次數
        pts INT 總得分
        vios INT 違規次數
        vio_lost_pts INT 違規失分
      technique_stats: 
        contestant_id INT
        360RoundHouseKickLeft INT
        360RoundHouseKickRight INT
        AxeKickLeft INT
        AxeKickRight INT
        BackHookKickLeft INT
        BackHookKickRight INT
        BackKickLeft INT
        BackKickRight INT
        FrontKickLeft INT
        FrontKickRight INT
        RoundHouseKickLeft INT
        RoundHouseKickRight INT
        SideKickLeft INT
        SideKickRight INT
        PunchLeft INT
        PunchRight INT
      body_stats:
        contestant_id INT
        height FLOAT
        weight FLOAT
    '''
    contestant_id = ContestantInsertValues[0]
    insert_db('contestant', ContestantInsertValues)
    insert_db('comp_stats', (contestant_id, ) + (0, ) * 12)
    insert_db('technique_stats', (contestant_id, ) + (0, ) * 16)
    insert_db('body_stats', (contestant_id, ) + (0, ) * 2)
    print(f'Contestant {contestant_id=} inserted.')

def get_contestant_stats(contestant_id):
    '''
    contestant_id: int
    return: tuple (contestant_id, contest_num, contest_tot_secs, wins, win_rounds, lose_rounds, punches, kicks, suc_punches, suc_kicks, pts, vios, vio_lost_pts)
    '''
    comp_stats = select_db('comp_stats', '*', f'contestant_id={contestant_id}')
    return comp_stats

def get_all_constant_name():
    '''
    return: list of tuple (contestant_id, name)
    '''
    return select_db('contestant', 'id, name', 'TRUE')    

def analyze_log(log):
    pass


if __name__ == '__main__':
  # insert_contestant((10, 'John', 'USA'))
  contestant_stats = get_contestant_stats(1)
  print(f'{contestant_stats=}')
  # contestant_name_list = get_all_constant_name()
  # print(f'{contestant_name_list=}')
  pass

