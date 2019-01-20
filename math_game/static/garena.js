function send_request()
{
	$("#hidden_form").submit()
}
	
function check_game()
{
	console.log(game_id)
	$.ajaxSetup({
		headers: {"X-CSRFToken": csrf_token }
	});
	$.ajax({
		url: "/check_game/",
		type: "POST",
		data: {
				"game_id": game_id,
			},
		datatype: "json",
		success: function (resp){
			var flag = resp.flag;
			if (flag=="yes")
			{
				send_request()
			}
			else 
			{
				$("#plist").html("")
				for (var p in resp.player_list)
				{
					$("#plist").append("<li>"+resp.player_list[p]+"</li>")
				}
			}
		}
	});
}

setInterval(check_game,1000);
