
""""
Put new Spritesheets paths, rects frame counts and number of columns of the spritesheet here
Example:

<YourEntityName> = {
    "<identifier 1>":  (
                        "RedLightGreenLight/Resources/Spritesheets/<SpriteSheetName1>.png",
                        (<x_left>,<y_top>,<width of one frame>,<height of one frame>),
                        <total number of frames>,
                        <number of COLUMNS of the spritesheet>
                        )
}
"""
PlayerEntity = {
    "idle":  ("RedLightGreenLight/Resources/Spritesheets/walk.png",     (0,0,300,515),  8, 8),
    "walk":   ("RedLightGreenLight/Resources/Spritesheets/walk.png",     (0,0,300,515),  8, 8),
    "dead":  ("RedLightGreenLight/Resources/Spritesheets/explosion.png",     (0,0,341,341),  9, 3)
}
