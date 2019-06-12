def in_rect(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx + rw)and(ry <= y <= ry + rh):
        return True
    return False
