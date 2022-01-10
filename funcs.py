"""
関数群
"""

def validate_facerect(x: float, y: float, h: float, w: float, mode: str='default') -> [int]:
    if mode == 'face':
        scale_factor = 1.2
    elif mode == 'fruit':
        scale_factor = 0.75
    elif mode == 'handsign':
        scale_factor = 1.75
    else:
        scale_factor = 1.0
    offset_factor = (scale_factor - 1) / (2*scale_factor)
    
    h = int(scale_factor * w * (126/134))
    w = int(scale_factor * w)
    x = int(x - offset_factor * w)
    
    if mode == 'face':
        y = int(y - offset_factor * h)
    elif mode == 'fruit':
        y = int(y - 1.8*offset_factor * h)
    elif mode == 'handsign':
        y = int(y - offset_factor * h)
    
    return (x, y, h, w)