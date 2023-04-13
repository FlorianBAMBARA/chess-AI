'''
this file would be responsible of storing the current game informations. it will also be resposible of checking the availble move et valid loves of the current chess game
'''

class GameState():
    def __init__(self):
        self.board=[
            ["bR","bKN","bB","bQ",'bK',"bB","bKN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wKN","wB","wQ",'wK',"wB","wKN","wR"]

        ]
        self.move_functiun={'P':self.get_pawn_moves,
                            'R':self.get_rook_moves,
                            'B':self.get_bishop_moves,
                            'KN':self.get_Knight_moves,
                            'K':self.get_king_moves,
                            'Q':self.get_queen_moves
                            }
        self.whitetomove=True
        self.movelog=[]
        self.pins=[]
        self.checks=[]
        self.enpassantPossible=()
        self.en_passant_move=False
        self.incheck=False
        self.black_king_location=(0,4)
        self.white_king_location=(7,4)
        self.checkmate=False
        self.stalemate=False
        
    
    
             
    def make_move(self,move):
        '''
        This function do not handle moove like castling en-passant and paw promotion

        '''
        self.board[move.start_row][move.start_col]="--"
        self.board[move.end_row][move.end_col]=move.piece_moved
        self.movelog.append(move)
        self.whitetomove=not self.whitetomove
        if move.piece_moved=='wK':
            self.white_king_location=(move.end_row,move.end_col)
        elif move.piece_moved=='bK':
            self.black_king_location=(move.end_row,move.end_col)

        ##pawn promtion
        if move.isPawn_promotion:
            self.board[move.end_row][move.end_col]=move.piece_moved[0]+'Q'
        # Enpassant_move
        if move.isenpassant_move:
            self.board[move.start_row][move.end_col]='--'

        #updating the en Passant-value
        if move.piece_moved[0]=='p' and abs(move.start_row-move.end_row)==2:
            row=(move.start_row+move.end_row)//2 #to give integer
            self.enpassantPossible=(row,move.start_col)
        else:
            self.enpassantPossible=()
        

    def undo_move(self):

        if len (self.movelog)!=0:
            move=self.movelog.pop()
            self.board[move.start_row][move.start_col]=move.piece_moved
            self.board[move.end_row][move.end_col]=move.piece_captured
            self.whitetomove=not self.whitetomove
            if move.piece_moved=='wK':
                self.white_king_location=(move.start_row,move.start_col)
            elif move.piece_moved=='bK':
                self.black_king_location=(move.start_row,move.start_col)

