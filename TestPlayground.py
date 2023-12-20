print("Hello World")

EXPECTED_BAKE_TIME = 40

def calculate_time_remainin(so_far):
        return (EXPECTED_BAKE_TIME - so_far)

remain = calculate_time_remainin(1)
print(remain)