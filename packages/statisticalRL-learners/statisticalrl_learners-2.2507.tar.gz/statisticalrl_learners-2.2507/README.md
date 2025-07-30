# Learners
Learning Agents for Statistical Reinforcement Learning


## Installation

    pip install statisticalRL-learners


## Test
You need to install statisticalRL-environments and statisticalRL-experiments before testing.

    pip install statisticalRL-environments
    pip install statisticalRL-experiments


# List of learners:
    
    
    Random
    Human
    Uniform

    MABs:
        MABOracle
        FTL
        UCB
        TS
        IMED
        BESA
    MDPs_dicrete:
        MDPOracle
        QLearning
        AdaQLearning
        IMED-RL
        KL-UCRL
        MED-RL
        PSRL
        UCRL2
        UCRL2.2
        UCRL2B
        UCRL2B-detR
        UCRL3
        UCRL3-lazy
        Known dynamics:
            IMED-KD
            PSRL-KD
            TS-KD
            UCB-KD
            UCRL3-KD
            UCRL3-KD-lazy
        Equivalence structure:
            CUCRL
            CUCRL-detR
            UCRL_SA_oracle
            UCRL_SA


# Usage

You can run an instance of a learner on an environment from StatisticalRL library.