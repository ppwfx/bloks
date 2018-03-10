def convert_env(env_dict):
    env_list = []
    for key, value in env_dict.items():
        env_list.append({"name": key, "value": value})

    return env_list