import ded_dict as ed
import numpy as np
import disjoint_path as ddp


def remove_duplicates(arr):
    hash_table = {}
    result = []
    for item in arr:
        item.sort()
        key = tuple(map(tuple, item))
        if key not in hash_table:
            hash_table[key] = True
            result.append(item)
    return result


def routing_path(s, dct, ind, s_path, t, rid="0"):
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


def packet(times):
    dct = ed.dct(M, N, L)

    S = ed.config(times, K, M, N, L)
    T = ed.config(times, K, M, N, L)

    dj_lib = {}
    for var in range(len(T)):  # disjoint path lib for each routing pair
        dj_lib[var] = ddp.path(M, N, L, S[var][:-1].copy(), T[var][:-1].copy())
    cycle = 0
    length = 0
    rec = 0  # the number of received packets
    mark = list(np.zeros(times, int))
    sb, tb = S.copy(), T.copy()
    link_label = []
    index = {}
    tdj = 0
    latency_distribution = np.zeros(terminated_cycle + 2)
    throughput_distribution = np.zeros(tp)
    while cycle < terminated_cycle:
        rec_p = 0  # the number of received packets per cycle
        for i in range(len(mark)):
            if i in index:
                path = dj_lib[i%times][index[i]]
            else:
                path = dj_lib[i%times][0]           # the first path for default
            if mark[i] == 0:
                disjoint_path = dj_lib[i%times]
                for var in range(len(disjoint_path)):  # each path in disjoint path
                    congestion_point = []  # list for save congested point
                    for point in disjoint_path[var]:  # search for congestion point
                        rid = '0' * (len(str(L * M ** N + 1)) - len(str(point[0]))) + "".join([str(x) for x in point])
                        if dct[rid] > max_p - 2:
                            congestion_point.append(point)
                    if len(congestion_point) < 1:  # path not congestion
                        path = disjoint_path[var]
                        index[i] = var
                        if var != 0:
                            tdj += 1
                        break
                if i not in index:  # all the path in congestion
                    mark[i] = -2
            res = routing_path(S[i], dct, mark[i], path, T[i])
            if S[i] != res[0]:
                link_label.append([S[i].copy(), res[0].copy()])
            dct, S[i], mark[i] = res[1], res[0], res[2]
            if mark[i] == 2:
                rec += 1
                mark[i] = -1
                rec_p += 1
                label = cycle - i // times  # latency distribution label
                latency_distribution[label] += 1
        S += sb
        T += tb
        mark += list(np.zeros(times, int))
        cycle += 1
        throughput_distribution[rec_p] += 1
    return length, cycle, latency_distribution, throughput_distribution


if __name__ == "__main__":
    K = 4     # number of nodes for each router
    M = 8      # number of routers in each dimension
    N = 1     # dimension of each group
    L = 5       # number of global links for each router
    max_p = 12   # buffer size

    terminated_cycle = 500

    offered = 600  # number of injected packets
    number = K * (L * M ** N + 1) * M ** N
    y = np.zeros(terminated_cycle + 2)  # save the result of the latency distribution
    tp = int(offered * 1.3)  # Define throughput with sufficient redundancy
    z = np.zeros(tp)  # save the result of the throughput distribution
    num = 100  # repeat the simulation for num times
    for j in range(num):
        res = packet(offered)
        y += res[2]
        z += res[3]
        print(res[1])
        print(j)

    y /= num
    z /= num

    file = open('latency_distribution_pccdj.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()

    file = open('throughput_distribution_pccdj.txt', 'w')
    for v in z:
        file.write(str(v) + '\n')
    file.close()

