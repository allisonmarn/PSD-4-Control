import tkinter, time, serial

### parameters
COM='COM7'
minutes=10
###
CR = chr(13)
syringe_pos=6000
s=None
count=0
pbs_amount=3000
incubation_time = minutes*60*1000 #in microseconds
initial_push = 4200 # geting the bacteria to the chip
experiment_duration = 60
pushes = experiment_duration/minutes

top = tkinter.Tk()
top.title('Pump Control')
top.geometry('200x250') # Size 200, 200

def initPump():
	global s
	global COM
	s = serial.Serial()
	s.baudrate=9600
	s.port=COM
	s.open()
	if (s.isOpen()):
		print("Pump is Initialized")
		#Enable h Factor Commands and Queries
		command = "/1h30001R"+CR 
		s.write(command.encode())
		time.sleep(1)
		command = "/1h20000R"+CR  #Initialize Valve
		s.write(command.encode())
		time.sleep(1)
		command = "/1h10010R"+CR #Initialize Syringe Only Initialize Syringe initializes the syringe. 10,000 + speed code
		s.write(command.encode())
		time.sleep(1)
	else:
		print("Pump not Initialized")

def start():
	global syringe_pos
	global incubation_time
	global pushes
	global count
	if (syringe_pos <= 6000) and (syringe_pos >= 50) and (count < pushes):
		syringe_pos=syringe_pos-50
		print(str(syringe_pos))
		command="/1A"+str(syringe_pos)+"R"+CR
		s.write(command.encode())
		count=count+1
		top.after(incubation_time, start)
	else:
		print("Experiment Done")

def stop():
	global s
	if s is not None:
		s.close()
	print ("Stop")
	
def pushPBS():
	print("PBS")
	global syringe_pos
	global pbs_amount
	command="/1S11R"+CR #speed 11
	s.write(command.encode())
	time.sleep(1)
	command="/1h27270R"+CR #valve at 270
	s.write(command.encode())
	print("valve to port 7")
	time.sleep(1)
	command="/1A"+str(pbs_amount)+"R"+CR
	s.write(command.encode())	
	time.sleep(10)
	command="/1h27045R"+CR #valve at 45 (chip)
	s.write(command.encode())
	print("valve to port 2")
	time.sleep(1)
	command="/1A"+str(0)+"R"+CR
	s.write(command.encode())	
	time.sleep(10)
	
def pushECOLI():
	global syringe_pos
	global incubation_time
	global initial_push
	print("incubation time:"+str(incubation_time))
	command="/1h27315R"+CR #valve at 315
	s.write(command.encode())
	print("valve to port 8")
	time.sleep(1)
	command="/1A"+str(syringe_pos)+"R"+CR
	s.write(command.encode())	
	time.sleep(10)
	command="/1h27045R"+CR #valve at 45 (chip)
	s.write(command.encode())
	print("valve to port 2")
	time.sleep(1)	
	syringe_pos=initial_push
	command="/1A"+str(syringe_pos)+"R"+CR
	s.write(command.encode())
	time.sleep(10)
	command="/1S40R"+CR #speed 40
	s.write(command.encode())	
	time.sleep(2)
	
def wash():
	command="/1h27315R"+CR #valve at 315
	s.write(command.encode())
	time.sleep(2)
	print("valve to port 8")
	command="/1S11R"+CR #speed 11
	s.write(command.encode())
	time.sleep(1)
	command="/1A"+str(0)+"R"+CR
	s.write(command.encode())	
	time.sleep(10)
	command="/1h27270R"+CR #valve at 270
	s.write(command.encode())
	print("valve to port 7")
	time.sleep(1)
	command="/1A"+str(pbs_amount)+"R"+CR
	s.write(command.encode())	
	time.sleep(10)
	command="/1h27045R"+CR #valve at 45 (chip)
	s.write(command.encode())
	print("valve to port 2")
	time.sleep(1)
	command="/1S40R"+CR #speed 40
	s.write(command.encode())	
	time.sleep(2)
	command="/1A"+str(0)+"R"+CR
	s.write(command.encode())	
	time.sleep(10)
	

initializeButton= tkinter.Button(top, height=2, width=20, text ="Initialize Pump", command = initPump)
pbsButton= tkinter.Button(top, height=2, width=20, text ="Push PBS", command = pushPBS)
ecoliButton= tkinter.Button(top, height=2, width=20, text ="Push First E. Coli", command = pushECOLI)
startButton = tkinter.Button(top, height=2, width=20, text ="Start Experiment", command = start)
stopButton = tkinter.Button(top, height=2, width=20, text ="Stop", command = stop)
washButton = tkinter.Button(top, height=2, width=20, text ="Wash", command = wash)

initializeButton.pack()
pbsButton.pack()
ecoliButton.pack()
startButton.pack()
stopButton.pack()
washButton.pack()
top.mainloop()