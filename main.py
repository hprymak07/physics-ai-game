from geoffrey import Agent
from game import Game

agent = Agent()
game = Game()

state_old = agent.get_state(game)
done = False
record = 0
while not done:

    action = agent.get_action(state_old)

    reward, done, state_new = game.step(action)
    score = game.score

    agent.remember(state_old,  reward, state_new, done)
    agent.train_short_memory(state_old, reward, state_new, done)
    agent.train_long_memory()
    state_old = state_new
    if done:
        game.reset()
        agent.n_games += 1


        if score > record:
            record = score
            agent.model.save()

        print('Game', agent.n_games, 'Score', score, 'Record:', record)

# def train():
#     plot_scores = []
#     plot_mean_scores =[]
#     total_score = 0
#     record = 0
#     agent = Agent()
#     game = Game()
#     print("I define these")
#     while True:
#         # get old state / current
#         state_old = agent.get_state(game)
#         print("state", state_old)

#         # get move on current state
#         final_move = agent.get_action(state_old)
#         print("final move",final_move)

    
#         reward, done, score = game.step(final_move)

#         state_new = agent.get_state(game)

#         #train short term memory
        




