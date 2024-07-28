# %%
def compute_hcf(x, y):
    if x > y:
        smaller = y
    else:
        smaller = x
    for i in range(1, smaller + 1):
        if (x % i == 0) and (y % i == 0):
            hcf = i
    return hcf


hcf = compute_hcf(300, 400)
print(f"The H.C.F. is {hcf}")
hcf

# % title="Find the H.C.F of two numbers" highlights=1,2-3,4-5,9
