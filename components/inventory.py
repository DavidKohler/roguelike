import libtcodpy as libtcod

from game_messages import Message

class Inventory:
    '''
    Component of player that allows for inventory
    '''
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        '''
        Adds item to inventory
        '''
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full',
                libtcod.yellow)})
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name.split('(')[0].strip()),
                libtcod.blue)})

            self.items.append(item)

        return results

    def drop_item(self, item):
        '''
        Drops item from inventory on current position
        '''
        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message(
            'You dropped the {0}'.format(item.name.split('(')[0]), libtcod.yellow)})

        return results

    def remove_item(self, item):
        '''
        Deletes item from inventory
        '''
        self.items.remove(item)

    def use(self, item_entity, **kwargs):
        '''
        Uses item specified in inventory
        '''
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            # equips item if equippable
            equippable_component = item_entity.equippable
            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used'\
                    .format(item_entity.name.split('(')[0]), libtcod.yellow)})
        else:
            # checks for targeting
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                # uses the use function of item
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results
