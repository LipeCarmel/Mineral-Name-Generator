from TextGenerator import MineralGenerator, save_gen

label = "mineral"
for i in range(20):
    generated = MineralGenerator()
    save_gen(label, generated)
