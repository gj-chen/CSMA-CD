# project 2 part 2
#Linear Backoff Algorithm 
#Gloria #997529775 
#Tsz Kit Lo #912404574

import random
import simpy
import math

RANDOM_SEED = 29
SIM_TIME = 1000000
MU = 1


""" Queue system  """		
class server_queue:
	def __init__(self, env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, collision):
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
		self.collision = collision
		

	def set_slot(self, host_current_slot):
		self.slot = host_current_slot

	def get_slot(self): 
		return self.slot 

	def set_backoff(self, host_num_backoffs): 
		self.n = host_num_backoffs

	def get_backoff(self): 
		return get_backoff 

	def calculate_backoff(self, current_slot):
		k = min(self.n, 1024) 
		#k = self.n
		#random_number = random.randint(0, 1) #random value between 0 and 1 
		delay_value = random.randint(0, k) 
		self.slot = self.slot + 1  + delay_value 
		self.n = self.n + 1 
		#print ("self.slot value %d" % self.slot)
	def set_collision(self, collision):
		self.collision = collision


	def process_packet(self, env, packet):
		with self.server.request() as req:
			start = env.now
			yield req
			yield env.timeout(random.expovariate(MU))
			latency = env.now - packet.arrival_time
			self.Packet_Delay.addNumber(latency)
			#self.Packet_Delay = int(latency) 

			if self.collision == 0:
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
				idle_period = arrival_time - self.start_idle_time
				self.Server_Idle_Periods.addNumber(idle_period)
				#self.Server_Idle_Periods = idle_period
				#print("Idle period of length {0} ended".format(idle_period))
			self.queue_len += 1
			env.process(self.process_packet(env, new_packet))

class simulation:
	def __init__(self,env,list_of_host,result):
		self.env = env
		self.list_of_host = list_of_host
		self.result = result
	def run_process(self,env,list_of_host, result):
		current_slot = 1 #will be our total number of slots 
		successful_slot = 0 #count the number of succuessful transmission
		collisions = 0 

		while True:
			yield env.timeout(1)
				
			list_of_slot = [list_of_host[0].get_slot(), list_of_host[1].get_slot(), list_of_host[2].get_slot(), list_of_host[3].get_slot(), list_of_host[4].get_slot(), list_of_host[5].get_slot(), list_of_host[6].get_slot(), list_of_host[7].get_slot(), list_of_host[8].get_slot(), list_of_host[9].get_slot()] 
			counter = 0 

			temp_slot_pos = 0 # store the position of slot
			first_hit_slot_pos = 0
			flag = 0
			

			for i in range(0,len(list_of_slot)): 
				if list_of_slot[i] == current_slot: #count the number of hit 
					counter += 1
					temp_slot_pos =  i
					if counter == 1:
						first_hit_slot_pos = i
						flag = 1
				if list_of_slot[i] == current_slot and counter > 1:
					#print("inside collision conditional")
					# apply backoff algorithm if collision occur
					# calculate new delay time 
					collisions += 1 
					if i == 0 :
						list_of_host[0].calculate_backoff(current_slot)
						list_of_host[0].set_collision(1)
					elif i == 1:
						list_of_host[1].calculate_backoff(current_slot)
						list_of_host[1].set_collision(1)
					elif i == 2:
						list_of_host[2].calculate_backoff(current_slot)
						list_of_host[2].set_collision(1)
					elif i == 3:
						list_of_host[3].calculate_backoff(current_slot)
						list_of_host[3].set_collision(1)
					elif i == 4:
						list_of_host[4].calculate_backoff(current_slot)
						list_of_host[4].set_collision(1)
					elif i == 5:
						list_of_host[5].calculate_backoff(current_slot)
						list_of_host[5].set_collision(1)
					elif i == 6:
						list_of_host[6].calculate_backoff(current_slot)
						list_of_host[6].set_collision(1)
					elif i == 7:
						list_of_host[7].calculate_backoff(current_slot)
						list_of_host[7].set_collision(1)
					elif i == 8:
						list_of_host[8].calculate_backoff(current_slot)
						list_of_host[8].set_collision(1)
					else:
						list_of_host[9].calculate_backoff(current_slot)
						list_of_host[9].set_collision(1)
					#print("leaves collision conditional")
			
			if flag == 1 and counter > 1:
				list_of_host[first_hit_slot_pos].calculate_backoff(current_slot)
				list_of_host[first_hit_slot_pos].set_collision(1)
				collisions += 1

			if counter == 1: #no collision
				#print("inside counter == 1")
				successful_slot += 1
				if temp_slot_pos == 0:
					# process packet
					list_of_host[0].set_slot(current_slot + 1)
					list_of_host[0].set_backoff(0)
					list_of_host[0].set_collision(0)
				elif temp_slot_pos == 1:
					list_of_host[1].set_slot(current_slot + 1)
					list_of_host[1].set_backoff(0)
					list_of_host[1].set_collision(0)
				elif temp_slot_pos == 2:
					list_of_host[2].set_slot(current_slot + 1)
					list_of_host[2].set_backoff(0)
					list_of_host[2].set_collision(0)
				elif temp_slot_pos == 3:
					list_of_host[3].set_slot(current_slot + 1)
					list_of_host[3].set_backoff(0)
					list_of_host[3].set_collision(0)
				elif temp_slot_pos == 4:
					list_of_host[4].set_slot(current_slot + 1)
					list_of_host[4].set_backoff(0)
					list_of_host[4].set_collision(0)
				elif temp_slot_pos == 5:
					list_of_host[5].set_slot(current_slot + 1)
					list_of_host[5].set_backoff(0)
					list_of_host[5].set_collision(0)
				elif temp_slot_pos == 6:
					list_of_host[6].set_slot(current_slot + 1)
					list_of_host[6].set_backoff(0)
					list_of_host[6].set_collision(0)
				elif temp_slot_pos == 7:
					list_of_host[7].set_slot(current_slot + 1)
					list_of_host[7].set_backoff(0)
					list_of_host[7].set_collision(0)
				elif temp_slot_pos == 8:
					list_of_host[8].set_slot(current_slot + 1)
					list_of_host[8].set_backoff(0)
					list_of_host[8].set_collision(0)
				else:
					list_of_host[9].set_slot(current_slot + 1)
					list_of_host[9].set_backoff(0)
					list_of_host[9].set_collision(0)

			list_of_host[0].packets_arrival(env)
			list_of_host[1].packets_arrival(env)
			list_of_host[2].packets_arrival(env)
			list_of_host[3].packets_arrival(env)
			list_of_host[4].packets_arrival(env)
			list_of_host[5].packets_arrival(env)
			list_of_host[6].packets_arrival(env)
			list_of_host[7].packets_arrival(env)
			list_of_host[8].packets_arrival(env)
			list_of_host[9].packets_arrival(env)


			#increment slot number
			current_slot += 1
			#print("counter value")
			#print counter

			throughput = float(successful_slot)/float(current_slot)
			#print("number of collisions %d" % collisions)
			#print("succesful slots")
			#print successful_slot
			#print("curent slots")
			#print current_slot
			#print("throughput")
			#print throughput
			result.set_throughput(throughput)

