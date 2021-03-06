import pygame, sys
from input import xo_input
from exit import exit_game
from UI.uicontainer import UIContainer
from UI.button import Button

class MainScreen:
    """
    Defines the main menu screen
    """
    def __init__(self, manager, screen):
        self.stateManager = manager
        self.window = screen

        self.uiContainer = UIContainer(self.window)
        self.uiContainer.horizontalStride = 0

        self.screenInfo = pygame.display.Info()
        
        # Button sizes and positions
        width = 250
        height = 60
        cx = self.screenInfo.current_w / 2
        cy = self.screenInfo.current_h / 2
        bx = cx - (width / 2)
        padding = 30
        dy = padding / 2 + height

        # Start game button
        self.gameButton = self.uiContainer.add_button("Start Game", bx, 0, width, height)
        self.gameButton.rect.y = cy - height * 2 - padding / 2  + 30

        # Instructions button
        self.instructionsButton = self.uiContainer.add_button("Instructions", bx, 0, width, height)
        self.instructionsButton.rect.y = self.gameButton.rect.y + dy

        # High Scores button
        self.highScoresButton = self.uiContainer.add_button("High Scores", bx, 0, width, height)
        self.highScoresButton.rect.y = self.instructionsButton.rect.y + dy

        # About button
        self.aboutButton = self.uiContainer.add_button("About", bx, 0, width, height)
        self.aboutButton.rect.y = self.highScoresButton.rect.y + dy 
        
        self.quitButton = self.uiContainer.add_button("Quit", bx, 0, width, height)
        self.quitButton.rect.y = self.aboutButton.rect.y + dy

        # Set button colors
        baseColor = (0, 0, 0)
        hoverColor = (255, 255, 255)
        clickColor = (128, 128, 128)
        hoverFill = 1
        for button in self.uiContainer.components:
            if isinstance(button, Button):
                button.font = pygame.font.SysFont("monospace", 30)
                button.baseColour = baseColor
                button.hoverColour = hoverColor
                button.clickColour = clickColor
                button.hoverFill = hoverFill
                
        # Load title image
        if sys.platform == "win32":
            self.titleImage = pygame.image.load("WinMedia/Images/titleXO.png").convert()
        else:
            self.titleImage = pygame.image.load("media/Images/titleXO.png").convert()

    def start(self):
        pass

   
    def update(self):
        if xo_input.escape:
            exit_game(1)

        if self.gameButton.was_pressed():
            self.stateManager.switchGameState("GameScreen")
        if self.instructionsButton.was_pressed():
            self.stateManager.switchGameState("InstructionsScreen")
        if self.highScoresButton.was_pressed():
            self.stateManager.switchGameState("HighScoreScreen")
        if self.aboutButton.was_pressed():
            self.stateManager.switchGameState("AboutScreen")
        if self.quitButton.was_pressed():
            exit_game(1)

        self.uiContainer.update()
    
    def draw(self):
        
        self.window.blit(self.titleImage, ((self.screenInfo.current_w/2) - (self.titleImage.get_rect().width/2), 50))
        
        # UI needs to be drawn LAST
        self.uiContainer.draw()
    
    def final(self):
        pass
