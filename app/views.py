from app import app
from flask import render_template
from flask import Flask,request, url_for, redirect, render_template
import json
from keras.models import load_model
import numpy as np 

model = load_model('H:/Educational/Flask Projects/Tic Tac Toe/app/static/model/my_model.h5')

py_board = [[2,2,2],[2,2,2],[2,2,2]]

def legal_moves_generator(current_board_state,turn_monitor):
    legal_moves_dict={}
    for i in range(current_board_state.shape[0]):
        for j in range(current_board_state.shape[1]):
            if current_board_state[i,j]==2:
                board_state_copy=current_board_state.copy()
                board_state_copy[i,j]=turn_monitor
                legal_moves_dict[(i,j)]=board_state_copy.flatten()
    return legal_moves_dict

def move_selector(model,current_board_state,turn_monitor):
    tracker={}
    legal_moves_dict=legal_moves_generator(current_board_state,turn_monitor)
    for legal_move_coord in legal_moves_dict:
        score=model.predict(legal_moves_dict[legal_move_coord].reshape(1,9))
        tracker[legal_move_coord]=score
    selected_move=max(tracker, key=tracker.get)
    new_board_state=legal_moves_dict[selected_move]
    score=tracker[selected_move]
    return selected_move,new_board_state,score

@app.route("/", methods=["GET", "POST"])
def index():
	return render_template("index.html")

@app.route("/tictactoe", methods=["GET", "POST"])
def tictactoe():
	board = request.args.get('board')
	turn = request.args.get('turn')
	generate_pyboard(board)
	selected_move,new_board_state,score=move_selector(model, np.array(py_board), int(turn))
	board = json.dumps(py_board)
	return str(selected_move)#json.dumps(board)	



def generate_pyboard(board):
	str_board = board.replace('[', '').replace(']', '') 
	cnt = 0
	cnt1 = 0
	for i in str_board.split(','):
		
		if type(eval(i)) == int:
			py_board[cnt1][cnt] = 2
		else:
			if 'o' in i:
				py_board[cnt1][cnt] = 0
			elif 'x' in i:
				py_board[cnt1][cnt] = 1

		if cnt == 2:
			cnt = 0
			cnt1 += 1
		else:
			cnt += 1



if __name__ == '__main__':
    app.run(debug=True)
