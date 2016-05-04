import pygame, sys
from input import xo_input
from UI.uicontainer import UIContainer
from fraction import *
from copy import deepcopy

class GameScreen:
    def __init__(self, manager, screen):
        self.stateManager = manager
        self.window = screen

        self.uiContainer = UIContainer(self.window)
        self.uiContainer.horizontalStride = 5
        self.initializedUI = False

        self.titleFont = pygame.font.SysFont("monospace", 45, bold=True)
        self.scoreFont = pygame.font.SysFont("monospace", 30)
        self.textColour = (128, 128, 128)

        self.screenInfo = pygame.display.Info()
        pass

    def start(self):
        if not self.initializedUI:
            # Button sizes
            padding = 10
            side_margin = 50
            top_margin = 150
            width = (self.screenInfo.current_w - (padding * 5) - (side_margin * 2)) / 5
            height = (self.screenInfo.current_h - (padding * 5) - (top_margin)) / 5

            self.fractionAnswers = []
            self.equalFractions = []
            self.answer = frac_random()

            for x in range(1, 30):
                self.fractionAnswers.append(frac_random())
                self.equalFractions.append(self.fractionAnswers[x - 1].get_equal_fraction())
                self.right_fracs, self.wrong_fracs = create_goal(self.answer)

            temp_frac = frac_random()
            temp_right_fracs = deepcopy(self.right_fracs)
            temp_wrong_fracs = deepcopy(self.wrong_fracs)

            for i in range(0, 5):
                for j in range(0, 5):
                    if(len(temp_right_fracs) > 0 and len(temp_wrong_fracs) > 0):
                        if(self.array_random(1,2) == 1):
                            rand = self.array_random(0,len(temp_right_fracs)-1)
                            temp_frac = temp_right_fracs[rand]
                            temp_right_fracs.remove(temp_right_fracs[rand])
                        else:
                            rand = self.array_random(0, len(temp_wrong_fracs) - 1)
                            temp_frac = temp_wrong_fracs[rand]
                            temp_wrong_fracs.remove(temp_wrong_fracs[rand])
                    elif(len(temp_right_fracs) > 0):
                        rand = self.array_random(0, len(temp_right_fracs) - 1)
                        temp_frac = temp_right_fracs[rand]
                        temp_right_fracs.remove(temp_right_fracs[rand])
                    else:
                        rand = self.array_random(0, len(temp_wrong_fracs) - 1)
                        temp_frac = temp_wrong_fracs[rand]
                        temp_wrong_fracs.remove(temp_wrong_fracs[rand])

                    button = self.uiContainer.add_button(str(temp_frac), (padding * i) + (width * i) + side_margin, (padding * j) + (height * j) + top_margin, width, height)
                    button.font = pygame.font.SysFont("monospace", 30)
                    button.baseColour = (0, 0, 0)
                    button.hoverColour = (255, 255, 255)
                    button.clickColour = (128, 128, 128)
                    button.hoverFill = 1

            self.initializedUI = True

        self.score = 0

        
    def update(self):
        if (xo_input.btn_cross):
            self.stateManager.switchGameState("MainScreen")

        endLoop = False
        for button in self.uiContainer.components:
            if(button.text != "" and button.was_pressed()):
                for frac in self.right_fracs:
                    print("frac: " + str(frac) + " button: " + button.text)
                    if(str(frac) == button.text):
                        self.score += 10
                        button.text = ""
                        endLoop = True
                        break
                print("Score: " + str(self.score))
                if(not endLoop):
                    self.score -= 5
                    button.text = ""
            #if(endLoop == True):
            #    print("breaking")
            #    break


        self.uiContainer.update()
    
    def draw(self):
        self.drawText("Score: " + str(self.score), self.scoreFont, (-self.screenInfo.current_w/2)+90,
                      (-self.screenInfo.current_h / 2) + 110)
        self.drawText("Find these multiples: " + str(self.answer), self.titleFont, 0, (-self.screenInfo.current_h/2) + 70)
        # UI needs to be drawn LAST
        self.uiContainer.draw()
    
    def final(self):
        pass

    def drawText(self, text, font, offsetX, offsetY):
        label = font.render(text, 1, self.textColour)
        text_width, text_height = font.size(text)
        self.window.blit(label, ((self.screenInfo.current_w/2) - (text_width/2) + offsetX, (self.screenInfo.current_h/2) - (text_height/2) + offsetY))

    def array_random(self, start, end):
        if(start == end):
            return start
        return randint(start, end)