class store_result:
	def __init__(self):
		self.throughput = 0
	def set_throughput(self,throughput):
		self.throughput = throughput
	def get_throughput(self):
		return self.throughput

""" Packet class """			
class Packet:
	def __init__(self, identifier, arrival_time):
		self.identifier = identifier
		self.arrival_time = arrival_time
	

class StatObject:
    def __init__(self):
        self.dataset =[]

    def addNumber(self,x):
        self.dataset.append(x)
    def sum(self):
        n = len(self.dataset)
        sum = 0
        for i in self.dataset:
            sum = sum + i
        return sum
    def mean(self):
        n = len(self.dataset)
        sum = 0
        for i in self.dataset:
            sum = sum + i
        return sum/n
    def maximum(self):
        return max(self.dataset)
    def minimum(self):
        return min(self.dataset)
    def count(self):
        return len(self.dataset)
    def median(self):
        self.dataset.sort()
        n = len(self.dataset)
        if n//2 != 0: # get the middle number
            return self.dataset[n//2]
        else: # find the average of the middle two numbers
            return ((self.dataset[n//2] + self.dataset[n//2 + 1])/2)
    def standarddeviation(self):
        temp = self.mean()
        sum = 0
        for i in self.dataset:
            sum = sum + (i - temp)**2
        sum = sum/(len(self.dataset) - 1)
        return math.sqrt(sum)

def main():
	


	random.seed(RANDOM_SEED)
	for arrival_rate in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]:

		host_current_slot = 1 
		host_num_backoffs = 0 
		

		env = simpy.Environment()
		Packet_Delay = StatObject()
		Server_Idle_Periods = StatObject()
		
		Host1 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host2 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host3 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host4 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host5 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host6 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host7 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host8 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host9 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)
		Host10 = server_queue(env, arrival_rate, Packet_Delay, Server_Idle_Periods, host_current_slot, host_num_backoffs, 1)

		result = store_result()

		list_of_host = [Host1,Host2,Host3,Host4,Host5,Host6,Host7,Host8,Host9,Host10]
		sim = simulation(env,list_of_host, result)
		env.process(sim.run_process(env, list_of_host, result))		
		env.run(until=SIM_TIME)

		print ("Lambda Value: %f" % arrival_rate)
		print ("Throughput: %f" % result.get_throughput())


	
if __name__ == '__main__': main()
