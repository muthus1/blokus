'''
Code for blockus bot

'''


import random
import sys
import fakes
from shape_definitions import ShapeKind, definitions 
import piece

class RandomBot:
    '''
    Bot that chooses randomly from possible moves
    '''

    def __init__(self, game: fakes.BlokusFake) -> None:
        self.game = game

    def move(self) -> None:
        '''
        Simple bot makes random choice from avaible move and makes that move
        '''

        poss_moves = self.game.available_moves()

        if poss_moves == set():
            self.game.retire()
        else:
            move : set[fakes.Piece]  = random.choice(list(poss_moves))
            self.game.maybe_place(move)


class SimpleBot: 
    '''
    Bot that uses blockus specific heuristic to preform bettter 
    '''

    def __init__(self, game: fakes.BlokusFake) -> None:
        self.game = game

    def move(self) -> None:
        poss_moves = self.game.available_moves()

        if poss_moves == set():
            self.game.retire()
        else:
            if self.av_biggest_piece() == None:
                print("SOMETHING GONE WRONG")
            self.game.maybe_place(self.av_biggest_piece())
        

    def av_biggest_piece(self) -> piece:
        """
        Identifies biggest piece, by going through definitions dictionary
            backwards, in avaiable moves and returns it
        """

        av_pieces = self.game.available_moves()
        av_pieces_shapekind = [x.shape.kind for x in av_pieces]

        all_pieces_shape_kind = list(definitions.keys())

        for i in range(len(all_pieces_shape_kind)):
            #reverse transversial
            if all_pieces_shape_kind[-1 * (i+1)] in av_pieces_shapekind:
                biggest_shape_kind = all_pieces_shape_kind[-1 * (i+1)]
                break
            
        for p in av_pieces:
            if p.shape.kind == biggest_shape_kind:
                return p

        return None





def simulation(NUM_GAMES: int):
    '''
    Simulates a given number of blockus games, prints bots win rate and tie 
    rate.
    '''

    wins : dict[int | str, int] = {1: 0, 2: 0, "Ties": 0}

    for _ in range(NUM_GAMES):
        
        #creates needed variables for a game
        num_players = 2
        dim_board = 11
        ul = (0,0)
        br = (dim_board, dim_board)

        game = fakes.BlokusFake(num_players, dim_board, {ul, br})
        bots : list[SimpleBot|RandomBot] = [RandomBot(game), SimpleBot(game)]
        player_index : int = 0

        while not game.game_over:
            
            #bot makes move
            bots[player_index].move()

            #updates whose turn it is
            player_index = (player_index + 1) % 2
            

        winners :  list[int] = game.winners

        #updates wins dictionary
        if winners == [1, 2]:
            wins["Ties"] += 1 
        else: 
            for winner in winners:
                wins[winner] += 1
    

    #output statistic of games
    print(f"Bot 0 Wins  | {(wins[1] / NUM_GAMES) * 100} %")
    print(f"Bot 1 Wins  | {(wins[2] / NUM_GAMES) * 100} %")
    print(f"Ties        | {(wins["Ties"] / NUM_GAMES) * 100} %")

#start of loop
if __name__ == "__main__":
    
    num_games : int = int(sys.argv[1])
    simulation(num_games)
