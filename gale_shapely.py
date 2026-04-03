def gale_shapley(P_pref, R_pref):

    n = len(P_pref)
    
    free_proposers = list(range(n))
    
    match_R = [-1] * n
    match_P = [-1] * n
    
    proposer_next_proposal_idx = [0] * n
    
    R_rank = [[0] * n for _ in range(n)]
    for r in range(n):
        for rank, p in enumerate(R_pref[r]):
            R_rank[r][p] = rank

    history = []

    while free_proposers:
        p = free_proposers.pop(0)
        
        if proposer_next_proposal_idx[p] >= n:
            continue
            
        r = P_pref[p][proposer_next_proposal_idx[p]]
        proposer_next_proposal_idx[p] += 1
        
        history.append(f"Proposer {p} proposes to Receiver {r}")
        
        if match_R[r] == -1:
            match_R[r] = p
            match_P[p] = r
            history.append(f" -> Accepted (Receiver {r} was free)")
            
        else:
            curr_p = match_R[r]
            
            if R_rank[r][p] < R_rank[r][curr_p]:
                match_P[curr_p] = -1  
                free_proposers.append(curr_p) 
                
                match_R[r] = p       
                match_P[p] = r
                history.append(f" -> Accepted (Receiver {r} dumps {curr_p} for {p})")
            else:
                free_proposers.append(p)  
                history.append(f" -> Rejected (Receiver {r} prefers current partner {curr_p})")

    return match_P, match_R, history

# P_raw = [
#     [3, 2, 4, 1],
#     [1, 2, 4, 3],
#     [1, 2, 3, 4],
#     [1, 2, 3, 4]
# ]

# R_raw = [
#     [1, 3, 2, 4],
#     [3, 1, 4, 2],
#     [4, 3, 2, 1],
#     [3, 4, 2, 1]
# ]

P_raw = [
    [1, 2, 3],
    [2, 3, 1],
    [3, 1, 2],
]

R_raw = [
    ["B","C","A"],
    ["C","A","B"],
    ["A","B","C"]
]

# P_pref = [[x - 1 for x in row] for row in P_raw]
# R_pref = [[x - 1 for x in row] for row in R_raw]
P_pref = P_raw
R_pref = R_raw
final_match_P, final_match_R, steps = gale_shapley(P_pref, R_pref)

print("--- Intermediate Proposals ---")
for step in steps:
    print(step)

# print("\n--- Final Matching (0-based) ---")
# print(f"Match_P (Index=Proposer, Value=Receiver): {final_match_P}")
# print(f"Match_R (Index=Receiver, Value=Proposer): {final_match_R}")

print("\n--- Final Matching (Readable 1-based) ---")
pairs = []
for p, r in enumerate(final_match_P):
    pairs.append(f"(P{p+1}, R{r+1})")
print(", ".join(pairs))