import esper

class Actor (object):
	def __init__(self, world: esper.World):
		self.world = world
		self.actor = self.world.create_entity()

	def add_component(self, component):
		self.world.add_component(self.actor, component)

	def remove_component(self, comp_type):
		self.world.remove_component(self.actor, comp_type)

	def get_component(self, comp_type):
		return self.world.component_for_entity(self.actor, comp_type)

	def delete(self):
		self.world.delete_entity(self.actor)
