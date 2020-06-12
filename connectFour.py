import random
import sys

#kernel matrix providing relative coordinates for cell
score_kernel = [[(0, 1), (0, 2), (0, 3)],
                [(1, 1), (2, 2), (3, 3)],
                [(1, 0), (2, 0), (3, 0)],
                [(1, -1), (2, -2), (3, -3)],
                [(0, -1), (0, -2), (0, -3)],
                [(-1, -1), (-2, -2), (-3, -3)],
                [(-1, 0), (-2, 0), (-3, 0)],
                [(-1, 1), (-2, 2), (-3, 3)]]

#determines the utility score at a single cell
def cell_score(game_state, cell_x, cell_y):
    score = 0
    cell_id = game_state[cell_y][cell_x]

    #detmines the score for each orthogonal and diagonal direction out of the cell
    for dir in score_kernel:
        dir_score = 1
        for element in dir:
            target_x = cell_x + element[0]
            target_y = cell_y + element[1]
            if (target_y < 0 or target_y >= len(game_state)
                    or target_x < 0 or target_x >= len(game_state[target_y])):
                #if there is no room for a 4 in a row in that direction, then the score for that direction is 0
                dir_score = 0
                break
            elif (game_state[target_y][target_x] != cell_id
                  and game_state[target_y][target_x] != 0):
                #if an opposing piece has been placed in that direction, then there can be no 4 in a row, and the score is 0
                dir_score = 0
                break
            elif game_state[target_y][target_x] == cell_id:
                #double the score for every similar piece in that direction
                dir_score *= 2

            if dir_score == 8:
                #if there are four in a row, set the score to 100 (very good outcome)
                return 100
        #add scores from all directions
        score += dir_score
    return score

#determines the overall utility score for the specified player
def utility_score(game_state, player_id):
    score = 0
    for i in range(len(game_state)):
        for j in range(len(game_state[i])):
            if game_state[i][j] == player_id:
                #add the utility score for each individual piece for this player
                score += cell_score(game_state, j, i)
            elif game_state[i][j] != 0:
                #subtract the utility score for each individual piece of the other player
                score -= cell_score(game_state, j, i)
    return score

def copy_game_state(game_state):
    return [row[:] for row in game_state]

#given the current game state and the player it is playing for, determines the best place to put a piece
def ai_make_move(game_state, player_id):
    max_score = -1 * sys.maxsize
    max_index = []
    for col in range(0, 7):
        curr_state = copy_game_state(game_state)
        #plays in every single column and minmaxes the scores of each
        play_turn(curr_state, col, player_id)
        score = mini_max_ab(curr_state, 4, -1 * sys.maxsize, sys.maxsize, player_id, False)
        if score > max_score:
            max_index = [col]
            max_score = score
        elif score == max_score:
            max_index.append(col)
    #if there are multiple columns of equal quality, choose randomly
    return random.choice(max_index)

#minmax algorithm, given gamestate, depth to explore, alpha and beta, the player id for the piece, and whether they are maximizing
def mini_max_ab(game_state, depth, alpha, beta, player_id, maximizing):
    curr_score = utility_score(game_state, player_id)
    if depth == 0 or curr_score > 100 or curr_score < -100:
        return curr_score

    if maximizing:
        max_eval = -1 * sys.maxsize
        for col in range(0, 7):
            curr_state = copy_game_state(game_state)
            play_turn(curr_state, col, player_id % 2 + 1)
            eval = mini_max_ab(curr_state, depth - 1, alpha, beta, player_id, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = sys.maxsize
        for col in range(0, 7):
            curr_state = copy_game_state(game_state)
            play_turn(curr_state, col, player_id)
            eval = mini_max_ab(curr_state, depth - 1, alpha, beta, player_id, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


#prints the game state to console in user friendly design
def print_board(game_state):
    def print_border():
        for c in range(0, len(game_state[0])):
            print("+---", end="")
        print("+")

    for cell in range(0, len(game_state[0])):
        print("  ", cell, " ", end="", sep="")
    print()
    for row in game_state:
        print_border()
        for cell in row:
            if cell == 0:
                output = " "
            elif cell == 1:
                output = "X"
            else:
                output = "O"
            print("|", output ,end=" ")
        print("|")
    print_border()


#takes an column index, game state and player id to modifiy the game state with the player's intended location
def play_turn(game_state, index, player_id = 1):
    if index < 0 or index >= len(game_state[0]):
        return False
    i = 0
    while i < len(game_state) \
    and game_state[i][index] == 0:
        i += 1
    
    if i == 0:
        return False
    game_state[i - 1][index] = player_id
    return True

if __name__ == "__main__":
    game_state = []

    for row in range(0, 6):
        game_state.append([])
        for col in range(0, 7):
            game_state[row].append(0)

    print_board(game_state)

    def game_progress(game_state):
        score1 = utility_score(game_state, 1)
        score2 = utility_score(game_state, 2)
        if score1 > 100:
            print("X has won")
            return False
        elif score1 < -100:
            print("O has won")
            return False
        else:
            print("Utility Score for X:", score1)
            print("Utility Score for O:", score2)
            return True

    turn = 1

    while game_progress(game_state):
        if turn == 1:
            print("X to move")
        else:
            print("O to move")
        while not play_turn(game_state, int(input()) \
                if turn == 1 else ai_make_move(game_state, 2), turn):
            print("invalid index, try again")
            pass
        print_board(game_state)
        turn = 2 if turn == 1 else 1











