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


def packet(lam):
    times = int(lam * (L*M**N+1) * M**N*K)
    dct = ed.dct(M, N, L)

    S = ed.config(lam, K, M, N, L)
    T = ed.config(lam, K, M, N, L)

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

    congestion_cycles = 50
    thi = [5] * times
    congested_path = []
    n_congested = 0

    while rec < times * 200:
        for i in range(len(mark)):
            if i in index:
                path = dj_lib[i%times][index[i]]
            else:
                path = dj_lib[i%times][0]           # the first path for default
            if mark[i] == 0:
                disjoint_path = dj_lib[i%times]
                for var in range(len(disjoint_path)):  # each path in disjoint path
                    flag = 1
                    for point in disjoint_path[var]:  # search for congestion point
                        rid = '0' * (len(str(L * M ** N + 1)) - len(str(point[0]))) + "".join([str(x) for x in point])
                        if dct[rid] > max_p - 2:
                            flag = 0
                            break
                    if flag:          # path not congestion
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
                if cycle > congestion_cycles:   # the congested path imply the destination node does not receive any packets in the last 10 cycles
                    if cycle <= thi[i%times] + congestion_cycles:
                        thi[i%times] = cycle
                    else:
                        if i%times not in congested_path:
                            congested_path.append(i%times)
                            n_congested += 1
        S += sb
        T += tb
        mark += list(np.zeros(times, int))
        cycle += 1
        if cycle > 650:
            break
    for var in range(len(thi)):
        if var not in congested_path:
            if cycle - thi[var] > congestion_cycles:
                congested_path.append(var)
                n_congested += 1
    throughput_dj = tdj/cycle
    length = length / rec
    link_label = remove_duplicates(link_label)
    link_rate = len(link_label)/((L*M+1)*M*((L+M-1)/2+K))
    return length, cycle, rec, link_rate, throughput_dj, n_congested


if __name__ == "__main__":
    K = 4     # number of nodes for each router
    M = 8      # number of routers in each dimension
    N = 1     # dimension of each group
    L = 5       # number of global links for each router
    max_p = 12   # buffer size

    lam = np.linspace(0.05, 0.9, 18)
    number = K*(L*M**N+1)*M**N
    y = np.zeros(len(lam))  # save the result of the packet latency
    z = np.zeros(len(lam))  # save the result of the throughput
    w = np.zeros(len(lam))  # save the result of the received ratio
    lu = np.zeros(len(lam))  # save the result of link utilized rate
    dju = np.zeros(len(lam))  # save the result of disjoint path utilized
    u = np.zeros(len(lam))  # save the result of congested paths
    num = 100  # repeat the simulation for num times

    for j in range(num):
        for i in range(len(lam)):
            res = packet(lam[i])
            y[i] += res[1]
            z[i] += res[2] / res[1]
            w[i] += res[2] / (res[1] * number * lam[i])
            lu[i] += res[3]
            dju += res[4]
            u[i] += res[5]
            print(lam[i], res[1], res[2] / res[1], res[2] / (res[1] * number * lam[i]), res[3], res[4], res[5])
        print(j)

    y /= num
    z /= num
    w /= num
    lu /= num
    dju /= num
    u /= num

    file = open('cycles_pccdj.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()

    file = open('Throughput_pccdj.txt', 'w')
    for v in z:
        file.write(str(v) + '\n')
    file.close()

    file = open('Received_pccdj.txt', 'w')
    for v in w:
        file.write(str(v) + '\n')
    file.close()

    file = open('link_utilized_rate_pccdj.txt', 'w')
    for v in lu:
        file.write(str(v) + '\n')
    file.close()

    file = open('disjoint path utilized_pccdj.txt', 'w')
    for v in dju:
        file.write(str(v) + '\n')
    file.close()

    file = open('congested_path_pccdj.txt', 'w')
    for v in u:
        file.write(str(v) + '\n')
    file.close()

