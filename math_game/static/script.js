console.log (csrf_token);
var player_name="";
var name = prompt("Enter your name");
function check_if_over ()
{
	if (player_name==name)
		alert("You Win!!!");
	$.ajaxSetup({
        headers: { "X-CSRFToken": csrf_token }
    });
	$.ajax({
		url: "/win_or_not/",
		type: "POST",
		data: JSON.stringify({ 
				"player_name": name,
			  }),
		datatype: "json",
		success: function (resp){
			var  flag = resp.flag;
			var player_name = resp.player_name;
			if (flag=="yes")
			{
				if (player_name==name)
					alert("You Win!!!");
				else
					alert(player_name + "Win!!");
			}
		}
	});
}

	
$("#submit").click(function(){
	setInterval(check_if_over,1000);
		
		/*$.ajax({
			url: "/check_answer",
			type: "POST",
			data: answer,
			datatype: "json",
			success: function (resp) {
				var result = resp.result;
				if (result=="correct")
				{
					$.ajax({
						url: "/update_winner"
						type: "POST",
						data: name,
						datatype: "json",
						success: function (resp){
						}
					});
				}
				else 
				{
					alert("Your answer is incorrect")
				}
			}
		});*/
});
