#Create object which stores each point charge
class Store_Charges:

    count = 0
    Charge_Arr = []

    def add_Charge(self, charge, position, velocity):
        Store_Charges.count += 1
        Store_Charges.Charge_Arr.append(Charge(Store_Charges.count, charge, position, velocity))

#Create object which describes each point charge
class Charge:
    def __init__(self, id, charge, position, velocity):
        self.id = id
        self.charge = charge
        self.position = position
        self.velocity = velocity
