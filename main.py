# import sys
# import gui
import lib as kg

output1 = kg.Output()
output1.set_mode(1600, 900)
output1.set_position(0, 0)
output1.set_adaptive_sync(True)

profile1 = kg.Profile()
profile1.outputs["Some Company ASDF 4242"] = output1

config = kg.Config()
config.profiles.append(profile1)
print(config)

kg.write_configs_to_disk(config)

try:
    read_config = kg.read_self_config()
except FileNotFoundError | KeyError | ValueError:
    print("oops! failed to read wlr-displays.json, starting new config.")
    read_config = kg.Config()

print(read_config)

print("equal: ", config.to_dict() == read_config.to_dict())

# app = gui.kgGui(application_id="me.marcelohdez.kgGui")
# app.run(sys.argv)
