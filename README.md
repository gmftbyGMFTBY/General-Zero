## The AlphaZero for the WTN-EinStein Chess

>* Thanks for this repo: https://github.com/junxiaosong/AlphaZero_Gomoku
>* Thanks for the author `junxiaosong` to answer my questions. 

### 1. Project Arch
1. game.py
    * Class `Board`: 

      Board class for the game to use

    * Class `Game`: 

      Game class for creating one game to run 
2. human_play.py
    * Class `Human`: 

      Human player instance to use in the competition

    * Funtion `run`: 

      Main function to create the players and the games to play
3. policy_value_net.py
    * Class `PolicyValueNet`: 

      Create the AlphaZero player
4. alphazero_mcts.py
    * Function `softmax`

    * Class `TreeNode`: 

      MCTS's node instance

    * Class `MCTS`: 

      MCTS class for the AlphaZero player to use

    * Class `MCTSPlayer`: 

      MCTS's player, the `pure_mcts.py`  use the pure MCTS player, but `alphazero_mcts.py` use the NN to help the MCTS to search.
5. train.py
    * `TrainPipeline`: 

      Train Pipleline for the training progress and create the model file

### 2. Model Save

1. model: 

   Save the current model file for TensorFlow and used by the `policy_value_net.py` to start play with human

   * `model-1-...`
   * `model-2-...`
   * `mode-3-...`
   * `model-4-...`
   * `model-5-...`

2. saved_models

   Save some model file for the training and testing progress, `1500 / 5000` means the number of the self-play games.

   `400 / 1000` means the number of the simulation in one self-play game. 

### 3. Chess log

the  `chess_log` folder is to contain the chess log because of the 2018 CGCC Competition. The program which can not create the chess log file for one game will not be able to attend the competition.

The format of the log file is defined by the CAAI, and can be found on this website: http://computergames.caai.cn/

### 4. Hardware details

1. The model training on the `GTX-1080` and the model `model-3-5000-1000` takes almost one day to finish.
   * CUDA 8.0
   * Python 3.5
   * tensorflow-gpu 1.4 
2. The CPU is `GenuineIntel`
3. OS is Ubuntu 14.04

### 5. Update Suggestion

1. Use  `multiprocessing` to paralle the MCTS, inorder to speed up

2. Deeper NN

3. Tkinter for the GUI shell

4. Choose `PyTorch` instead of `TensorFlow`

   The GPU is less working under TensorFlow, most working of this program is the CPU (simulation of the self-play)

### 6. Some Experience

1. In my opinion, the pure MCTS is powerful, but the bad aspect of the pure MCTS is that the random rollout

2. AlphaZero can be better with more simulations (400 is less, 1000 is just soso, in the competition can be 6000+)

   Remember more simulations is more time cost. The time limitation is 4 minites.

3. pure MCTS will be worst with more simulations, I think the reason is that more simulations can confuse the program.

   for pure MCTS, more simulations means making mistakes easiler.

4. **`This experience is very important.`** During the training process, I found that clear the dataset queue sometimes can improve the performance of the model, I think the most import reason is that the dataset queue (In the `train.py` is 10000) can store the lots of data which created long time ago, may influence the training process (Sample 512 samples from the 10000 dataset, so the possibility of using the old data is high, but old data is useless or bad for current model, So the queue must be changing). So I think that when the `loss` is stable for a while, We should clear the dataset queue and retraing the model from the begining. Or in other words, **`The size of the dataset deque  must be changeto adapt the better performance`**.

5. The pre-simulation progress ...

### 7. Getting Start

```python
# need to install the tensorflow==1.4
python human_play.py

# train to create the model
python train.py
```

