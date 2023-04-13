import pygame as p
import Engine
from contants import*

    
def main():
    p.init()
    load_images()
    win=p.display.set_mode((width,height))
    clock=p.time.Clock()
    win.fill(p.Color("white"))
    game_state=Engine.GameState()
    valid_moves=game_state.get_valid_moves()
    move_made=False # this is a flag variable to avoid getting at all frame all the valid moves
    running=True
    selected_square=() # track the last click on the curennt game
    player_clicks=[]# this will track the layers clicks on a list of two tuple. [(4,5),(3,6)]
    GAME_OVER = False
    while running:
        for event in p.event.get():
            if event.type==p.QUIT:
                running=False

            elif event.type==p.MOUSEBUTTONDOWN:
                #Mouse handler
                if p.mouse.get_pressed()[0]:
                    location=p.mouse.get_pos()
                    col=location[0]//square_size
                    row=location[1]//square_size
                    # print((row,col))

                    if selected_square==(row,col): #checking if the the player cliked twice on the same square to unselect it 
                        selected_square=()
                        player_clicks=[]
                    else:
                        selected_square=(row,col)
                        player_clicks.append((row,col))

                    if len(player_clicks)==2:

                        move=Engine.Move(player_clicks[0],player_clicks[1],game_state.board)
                        for i in range(len(valid_moves)):
                            if move==valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made=True
                                selected_square=()
                                player_clicks=[]
                        if not move_made:
                            player_clicks=[selected_square]
                        
            

            elif event.type==p.KEYDOWN:
                if event.key==p.K_z: # undo whhen press the button z
                    game_state.undo_move()
                    move_made=True
        if move_made:
            valid_moves=game_state.get_valid_moves()
            move_made=False
                        


        draw_board(win)
        draw_pieces(win,game_state.board)
        clock.tick(FPS)
        p.display.flip()
        

def draw_game_state(win,game_state):

    draw_board(win) # draw the square of the board
    
    draw_pieces(win,game_state.board) # draw the piece on top the squares


    
def draw_board(win):
    '''
    draw the square of the board
    '''
    colors=[p.Color('white'),p.Color('blue')]
    for r in range(dimension):
        for c in range(dimension):
            color=colors[((r+c)%2)] #the ligth square are always on the pair value of the somme of their row and column values.
            p.draw.rect(win,color,(c*square_size,r*square_size,square_size,square_size))


def draw_pieces(win,board):
    for r in range( dimension):
        for c in range (dimension):
            piece=board[r][c]
            if piece!='--':
                win.blit(Images[piece],(c*square_size,r*square_size,square_size,square_size))




if __name__=="__main__":
    main()