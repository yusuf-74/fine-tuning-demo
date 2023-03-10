import json

ans = ""

for i in range(5,11):
    with open(f"prompts_completion_maker/Q{i}_bot.json", "r") as read_file:
        data = json.load(read_file)
        ans += data["content"]
with open(f"prompts_completion_maker/all_bot.txt", "w") as write_file:
    write_file.write(ans)
        