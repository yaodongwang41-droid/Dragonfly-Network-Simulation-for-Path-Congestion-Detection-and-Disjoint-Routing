import ded_dict as ed
import numpy as np
import disjoint_path as ddp
import random


def routing_path(s, dct, ind, s_path, t, max_p=16, rid="0"):
    if ind == -1:   # packet in destination node
        return s, dct, ind
    elif ind == -2:   # delay packet
        ind = 0
        return s, dct, ind
    elif ind == 0:  # s in source node
        rid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s[:-1]])
        if dct[rid] < max_p:
            dct[rid] += 1
            ind = 1
            s = s[:-1]
        return s, dct, ind
    else:
        for var in range(len(s_path)):
            if s_path[var] == s:
                if var == len(s_path)-1:  # s in destination router
                    cid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
                    dct[cid] -= 1
                    ind = 2
                    return t, dct, ind
                else:
                    out_router = s_path[var + 1]
                    rid = '0' * (len(str(L * M ** N + 1)) - len(str(s_path[var + 1][0]))) + "".join([str(x) for x in s_path[var + 1]])
        if dct[rid] < max_p:
            cid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
            dct[cid] -= 1
            dct[rid] += 1
            s = out_router
        return s, dct, ind


def packet(groups=10):
    real_times = (K*M-12)*groups
    dct = ed.dct(M, N, L)

    group_list = [x for x in range(M * L + 1)]
    random.shuffle(group_list)
    SF = ed.config_multi_group(real_times, K, M, N, L, group_list[0:9])
    TF = ed.config_multi_group(real_times, K, M, N, L, [group_list[10]] * groups)

    dj_lib = {}
    for var in range(len(TF)):     # disjoint path lib for each routing pair
        dj_lib[var] = ddp.path(M, N, L, SF[var][:-1].copy(), TF[var][:-1].copy())
        # if SF[var][:-1] not in dj_lib[var][0]:
        #     print(dj_lib[var][0], SF[var][:-1], TF[var][:-1])
    S = SF[0:len(SF)//groups]         # select 20% of the source-destination pairs
    T = TF[0:len(TF)//groups]
    times = real_times//groups
    cycle = 0
    mark = list(np.zeros(times, int))
    sb, tb = S.copy(), T.copy()
    throughput = []
    index = {}
    dj_utilized = np.zeros(terminate_cycle-1, int)
    while cycle < 200+terminate_cycle:    # simulate for 300 cycles
        rec = 0  # the number of received packets
        for i in range(len(mark)):
            if cycle > 220:
                if i > diff:
                    label = (i-diff-1) % times
                else:
                    label = i % (times//groups)
            else:
                label = i % times
            if i in index:
                path = dj_lib[label][index[i]]
                # print(dj_lib[label])
                # print(path, S[i], label, i, cycle)
            else:
                path = dj_lib[label][0]           # the first path for default

            if cycle > 220 and mark[i] == 0:
                disjoint_path = dj_lib[label]
                for var in range(len(disjoint_path)):      # each path in disjoint path
                    congestion_point = []
                    for point in disjoint_path[var]:  # search for congestion point
                        rid = '0' * (len(str(L * M ** N + 1)) - len(str(point[0]))) + "".join([str(x) for x in point])
                        if dct[rid] > 14:
                            congestion_point.append(point)
                    if len(congestion_point) < 1:  # path not congestion
                        path = disjoint_path[var]
                        index[i] = var
                        if var != 0:
                            dj_utilized[cycle-201] += 1
                        break
                else:   # all the path in congestion
                    mark[i] = -2
            res = routing_path(S[i], dct, mark[i], path, T[i])
            S[i], dct, mark[i] = res[0], res[1], res[2]
            if mark[i] == 2:
                rec += 1
                mark[i] = -1
        if cycle > 200:
            throughput.append(rec)
        if cycle == 220:  # add more source-destination pairs
            times = real_times
            sb, tb = SF.copy(), TF.copy()
            diff = i
        S += sb
        T += tb
        mark += list(np.zeros(times, int))
        cycle += 1
    return throughput, dj_utilized


if __name__ == "__main__":
    K = 4     # number of nodes for each router
    M = 8      # number of routers in each dimension
    N = 1     # dimension of each group
    L = 5       # number of global links for each router

    num = 100  # repeat the simulation for num times
    terminate_cycle = 100
    y = np.zeros(terminate_cycle-1, int)
    z = np.zeros(terminate_cycle - 1, int)
    for j in range(num):
        res = packet()
        y += res[0]
        z += res[1]
        print(j)
    y = y/num
    z = z/num

    file = open('cycles_pccdj_mg.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()

    file = open('cycles_dj_mg.txt', 'w')
    for u in z:
        file.write(str(u) + '\n')
    file.close()