#----------------------------------------
    def get_valid_moves(self):
        #1) Generate all possibles moves
        moves=self.get_all_possibles_moves()

        #2) for ech move, make the move.
        for i in range(len(moves)-1,-1,-1):
            self.make_move(moves[i])
            #3) generate all opponent's moves
            #4) for each of your opponent's moves, see if they attack your king
            self.whitetomove=not self.whitetomove
            if self.in_check():
                moves.remove(moves[i]) #5) if they do attack your king, not a valid moves
            self.whitetomove= not self.whitetomove
            self.undo_move()
        if len(moves)==0:
            if self.in_check():
                self.checkmate=True
            else:
                self.checkmate=True
        else:
            self.checkmate=False
            self.stalemate=False

        return moves
    

    def in_check(self):
        '''
        Determine if the current player is in check
        '''
        if self.whitetomove:
            return self.square_under_attack(self.white_king_location[0],self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0],self.black_king_location[1])
        
    def  square_under_attack(self,r,c):
        ''' 
        Determine if the enemy can attack the square r,c
        
        '''
        self.whitetomove= not self.whitetomove
        opponent_moves=self.get_all_possibles_moves()
        self.whitetomove= not self.whitetomove
        for move in opponent_moves:
            if move.end_row==r and move.end_col==c:
                return True
            
        return False
        

    def get_all_possibles_moves(self):
        moves=[]
        for r in range(len(self.board)):# r rterur each row list
            for c in range(len(self.board[r])):# c return eeach columns value in the current r
                turn=self.board[r][c][0]
                
                if (turn=='w' and self.whitetomove) or (turn=='b' and not self.whitetomove):
                    piece=self.board[r][c][1:]
                    self.move_functiun[piece](r,c,moves)
        return moves

    def get_pawn_moves(self,r,c,moves):

        if self.whitetomove:
            # advancing part
            if self.board[r-1][c]=='--':
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[5][c]=='--' and self.board[4][c]=='--':
                    moves.append(Move((r,c),(r-2,c),self.board))
            # capture part
            if c-1>=0: #left capture
                if self.board[r-1][c-1][0]=='b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1)==self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,enpassant_move=((r-1,c-1))))

            if c+1<8: #right capture
                if self.board[r-1][c+1][0]=='b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1)==self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board,enpassant_move=((r-1,c+1))))

        else:
            # advancing part
            if self.board[r+1][c]=='--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+1][c]=='--' and self.board[r+2][c]=='--':
                    moves.append(Move((r,c),(r+2,c),self.board))
            # capture part
            if c-1>=0: #left capture
                if self.board[r+1][c-1][0]=='w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif self.enpassantPossible==(r+1,c-1):
                    moves.append(Move((r,c),(r+1,c-1),self.board,enpassant_move=(r+1,c-1)))

            if c+1<8: # right capture
                if self.board[r+1][c+1][0]=='w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif self.enpassantPossible==(r+1,c+1):
                    moves.append(Move((r,c),(r+1,c+1),self.board,enpassant_move=(r+1,c+1)))

        




    def get_rook_moves(self,r,c,moves):
        directions=((-1,0),(0,-1),(1,0),(0,1)) # up, left,down,rigth
        enemy_color="b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1,8):
                end_row=r+d[0]*i
                end_col=c+d[1]*i
                if 0<=end_row<8 and 0<=end_col<8: # on board
                    endPiece=self.board[end_row][end_col]
                    if endPiece=='--':
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                    elif endPiece[0]==enemy_color:
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                        break
                    else:
                        break
                else:
                    break

                
            
    def get_bishop_moves(self,r,c,moves):

        directions=((-1,-1),(-1,1),(1,-1),(1,1)) # up, left,down,rigth
        enemy_color="b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1,8):
                end_row=r+d[0]*i
                end_col=c+d[1]*i
                if 0<=end_row<8 and 0<=end_col<8: # on board
                    endPiece=self.board[end_row][end_col]
                    if endPiece=='--':
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                    elif endPiece[0]==enemy_color:
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_Knight_moves(self,r,c,moves):
        directions=((-1,2),(-1,-2),(1,2),(1,-2),(-2,1),(-2,-1),(2,1),(2,-1)) # up, left,down,rigth
        enemy_color="b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1,8):
                end_row=r+d[0]*i
                end_col=c+d[1]*i
                if 0<=end_row<8 and 0<=end_col<8: # on board
                    endPiece=self.board[end_row][end_col]
                    if endPiece=='--':
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                    elif endPiece[0]==enemy_color:
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                        break
                    else:
                        break
                else:
                    break
        
    def get_queen_moves(self,r,c,moves):
        # comporte comme un bishop et une tour
        #-------------------------------------------------------------------Bishop Part-------------------------------------------------------------------#
        self.get_bishop_moves(r,c,moves)
        #-------------------------------------------------------------------Rook Part-------------------------------------------------------------------#
        self.get_rook_moves(r,c,moves)

    def get_king_moves(self,r,c,moves):
        directions=((-1,-1),(-1,0),(-1,1),(0,1),(0,-1),(1,-1),(1,0),(1,1)) # up, left,down,rigth
        enemy_color="b" if self.whitetomove else "w"
        for d in directions:
            for i in range(1,8):
                end_row=r+d[0]*i
                end_col=c+d[1]*i
                if 0<=end_row<8 and 0<=end_col<8: # on board
                    endPiece=self.board[end_row][end_col]
                    if endPiece=='--':
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                    elif endPiece[0]==enemy_color:
                        moves.append(Move((r,c),(end_row,end_col),self.board))
                        break
                    else:
                        break
                else:
                    break




class Move():
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_move = False
        if self.piece_moved == 'wP' or self.piece_moved == 'bP':
            self.is_pawn_move = True
        self.is_enpassant_move = False
        if self.is_pawn_move and self.start_col != self.end_col and self.piece_captured == '--':
            self.is_enpassant_move = True
        self.is_castle_move = False
        if self.piece_moved == 'wK' or self.piece_moved == 'bK':
            if abs(self.end_col - self.start_col) == 2:
                self.is_castle_move = True
        self.isPawn_promotion = False
        if self.is_pawn_move:
            if self.end_row == 0 or self.end_row == 7:
                self.isPawn_promotion = True
                self.promotion_piece = 'Q'
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]