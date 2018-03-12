from blocks import *
from board import *
from boardClass import *
from tree import *
import string
import copy
import time

global current
global opponent

def three_unbroken(best_block, boardCells):
    idx = 0
    for blocks in best_block:
        if blocks[0] >= 3:
            for block in blocks[1]:
                block_1 = [boardCells[block[0]].char, boardCells[block[1]].char, boardCells[block[2]].char]
                block_2 = [boardCells[block[1]].char, boardCells[block[2]].char, boardCells[block[3]].char]
                block_3 = [boardCells[block[2]].char, boardCells[block[3]].char, boardCells[block[4]].char]
                if '.' not in block_1:
                    return True, block, idx
                if '.' not in block_2:
                    return True, block, idx
                if '.' not in block_3:
                    return True, block, idx
                idx += 1
    return False, None, 0

def four_unbroken(best_block, boardCells):
    if best_block[0][0] == 4:
        for block in best_block[0][1]:
            block_1 = [boardCells[block[0]].char, boardCells[block[1]].char, boardCells[block[2]].char, boardCells[block[3]].char]
            block_2 = [boardCells[block[1]].char, boardCells[block[2]].char, boardCells[block[3]].char, boardCells[block[4]].char]
            if '.' not in block_1:
                return True, block
            if '.' not in block_2:
                return True, block
        return False, None
    else:
        return False, None

