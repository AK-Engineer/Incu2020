filename = "./interface.txt"
with open(filename, encoding="utf8") as f:
    content = f.readlines()

# remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

interfaces_final = {}
x = 0;
for y in content:
    if y.endswith(":"):
        interface = {}
        names = []
        descs = []
        states = []
        interface[x] = {}
        interface[x]['Switch_name'] = y
    else:
        words = y.split(",")
        for word in words:
            if (word.startswith("int")):
                names.append(word)
                interface[x]['Interface_name'] = names
            elif (word.strip().startswith("“")):
                descs.append(word.strip().strip("“”"))
                interface[x]['Description'] = descs
            elif (word.strip().lower() == "up") or (word.strip().lower() == "down"):
                states.append(word.strip().lower())
                interface[x]['State'] = states
            else:
                interfaces_final.update(interface)
                x += 1


