from __future__ import unicode_literals

from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
import random
import time
from django.db import transaction
from . import models

def index(request):
	number = random.randint (123456,123456789);
	return render(request,"index.html",{"game_id": number})

def check_win (request):
	try:
		data = json.loads(str(request.body.decode()))
		game_id = data["game_id"]
		G = models.Game.objects.get(game_id=game_id)
		winner = G.winner
		if (winner==None or winner==""):
			response_data = {"flag": "no"}
		else:
			name = winner
			response_data = { "flag":"yes", "player_name": name};
	except:
		response_data={"flag":"no"}
	return JsonResponse(response_data);

def update_winner(request):
	try:
		data = json.loads(str(request.body.decode()))
		game_id = data["game_id"]
		player_name = data["name"]
		G = models.Game.objects.get(game_id=game_id)
		winner=G.winner
		if (winner==None or winner==""):
			with transaction.atomic():
				G=models.Game.objects.select_for_update().get(game_id=game_id)
				if (G.winner=="" or G.winner==""):
					G.winner = player_name
					G.question=""
					P = G.player_set.get(name=player_name)
					P.wins = P.wins + 1
					P.save()
					G.save()
					response_data={"flag": "yes"}
				else:
					response_data={"flag": "no"}
	except:
		response_data={"flag":"no"}

	return JsonResponse(response_data)

def check_game (request):
	print (request.POST);
	game_id = request.POST['game_id']
	G = models.Game.objects.get(game_id=game_id)
	np = G.player_set.count()
	mp = G.no_of_players
	plist = [str(p) for p in list(G.player_set.all())]
	if (np==mp):
		G.start_time=int(time.time())
		G.save()
		response_data = {"flag":"yes"}
		return JsonResponse(response_data)
	response_data={"flag":"no","player_list":plist}
	return JsonResponse(response_data);

def check_name (tmp_name):
	name=""
	for ch in tmp_name:
		if (ch>='A' and ch<='Z'):
			name+=ch
		elif (ch>='a' and ch<='z'):
			name+=ch
		elif (ch=='.'):
			name+=ch
		elif (ch>='0' and ch<='9'):
			name+=ch
	if (name==""):
		name="UNKNOWN"
	return name

def check_game_id (tmp_game_id):
	game_id=""
	for ch in str(tmp_game_id):
		if (ch>='0' and ch<='9'):
			game_id=game_id+ch
	if (game_id==""):
		game_id=123456
	return game_id

def create_game (request):
	print (request.POST);
	name=request.POST['pname1']
	game_id = request.POST['game_id']
	name = check_name(name)
	game_id = check_game_id (game_id)
	while (True):
		try:
			G = models.Game.objects.get(game_id=game_id)
		except models.Game.DoesNotExist:
			break
		game_id=random.randint (123456,123456789);
	game_hash=name+"&"+str(game_id)
	no_of_players = int(request.POST['no_of_players'])
	seconds=3600
	rounds=200
	if (request.POST['round']=='minutes'):
		seconds=int(request.POST['minutes'])
		seconds=seconds*60
	else:
		rounds=int(request.POST['questions'])
	G = models.Game(game_id=game_id,no_of_players=no_of_players,rounds=rounds,seconds=seconds,rounds_over=0,seconds_over=0)
	G.save();
	G.player_set.create(name=name)
	G.save();
	print(G)
	return redirect("/game_arena/"+game_hash+"&Create/");

def notpresent(G,name):
	for p in list(G.player_set.all()):
		if (p.name==name):
			return False
	return True

