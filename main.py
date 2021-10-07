import pygame, sys, math 

pygame.init()
WIDTH,HEIGHT = 900,700
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
WELCOME_SCREEN_BG_COLOR = (0,0,0)
BG_COLOR = (0,0,0)

LOCUS = None 

#defining the option boxes class 
class Option_box:
	def __init__(self,x,y,width,height,color,hover_color):
		self.x,self.y = x,y
		self.width = width
		self.height = height
		self.color = color
		self.hover_color = hover_color 

	def draw(self,m_pos,display_text,text_size,text_color):
		if self.x+self.width>=m_pos[0]>=self.x and self.y+self.height>=m_pos[1]>=self.y :
			self.current_color = self.hover_color
		else:
			self.current_color =self.color

		self.display_text = pygame.font.Font("freesansbold.ttf",text_size).render(display_text,True,text_color)

		pygame.draw.rect(SCREEN,self.current_color,pygame.Rect(self.x,self.y,self.width,self.height))
		SCREEN.blit(self.display_text,(self.x,self.y))

	def clicked(self,m_pressed):
		if True in m_pressed and self.current_color == self.hover_color:
			return True
		return False 



#defining the welcome screen class 
class welcome_screen:
	def __init__(self):
		global WELCOME_SCREEN_BG_COLOR,BG_COLOR,LOCUS

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
					pygame.quit()
					sys.exit()

			#mouse position and mouse pressed
			self.m_pos,self.m_pressed = pygame.mouse.get_pos(),pygame.mouse.get_pressed()

			#buttons 
			circle_btn = Option_box(10,5,100,50,(0,128,128),(0,255,255))
			parabola_btn = Option_box(125,5,100,50,(0,128,128),(0,255,255))
			light_mode_btn = Option_box(310,HEIGHT//2,125,75,(200,200,200),(220,220,220))
			dark_mode_btn = Option_box(440,HEIGHT//2,125,75,(70,70,70),(30,30,30))


			SCREEN.fill(WELCOME_SCREEN_BG_COLOR)
			circle_btn.draw(self.m_pos,"Circle",25,(30,30,30))
			parabola_btn.draw(self.m_pos,"Parabola",20,(30,30,30))
			light_mode_btn.draw(self.m_pos,"Light Mode",20,(40,40,40))
			dark_mode_btn.draw(self.m_pos,"Dark Mode",20,(240,240,240))

			if light_mode_btn.clicked(self.m_pressed):
				BG_COLOR = (255,255,255)
				WELCOME_SCREEN_BG_COLOR = (255,255,255)
			elif dark_mode_btn.clicked(self.m_pressed):
				BG_COLOR = (0,0,0)
				WELCOME_SCREEN_BG_COLOR = (0,0,0)

			if circle_btn.clicked(self.m_pressed):
				LOCUS = 'circle'
				break
			elif parabola_btn.clicked(self.m_pressed):
				LOCUS = 'parabola'
				break

			pygame.display.update()



#defining the pointer which will point at the locus
class Pointer:
	def __init__(self):
		global BG_COLOR
		
		self.radius = 10
		if BG_COLOR == (0,0,0):
			self.color = (255,0,0)
		else:
			self.color = (0,130,0) 

		if LOCUS == "circle":
			self.circle_radius = 150
			self.current_angle = 0 
			self.center = [WIDTH//2,HEIGHT//2]
			if BG_COLOR == (0,0,0):
				self.circle_line_color = (0,255,255)
			else:
				self.circle_line_color = (0,0,0)

	def draw(self,x,y):

		if LOCUS == "circle": 
			pygame.draw.circle(SCREEN, (255,0,255), (self.center[0],self.center[1]), self.circle_radius) 
			pygame.draw.circle(SCREEN, BG_COLOR, (self.center[0],self.center[1]), self.circle_radius-2) 
			pygame.draw.line(SCREEN, self.circle_line_color, (self.center[0],self.center[1]), (x,y))

		elif LOCUS == "parabola":
			prev_temp_x,prev_temp_y = 200,HEIGHT-50 			
			temp_x,temp_y = 200,HEIGHT-50 
			temp_y_dis = -20 
			while(temp_y<=HEIGHT-50):
				pygame.draw.line(SCREEN,(255,0,255),(prev_temp_x,prev_temp_y), (temp_x,temp_y))
				prev_temp_x,prev_temp_y = temp_x,temp_y
				temp_x += 5
				temp_y += temp_y_dis
				temp_y_dis += 0.4

		pygame.draw.circle(SCREEN, self.color, (x,y), self.radius) 

	def circle_locus(self):
		x = self.center[0]+self.circle_radius*math.cos(self.current_angle/57.2958)
		y = self.center[1]+self.circle_radius*math.sin(self.current_angle/57.2958)
		self.current_angle += 1

		return(x,y)

	def parabola_locus(self,x,y,y_dis,pointer_direction):
		if pointer_direction == "forward": 
			x +=  5
			y += y_dis
			y_dis += 0.4
			if y > HEIGHT - 50 :
				y = HEIGHT - 50 
				pointer_direction = "backward"
				y_dis = 20 
		else:
			x -= 5
			y -= y_dis
			y_dis -= 0.4

			if y > HEIGHT - 50 :
				y = HEIGHT - 50
				pointer_direction = "forward"
				y_dis = -20

		print(pointer_direction)

		return(x,y,y_dis,pointer_direction) 




if __name__ == "__main__":
	welcome_screen()

	pointer = Pointer()
	if LOCUS == "parabola":
		x = 200
		y = HEIGHT - 50
		y_dis = -20
		fps = 25
		pointer_direction = "forward"
	elif LOCUS == "circle":
		fps = 100

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()

		if LOCUS == "circle": 
			x,y = pointer.circle_locus()
		elif LOCUS == "parabola":
			x,y,y_dis,pointer_direction = pointer.parabola_locus(x,y,y_dis,pointer_direction)

		SCREEN.fill(BG_COLOR)
		pointer.draw(x,y)

		pygame.time.Clock().tick(fps)
		pygame.display.update()





