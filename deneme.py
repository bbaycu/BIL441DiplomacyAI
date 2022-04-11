from Game import Game

game = Game(True)
game.playTheGame()

"""
#Try supports and support cuts
game.addOrder("mov","mun","trl")
game.resolveOrders()
game.addOrder("mov","trl","vie")
game.addOrder("mov","ven","tri")
game.addOrder("mov","tri","alb")
game.addOrder("mov","bud","tri")
game.addOrder("sup","bud","tri","vie")
game.resolveOrders()
"""
"""
game.addOrder("mov","mun","trl")
game.resolveOrders()
game.addOrder("sup","ven","tri","trl")
game.addOrder("mov","ven","tri")
game.resolveOrders()
"""

print()