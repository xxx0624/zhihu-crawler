from Queue import Queue


user_id_queue = Queue()

def put_user(user_id):
	user_id_queue.put(user_id)

def get_user():
	import main
	if user_id_queue.qsize()>0 and main.mylock_queue.locked()==False:
		main.mylock_queue.acquire()
		userid = user_id_queue.get()
		main.mylock_queue.release()
		return userid

def q_size():
	return user_id_queue.qsize()