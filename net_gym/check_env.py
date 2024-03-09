from stable_baselines3.common.env_checker import check_env
from envs.env_netem import NetEnv

env = NetEnv('test12345')
check_env(env, warn=True)