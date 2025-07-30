import pickle
import time
import os


def oneXpNoRender(env,learner,timeHorizon,root_folder):
    observation, info = env.reset()
    learner.reset(observation)
    cumreward = 0.
    cumrewards = []
    cummean = 0.
    cummeans = []
    print("[Info] New initialization of ", learner.name(), ' for environment ',env.name)
    #print("Initial state:" + str(observation))
    for t in range(timeHorizon):
        state = observation
        action = learner.play(state)  # Get action
        observation, reward, done,truncated, info = env.step(action)
        learner.update(state, action, reward, observation)  # Update learners
        #print("info:",info, "reward:", reward)
        cumreward += reward
        try:
            cummean += info["mean"]
        except TypeError:
            cummean += reward
        cumrewards.append(cumreward)
        cummeans.append(cummean)

        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            observation, info=env.reset()
            #break

    #print("Cumreward: " + str(cumreward))
    #print("Cummean: " + str(cummean))
    return cummeans #cumrewards,cummeans


def oneXpNoRenderWithDump(env,learner,timeHorizon,root_folder):
    observation,info = env.reset()
    learner.reset(observation)
    cumreward = 0.
    cumrewards = []
    cummean = 0.
    cummeans = []
    print("[Info] New initialization of ", learner.name(), ' for environment ',env.name)
    #print("Initial state:" + str(observation))
    for t in range(timeHorizon):
        state = observation
        action = learner.play(state)  # Get action
        observation, reward, done, truncated, info = env.step(action)
        learner.update(state, action, reward, observation)  # Update learners
        #print("info:",info, "reward:", reward)
        cumreward += reward
        try:
            cummean += info["mean"]
        except TypeError:
            cummean +=reward
        cumrewards.append(cumreward)
        cummeans.append(cummean)

        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            observation, info = env.reset() # converts an episodic MDP into an infinite time horizon MDP
            #break

    filename = root_folder+"cumMeans_" + env.name + "_" + learner.name() + "_" + str(timeHorizon) +"_" + str(time.time())
    file =  open(filename,'wb')
    file.truncate(0)
    pickle.dump(cummeans, file)
    file.close()
    return filename

def oneRunOptWithDump(env, opti_learner, timeHorizon, root_folder):
 ## Cumlative reward of optimal policy:
    opttimeHorizon = min(max((1000000, timeHorizon)),10**8)
    cumReward_opti = oneXpNoRender(env, opti_learner, opttimeHorizon, root_folder=root_folder)
    gain =  cumReward_opti[-1] / len(cumReward_opti)
    #print("Average gain is ", gain)
    opti_cumgain = [[t * gain for t in range(timeHorizon)]]
    filename = root_folder+"cumMeans_" + env.name + "_" + opti_learner.name() + "_" + str(timeHorizon) + "_" + str(time.time())
    file = open(filename, 'wb')
    file.truncate(0)
    pickle.dump(opti_cumgain, file)
    file.close()
    return filename

def clear_auxiliaryfiles(env,root_folder):
        for file in os.listdir(root_folder):
            if file.startswith("cumMeans_" + env.name):
                os.remove(root_folder+file)