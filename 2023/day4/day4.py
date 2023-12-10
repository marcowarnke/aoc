from collections import defaultdict

with open("input", "r") as f:
    pts = []
    td = defaultdict(int)
    for line in f:
        pte = 0
        ptc = 0
        cn, ns = line.split(":")
        _, cn = cn.split()
        cn = int(cn)
        wn, hn = ns.split("|")
        wns = wn.split()
        hns = hn.split()
        for n in hns:
            if n in wns:
                pte += 1
        if pte > 0:
            ptc = 2 ** (pte - 1)
        pts.append(ptc)

        print(cn)
        for k in range(0, td[cn] + 1):
            for l in range(1, pte + 1):
                td[cn+l] += 1
    print(sum(pts))
    print(td)
    print(len(td.values()) + sum([x for x in td.values()]))
