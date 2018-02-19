

  player = Player()
  mapa = Map()
  mapa.create_path()
  mapa.create_wall()
  inter = Interface()
  #inter.show(mapa, "bp", player)
  BP = BuildingPhase()

class Cykl(object):
  game_active = True
  loops = 5   #number of simulations
  def execute(self):
      while cls.game_active == True:
          BP.start()
          n = raw_input("\n\n T, Q or B ?: ")
          if n == "Q":
              cls.game_active = False
              print "The end"
          elif n == "T":
              RivalWave.create(mapa)
              inter.show(mapa,"bp", player)
              BP.set_tower(mapa)
              inter.show(mapa,"bp", player)
          elif n == "B":
              simulator = Simulator(200)
              RivalWave.generate(simulator, mapa)
              inter.show(mapa, "sim")
              simulator.execute_all()
              inter.show(mapa, "sim")
          else:
              print "Wrong command"
