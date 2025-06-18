# import sys
# import gui
import kanshi

output1 = kanshi.Output()
output1.set_mode(1600, 900)
output1.set_position(0, 0)
output1.set_adaptive_sync(True)

profile1 = kanshi.Profile()
profile1.outputs["Some Company ASDF 4242"] = output1

config = kanshi.Config()
config.profiles.append(profile1)
print(config)

kanshi.write_configs_to_disk(config)
read_config = kanshi.read_self_config()
print(read_config)

print("equal: ", config.to_dict() == read_config.to_dict())

# app = gui.KanshiGui(application_id="me.marcelohdez.KanshiGui")
# app.run(sys.argv)
