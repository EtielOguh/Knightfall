def can_buff(item):
    if item.buff >= 9:
        return False
    return True
        
def apply_buff(item):
    item.buff += 1