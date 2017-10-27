import pygame
from Environment import Environment

class SokobanGui(object):
    """
    Class to draw the Sokoban GUI.
    """
    def __init__(self, theme="default"):
        self.theme = theme
        self.environment = Environment()

    def drawComplete(self):
        self.environment.screen.fill((0, 0, 0))

    def drawLevel(self, matrix_to_draw):

        # Load level images
        wall = pygame.image.load(self.environment.getPath() +
                                '/themes/' + self.theme + '/images/wall.png').convert()
        box = pygame.image.load(self.environment.getPath() +
                                '/themes/' + self.theme + '/images/box.png').convert()
        box_on_target = pygame.image.load(self.environment.getPath(
            ) + '/themes/' + self.theme + '/images/box_on_target.png').convert()
        space = pygame.image.load(self.environment.getPath(
            ) + '/themes/' + self.theme + '/images/space.png').convert()
        target = pygame.image.load(self.environment.getPath(
            ) + '/themes/' + self.theme + '/images/target.png').convert()
        player = pygame.image.load(self.environment.getPath(
            ) + '/themes/' + self.theme + '/images/player.png').convert()

        # If horizontal or vertical resolution is not enough to fit the level images then resize images
        if matrix_to_draw.getSize()[0] > self.environment.size[0] / 36 or matrix_to_draw.getSize()[1] > self.environment.size[1] / 36:

            # If level's x size > level's y size then resize according to x axis
            if matrix_to_draw.getSize()[0] / matrix_to_draw.getSize()[1] >= 1:
                new_image_size = self.environment.size[0] / matrix_to_draw.getSize()[0]
            # If level's y size > level's x size then resize according to y axis
            else:
                new_image_size = self.environment.size[1] / matrix_to_draw.getSize()[1]

            # Just to the resize job
            wall = pygame.transform.scale(wall, (new_image_size, new_image_size))
            box = pygame.transform.scale(box, (new_image_size, new_image_size))
            box_on_target = pygame.transform.scale(
                box_on_target, (new_image_size, new_image_size))
            space = pygame.transform.scale(space, (new_image_size, new_image_size))
            target = pygame.transform.scale(target, (new_image_size, new_image_size))
            player = pygame.transform.scale(player, (new_image_size, new_image_size))

        # Just a Dictionary (associative array in pyhton's lingua) to map images to characters used in level design
        images = {'#': wall, ' ': space, '$': box,
            '.': target, '@': player, '*': box_on_target}

        # Get image size. Images are always squares so it doesn't care if you get width or height
        box_size = wall.get_width()

        # Iterate all Rows
        for i in range(0, len(matrix_to_draw)):
            # Iterate all columns of the row
            for c in range(0, len(matrix_to_draw[i])):
                self.environment.screen.blit(
                    images[matrix_to_draw[i][c]], (c * box_size, i * box_size))

        pygame.display.update()
