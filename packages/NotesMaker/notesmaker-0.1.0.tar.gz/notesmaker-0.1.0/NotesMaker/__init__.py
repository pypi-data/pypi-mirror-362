import winsound as ws
import threading as th

base_note = 329.63
def playNote(note):
	global base_note
	th.Thread(target=lambda: ws.Beep(int((base_note * (2 ** (note /12))) // 1), 500)).start()

if __name__ == '__main__':
	while True:
		try:
			note = int(input("Enter Note + or - from E4:    "))
			print(base_note * (2 ** (note /12)))
			playNote(note)
		except:
			pass