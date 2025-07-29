"""FORM (First Order Reliability Method) module for Fesslix.

"""

# Fesslix - Stochastic Analysis
# Copyright (C) 2010-2025 Wolfgang Betz
#
# Fesslix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fesslix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fesslix.  If not, see <http://www.gnu.org/licenses/>. 

import fesslix as flx

import numpy as np
import scipy.optimize



##################################################
# FORM analysis                                  #
##################################################

def perform_FORM(lsf, sampler, config):
    ## config
    ##   method » 'COBYLA' or 'SLSQP'
    ##   disp » controls output in scipy.optimize.minimize
    ##   fd_eps » SLSQP: finite difference step size
    ##   rhobeg » COBYLA: initial trust region radius
    ##   u0 » start point of optimization
    ##   print_lsf » output current sample at each iteration step (lsf-call)
    ## process configuration
    if 'method' in config:
        opt_meth = config['method']
    else:
        opt_meth = 'COBYLA'
    opt_options = {'disp': True, 'maxiter': 1000}
    if opt_meth == 'SLSQP':
        if 'fd_eps' in config:
            opt_options['eps'] = config['fd_eps']
    if opt_meth == 'COBYLA':
        if 'rhobeg' in config:
            opt_options['rhobeg'] = config['rhobeg']
    ## number of random variables
    M = sampler.get_NRV()
    ## start point of optimization
    if 'u0' in config:
        u0 = config['u0']
    else:
        u0 = np.zeros(M)
    if 'print_lsf' in config:
        print_lsf = config['print_lsf']
    else:
        print_lsf = True
    ## Constraint for optimization
    def eval_lsf_of_u(lsf, u, sampler):
        sampler.assign_u(u)
        res = lsf()
        x_vec = sampler.get_values('x')
        if print_lsf:
            print(res, u, x_vec)
        return res
    constr = {'type': 'ineq', 'fun': lambda u: -eval_lsf_of_u(lsf, u, sampler) }
    ## objective function for optimization
    def objective(u):
        return np.linalg.norm(u)
    # Call optimizer
    res_ = scipy.optimize.minimize(objective, u0, constraints=[constr], method=opt_meth, options=opt_options)
    # Extract reliability index and design point
    res = {}
    res['u_star'] = res_.x
    res['beta'] = np.linalg.norm(res['u_star'])
    res['pf'] = flx.cdfn(-res['beta'])

    return res



