def run(n):
    try:
        mod = __import__(f"pandes.programs.prog{n}", fromlist=["get_code"])
        print(mod.get_code())
    except ModuleNotFoundError:
        print(f"No program found for number {n}")