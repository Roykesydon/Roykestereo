def get_env() -> dict:
    with open("../.env", "r") as file:
        lines = file.readlines()

        env_dict = {}
        for line in lines:
            if line != "":
                env_dict[line.split("=")[0].strip()] = line.split("=")[1].strip()

        return env_dict
