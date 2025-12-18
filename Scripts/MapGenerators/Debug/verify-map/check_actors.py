"""
Quick script to check what actors exist in the map
Run this in UE5 Editor Console after opening the map
"""

import unreal

# Get all actors in current level
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()

print("\n" + "="*60)
print("ACTORS IN CURRENT LEVEL")
print("="*60)

actor_list = []
for actor in all_actors:
    if actor:
        label = actor.get_actor_label()
        class_name = actor.get_class().get_name()
        location = actor.get_actor_location()
        actor_list.append({
            'label': label,
            'class': class_name,
            'location': location
        })

# Sort by label
actor_list.sort(key=lambda x: x['label'])

print(f"\nTotal actors: {len(actor_list)}\n")

for i, info in enumerate(actor_list, 1):
    print(f"{i}. {info['label']}")
    print(f"   Class: {info['class']}")
    print(f"   Location: ({info['location'].x:.1f}, {info['location'].y:.1f}, {info['location'].z:.1f})")
    print()

print("="*60)
