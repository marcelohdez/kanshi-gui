# import sys
# import gui
import lib as wd

state = wd.get_current_state()

print("CURRENT STATE:")
for desc, output_state in state.items():
    print("description:", desc)
    print(output_state)

# see current output states in kanshi format
profile = wd.Profile()
for desc, output_state in state.items():
    profile.outputs[desc] = output_state.to_kanshi_output()

config = wd.Config()
config.profiles.append(profile)

print("\nFOR KANSHI:")
print(config)

# app = gui.kgGui(application_id="me.marcelohdez.kgGui")
# app.run(sys.argv)
