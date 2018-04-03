from src.game import Game

def main():
    print('Welcome to Ant-1!')
    game = Game()
    # game.run()
    game.run_episodes(num_episodes=10, num_frames=5e4)

if __name__ == '__main__':
    main()
