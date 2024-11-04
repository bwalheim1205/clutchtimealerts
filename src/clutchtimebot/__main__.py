import argparse
from clutchtimebot.clutch_alerts import ClutchAlertsService

if __name__ == "__main__":
    # TODO add argument configurations
    parser = argparse.ArgumentParser()
    ClutchAlertsService().run()
