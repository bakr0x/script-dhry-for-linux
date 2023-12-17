import time
import pygame
import select
import sys

ALERT_INTERVAL_MINUTES = 30
ALERT_FILE = 'eff.mp3'

def initialize_mixer():
    pygame.mixer.init()

def load_alert_sound(file):
    try:
        pygame.mixer.music.load(file)
    except pygame.error as e:
        print(f"Error loading sound file: {e}")
        sys.exit(1)

def alert():
    print("ALERT! Time to take a break!")
    pygame.mixer.music.play(loops=-1)

def stop_alert():
    print("Alert stopped.")
    pygame.mixer.music.stop()

def main():
    try:
        initialize_mixer()
        load_alert_sound(ALERT_FILE)

        while True:
            alert_interval = ALERT_INTERVAL_MINUTES * 60
            alert_triggered = False

            input("Press Enter to start the countdown...")
            print("\nCountdown started.")

            clock = pygame.time.Clock()

            for _ in range(alert_interval):
                clock.tick(1)
                time_remaining = alert_interval - pygame.time.get_ticks() // 1000
                print(f"Time remaining: {time_remaining // 60} minutes {time_remaining % 60} seconds", end='\r')

                if input_available():
                    print("\nUser input detected. Stopping the sound and restarting the timer.")
                    stop_alert()
                    alert_triggered = False
                    break

            stop_alert()

            if not alert_triggered:
                alert()

                while True:
                    if input_available():
                        print("\nUser input detected. Stopping the sound.")
                        stop_alert()
                        break

    except KeyboardInterrupt:
        print("\nScript terminated by user.")

def input_available():
    # Check for keyboard input on Linux
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

if __name__ == "__main__":
    main()
