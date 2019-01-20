$("#answer").val('')
$("#answer").focus()

function update_time()
{
	$.ajaxSetup({
			headers: {"X-CSRFToken": csrf_token }
		});
	$.ajax({
			url: "/update_time/",
			type: "POST",
			data: JSON.stringify({
					"game_id": game_id,
			}),
			datatype: "json",
			success: function(response){
				var sec = response.sec;
				if (sec=="yes"){
					var flag = response.flag;
					if (flag=="yes")
					{
						$("#hidden_form").submit()
					}
					var seconds = Number(response.seconds)
					var minutes = Math.floor(seconds/60)
					var am = Math.floor(minutes/10)
					var bm = minutes%10
					var as = Math.floor((seconds%60)/10)
					var bs = (seconds%60)%10
					$("#seconds").html("TIME LEFT: "+am+bm+":"+as+bs);
				}
			}
		});
}
setInterval(update_time,1000);
$("#submit").click(function(){
	var user_answer = $("#answer").val()
	if (user_answer==answer)
	{
		$.ajaxSetup({
			headers: {"X-CSRFToken": csrf_token }
		});
		$.ajax({
			url: "/update_winner/",
			type: "POST",
			data: JSON.stringify({
					"game_id": game_id,
					"name": name,
			}),
			datatype: "json",
			success: function(response){
				var flag = response.flag;
				if (flag=="yes"){
					wins=Number(wins) + 1
					$("#wins").html("WINS: "+wins)
				}
			}
		});
	}
	else
	{
		$("#prompt").html("Wrong Answer. Try Again!!");
	}
		$("#answer").val('')
		$("#answer").focus()
})
ans = document.getElementById("answer");
ans.addEventListener("keyup", function(event) {
	event.preventDefault();
	if (event.keyCode==13) {
		$("#submit").click()
		
	}
});

var start;
var milliseconds;
var check_win_id;
var sleep_id;
function sleep  ()
{
	console.log(start)
	console.log(milliseconds);
	if ((new Date().getTime() - start)>milliseconds)
		clearInterval (sleep_id);
		$("#hidden_form").submit()
}

function check_win ()
{
	$.ajaxSetup({
			headers: {"X-CSRFToken": csrf_token }
		});
	$.ajax({
			url: "/check_win/",
			type: "POST",
			data: JSON.stringify({
					"game_id": game_id,
					"name": name,
			}),
			datatype: "json",
			success: function(response){
				var flag = response.flag;
				if (flag=="yes"){
					var pname = response.player_name;
					if (name!=pname)
						$("#prompt").html("Sorry!! " + pname + " already won!! Loading next Game in 3 seconds!!")
					else 
						$("#prompt").html("Congrats!! You Win!! Loading next Game in 3 seconds!!")
					$("#wins_input").val(wins)	
					start = new Date().getTime();
					milliseconds=2000;
					clearInterval(check_win_id);
					sleep_id=setInterval(sleep,1000);
				}
			}
		});
}
check_win_id = setInterval(check_win,1000);
