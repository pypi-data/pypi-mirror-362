


import statisticalrl_environments as srl
from statisticalrl_environments.register import make
env = make('river-swim-6')
from statisticalrl_environments.fulldemo import print_registered_environments,random_environment,all_environments

# print_registered_environments()
# random_environment()
# all_environments()

import statisticalrl_learners as srla

from statisticalrl_learners.MDPs_discrete.PSRL import PSRL

