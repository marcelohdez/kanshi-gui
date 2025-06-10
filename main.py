# import sys
# import gui
import kanshi


config = kanshi.Config()
profile1 = kanshi.Profile()
output1 = kanshi.Output()

output1.set_mode(1600, 900)
output1.set_position(0, 0)
output1.set_adaptive_sync(True)

profile1.outputs["Some Company ASDF 4242"] = output1

config.profiles.append(profile1)
kanshi.write_config(config, "config-kanshi-gui")

# app = gui.KanshiGui(application_id="me.marcelohdez.KanshiGui")
# app.run(sys.argv)
