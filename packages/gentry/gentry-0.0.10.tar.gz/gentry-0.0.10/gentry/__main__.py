# just an example on how to use the Tree class

from collections import defaultdict
from .tree import Tree, Count
from .mermaid import Mermaid, Shape, Style

class Family(Tree, Mermaid):...

class Person(Tree, Mermaid):
    _groups = { "children"}
    
class GrandMother(Person):
    _style = Style.function
    _shape = Shape.braces

class Mother(Person):
    _groups = {"girls", "boys"}
 
class Child(Person):
    _include_properties = True

class FamilyCount(Count):
    """
    We only count real persons, so we define a specialized member function
    for any Family node that returns 0 and will not be counted.
    """
    def _do_count_Family(self, tree:Family):
        return 0

# define a few children  
c1 = Child("Alice")
c2 = Child("Bob")
c3 = Child("Cherryl", properties={"chess master": "ELO 2235"})
c4 = Child("Dick")
c5 = Child("Ellen")
c6 = Child("Fergal")
c7 = Child("Gladys", properties={"drivers license": 2023, "nose piercing": 2024})
c8 = Child("Hank")

# Mothers have girls and boys attributes defined, so those can be assigned directly
m1 = Mother("Anna")
m1.girls = [c1,c3]
m1.boys = [c2,c4]

m2 = Mother("Beatrice")
m2.girls.append(c5)     # under the hood they are all items in a defaultdict(list) so we can append directly
m2.girls.append(c7)
m2.boys = [c6,c8]

# Grandmothers do not make the distinction
g1 = GrandMother("Granny")
g1.children = [m1, m2]
# so this would fail:
# g1.girls = [m1, m2]

# Family does not have any direct access attributes defined, but anything
# that is passed as the children argument (and can be converted to a defaultdict(list))
# will be added to the _children attribute, so will still be automatically discovered
# by Visitor derived classes.
f1 = Family("The Andersons", children={"matriarch":[g1]})

counter = FamilyCount(f1, strict=False)

assert counter.count() == 11

print(f1)
