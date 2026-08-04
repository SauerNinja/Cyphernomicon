import re, os, json, html

SRC = "/home/claude/work/Cyphernomicon-master"
OUT = "/home/claude/work/build/data"
os.makedirs(OUT, exist_ok=True)

sections = [
    "01-Introduction","02-MFAQ","03-Cypherpunks","04-Goals-and-Ideology","05-Cryptology",
    "06-The-Need-For-Strong-Crypto","07-Summary-PGP","08-Anonymity","09-Policy","10-Legal-Issues",
    "11-Surveillance","12-Digital-Cash","13-Activism-and-Projects","14-Other-Advanced-Crypto-Applications",
    "15-Reputations-and-Credentials","16-Crypto-Anarchy","17-The-Future","18-Loose-Ends",
    "19-Appendices","20-Readme"
]

heading_re = re.compile(r'^(#{1,3}\s*)?(\d+(?:\.\d+){0,4})\.?\s+(.*)$')
bullet_re = re.compile(r'^(\s*)([-+])\s+(.*)$')

def parse_file(path, top_num):
    with open(path, encoding='utf-8', errors='replace') as f:
        raw_lines = f.readlines()

    # strip trailing whitespace, keep track of blank lines as separators
    lines = [l.rstrip('\n') for l in raw_lines]

    # top of file: Title \n ==== underline, skip those two lines if present
    start = 0
    if len(lines) >= 2 and re.match(r'^=+\s*$', lines[1] or ''):
        start = 2

    root = {"type": "root", "children": []}
    # heading stack: list of (level, node)
    heading_stack = [(0, root)]
    # bullet stack for current heading context: list of (indent, node_children_list)
    bullet_stack = []
    last_node = None  # last node that can receive continuation text (heading or bullet)
    last_container = root["children"]

    def current_heading_children():
        return heading_stack[-1][1]["children"]

    for raw in lines[start:]:
        line = raw.rstrip()
        if not line.strip():
            continue
        bm_check = bullet_re.match(line)
        m = None if bm_check else heading_re.match(line.strip())
        if m and m.group(2).split('.')[0] == str(top_num):
            num = m.group(2)
            title = m.group(3).strip()
            level = num.count('.') + 1
            node = {"type": "heading", "num": num, "title": title, "children": [], "text": ""}
            # pop heading_stack until level fits
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack[-1][1]["children"].append(node)
            heading_stack.append((level, node))
            bullet_stack = []  # reset bullet nesting under new heading
            last_node = node
            continue
        bm = bm_check
        if bm:
            indent = len(bm.group(1))
            text = bm.group(3).strip()
            node = {"type": "bullet", "text": text, "children": []}
            # pop bullet_stack until indent fits under top
            while bullet_stack and bullet_stack[-1][0] >= indent:
                bullet_stack.pop()
            if bullet_stack:
                parent_children = bullet_stack[-1][1]
            else:
                parent_children = heading_stack[-1][1]["children"]
            parent_children.append(node)
            bullet_stack.append((indent, node["children"]))
            last_node = node
            continue
        # continuation line: append to last_node's text
        text = line.strip()
        if last_node is not None:
            if last_node["type"] == "heading":
                last_node["text"] = (last_node["text"] + " " + text).strip()
            else:
                last_node["text"] = (last_node["text"] + " " + text).strip()
        else:
            # orphan paragraph at root
            node = {"type": "para", "text": text, "children": []}
            root["children"].append(node)
            last_node = node

    return root["children"]

all_data = {}
for sec in sections:
    fname = f"{sec}.md"
    path = os.path.join(SRC, sec, fname)
    top_num = int(sec.split('-')[0])
    tree = parse_file(path, top_num)
    all_data[sec] = tree
    with open(os.path.join(OUT, f"{sec}.json"), "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False)
    # quick stats
    def count(nodes):
        c = 0
        for n in nodes:
            c += 1
            c += count(n["children"])
        return c
    print(sec, "nodes:", count(tree))

print("DONE")
