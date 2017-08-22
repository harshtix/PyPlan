import numpy as np
import multiprocessing
import matplotlib.pyplot as plt


def generate_regret_curves(bandits, pull_max, slot_machines, num_trials=20):
    """Generate and graph regret curves for bandits x pull_values on simulator.

    :param bandits: the bandit classes to use.
    :param pull_max: the maximum number of pulls to use.
    :param slot_machines: slot machines (BanditProblems) from vegas which will be used to measure regret.
    :param num_trials: how many trials we will run.
    """
    # Generate data
    processes_to_create = min(multiprocessing.cpu_count() - 1, len(bandits))
    pull_max = int(pull_max)
    with multiprocessing.Pool(processes=processes_to_create) as pool:
        outputs = pool.starmap(run_machine, [[bandit, pull_max, slot_machines, num_trials] for bandit in bandits])

    cumulative, simple = {}, {}
    for output in outputs:
        bandit, temp_cumulative, temp_simple = output  # cumulative and simple are same for all bandits
        cumulative[bandit], simple[bandit] = temp_cumulative, temp_simple

    for machine_idx in range(len(slot_machines)):
        # Construct and display graphs for each bandit algorithm
        plt.figure()
        for regret_type in ('Cumulative', 'Simple'):
            ax = plt.subplot(121 if regret_type == 'Cumulative' else 122)
            ax.grid('on')

            ax.set_xlim(1, pull_max + 1)
            ax.set_xlabel('Number of Pulls')
            ax.set_ylabel(regret_type + ' Regret')

            regret_dict = cumulative if regret_type == 'Cumulative' else simple
            for bandit in bandits:
                ax.plot(range(1, pull_max + 1), regret_dict[bandit][machine_idx], label=bandit.name)

            ax.legend(loc='lower right')
            ax.set_title(regret_type + ' Regret for Slot Machine {} ({} trials)'.format(machine_idx + 1, num_trials))
    plt.show()


def run_machine(bandit, pull_max, slot_machines, num_trials):
    cumulative, simple = [np.array([[0.0 for _ in range(pull_max)] for _ in range(len(slot_machines))])
                          for _ in range(2)]

    for machine_idx, machine in enumerate(slot_machines):
        new_bandit = bandit(machine.num_arms)
        for trial_num in range(1, num_trials + 1):
            new_bandit.initialize()
            for pull_num in range(pull_max):
                # Pull an arm and update the bandit
                arm = new_bandit.select_pull_arm()
                reward = machine.pull(arm)
                new_bandit.update(arm, reward)

                # Calculate regrets and update our averages
                cumulative[machine_idx][pull_num] += get_cumulative_regret(new_bandit, machine.max_expected_reward)
                simple[machine_idx][pull_num] += get_simple_regret(new_bandit, machine.max_expected_reward)

        # Compute averages (do all at once to take advantage of numpy)
        cumulative[machine_idx] /= num_trials
        simple[machine_idx] /= num_trials

    return bandit, cumulative, simple


def get_cumulative_regret(bandit, max_reward):
    """Return the accrued cumulative regret."""
    return bandit.total_pulls * max_reward - np.sum(bandit.average_reward * bandit.num_pulls)


def get_simple_regret(bandit, max_reward):
    return max_reward - bandit.get_best_reward()
