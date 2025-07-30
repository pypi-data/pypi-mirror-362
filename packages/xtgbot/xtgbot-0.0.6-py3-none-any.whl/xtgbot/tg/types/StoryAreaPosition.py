from ..base_type import base_type
from typing import Optional

@base_type
class StoryAreaPosition:
    '''
    Describes the position of a clickable area within a story.
    '''

    corner_radius_percentage: float
    '''
    The radius of the rectangle corner rounding, as a percentage of the media width
    '''

    rotation_angle: float
    '''
    The clockwise rotation angle of the rectangle, in degrees; 0-360
    '''

    height_percentage: float
    '''
    The height of the area's rectangle, as a percentage of the media height
    '''

    width_percentage: float
    '''
    The width of the area's rectangle, as a percentage of the media width
    '''

    y_percentage: float
    '''
    The ordinate of the area's center, as a percentage of the media height
    '''

    x_percentage: float
    '''
    The abscissa of the area's center, as a percentage of the media width
    '''