def reflex(boardCells, board, player, p1_moves, p2_moves, p1_idx, p2_idx, current, opponent):
    best_count_red, winning_blocks_red = winning_blocks(boardCells, 'red')
    best_count_blue, winning_blocks_blue = winning_blocks(boardCells, 'blue')

    if player == 'red':
        four_red, block_red = four_unbroken(best_count_red, boardCells)
        four_blue, block_blue = four_unbroken(best_count_blue, boardCells)
        three_blue, block_3_blue, idx = three_unbroken(best_count_blue, boardCells)
        if p1_idx == 0 and p2_idx == 0:
            boardCells[(3,3)].set_char(p1_moves[p1_idx])
            board[boardCells[(3,3)].idx] = boardCells[(3,3)].char
            board_string = ''.join(board)
            print board_string
            if current == 'reflex' and opponent == 'reflex':
                return reflex(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='reflex', opponent ='reflex')
            elif current == 'reflex' and opponent == 'minimax':
                return minimax_setup(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='minimax', opponent = 'reflex')
            for coord in block_red:
                if boardCells[coord].char == '.':
                    boardCells[coord].set_char(p1_moves[p1_idx])
                board[boardCells[coord].idx] = boardCells[coord].char
                board_string = ''.join(board)
                print board_string
                return boardCells
        elif four_blue == True:
            for coord in block_blue:
                if boardCells[coord].char == '.':
                    boardCells[coord].set_char(p1_moves[p1_idx])
            board[boardCells[coord].idx] = boardCells[coord].char
            board_string = ''.join(board)
            print board_string
            if opponent == 'reflex' and current == 'reflex':
                return reflex(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='reflex', opponent ='reflex')
            elif current == 'reflex' and opponent == 'minimax':
                return minimax_setup(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current = 'minimax', opponent = 'reflex')

        elif three_blue == True:
            if boardCells[block_3_blue[0]].char != '.' and boardCells[block_3_blue[1]].char != '.' and boardCells[block_3_blue[2]].char != '.':
                boardCells[block_3_blue[3]].set_char(p1_moves[p1_idx])
                board[boardCells[block_3_blue[3]].idx] = boardCells[block_3_blue[3]].char
            elif boardCells[block_3_blue[1]].char != '.' and boardCells[block_3_blue[2]].char != '.' and boardCells[block_3_blue[3]].char != '.':
                if boardCells[block_3_blue[0]].char == '.':
                    boardCells[block_3_blue[0]].set_char(p1_moves[p1_idx])
                    board[boardCells[block_3_blue[0]].idx] = boardCells[block_3_blue[0]].char
                else:
                    boardCells[block_3_blue[4]].set_char(p1_moves[p1_idx])
                    board[boardCells[block_3_blue[4]].idx] = boardCells[block_3_blue[4]].char
            else:
                boardCells[block_3_blue[1]].set_char(p1_moves[p1_idx])
                board[boardCells[block_3_blue[1]].idx] = boardCells[block_3_blue[1]].char
            board_string = ''.join(board)
            print board_string
            if opponent == 'reflex' and current == 'reflex':
                return reflex(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current = 'reflex', opponent = 'reflex')
            elif current == 'reflex' and opponent == 'minimax':
                return minimax_setup(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current = 'minimax', opponent ='reflex')
        else:
            if best_count_red[0][1] != [] or best_count_red[1][1] != [] or best_count_red[2][1] != [] or best_count_red[3][1] != []:
                for blocks in best_count_red:
                    if blocks[1] != []:
                        block = blocks[1][0]
                        zero_block = ['.', '.', '.', '.', '.']
                        curr_block = [boardCells[block[0]].char, boardCells[block[1]].char, boardCells[block[2]].char, boardCells[block[3]].char, boardCells[block[4]].char]
                        if zero_block == curr_block:
                            boardCells[block[0]].set_char(p1_moves[p1_idx])
                            board[boardCells[block[0]].idx] = boardCells[block[0]].char
                            board_string = ''.join(board)
                            print board_string
                            if opponent == 'reflex' and current == 'reflex':
                                return reflex(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='reflex', opponent ='reflex')
                            elif current == 'reflex' and opponent == 'minimax':
                                return minimax_setup(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='minimax', opponent ='reflex')

                        else:
                            for i in range(len(block)):
                                if (boardCells[block[i]].char == '.' and boardCells[block[i+1]].char != '.' and i != 4) or (boardCells[block[i]].char == '.' and boardCells[block[i-1]].char != '.' and i != 0):
                                    boardCells[block[i]].set_char(p1_moves[p1_idx])
                                    board[boardCells[block[i]].idx] = boardCells[block[i]].char
                                    board_string = ''.join(board)
                                    print board_string
                                    if opponent == 'reflex' and current == 'reflex':
                                        return reflex(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='reflex', opponent= 'reflex')
                                    elif current == 'reflex' and opponent == 'minimax':
                                        return minimax_setup(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current= 'minimax', opponent ='reflex')
            else:
                for y in range (7):
                    for x in range(7):
                        if boardCells[(x,y)].char == '.':
                            boardCells[(x,y)].set_char(p1_moves[p1_idx])
                            board[boardCells[(x,y)].idx] = boardCells[(x,y)].char
                            board_string = ''.join(board)
                            print board_string
                            if opponent == 'reflex' and current == 'reflex':
                                return reflex(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx + 1), p2_idx, current ='reflex', opponent ='reflex')
                            elif current == 'reflex' and opponent == 'minimax':
                                return minimax_setup(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='minimax', opponent ='reflex')
                return boardCells
    else:
        four_red, block_red = four_unbroken(best_count_red, boardCells)
        four_blue, block_blue = four_unbroken(best_count_blue, boardCells)
        three_red, block_3_red, idx = three_unbroken(best_count_red, boardCells)
        if p1_idx == 0 and p2_idx == 0:
            boardCells[(3,3)].set_char(p2_moves[p2_idx])
            board[boardCells[(3,3)].idx] = boardCells[(3,3)].char
            board_string = ''.join(board)
            print board_string
            if current == 'reflex' and opponent == 'reflex':
                return reflex(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current ='reflex', opponent ='reflex')
            elif current == 'reflex' and opponent == 'minimax':
                return minimax_setup(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current ='minimax', opponent ='reflex')

        elif four_blue == True:
            for coord in block_blue:
                if boardCells[coord].char == '.':
                    boardCells[coord].set_char(p2_moves[p2_idx])
                board[boardCells[coord].idx] = boardCells[coord].char
                board_string = ''.join(board)
                print board_string
                return boardCells
        elif four_red == True:
            for coord in block_red:
                if boardCells[coord].char == '.':
                    boardCells[coord].set_char(p2_moves[p2_idx])
            board[boardCells[coord].idx] = boardCells[coord].char
            board_string = ''.join(board)
            print board_string
            if current == 'reflex' and opponent == 'reflex':
                return reflex(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current ='reflex', opponent ='reflex')
            elif current == 'reflex' and opponent == 'minimax':
                return minimax_setup(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current ='minimax', opponent='reflex')
        elif three_red == True:
            if boardCells[block_3_red[0]].char != '.' and boardCells[block_3_red[1]].char != '.' and boardCells[block_3_red[2]].char != '.':
                boardCells[block_3_red[3]].set_char(p2_moves[p2_idx])
                board[boardCells[block_3_red[3]].idx] = boardCells[block_3_red[3]].char
            elif boardCells[block_3_red[1]].char != '.' and boardCells[block_3_red[2]].char != '.' and boardCells[block_3_red[3]].char != '.':
                if boardCells[block_3_red[0]].char == '.':
                    boardCells[block_3_red[0]].set_char(p2_moves[p2_idx])
                    board[boardCells[block_3_red[0]].idx] = boardCells[block_3_red[0]].char
                else:
                    boardCells[block_3_red[4]].set_char(p2_moves[p2_idx])
                    board[boardCells[block_3_red[4]].idx] = boardCells[block_3_red[4]].char
            else:
                boardCells[block_3_red[1]].set_char(p2_moves[p2_idx])
                board[boardCells[block_3_red[1]].idx] = boardCells[block_3_red[1]].char
            board_string = ''.join(board)
            print board_string
            if current == 'reflex' and opponent == 'reflex':
                return reflex(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx + 1), current ='reflex', opponent ='reflex')
            elif current == 'reflex' and opponent == 'minimax':
                return minimax_setup(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current = 'minimax', opponent ='reflex')
        else:
            if best_count_blue[0][1] != [] or best_count_blue[1][1] != [] or best_count_blue[2][1] != [] or best_count_blue[3][1] != []:
                for blocks in best_count_blue:
                    if blocks[1] != []:
                        block = blocks[1][0]
                        zero_block = ['.', '.', '.', '.', '.']
                        curr_block = [boardCells[block[0]].char, boardCells[block[1]].char, boardCells[block[2]].char, boardCells[block[3]].char, boardCells[block[4]].char]
                        if zero_block == curr_block:
                            boardCells[block[0]].set_char(p2_moves[p2_idx])
                            board[boardCells[block[0]].idx] = boardCells[block[0]].char
                            board_string = ''.join(board)
                            print board_string
                            if current == 'reflex' and opponent == 'reflex':
                                return reflex(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx + 1), current ='reflex', opponent ='reflex')
                            elif current == 'reflex' and opponent == 'minimax':
                                return minimax_setup(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current ='minimax', opponent ='reflex')
                        else:
                            for i in range(len(block)):
                                if (boardCells[block[i]].char == '.' and boardCells[block[i+1]].char != '.' and i != 4) or (boardCells[block[i]].char == '.' and boardCells[block[i-1]].char != '.' and i != 0):
                                    boardCells[block[i]].set_char(p2_moves[p2_idx])
                                    board[boardCells[block[i]].idx] = boardCells[block[i]].char
                                    board_string = ''.join(board)
                                    print board_string
                                    if current == 'reflex' and opponent == 'reflex':
                                        return reflex(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx + 1), current ='reflex', opponent ='reflex')
                                    elif current == 'reflex' and opponent == 'minimax':
                                        return minimax_setup(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current ='minimax', opponent ='reflex')
            else:
                for y in range (7):
                    for x in range(7):
                        if boardCells[(x,y)].char == '.':
                            boardCells[(x,y)].set_char(p2_moves[p2_idx])
                            board[boardCells[(x,y)].idx] = boardCells[(x,y)].char
                            board_string = ''.join(board)
                            print board_string
                            if current == 'reflex' and opponent == 'reflex':
                                return reflex(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current ='reflex', opponent ='reflex')
                            elif current == 'reflex' and opponent == 'minimax':
                                return minimax_setup(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current ='minimax', opponent ='reflex')
                return boardCells

