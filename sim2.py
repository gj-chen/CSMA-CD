# project 2 part 2

import random
import simpy
import math

RANDOM_SEED = 29
SIM_TIME = 1000000
MU = 1

collision = 0 

""" Queue system  """		
class server_queue:
	def __init__(self, env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs):
		self.server = simpy.Resource(env, capacity = 1)
		self.env = env
		self.queue_len = 0 #L 
		self.flag_processing = 0
		self.packet_number = 0 
		self.sum_time_length = 0
		self.start_idle_time = 0
		self.arrival_rate = arrival_rate
		self.Packet_Delay = Packet_Delay
		self.Server_Idle_Periods = Server_Idle_Periods
		self.slot = host_current_slot #S 
		self.n = host_num_backoffs #N 
		

	def set_slot(self, host_current_slot):
		self.slot = host_current_slot

	def get_slot(self): 
		return self.slot 

	def set_backoff(self, host_num_backoffs): 
		self.n = host_num_backoffs

	def get_backoff(self): 
		return get_backoff 

	def calculate_backoff(self, current_slot):
		k = min(self.host_num_backoffs, 1024) 
		random_number = randint(0, 1) #random value between 0 and 1 
		delay_value = pow(2, self.n) * random_number
		self.slot = self.slot + 1 + delay_value 
		self.n = self.n + 1 



	def process_packet(self, env, packet):
		with self.server.request() as req:
			start = env.now
			yield req
			yield env.timeout(random.expovariate(MU))
			latency = env.now - packet.arrival_time
			self.Packet_Delay.addNumber(latency)
			#print("Packet number {0} with arrival time {1} latency {2}".format(packet.identifier, packet.arrival_time, latency))
			if collision == 0:
				self.queue_len -= 1
			
			if self.queue_len == 0:
				self.flag_processing = 0
				self.start_idle_time = env.now
				
	def packets_arrival(self, env):
		# packet arrivals 
		
		while True:
		     # Infinite loop for generating packets
			yield env.timeout(random.expovariate(self.arrival_rate))
			  # arrival time of one packet

			self.packet_number += 1
			  # packet id
			arrival_time = env.now  
			#print(self.num_pkt_total, "packet arrival")
			new_packet = Packet(self.packet_number,arrival_time)
			if self.flag_processing == 0:
				self.flag_processing = 1
				idle_period = env.now - self.start_idle_time
				self.Server_Idle_Periods.addNumber(idle_period)
				
				#print("Idle period of length {0} ended".format(idle_period))
			self.queue_len += 1
			env.process(self.process_packet(env, new_packet))
	

""" Packet class """			
class Packet:
	def __init__(self, identifier, arrival_time):
		self.identifier = identifier
		self.arrival_time = arrival_time
		

def main():
	host_current_slot = 1 
	host_num_backoffs = 0 
	current_slot = 1 #will be our total number of slots 


	random.seed(RANDOM_SEED)
	for arrival_rate in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]:
		env = simpy.Environment()
		
		Host1 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host2 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host3 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host4 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host5 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host6 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host7 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host8 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host9 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		Host10 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs)
		
		env.process(Host1.packets_arrival(env))
		env.process(Host2.packets_arrival(env))
		env.process(Host3.packets_arrival(env))
		env.process(Host4.packets_arrival(env))
		env.process(Host5.packets_arrival(env))
		env.process(Host6.packets_arrival(env))
		env.process(Host7.packets_arrival(env))
		env.process(Host8.packets_arrival(env))
		env.process(Host9.packets_arrival(env))
		env.process(Host10.packets_arrival(env))

		list_of_slot = [[Host1.get_slot(), '1'], [Host2.get_slot(), '2'], [Host3.get_slot(), '3'], [Host4.get_slot(), '4'], [Host5.get_slot(), '5'],[Host6.get_slot(), '6'], [Host7.get_slot(), '7'][Host8.get_slot(), '8'], [Host9.get_slot(), '9'], [Host10.get_slot(), '10']] 

		counter = 0 
		collision = 0
		for lst in list_of_slot:
			for x in lst:
				if(isinstance(x,int)):
					if x == current_slot: 
						counter += 1 

		for lst in list_of_slot:
			for x in lst:
				if(isinstance(x, str) and  counter > 1):
					collision = 1
					#Host 1 apply backoff algorithm 
					# calculate new delay time 
					if(x == '1'):
						Host1.calculate_backoff(current_slot)
					if(x == '2'):
						Host2.calculate_backoff(current_slot)
					if(x == '3'):
						Host3.calculate_backoff(current_slot)
					if(x == '4'):
						Host4.calculate_backoff(current_slot)
					if(x == '5'):
						Host5.calculate_backoff(current_slot)
					if(x == '6'):
						Host6.calculate_backoff(current_slot)
					if(x == '7'):
						Host7.calculate_backoff(current_slot)	
					if(x == '8'):
						Host8.calculate_backoff(current_slot)
					if(x == '9'):
						Host9.calculate_backoff(current_slot)
					if(x == '10'):
						Host10.calculate_backoff(current_slot)
				if collision == 0: 
				#process packet 
				#increment slot number
				#set n = 0 





		#increment current slot



		env.run(until=SIM_TIME)

	
if __name__ == '__main__': main()