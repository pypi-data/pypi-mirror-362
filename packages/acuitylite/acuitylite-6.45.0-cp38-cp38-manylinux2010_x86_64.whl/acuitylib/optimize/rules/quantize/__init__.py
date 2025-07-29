from acuitylib.pass_manager import SwPass

class QntPass(SwPass):

    def __init__(self):
        SwPass.__init__(self)
        self.ptype = "QNTPASS"
