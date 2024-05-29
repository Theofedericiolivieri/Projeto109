import cv2
import math
import mediapipe as mp
from pynput.mouse import Button, Controller
import pyautogui
mouse=Controller()
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
(screen_width, screen_height) = pyautogui.size()
mp_hands = mp_solutions.hands
mp_drawing = mp_solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
tipIds = [4, 8, 12, 16, 20]
pinch=False
# Defina uma função para contar os dedos
def countFingers(image, hand_landmarks, handNo=0):
    global pinch
    if hand_landmarks:
        # Obtenha todos os pontos de referência da PRIMEIRA mão VÍSIVEL
        landmarks = hand_landmarks[handNo].landmark
        # Conte os dedos
        fingers = []
        for lm_index in tipIds:
            # Obtenha os valores y da ponta e da parte inferior do dedo
            finger_tip_y = landmarks[lm_index].y
            finger_bottom_y = landmarks[lm_index - 2].y
            # Verifique se ALGUM DEDO está ABERTO ou FECHADO
            if lm_index !=4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)
                if finger_bottom_y < finger_tip_y:
                    fingers.append(0)
        totalFingers = fingers.count(1)
        # PINÇA
        # Desenhe uma LINHA entre a PONTA DO DEDO e a PONTA DO POLEGAR
        finger_tip_x = int((landmarks[8].x)*width)
        finger_tip_y = int((landmarks[8].y)*height)
        thumb_tip_x = int((landmarks[4].x)*width)
        thumb_tip_y = int((landmarks[4].y)*height)
        cv2.line(image, (finger_tip_x, finger_tip_y),(thumb_tip_x, thumb_tip_y),(255,0,0),2)
        # Desenhe um CÍRCULO no CENTRO da LINHA entre a PONTA DO DEDO e a PONTA DO POLEGAR
        center_x = int((finger_tip_x + thumb_tip_x)/2)
        center_y = int((finger_tip_y + thumb_tip_y)/2)
        cv2.circle(image,(center_x, center_y), 2, (0,0,255), 2)
        # Calcule a DISTÂNCIA entre a PONTA DO DEDO e a PONTA DO POLEGAR
        distance = math.sqrt(((finger_tip_x - thumb_tip_x)**2) + ((finger_tip_y - thumb_tip_y)**2))
        # print("Distância: ", distance)
        print("Tamanho da Tela do Computador:",screen_width, screen_height, "Tamanho da Janela de Resultado: ", width, height)
        print("Posição do Mouse: ", mouse.position, "PPosição Central da Linha das Pontas: ", center_x, center_y)
        # Defina a posição do mouse na tela em relação ao tamanho da janela de resultado	
		relative_mouse_x = (center_x/width)*screen_width
		relative_mouse_y = (center_y/height)*screen_height
		mouse.position = (relative_mouse_x, relative_mouse_y)
		# Verifique as condições de formação da PINÇA
		if distance > 40:
			if pinch == True:
				pinch = False			
				mouse.release(Button.left)
		if distance <= 40 :
			if(pinch==False):
				pinch=True
				mouse.press(Button.left)
# Defina uma função para 
def drawHandLanmarks(image, hand_landmarks):
    # Desenhar as conexões entre os pontos de referência
    if hand_landmarks:
      for landmarks in hand_landmarks:  
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
while True:
	success, image = cap.read()