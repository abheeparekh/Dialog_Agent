import subprocess


path='/mnt/c/Users/abhee/Downloads/pomdp/pomdp-solve-5.4/src/pomdp-solve'
timeout = 80
#subprocess.check_output([path, 'pomdp_3.pomdp', \
#            '--timeout', str(timeout), '--output', 'policy_3.policy'])
subprocess.check_output([path, '9.pomdp', \
            '--timeout', str(timeout), '--output', '9.policy'])
