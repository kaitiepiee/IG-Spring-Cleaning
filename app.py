import json

# Load followers
with open('followers_1.json', 'r', encoding='utf-8') as f:
    followers_data = json.load(f)
    followers = set(user['string_list_data'][0]['value'] for user in followers_data)

# Load followees
with open('following.json', 'r', encoding='utf-8') as f:
    following_data = json.load(f)
    followees_data = following_data["relationships_following"]
    followees = set(user['string_list_data'][0]['value'] for user in followees_data)

# Categorize
mutuals = sorted(followers & followees)
ghosts = sorted(followees - followers)    # you follow, they don’t
fans = sorted(followers - followees)      # they follow you, you don’t

# Write to file
with open('insta_relationships.txt', 'w', encoding='utf-8') as out:
    out.write("🤝 Mutuals (you follow each other):\n")
    for user in mutuals:
        out.write(f"{user}\n")

    out.write("\n💔 Ghosts (you follow them, they don't follow back):\n")
    for user in ghosts:
        out.write(f"{user}\n")

    out.write("\n👀 Fans (they follow you, but you don’t follow back):\n")
    for user in fans:
        out.write(f"{user}\n")

print("✅ Saved to insta_relationships.txt!")
