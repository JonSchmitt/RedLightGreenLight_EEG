
""""
Put new Spritesheets paths, rects frame counts and number of columns of the spritesheet here
Example:

<YourEntityName> = {
    "EntityStatesEnum.<enum>":  (
                        "RedLightGreenLight/Resources/Spritesheets/<SpriteSheetName1>.png",
                        (<x_left>,<y_top>,<width of one frame>,<height of one frame>),
                        <total number of frames>,
                        <number of COLUMNS of the spritesheet>
                        )
}
"""
from RedLightGreenLight.States.Game.Entites.EntityStates.EntityStatesEnum import EntityStatesEnum

PlayerEntity = {
    EntityStatesEnum.IDLE:      ("RedLightGreenLight/Resources/Spritesheets/walk.png",          (0,0,300,515),  8, 8),
    EntityStatesEnum.WALKING:   ("RedLightGreenLight/Resources/Spritesheets/walk.png",          (0,0,300,515),  8, 8),
    EntityStatesEnum.DEAD:      ("RedLightGreenLight/Resources/Spritesheets/explosion.png",     (0,0,341,341),  9, 3)
}
