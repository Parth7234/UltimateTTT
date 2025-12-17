import random
import time

def check_global_winner(board):
    global_board = [['.' for _ in range(3)] for _ in range(3)]
    for i in range(3):
            for j in range(3):
                curr_board = [[0 for _ in range(3)] for _ in range(3)]
                for k in range(3):
                    for l in range(3):
                        curr_board[k][l]=(board[i*3+k][j*3+l])
                if(check_local_winner(curr_board)==1):
                    global_board[i][j]='X'
                elif(check_local_winner(curr_board)==2):
                    global_board[i][j]='O'
                else:
                    global_board[i][j]='.'
    
    if(check_local_winner(global_board))==1:
        return 1
    elif(check_local_winner(global_board))==2:
        return 2
    else:
        count_x=0
        count_y=0
        for i in range(3):
            for j in range(3):
                if(global_board[i][j]=='X'):
                    count_x+=1
                elif(global_board[i][j]=='O'):
                    count_y+=1

        if(count_x>count_y and check_board_full(global_board)):
            return 1
        elif(count_y>count_x and check_board_full(global_board)):
            return 2
        else:
            return 0

def check_local_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == 'X':
                return 1
            elif board[i][0] == 'O':
                return 2
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == 'X':
                return 1
            elif board[0][i] == 'O':
                return 2

    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'X':
            return 1
        elif board[0][0] == 'O':
            return 2
    if board[0][2] == board[1][1] == board[2][0]:
        if board[1][1] == 'X':
            return 1
        elif board[1][1] == 'O':
            return 2

    return 0 
   
def evaluate(board,prev_move,player,player_number,player_symbol):
    dest_x=prev_move[0]%3
    dest_y=prev_move[1]%3
    home_x=prev_move[0]//3
    home_y=prev_move[1]//3
    flag=True
    score=0
    if player_symbol=='X':
        opponent_symbol='O'
    else:
        opponent_symbol='X'
    winner=check_global_winner(board)
    if(winner==player):
        return +100000
    elif winner==3-player:
        return -100000
    else:
        score=0
        home_board = [[0 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                home_board[i][j]=board[home_x*3+i][home_y*3+j]
        winner=check_local_winner(home_board)
        if winner==player:
            if(home_x==1 and home_y==1):
                score+=15000
            else:
                score+=10000
        elif winner==3-player:
            if(home_x==1 and home_y==1):
                score-=15000
            else:
                score-=10000

        return score

def check_board_full(board):
    for i in range(3):
        if(board[i][0]==board[i][1]==board[i][2] and board[i][0]!='.'):
            return True
        if(board[0][i]==board[1][i]==board[2][i] and board[0][i]!='.'):
            return True
    if(board[0][0]==board[1][1]==board[2][2] and board[0][0]!='.'):
        return True
    if(board[0][2]==board[1][1]==board[2][0] and board[1][1]!='.'):
        return True  
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == '.':
                return False 

    return True

def get_all_moves(board,prev_move):
    valid_moves=[]
    board_x=prev_move[0]%3
    board_y=prev_move[1]%3
    my_board = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            my_board[i][j]=board[board_x*3+i][board_y*3+j]
    
    if(check_board_full(my_board)):
        for i in range(3):
            for j in range(3):
                curr_board = [[0 for _ in range(3)] for _ in range(3)]
                temp_moves=[]
                for k in range(3):
                    for l in range(3):
                        curr_board[k][l]=board[i*3+k][j*3+l]
                        if(board[i*3+k][j*3+l]=='.'):
                            temp_moves.append((i*3+k,j*3+l))
                if(not check_board_full(curr_board)):
                    valid_moves+=temp_moves
        return valid_moves
    
    else:
        for i in range(3):
            for j in range(3):
                if board[board_x*3+i][board_y*3+j]=='.':
                    valid_moves.append((board_x*3+i,board_y*3+j))
        return valid_moves

def minimax(board,prev_move,depth,is_maximizing_player,player,alpha,beta,start_time,time_limit):
    if time.time()-start_time>time_limit:
        return None,100000000
    if player==2:
        winning_symbol='O'
        if is_maximizing_player:
            player_symbol='O'
            player_number=2
        else:
            player_symbol='X'
            player_number=1
    else:
        winning_symbol='X'
        if is_maximizing_player:
            player_symbol='X'
            player_number=1
        else:
            player_symbol='O'
            player_number=2

    score=evaluate(board,prev_move,player,player_number,player_symbol)

    if(depth==0 or score==100000 or score==-100000):
        return None,score
    
    valid_moves=get_all_moves(board,prev_move)
    if not valid_moves:
        return None, score
    
    if(is_maximizing_player):
        best_score=float('-inf')
        best_move=random.choice(valid_moves)
        for move in valid_moves:
            board[move[0]][move[1]]=player_symbol
            _,temp_score=minimax(board,move,depth-1,False,player,alpha,beta,start_time,time_limit)
            board[move[0]][move[1]]='.'
            if(temp_score>best_score):
                best_score=temp_score
                best_move=move
            if temp_score==100000000:
                return None,100000000
            alpha=max(alpha,best_score)
            if(alpha>=beta):
                break
        return best_move,best_score
    
    else:
        best_score=float('inf')
        best_move=random.choice(valid_moves)
        for move in valid_moves:
            board[move[0]][move[1]]=player_symbol
            _,temp_score=minimax(board,move,depth-1,True,player,alpha,beta,start_time,time_limit)
            board[move[0]][move[1]]='.'
            if(temp_score<best_score):
                best_score=temp_score
                best_move=move
            if temp_score==100000000:
                return None,100000000
            beta=min(beta,best_score)
            if(alpha>=beta):
                break
        return best_move,best_score

def play(board, prev_move, player):
    my_board=[[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            my_board[i][j]=board[i][j]
    
    for i in range(9):
        for j in range(9):
            if(my_board[i][j]==0):
                my_board[i][j]='.'
            elif(my_board[i][j]==1):
                my_board[i][j]='X'
            else:
                my_board[i][j]='O'

    if prev_move==None:
        return (4,4)
    start_time=time.time()
    time_limit=3.8

    best_move=None
    depth=6
    best_move,alert = minimax(my_board, prev_move, depth, True, player,float('-inf'),float('inf'),start_time,time_limit)
    count=0
    if best_move is not None:
        return best_move
    
    if best_move is None:
        fallback_moves = get_all_moves(my_board, prev_move)
        if fallback_moves:
            return random.choice(fallback_moves)
        else:
            print("The game was a draw and I didn't return an invalid move")
            return (0, 0)

#       0   1   2 | 3   4   5 | 6   7   8
#     -------------------------------------
#  0 | 00  01  02 | 03  04  05 | 06  07  08
#  1 | 10  11  12 | 13  14  15 | 16  17  18
#  2 | 20  21  22 | 23  24  25 | 26  27  28
#    |-----------+-----------+-----------
#  3 | 30  31  32 | 33  34  35 | 36  37  38
#  4 | 40  41  42 | 43  44  45 | 46  47  48
#  5 | 50  51  52 | 53  54  55 | 56  57  58
#    |-----------+-----------+-----------
#  6 | 60  61  62 | 63  64  65 | 66  67  68
#  7 | 70  71  72 | 73  74  75 | 76  77  78
#  8 | 80  81  82 | 83  84  85 | 86  87  88


