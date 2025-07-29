from .constants import *
from .mobility import *
import numpy as np

def CoulombForce(q1, q2, pos1, pos2, safety = 7e-9):
    r2 = max(safety**2, sum((pos1-pos2)**2))
    Fs = -kE_SI*q1*q2/r2/epsR_Si
    return Fs*(pos2-pos1)/r2**0.5

def getEffectiveCoulombField(objects):
    Ecoul = np.zeros((len(objects), 3))
    for i in range(len(objects)):
        Q = objects[i].q
        F = np.zeros(3)
        for j in range(len(objects)):
            if i != j:
                F+= CoulombForce(Q, objects[j].q, objects[i].pos[-1], objects[j].pos[-1])
            Ecoul[i] = F/Q
    return Ecoul

def insideBoundaryCheck(pos, bounds):
    return ((pos[0] >= bounds[0][0]) & (pos[0] <= bounds[0][1]) & (pos[1] >= bounds[1][0]) & (pos[1] <= bounds[1][1])
            & (pos[2] >= bounds[2][0]) & (pos[2] <= bounds[2][1]))

def updateQuasiParticles(objects, ds, maxdt, Ex_i, Ey_i, Ez_i, E_i, bounds, temp, diffusion=True, coulomb=False,
                         tauTrap = lambda x, y, z : 1e9, NI = lambda x, y, z : 1e16,
                         mobility_e = canali_mobility_e, mobility_h = canali_mobility_h):
    #Vector to save the effective electric field for each particle at the time step
    Eeff = np.zeros((len(objects), 3))

    # If coulomb is enabled, an effective electric field because of all other charges is added (plasma effects)
    if coulomb:
        Eeff += getEffectiveCoulombField(objects)

    for i in range(len(objects)):
        pos = objects[i].pos[-1]
        dt = maxdt

        Eeff[i] += np.array([Ex_i(pos), Ey_i(pos), Ez_i(pos)])

        if objects[i].q < 0:
            mu = mobility_e(temp, NI(*pos), np.linalg.norm(Eeff[i]))
            dv = -mu*Eeff[i]
            # print(mu, dv, Eeff[i])
        else:
            mu = mobility_h(temp, NI(*pos), np.linalg.norm(Eeff[i]))
            dv = mu*Eeff[i]

        if not coulomb:
            dt = min(abs(ds/np.linalg.norm(dv)), maxdt)

        if diffusion:
            dv += ((diffusion_electron(temp) if objects[i].q < 0 else diffusion_hole(temp))/dt)**0.5*np.random.normal(size=3)

        t = objects[i].time[-1]+dt
        pos = objects[i].pos[-1]+dv*dt
        #Check if particles are still inside the specified boundaries, otherwise kill them
        objects[i].alive = insideBoundaryCheck(pos, bounds)

        if objects[i].alive:
            objects[i].addTime(t)
            objects[i].addVel(dv)
            objects[i].addPos(pos)
        
        else:
            #currently only interpolates on z
            objects[i].addVel(dv)
            if pos[2] > bounds[2][1]:
                # print("out of bounds, crossed top contact")
                dt = (bounds[2][1] - objects[i].pos[-1][2])/objects[i].vel[-1][2]
                objects[i].addTime(objects[i].time[-1]+dt)
                objects[i].addPos(objects[i].pos[-1]+objects[i].vel[-1]*dt)
            elif pos[2] < bounds[2][0]:
                # print("out of bounds, crossed bottom contact")
                dt = (bounds[2][0] - objects[i].pos[-1][2])/objects[i].vel[-1][2]
                objects[i].addTime(objects[i].time[-1]+dt)
                objects[i].addPos(objects[i].pos[-1]+objects[i].vel[-1]*dt)
            else:
                objects[i].addTime(t)
                objects[i].addVel(dv)
                objects[i].addPos(pos)

        #Check whether a particle is captured. If so, the particle is killed. 
        #dt must be substantially smaller than tauTrap in order for Poisson process to work
        p = dt/tauTrap(*(objects[i].pos[-1]))
        r = np.random.random()
        if r < p:
            objects[i].alive = False

    return objects

def propagateCharge(object, ds, maxdt, Ex_i, Ey_i, Ez_i, E_i, bounds, temp, diffusion=True,
                         tauTrap = lambda x, y, z : 1e9, NI = lambda x, y, z : 1e16,
                         mobility_e = canali_mobility_e, mobility_h = canali_mobility_h):
    
    while object.alive:
        pos = object.pos[-1]
        dt = maxdt
        Eeff = np.array([Ex_i(pos), Ey_i(pos), Ez_i(pos)])

        if object.q < 0:
            mu = mobility_e(temp, NI(*pos), np.linalg.norm(Eeff))
            dv = -mu*Eeff
            # print(mu, dv, Eeff[i])
        else:
            mu = mobility_h(temp, NI(*pos), np.linalg.norm(Eeff))
            dv = mu*Eeff

        dt = min(abs(ds/np.linalg.norm(dv)), maxdt)

        if diffusion:
            dv += ((diffusion_electron(temp) if object.q < 0 else diffusion_hole(temp))/dt)**0.5*np.random.normal(size=3)

        t = object.time[-1]+dt
        pos = object.pos[-1]+dv*dt
        #Check if particles are still inside the specified boundaries, otherwise kill them
        object.alive = insideBoundaryCheck(pos, bounds)

        if object.alive:
            object.addTime(t)
            object.addVel(dv)
            object.addPos(pos)
        
        else:
            #currently only interpolates on z
            object.addVel(dv)
            if pos[2] > bounds[2][1]:
                # print("out of bounds, crossed top contact")
                dt = (bounds[2][1] - object.pos[-1][2])/object.vel[-1][2]
                object.addTime(object.time[-1]+dt)
                object.addPos(object.pos[-1]+object.vel[-1]*dt)
            elif pos[2] < bounds[2][0]:
                # print("out of bounds, crossed bottom contact")
                dt = (bounds[2][0] - object.pos[-1][2])/object.vel[-1][2]
                object.addTime(object.time[-1]+dt)
                object.addPos(object.pos[-1]+object.vel[-1]*dt)
            else:
                object.addTime(t)
                object.addVel(dv)
                object.addPos(pos)

        #Check whether a particle is captured. If so, the particle is killed. 
        #dt must be substantially smaller than tauTrap in order for Poisson process to work
        p = dt/tauTrap(*(object.pos[-1]))
        r = np.random.random()
        if r < p:
            object.alive = False

    return object

if __name__ == "__main__":
    x, y, z, t = propagateCharge(0, 0, 0, 1e-4, lambda a : [0,], lambda a : [0,], lambda a: [-750e2,], lambda a : [-750e2,], [[-1, 1], [-1, 1], [0, 0.002]], 130, diffusion=True)
