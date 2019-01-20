from django.conf.urls import url,include
from . import views
urlpatterns = [
	url(r'^$',views.index,name="index"),
	url('^check_game/$',views.check_game,name="check_game"),
	url('^create_game/$',views.create_game,name="create_game"),
	url('^join_game/$',views.join_game,name="join_game"),
	url('^start_game/$',views.start_game,name="start_game"),
	url('^game_arena/(?P<game_hash>[A-Za-z0-9\&\.\+_-]*)',views.game_arena,name="game_arena"),
	url('^check_win/$',views.check_win,name="check_win"),
	url('^update_winner/$',views.update_winner,name="update_winner"),
	url('^update_time/$',views.update_time,name="update_time"),
]