def join_game (request):
	name=request.POST['pname2']
	game_id = request.POST['game_id']
	name = check_name(name)
	game_id = check_game_id (game_id)
	try:
		G = models.Game.objects.get(game_id=game_id)
		np = G.no_of_players
		mp = G.player_set.count()
		if (G==None or mp==np):
			return render(request,"garena.html",{"error": "NO SUCH GAME PRESENT!!"})
	except models.Game.DoesNotExist:
		return render(request,"garena.html",{"error": "NO SUCH GAME PRESENT!!"})
	np = G.player_set.count()
	mp = G.no_of_players
	game_hash=name+"&"+game_id
	if (G.rounds_over>0):
		return render(request,"garena.html",{"error": "Sorry, Game Already Started. You Cannot Join Now!! :("})
	if (notpresent(G,name)):
		G.player_set.create(name=name)
	else:
		return render(request,"garena.html",{"error": "Player with this mySingle is already in the Game. If you want to join again, change mySingle or contact admin for the same"})
	G.save();
	return redirect("/game_arena/"+game_hash+"/");

def update_time (request):
	try:
		data = json.loads(str(request.body.decode()))
		game_id = data["game_id"]
		G = models.Game.objects.get(game_id=game_id)
		if (G.seconds>600):
			response_data={"sec": "no"}
			return JsonResponse(response_data)
		cur_time = int(time.time())
		G.seconds_over = cur_time - G.start_time
		print (G.seconds_over)
		print(cur_time)
		G.save()
		seconds_left = G.seconds - G.seconds_over
		if (G.seconds<=G.seconds_over):
			seconds_left = 0
			response_data={"flag": "yes","sec": "yes", "seconds": seconds_left}
		else:
			response_data={"flag": "no","sec": "yes", "seconds": seconds_left}
	except:
		response_data={"flag": "no","sec": "yes", "seconds": 0}
	return JsonResponse(response_data)

def start_game (request):
	name = request.POST['name']
	game_id = request.POST['game_id']
	wins = request.POST['wins']
	try:
		G = models.Game.objects.get(game_id=game_id)
	except models.Game.DoesNotExist:
		return render(request,"garena.html",{"error": "NO SUCH GAME PRESENT!!"})
	G.winner = ""
	print (G.rounds_over)
	if (G.rounds_over>=G.rounds or G.seconds<=G.seconds_over):
		winners = []
		p = list(G.player_set.all())
		p.sort(key=lambda x: x.wins, reverse=True)
		G.no_of_players-=1
		G.save()
		return render(request,"results.html",{"winners": p})

	G.save()
	ques = G.question
	if (ques==None or ques==""):
		with transaction.atomic():
			G=models.Game.objects.select_for_update().get(game_id=game_id)
			if (G.question=="" or ques==""):
				op = random.randint(1,3);
				high=100;
				if (op==3):
					high=15
				a = random.randint(1,high);
				b = random.randint(1,high);
				answer=10
				if (op==1):
					c='+'
					answer=a+b
				elif (op==2):
					c='-'
					answer=a-b
				else:
					c='*'
					answer=a*b
				question = "What is "+str(a)+str(c)+str(b)+"?"
				G.question = question
				G.answer=answer
				G.rounds_over+=1
				G.save()
	else:
		question = G.question
		answer=G.answer
	players = list(G.player_set.all());
	players.sort(key = lambda x: x.wins, reverse = True)
	if (len(players)>5):
		players=players[:5]
	if (G.rounds<=100):
		rounds_left=G.rounds-G.rounds_over
		return render(request,"game.html",{"name": name, "game_id": game_id, "wins": wins, "question": question, "answer": answer, "players": players, "rounds": rounds_left+1} );
	else:
		seconds_left=G.seconds-G.seconds_over
		return render(request,"game.html",{"name": name, "game_id": game_id, "wins": wins, "question": question, "answer": answer, "players": players, "seconds": seconds_left} );

def game_arena (request,game_hash):
	gm_hash = game_hash.split("&")
	print (gm_hash)
	name=gm_hash[0]
	game_id = gm_hash[1]
	G=models.Game.objects.get(game_id=game_id)
	if (G.rounds_over>0):
		return render(request,"garena.html",{"error": "NO SUCH GAME PRESENT!!"})
	creator=False
	if (len(gm_hash)>2):
		if (gm_hash[2]=="Create"):
			creator=True
	return render (request,"garena.html",{"name": name, "game_id": game_id, "creator": creator} );
