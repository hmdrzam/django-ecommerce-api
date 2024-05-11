from treebeard.mp_tree import MP_NodeQuerySet


class CategoryQuerySet(MP_NodeQuerySet):

    def active(self):
        return self.filter(active=True)

    def depth(self):
        return self.filter(depth=1)