def eval_fn(boardCells, coord, player):
    best_count_player, winning_blocks_player = winning_blocks(boardCells, player)
    winning_blocks_coord = [block for block in winning_blocks_player if coord in block]
    potential = 0
    count = 0
    for block in winning_blocks_coord:
        for coords in block:
            if boardCells[coords].char != '.':
                count += 1
        potential += count
        count = 0
    return potential

def minimum(nodes):
    min_val = 10000000000000
    for node in nodes:
        if node.value < min_val:
            min_val = node.value

    return min_val

def maximum(nodes):
    max_val = 0
    for node in nodes:
        if node.vaue > max_val:
            max_val = node.value
    return max_val

def minimax(first_moves, player):
    max_val = 0
    min_val = 0
    max_vals = []
    for dep1 in first_moves:
        for dep2 in dep1.children:
            for dep3 in dep2.children:
                dep3.set_value(eval_fn(dep3.boardCells, (dep3.x, dep3.y), player))
            dep2.set_value(maximum(dep2.children))
        dep1.set_value(minimum(dep1.children))

    for node in first_moves:
        if node.value > max_val:
            max_val = node.value
            ret_node = node

    return (ret_node.x, ret_node.y)

def minimax_setup(boardCells, board, player, p1_moves, p2_moves, p1_idx, p2_idx, current, opponent):
    if p1_idx == 0 and p2_idx == 0:
        boardCells[(3,3)].set_char(p1_moves[p1_idx])
        board[boardCells[(3,3)].idx] = boardCells[(3,3)].char
        board_string = ''.join(board)
        print board_string
        if current == 'minimax' and opponent == 'reflex':
            return reflex(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='reflex', opponent ='minimax')
    first_moves = []
    if player == 'red':
        start_time = time.time()
        for x in range(7):
            for y in range(7):
                print (x,y)
                dep1_boardCells = copy.deepcopy(boardCells)
                if dep1_boardCells[(x,y)].char == '.':
                    dep1_boardCells[(x,y)].set_char(p1_moves[p1_idx])
                    dep1_node = tree(dep1_boardCells, x, y, 0)
                    for i in range(7):
                        for j in range(7):
                            dep2_boardCells = copy.deepcopy(dep1_boardCells)
                            if dep2_boardCells[(i,j)].char == '.':
                                dep2_boardCells[(i,j)].set_char(p2_moves[p2_idx])
                                dep2_node = tree(dep2_boardCells, i, j, 0)
                                for k in range(7):
                                    for l in range(7):
                                        dep3_boardCells = copy.deepcopy(dep2_boardCells)
                                        if dep3_boardCells[(k,l)].char == '.':
                                            dep3_boardCells[(k,l)].set_char(p1_moves[p1_idx+1])
                                            dep3_node = tree(dep3_boardCells, k, l, 0)
                                            dep2_node.children_append(dep3_node)
                                dep1_node.children_append(dep2_node)
                    first_moves.append(dep1_node)
        next_move = minimax(first_moves, 'red')
        boardCells[next_move].set_char(p1_moves[p1_idx])
        board[boardCells[next_move].idx] = boardCells[next_move].char
        board_string = ''.join(board)
        print board_string
        elapsed_time = time.time() - start_time
        print elapsed_time
        best_count, winning_blocks_red = winning_blocks(boardCells, 'red')
        if best_count[0][0] == 5:
            return boardCells
        else:
            if current == 'minimax' and opponent == 'reflex':
                return reflex(boardCells, board, 'blue', p1_moves, p2_moves, (p1_idx+1), p2_idx, current ='reflex', opponent ='minimax')

    else:
        for x in range(7):
            for y in range(7):
                dep1_boardCells = boardCells.copy()
                if dep1_boardCells[(x,y)].char == '.':
                    dep1_boardCells[(x,y)].set_char(p2_moves[p2_idx])
                    dep1_node = tree(dep1_boardCells, 0)
                    for i in range(7):
                        for j in range(7):
                            dep2_boardCells = dep1_boardCells.copy()
                            if dep2_boardCells[(i,j)].char == '.':
                                dep2_boardCells[(i,j)].set_char(p1_moves[p1_idx])
                                dep2_node = tree(dep2_boardCells, 0)
                                for k in range(7):
                                    for l in range(7):
                                        dep3_boardCells = dep2_boardCells.copy()
                                        if dep3_boardCells[(k,l)].char == '.':
                                            dep3_boardCells[(k,l)].set_char(p2_moves[p2_idx+1])
                                            dep3_node = tree(dep3_boardCells, 0)
                                            dep2_node.children_append(dep3_node)
                                dep1_node.children_append(dep2_node)
                    first_moves.append(dep1_node)
        next_move = minimax(first_moves, 'blue')
        boardCells[next_move].set_char(p2_moves[p2_idx])
        board[boardCells[next_move].idx] = boardCells[next_move].char
        board_string = ''.join(board)
        print board_string
        best_count, winning_blocks_blue = winning_blocks(boardCells, 'blue')
        print best_count[0][0]
        if best_count[0][0] == 5:
            return boardCells
        else:
            if current == 'minimax' and opponent == 'reflex':
                return reflex(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, (p2_idx+1), current = 'reflex', opponent ='minimax')


p1_moves = list(string.ascii_lowercase)
p2_moves = list(string.ascii_uppercase)
p1_idx = 0
p2_idx = 0

board, boardCells = initBoard()

for x in range(7):
    for y in range(7):
        board[boardCells[(x,y)].idx] = boardCells[(x,y)].char
        board[boardCells[(x,y)].idx] = boardCells[(x,y)].char

boardCells = minimax_setup(boardCells, board, 'red', p1_moves, p2_moves, p1_idx, p2_idx, current ='minimax', opponent='reflex')

for x in range(7):
    for y in range(7):
        board[boardCells[(x,y)].idx] = boardCells[(x,y)].char
        board[boardCells[(x,y)].idx] = boardCells[(x,y)].char

board_string = ''.join(board)
print board_string
file = open('rm_agent.txt', 'w')
file.write(board_string)
