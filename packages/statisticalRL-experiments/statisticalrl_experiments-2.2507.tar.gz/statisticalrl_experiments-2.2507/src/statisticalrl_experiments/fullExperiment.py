import statisticalrl_experiments.oneRun as oR
import statisticalrl_experiments.parallelRuns as pR
import statisticalrl_experiments.analyzeRuns as aR
import statisticalrl_experiments.plotResults as plR

import time
import numpy as np

#from src.statisticalrl_experiments.utils import get_project_root_dir
#ROOT= get_project_root_dir()+"/src/results"
import os
ROOT="results/"

def runLargeMulticoreExperiment(env, agents, oracle, timeHorizon=1000, nbReplicates=100, root_folder=ROOT):
    try:
        os.mkdir(root_folder)
    except:
        ()

    envFullName= env.name

    #opti_learner=opt.build_opti(envFullName, env.env, env.observation_space.n, env.action_space.n)
    learners = [x[0](**x[1]) for x in agents]

    print("*********************************************")
    dump_cumRewardsAlgos = []
    names = []
    meanelapsedtimes = []

    for learner in learners:
        names.append(learner.name())
        dump_cumRewards, meanelapsedtime = pR.multicoreRuns(envFullName, learner, nbReplicates, timeHorizon,oR.oneXpNoRenderWithDump, root_folder=root_folder)
        dump_cumRewardsAlgos.append(dump_cumRewards)
        meanelapsedtimes.append(meanelapsedtime)

    ## Cumlative reward of optimal policy:
    opttimeHorizon = min(max((10000, timeHorizon)),10**8)
    dump_cumRewardsopt = oR.oneRunOptWithDump(env, oracle, opttimeHorizon, root_folder=root_folder)
    dump_cumRewardsAlgos.append(dump_cumRewardsopt)

    ## Report statistics and compute regret:
    #print('************** ANALYSIS **************')
    timestamp = str(time.time())
    logfilename=root_folder+"logfile_"+env.name+"_"+timestamp+".txt"
    logfile = open(logfilename,'w')
    logfile.write("Environment "+env.name +"\n")
    logfile.write("Optimal policy is: " + str(oracle.policy)+"\n")
    logfile.write("Learners "+str([learner.name() for learner in learners]) +"\n")
    logfile.write("Time horizon is "+ str(timeHorizon) + ", nb of replicates is "+ str(nbReplicates) +"\n")
    [logfile.write(str(names[i])+ " average runtime is "+ str(meanelapsedtimes[i])  +"\n") for i in range(len(names))]
    mean,median, quantile1,quantile2,times = aR.computeCumulativeRegrets(names, dump_cumRewardsAlgos, timeHorizon, envFullName, root_folder=root_folder)
    title = f"{env.name}"
    plR.plotCumulativeRegrets(names, envFullName, title, mean, median, quantile1, quantile2, times, timeHorizon, logfile=logfile, timestamp=timestamp, root_folder=root_folder)
    #print("*********************************************")
    oR.clear_auxiliaryfiles(env, root_folder)
    print("\n[INFO] A log-file has been generated in ",logfilename)



import statisticalrl_learners.MDPs_discrete.Optimal.OptimalControl  as opt
def runBayesianExperiment(name, envs, agents, timeHorizon=1000, nbReplicates=100, root_folder=ROOT):

    #TODO : This does not work !! Strangely enough the last xp gives correct output, but not previous ones, seems like a ref problem.
    # All indicates that the  regret is computed w.r.t. a reference that is changing/not reallocated.

    timestamp0 = str(time.time())
    logfilename = root_folder + "logfile_Bayesian" + name + "_" + timestamp0 + ".txt"
    logfile = open(logfilename, 'w')
    logfile.write("Environments " + name + ". Number of instances is "+str(len(envs)) + "\n")
    #logfile.write("Learners " + str([learner.name() for learner in learners]) + "\n")
    logfile.write("Time horizon is " + str(timeHorizon) + ", nbplicates is " + str(nbReplicates) + "\n")

    means = []
    medians = []
    quantiles1 = []
    quantiles2= []
    timess=[]
    meanelapsedtimess = []
    opti_learners = []

    #mean = np.zeros((len(envs),len(agents),timeHorizon))

    for env in envs:
        #env = bW.makeWorld(env2.name)
        print("Env name:", env.name)
        opti = opt.build_opti(env.name, env.env, env.observation_space.n, env.action_space.n)
        opti_learners.append(opti)
        learners = [x[0](**x[1]) for x in agents]

        dump_cumRewardsAlgos = []
        meanelapsedtimes = []
        names = []

        for learner in learners:
            names.append(learner.name())
            dump_cumRewards, meanelapsedtime = pR.multicoreRuns(env.name, learner, nbReplicates, timeHorizon,oR.oneXpNoRenderWithDump)
            dump_cumRewardsAlgos.append(dump_cumRewards)
            meanelapsedtimes.append(meanelapsedtime)

        ## Cumlative reward of optimal policy:
        opttimeHorizon = min(max((10000, timeHorizon)),10**8)
        dump_cumRewardsopt = oR.oneRunOptWithDump(env, opti_learners[-1], opttimeHorizon)
        dump_cumRewardsAlgos.append(dump_cumRewardsopt)

    ## Report statistics and compute regret:
    #print('************** ANALYSIS **************')

        mean,median, quantile1,quantile2,times = aR.computeCumulativeRegrets(names, dump_cumRewardsAlgos, timeHorizon, env.name)
        print("Mean", mean)
        timestamp = str(time.time())
        title = f"{env.name}"
        plR.plotCumulativeRegrets(names, env.name, title, mean, median, quantile1, quantile2, times, timeHorizon, logfile=logfile, timestamp=timestamp, root_folder=root_folder)


        oR.clear_auxiliaryfiles(env)

        means.append(mean)
        medians.append(median)
        quantiles1.append(quantile1)
        quantiles2.append(quantile2)
        timess.append(times)
        meanelapsedtimess.append(meanelapsedtimes)

        #means[jenv][ilearner] = [,,,,,]

    m=[[np.mean([means[jenv][ilearner][t] for jenv in range(len(envs))]) for t in range(timeHorizon)] for ilearner in range(len(agents))]
    md=[[np.mean([medians[jenv][ilearner][t] for jenv in range(len(envs))]) for t in range(timeHorizon)] for ilearner in range(len(agents))]
    q1=[[np.mean([quantiles1[jenv][ilearner][t] for jenv in range(len(envs))]) for t in range(timeHorizon)] for ilearner in range(len(agents))]
    q2=[[np.mean([quantiles2[jenv][ilearner][t] for jenv in range(len(envs))]) for t in range(timeHorizon)] for ilearner in range(len(agents))]
    mt=[np.mean([meanelapsedtimess[jenv][ilearner] for jenv in range(len(envs))]) for ilearner in range(len(agents))]
    tt=[np.mean([timess[jenv][t] for jenv in range(len(envs))]) for t in range(timeHorizon)]
    #tt = timess[0]

    #TODO: THE FOLLOWING does not compute the right thing
    [logfile.write(str(names[i])+ " average runtime is "+ str(mt[i])  +"\n") for i in range(len(agents))]
    plR.plotCumulativeRegrets(names, name, f"Bayesian ({len(envs)} many)",
                              m, md, q1, q2, tt,
                              timeHorizon, logfile=logfile, timestamp=timestamp0,root_folder=root_folder)


    #print("*********************************************")

    print("\n[INFO] A log-file has been generated in ",logfilename)
