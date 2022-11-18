import random
import cv2
from keras.models import load_model
import numpy as np
model = load_model('keras_model.h5')
cap = cv2.VideoCapture(-1)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
import time

choice_list = ['r', 'p', 's']
print('test')
class play_RPS:

    def __init__(self, choice_list):
        self.ComputerChoice = choice_list[random.randint(0, len(choice_list)-1)]
        self.ComputerScore = 0
        self.userScore = 0
        self.get_prediction

    def computerchoice(self):
        return choice_list[random.randint(0, len(choice_list)-1)]
    
    def check_winner(self, user_choice):
        if (user_choice == self.ComputerChoice)[0]:
            print('This is a draw! You both chose {}.'.format(self.ComputerChoice))
        else:
            if user_choice == 'r':
                if self.ComputerChoice == 's':
                    print('You win! They chose {}'.format(self.ComputerChoice))
                    self.userScore += 1
                else:
                    print('You lose! The computer wins HAHA. They chose {}'.format(self.ComputerChoice))
                    self.ComputerScore += 1
            elif user_choice == 'p':
                if self.ComputerChoice == 'r':
                    print('You win! They chose {}'.format(self.ComputerChoice))
                    self.userScore += 1
                else:
                    print('You lose! The computer wins HAHA. They chose {}'.format(self.ComputerChoice))
                    self.ComputerScore += 1                
            elif user_choice == 's':
                if self.ComputerChoice == 'p':
                    print('You win! They chose {}'.format(self.ComputerChoice))
                    self.userScore += 1
                else:
                    print('You lose! The computer wins HAHA. They chose {}'.format(self.ComputerChoice))
                    self.ComputerScore += 1
    
    def get_prediction(self):
        flag = False
        while True: 
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = model.predict(data)
            if prediction[0][0] > 0.5:
                user_choice = 'r'
            elif prediction[0][1] > 0.5:
                user_choice = 'p'
            elif prediction[0][2] > 0.5:
                user_choice = 's'
            else:
                user_choice = 'n'
            cv2.imshow('frame', frame)


            print(prediction)
            if cv2.waitKey(1) & 0xFF == ord('f') and flag == False:
                flag = True
                start_time = time.time()
            if flag == True:
                end_time = 5 - (time.time() - start_time)
                cv2.putText(frame, str(int(end_time)), (50, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (10, 0, 0), 3, cv2.LINE_4)
                cv2.imshow('Timer', frame)
                if end_time <= 0:
                    if user_choice == 'n':
                        start_time = time.time()
                        flag = False
                        cv2.destroyAllWindows
                    else:
                        break

        # After the loop release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

    def get_user_choice(self):
        user_choice = input('Please press r = rock, p = paper, s = scissors')
        while True:
            if not user_choice in choice_list:
                continue
            else:
                break
        self.check_winner(user_choice)

def play(choice_list):
    game = play_RPS(choice_list)
    game.get_prediction()

    while True:
        if game.userScore == 3:
            print('You win!')
            break
        if game.ComputerScore == 3:
            print('Computer wins!')
            break
        else:
            continue

if __name__ == '__main__':
    choice_list = ['r', 'p', 's']
    play(choice_list)