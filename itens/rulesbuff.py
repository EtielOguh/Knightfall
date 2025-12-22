from itens.stone import Stone

def can_buff(item):
    
    if isinstance(item, Stone):
        return False
    
    if item.buff >= 9:
        return False
    return True
        
def apply_buff(item):
    item.buff += 1