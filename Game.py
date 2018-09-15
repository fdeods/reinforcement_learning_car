import os
import pygame
import sys
from math import tan, radians, degrees, sin, cos

from Car import *
from Track import Track
from Config import *
from utils import message_to_screen, map_distances_to_colors
from learner import *
from policy import *
from logger import *
from state import State

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car learning")
        self.screen = pygame.display.set_mode((display_width, display_height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        self.car_image = pygame.image.load(image_path)

        self.car = None
        self.track = None
        self.learner = None
        self.logger = None

        self.points = 0
        self.crashed = False

    def reset_game(self, car_class, start_pos):
        self.points = 0
        self.car = car_class(start_pos)

    def nonStopCarRun(self):
        self.car_image = pygame.transform.scale(self.car_image, (car_length, car_width))
        self.reset_game(NonStopCar, self.track.start_pos)
        action = 0

        while not self.exit:
            dt = self.clock.get_time() / 500

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_RIGHT]:
                action = 1
            elif pressed[pygame.K_LEFT]:
                action = 2
            else:
                action = 0

            # Logic
            self.car.update(action)

            # Count car edges 
            (c1, c2) = self.car.position * ppu

            collision_detected = self.track.check_collision(self.car.corners)

            self.points += 1

            if self.points == winning_points:
                break

            distances = self.track.measure_intersections((c1,c2), self.car.sensors)

            if collision_detected:
                self.reset_game(NonStopCar, self.track.start_pos)
                action = 0
                self.clock.tick(self.ticks)
                continue
            
            # Drawing
            self.screen.fill((0, 0, 0))
            self.track.draw()
            rotated = pygame.transform.rotate(self.car_image, self.car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, (c1 - rect.width / 2, c2 - rect.height / 2))

            colors = map_distances_to_colors(distances)

            # draw car points
            pygame.draw.circle(self.screen, (255, 255, 255), self.car.front_point, 2)
            pygame.draw.circle(self.screen, (255, 255, 255), self.car.back_point, 2)

            for corner in self.car.corners:
                pygame.draw.circle(self.screen, (0, 0, 255), corner, 2)

            # draw sensor lines
            for i in range(len(self.car.sensors)):
                pygame.draw.line(self.screen, colors[i], (c1, c2), self.car.sensors[i])

            self.update_stats(distances, colors)

            pygame.display.flip()
            self.clock.tick(self.ticks)
        
    def nonStopCarRun_learning(self):
        self.car_image = pygame.transform.scale(self.car_image, (car_length, car_width))
        self.reset_game(NonStopCar, self.track.start_pos)
        action = 0
        prevstate = 0
        iteration = 1
        history = []
        self.logger.add_entry("Iteration = 0")

        (c1, c2) = self.car.position * ppu
        distances = self.track.measure_intersections((c1,c2), self.car.sensors)
        prevstate = State(distances, self.gran)
        prevaction = 0

        while not self.exit:
            if len(history) == number_of_probes:
                print("")
                print("level impossible")
                break

            iteration += 1

            # # Event queue
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         self.exit = True

            # # User input
            # pressed = pygame.key.get_pressed()

            # if pressed[pygame.K_r] and self.crashed == True:
            #     crashed = False
            #     self.reset_game(NonStopCar, self.track.start_pos)
            #     self.clock.tick(self.ticks)
            #     continue

            # Logic
            self.car.update(action)

            # Count car edges 
            (c1, c2) = self.car.position * ppu

            collision_detected = self.track.check_collision(self.car.corners)

            self.points += 1

            if self.points == winning_points:
                print("")
                print("level completed")
                history.append(str(self.points))
                # self.reset_game(NonStopCar, self.track.start_pos)
                # action = 0
                # self.clock.tick(self.ticks)
                # continue
                break

            distances = self.track.measure_intersections((c1,c2), self.car.sensors)

            if iteration % states_granularity == 0:
                self.logger.add_entry("car in : " + str(c1) + " " + str(c2))
                self.logger.add_entry("car angle = " + str(self.car.angle))

                s = State(distances, self.gran)

                logging = [str(s.hash())]
                logging.append(str(distances))
                logging.append(str(self.learner.qtable[self.learner.state_to_number(s), :]))

                action = self.learner.get_best_action(s)  # get the best action so far in this state

                logging.append(" -> " + str(action) + " ----> ")

                r0 = self.learner.calculate_score(collision_detected)  # get the immediate reward of this step
                s1 = self.learner.new_state_after_action(s, action, self.car, self.track, self.gran)  # new state after taking the best action
                # build the Q table, indexed by (state, action) pair
                self.learner.learn(s, action, s1, r0)
                
                logging.append(str(self.learner.qtable[self.learner.state_to_number(s), :]))
                self.logger.add_entry(' '.join(logging))
                self.logger.add_entry("predicted state = " + str(s1.hash()))

                if collision_detected:
                    self.logger.add_entry("overall states visited = " + str(len(self.learner.QIDic)))
                    self.logger.add_entry("===============================================")
                    history.append(str(self.points))
                    self.logger.add_entry("Iteration = " + str(len(history)))
                    print(str(len(history)), end =" ")
                    sys.stdout.flush()
                    self.reset_game(NonStopCar, self.track.start_pos)
                    action = 0
                    self.clock.tick(self.ticks)
                    continue
            
            # Drawing
            # self.screen.fill((0, 0, 0))
            # self.track.draw()
            # rotated = pygame.transform.rotate(self.car_image, self.car.angle)
            # rect = rotated.get_rect()
            # self.screen.blit(rotated, (c1 - rect.width / 2, c2 - rect.height / 2))

            # colors = map_distances_to_colors(distances)

            # # draw car points
            # pygame.draw.circle(self.screen, (255, 255, 255), self.car.front_point, 2)
            # pygame.draw.circle(self.screen, (255, 255, 255), self.car.back_point, 2)

            # for corner in self.car.corners:
            #     pygame.draw.circle(self.screen, (0, 0, 255), corner, 2)

            # # draw sensor lines
            # for i in range(len(self.car.sensors)):
            #     pygame.draw.line(self.screen, colors[i], (c1, c2), self.car.sensors[i])

            # self.update_stats(distances, colors)

            # pygame.display.flip()
            # self.clock.tick(self.ticks)
            self.logger.flush()

        self.learner.log_statistics(history, self.track.track_number, self.gran)

    def update_stats(self, distances, colors):
        message_to_screen(self.screen, "POINTS = " + str(self.points), white, (int((display_width / 2)), int(display_height / 2)), size=FontSize.MEDIUM)
        message_to_screen(self.screen, "L60 = " + str(distances[0]), colors[0], (100,30), size=FontSize.SMALL)
        message_to_screen(self.screen, "L30 = " + str(distances[1]), colors[1], (100,60), size=FontSize.SMALL)
        message_to_screen(self.screen, "DIR = " + str(distances[2]), colors[2], (100,90), size=FontSize.SMALL)
        message_to_screen(self.screen, "R30 = " + str(distances[3]), colors[3], (100,120), size=FontSize.SMALL)
        message_to_screen(self.screen, "R60 = " + str(distances[4]), colors[4], (100,150), size=FontSize.SMALL)


    def run_myself(self):
        for i in range(5):
            print(i)
            self.track = Track(self.screen, i)
            self.nonStopCarRun()


    def run_const_learner(self, learner, policy):
        self.logger = Logger(learner, policy, self.gran)
        self.learner = create_learner(learner, policy)

        for i in range(5):
            self.track = Track(self.screen, i)
            self.nonStopCarRun_learning()

        self.logger.close()
            

    def run_non_const_learner(self, learner, policy):
        self.logger = Logger(learner, policy, self.gran)

        for i in range(1):
            self.learner = create_learner(learner, policy)
            self.track = Track(self.screen, i)
            self.nonStopCarRun_learning()

        self.logger.close()


    def run_game(self, gran, learner=None, const_learner=True, policy="greedy"):
        self.gran = gran

        if learner == None:
            self.run_myself()
        elif const_learner:
            self.run_const_learner(learner, policy)
        else:
            self.run_non_const_learner(learner, policy)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    #game.run_game("sarsa")
    # game.run_game("qlearning")
    #game.run_game("qlearning", False)
    #game.run_game(50, "sarsa", False)
    #game.run_game(40, "sarsa", False)
    game.run_game(40, "sarsa", False, "random")
    #game.run_game(25, "sarsa", False)
    # game.run_game()
